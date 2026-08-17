#!/usr/bin/env python3
"""Apply durable local routing overrides without replacing upstream skill bodies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s|$)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        help="Override configuration (default: config/local-skill-overrides.json).",
    )
    parser.add_argument(
        "--root",
        action="append",
        type=Path,
        dest="roots",
        help="Skill root to update. Repeat for multiple roots.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without writing files.",
    )
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if (
        config.get("version") != 1
        or not isinstance(config.get("skills"), dict)
        or not isinstance(config.get("reference_only"), dict)
    ):
        raise ValueError(f"Unsupported override config: {path}")
    return config


def default_roots(root: Path) -> list[Path]:
    candidates = [root / "skills", Path.home() / ".agents" / "skills"]
    resolved: list[Path] = []
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate.is_dir() and candidate not in resolved:
            resolved.append(candidate)
    return resolved


def split_frontmatter(text: str, path: Path) -> tuple[list[str], str]:
    normalized = text.replace("\r\n", "\n")
    lines = normalized.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing YAML frontmatter in {path}")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "".join(lines[index:])
    raise ValueError(f"Unterminated YAML frontmatter in {path}")


def key_spans(lines: list[str]) -> dict[str, tuple[int, int]]:
    starts: list[tuple[str, int]] = []
    for index, line in enumerate(lines):
        match = TOP_LEVEL_KEY_RE.match(line)
        if match:
            starts.append((match.group(1), index))
    return {
        key: (start, starts[index + 1][1] if index + 1 < len(starts) else len(lines))
        for index, (key, start) in enumerate(starts)
    }


def yaml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (str, int, float)):
        return json.dumps(value, ensure_ascii=False)
    raise ValueError(f"Unsupported frontmatter value: {value!r}")


def render_override(text: str, path: Path, overrides: dict[str, Any]) -> str:
    frontmatter, remainder = split_frontmatter(text, path)
    spans = key_spans(frontmatter)
    for key, value in overrides.items():
        replacement = [f"{key}: {yaml_value(value)}\n"]
        if key in spans:
            start, end = spans[key]
            frontmatter[start:end] = replacement
        else:
            frontmatter.extend(replacement)
        spans = key_spans(frontmatter)
    return "---\n" + "".join(frontmatter) + remainder


def apply_active_skill(
    skills_root: Path,
    name: str,
    settings: dict[str, Any],
    check: bool,
) -> bool:
    path = skills_root / name / "SKILL.md"
    if not path.is_file():
        raise FileNotFoundError(f"Missing active skill: {path}")
    current = path.read_text(encoding="utf-8")
    desired = render_override(current, path, settings.get("frontmatter", {}))
    if current.replace("\r\n", "\n") == desired:
        return False
    if not check:
        path.write_text(desired, encoding="utf-8", newline="\n")
    return True


def apply_reference_skill(
    skills_root: Path,
    name: str,
    settings: dict[str, Any],
    check: bool,
) -> bool:
    directory = skills_root / name
    active = directory / "SKILL.md"
    reference = directory / settings.get("file", "REFERENCE.md")
    if active.is_file():
        if not check:
            reference.write_bytes(active.read_bytes())
            active.unlink()
        return True
    if not reference.is_file():
        raise FileNotFoundError(f"Missing reference-only skill: {reference}")
    return False


def main() -> int:
    args = parse_args()
    root = repo_root()
    config_path = args.config or root / "config" / "local-skill-overrides.json"
    config = load_config(config_path)
    roots = [path.resolve() for path in args.roots] if args.roots else default_roots(root)
    if not roots:
        raise FileNotFoundError("No skill roots found")

    changed: list[str] = []
    for skills_root in roots:
        if not skills_root.is_dir():
            raise FileNotFoundError(f"Skill root does not exist: {skills_root}")
        for name, settings in config["skills"].items():
            if apply_active_skill(skills_root, name, settings, args.check):
                changed.append(f"{skills_root}:{name}")
        for name, settings in config["reference_only"].items():
            if apply_reference_skill(skills_root, name, settings, args.check):
                changed.append(f"{skills_root}:{name} (reference-only)")

    if changed:
        verb = "Need override" if args.check else "Applied override"
        for item in changed:
            print(f"{verb}: {item}")
        return 1 if args.check else 0

    print(f"Local skill overrides are current in {len(roots)} root(s).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Override application failed: {error}", file=sys.stderr)
        sys.exit(2)
