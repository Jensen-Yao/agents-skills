#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from font_utils import ROLE_FALLBACKS, font_inventory_summary, installed_font_match


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List fonts visible to visiomaster on this Windows machine.")
    parser.add_argument("--json", action="store_true", help="Write machine-readable JSON.")
    parser.add_argument("--limit", type=int, default=80, help="Number of font names to print in text mode.")
    parser.add_argument("--check", action="append", default=[], help="Check whether a font family is installed. Can be repeated.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = font_inventory_summary()
    checks = {name: installed_font_match(name) for name in args.check}
    if args.json:
        print(json.dumps({**summary, "checks": checks}, indent=2, ensure_ascii=False))
        return 0

    print(f"Installed base font families: {summary['font_count']}")
    print(f"Installed registry font entries: {summary['font_entry_count']}")
    print(f"Canonical lookup entries: {summary['canonical_count']}")
    for name, match in checks.items():
        print(f"check {name}: {match or 'not found'}")
    print("")
    print("Role fallback availability:")
    for role, candidates in ROLE_FALLBACKS.items():
        available = [font for font in candidates if installed_font_match(font)]
        print(f"- {role}: {available[0] if available else 'no preferred font found'}")
    print("")
    print(f"First {min(args.limit, len(summary['fonts']))} fonts:")
    for font in summary["fonts"][: args.limit]:
        print(font)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
