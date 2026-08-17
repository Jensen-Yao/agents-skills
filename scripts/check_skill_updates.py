#!/usr/bin/env python3
"""Check the published catalog and configured public skill sources for drift."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


README_SKILL_RE = re.compile(r"\(skills/([^/]+)/SKILL\.md\)")
PAGE_SKILL_RE = re.compile(r'data-name="([^"]+)"')
DEFAULT_IGNORES = [".DS_Store", "**/.DS_Store", "Thumbs.db", "**/Thumbs.db"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        help="Upstream configuration (default: config/upstreams.json).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("skill-update-report.md"),
        help="Markdown report path.",
    )
    parser.add_argument(
        "--json",
        dest="json_path",
        type=Path,
        default=Path("skill-update-report.json"),
        help="Machine-readable report path.",
    )
    parser.add_argument(
        "--skip-upstreams",
        action="store_true",
        help="Check README and Pages catalogs without cloning upstreams.",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("version") != 1 or not isinstance(config.get("repositories"), list):
        raise ValueError(f"Unsupported upstream config: {path}")
    return config


def skill_directories(skills_root: Path) -> set[str]:
    return {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def catalog_findings(root: Path, installed: set[str]) -> list[dict[str, Any]]:
    readme = (root / "README.md").read_text(encoding="utf-8")
    page = (root / "docs" / "index.html").read_text(encoding="utf-8")
    readme_skills = set(README_SKILL_RE.findall(readme))
    page_skills = set(PAGE_SKILL_RE.findall(page))

    findings: list[dict[str, Any]] = []
    for surface, published in (("README", readme_skills), ("Pages", page_skills)):
        missing = sorted(installed - published)
        stale = sorted(published - installed)
        if missing:
            findings.append({"surface": surface, "kind": "missing", "skills": missing})
        if stale:
            findings.append({"surface": surface, "kind": "stale", "skills": stale})
    return findings


def clone_repository(url: str, destination: Path) -> None:
    result = subprocess.run(
        ["git", "clone", "--depth", "1", "--quiet", url, str(destination)],
        text=True,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise RuntimeError(f"Failed to clone {url}: {detail}")


def discover_sources(
    checkout: Path,
    installed: set[str],
    options: dict[str, Any],
) -> dict[str, str]:
    excluded = set(options.get("exclude", []))
    installed_only = options.get("include_installed_only", True)
    matches: dict[str, list[Path]] = {}
    for skill_file in checkout.rglob("SKILL.md"):
        if ".git" in skill_file.parts:
            continue
        name = skill_file.parent.name
        if name in excluded or (installed_only and name not in installed):
            continue
        matches.setdefault(name, []).append(skill_file.parent)

    duplicates = {name: paths for name, paths in matches.items() if len(paths) > 1}
    if duplicates:
        details = ", ".join(
            f"{name}: {[path.relative_to(checkout).as_posix() for path in paths]}"
            for name, paths in sorted(duplicates.items())
        )
        raise RuntimeError(f"Ambiguous discovered skill paths ({details})")

    return {
        name: paths[0].relative_to(checkout).as_posix()
        for name, paths in sorted(matches.items())
    }


def ignored(relative_path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(relative_path, pattern) for pattern in patterns)


def content_digest(path: Path) -> str:
    data = path.read_bytes()
    if b"\x00" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def compare_skill(source: Path, local: Path, patterns: list[str]) -> list[str]:
    differences: list[str] = []
    for source_file in sorted(path for path in source.rglob("*") if path.is_file()):
        relative = source_file.relative_to(source).as_posix()
        if ignored(relative, patterns):
            continue
        local_file = local / Path(relative)
        if not local_file.is_file():
            differences.append(f"missing {relative}")
        elif content_digest(source_file) != content_digest(local_file):
            differences.append(f"changed {relative}")
    return differences


def upstream_findings(
    root: Path,
    installed: set[str],
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="agents-skills-upstreams-") as temp_dir:
        temp_root = Path(temp_dir)
        for index, repository in enumerate(config["repositories"]):
            repo_name = repository["repository"]
            checkout = temp_root / f"repo-{index}"
            clone_repository(repository["url"], checkout)

            if "discover" in repository:
                mappings = discover_sources(checkout, installed, repository["discover"])
            else:
                mappings = repository.get("skills", {})

            patterns = DEFAULT_IGNORES + repository.get("ignore", [])
            for local_name, source_path in sorted(mappings.items()):
                if local_name not in installed:
                    continue
                source = checkout / Path(source_path)
                if not (source / "SKILL.md").is_file():
                    raise RuntimeError(
                        f"Configured source {repo_name}:{source_path} has no SKILL.md"
                    )
                differences = compare_skill(source, root / "skills" / local_name, patterns)
                if differences:
                    findings.append(
                        {
                            "repository": repo_name,
                            "skill": local_name,
                            "source": source_path,
                            "differences": differences,
                        }
                    )
    return findings


def render_report(result: dict[str, Any]) -> str:
    catalog = result["catalog"]
    upstreams = result["upstreams"]
    lines = ["## Skill update report", ""]
    if not catalog and not upstreams:
        lines.extend(
            [
                "All installed skills are listed in README and Pages, and all configured public upstreams match.",
                "",
                "No action is required.",
            ]
        )
        return "\n".join(lines) + "\n"

    lines.append(
        f"Found **{result['update_count']}** update item(s). Check the boxes after synchronizing the repository."
    )
    if catalog:
        lines.extend(["", "### Catalog drift", ""])
        for finding in catalog:
            action = "missing" if finding["kind"] == "missing" else "no longer installed"
            skills = ", ".join(f"`{name}`" for name in finding["skills"])
            lines.append(f"- [ ] **{finding['surface']}**: {action}: {skills}")

    if upstreams:
        lines.extend(["", "### Upstream changes", ""])
        for finding in upstreams:
            preview = ", ".join(finding["differences"][:5])
            if len(finding["differences"]) > 5:
                preview += f", +{len(finding['differences']) - 5} more"
            lines.append(
                f"- [ ] `{finding['skill']}` from **{finding['repository']}** ({preview})"
            )

    lines.extend(
        [
            "",
            "### Resolution",
            "",
            "Synchronize the listed skills, update README and `docs/index.html` when needed, then run the workflow again. The issue closes automatically when the report is clean.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(result: dict[str, Any], report_path: Path, json_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(result), encoding="utf-8", newline="\n")
    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    args = parse_args()
    root = repo_root()
    config_path = args.config or root / "config" / "upstreams.json"
    report_path = args.report if args.report.is_absolute() else root / args.report
    json_path = args.json_path if args.json_path.is_absolute() else root / args.json_path

    try:
        installed = skill_directories(root / "skills")
        catalog = catalog_findings(root, installed)
        upstreams: list[dict[str, Any]] = []
        if not args.skip_upstreams:
            upstreams = upstream_findings(root, installed, load_config(config_path))
        result = {
            "installed_count": len(installed),
            "update_count": len(catalog) + len(upstreams),
            "catalog": catalog,
            "upstreams": upstreams,
        }
        write_outputs(result, report_path, json_path)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"Update check failed: {error}", file=sys.stderr)
        return 2

    print(
        f"Checked {result['installed_count']} installed skills; "
        f"found {result['update_count']} update item(s)."
    )
    return 1 if result["update_count"] else 0


if __name__ == "__main__":
    sys.exit(main())
