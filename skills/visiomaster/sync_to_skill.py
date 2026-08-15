from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


INCLUDE_ITEMS = [
    "agents",
    "docs",
    "references",
    "scripts",
    "templates",
    "requirements.txt",
]

IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".git", ".github")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync the reusable visiomaster skill files from this repo to a Codex skill directory."
    )
    parser.add_argument(
        "--skill-dir",
        default=str(Path.home() / ".codex" / "skills" / "visiomaster"),
        help="Target Codex skill directory. Defaults to ~/.codex/skills/visiomaster.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be copied without writing files.")
    parser.add_argument(
        "--include-skill-md",
        action="store_true",
        help="Also copy SKILL.md from the repo. Leave this off to preserve local environment-specific settings.",
    )
    parser.add_argument(
        "--merge-skill-md",
        action="store_true",
        help="Merge repo SKILL.md into the target while preserving the target Environment section.",
    )
    return parser.parse_args()


def copy_item(src: Path, dst: Path, dry_run: bool) -> None:
    if src.is_dir():
        if dst.exists():
            if dry_run:
                print(f"[dry-run] remove dir  {dst}")
            else:
                shutil.rmtree(dst)
        if dry_run:
            print(f"[dry-run] copy dir    {src} -> {dst}")
        else:
            shutil.copytree(src, dst, ignore=IGNORE_PATTERNS)
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"[dry-run] copy file   {src} -> {dst}")
    else:
        shutil.copy2(src, dst)


def replace_section(text: str, heading: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}\s*$.*?)(?=^## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if match:
        start, end = match.span(1)
        return text[:start] + replacement.rstrip() + "\n\n" + text[end:]
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"


def extract_section(text: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}\s*$.*?)(?=^## |\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).rstrip() if match else None


def merge_skill_md(src: Path, dst: Path, dry_run: bool) -> None:
    repo_text = src.read_text(encoding="utf-8")
    if not dst.exists():
        if dry_run:
            print(f"[dry-run] copy file   {src} -> {dst}")
        else:
            shutil.copy2(src, dst)
        return

    local_text = dst.read_text(encoding="utf-8")
    local_environment = extract_section(local_text, "Environment")
    merged = repo_text
    if local_environment:
        merged = replace_section(merged, "Environment", local_environment)
    if dry_run:
        print(f"[dry-run] merge file  {src} -> {dst} (preserve target Environment section)")
    else:
        dst.write_text(merged, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    skill_dir = Path(args.skill_dir).resolve()
    skill_dir.mkdir(parents=True, exist_ok=True)

    print(f"Source: {repo_root}")
    print(f"Target: {skill_dir}")

    if args.include_skill_md and args.merge_skill_md:
        raise ValueError("Use either --include-skill-md or --merge-skill-md, not both.")

    items = [*INCLUDE_ITEMS]
    if args.include_skill_md:
        items = ["SKILL.md", *items]
    if args.merge_skill_md:
        merge_skill_md(repo_root / "SKILL.md", skill_dir / "SKILL.md", args.dry_run)

    for item in items:
        src = repo_root / item
        if not src.exists():
            print(f"[skip] missing {src}")
            continue
        dst = skill_dir / item
        copy_item(src, dst, args.dry_run)

    print("Sync complete." if not args.dry_run else "Dry run complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
