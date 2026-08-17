#!/usr/bin/env python3
"""Expose the canonical skills to local DSH and model-management skill roots."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        help="Target configuration (default: config/skill-targets.json).",
    )
    parser.add_argument(
        "--target",
        action="append",
        dest="targets",
        help="Sync only the named target. Repeat to select several targets.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report missing or conflicting links without changing the filesystem.",
    )
    return parser.parse_args()


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if config.get("version") != 1:
        raise ValueError(f"Unsupported target config: {path}")
    if not isinstance(config.get("targets"), list):
        raise ValueError(f"Target config requires a targets list: {path}")
    return config


def canonical_source(config: dict[str, Any], root: Path) -> Path:
    configured = config.get("source")
    source = (Path(configured) if configured else root / "skills").expanduser()
    if not source.is_absolute():
        source = root / source
    return source.resolve()


def skill_entries(source: Path) -> list[Path]:
    return sorted(
        entry
        for entry in source.iterdir()
        if entry.is_dir() and ((entry / "SKILL.md").is_file() or (entry / "REFERENCE.md").is_file())
    )


def junction_target(path: Path) -> Path | None:
    if not path.is_junction():
        return None
    return Path(os.path.realpath(path))


def create_junction(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(target), str(source)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown mklink error"
        raise RuntimeError(f"Failed to link {target} -> {source}: {detail}")


def sync_target(source: Path, target: Path, check: bool) -> tuple[int, int]:
    if not source.is_dir():
        raise FileNotFoundError(f"Canonical skill root does not exist: {source}")
    if not target.is_dir():
        raise FileNotFoundError(f"Skill target does not exist: {target}")

    created = 0
    conflicts = 0
    for source_entry in skill_entries(source):
        destination = target / source_entry.name
        if not destination.exists() and not destination.is_symlink():
            if not check:
                create_junction(source_entry, destination)
            created += 1
            continue

        resolved = junction_target(destination)
        if resolved is not None and resolved == source_entry.resolve():
            continue

        conflicts += 1
        print(
            f"Conflict preserved: {destination} already exists and is not a link to {source_entry}",
            file=sys.stderr,
        )
    return created, conflicts


def main() -> int:
    args = parse_args()
    root = repo_root()
    config_path = args.config or root / "config" / "skill-targets.json"
    config = load_config(config_path)
    source = canonical_source(config, root)
    selected = set(args.targets or [])
    targets = [item for item in config["targets"] if not selected or item.get("name") in selected]
    if selected and len(targets) != len(selected):
        unknown = sorted(selected - {item.get("name") for item in targets})
        raise ValueError(f"Unknown target(s): {', '.join(unknown)}")

    total_created = 0
    total_conflicts = 0
    for item in targets:
        name = item.get("name")
        target = Path(str(item.get("path"))).expanduser().resolve()
        created, conflicts = sync_target(source, target, args.check)
        total_created += created
        total_conflicts += conflicts
        action = "would create" if args.check else "created/verified"
        print(f"{name}: {action} {created} link(s); {conflicts} conflict(s)")

    if total_conflicts:
        return 2
    return 1 if args.check and total_created else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Skill target sync failed: {error}", file=sys.stderr)
        sys.exit(2)
