#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def candidate_stencil_roots() -> list[Path]:
    roots: list[Path] = []
    for env_name in ("ProgramFiles", "ProgramFiles(x86)"):
        root = os.environ.get(env_name)
        if root:
            roots.append(Path(root) / "Microsoft Office" / "root" / "Office16" / "Visio Content")
            roots.append(Path(root) / "Microsoft Office" / "Office16" / "Visio Content")
    roots.append(Path(r"C:\Program Files\Microsoft Office\root\Office16\Visio Content"))
    return roots


def find_stencils(max_stencils: int | None = None) -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for root in candidate_stencil_roots():
        if not root.exists():
            continue
        for pattern in ("*.vssx", "*.vss", "*.vstx", "*.vst"):
            for path in root.rglob(pattern):
                resolved = path.resolve()
                if resolved in seen:
                    continue
                seen.add(resolved)
                paths.append(resolved)
                if max_stencils and len(paths) >= max_stencils:
                    return paths
    return paths


def master_record(stencil_path: Path, master: Any) -> dict[str, str]:
    def read_attr(name: str) -> str:
        try:
            return str(getattr(master, name))
        except Exception:
            return ""

    return {
        "stencil": str(stencil_path),
        "name": read_attr("Name"),
        "name_u": read_attr("NameU"),
        "prompt": read_attr("Prompt"),
    }


def enumerate_masters(stencils: list[Path], visible: bool = False) -> list[dict[str, str]]:
    try:
        import win32com.client.gencache as gencache
    except ImportError as exc:
        raise SystemExit("pywin32 is required in the active Python environment.") from exc

    app = gencache.EnsureDispatch("Visio.Application")
    app.Visible = bool(visible)
    try:
        app.AlertResponse = 7
    except Exception:
        pass

    records: list[dict[str, str]] = []
    try:
        for stencil_path in stencils:
            doc = None
            try:
                doc = app.Documents.OpenEx(str(stencil_path), 64)
                count = int(doc.Masters.Count)
                for index in range(1, count + 1):
                    records.append(master_record(stencil_path, doc.Masters.Item(index)))
            except Exception as exc:
                records.append({"stencil": str(stencil_path), "name": "", "name_u": "", "prompt": f"ERROR: {exc}"})
            finally:
                if doc is not None:
                    try:
                        doc.Close()
                    except Exception:
                        pass
    finally:
        if not visible:
            try:
                app.Quit()
            except Exception:
                pass
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enumerate installed Visio stencil masters for local mapping research.")
    parser.add_argument("--stencil", action="append", help="Specific stencil path. Can be repeated.")
    parser.add_argument("--output", help="Optional JSON output path.")
    parser.add_argument("--max-stencils", type=int, help="Limit auto-discovered stencils for quick inspection.")
    parser.add_argument("--visible", action="store_true", help="Show Visio while scanning.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    stencils = [Path(item).resolve() for item in args.stencil] if args.stencil else find_stencils(args.max_stencils)
    records = enumerate_masters(stencils, visible=args.visible)

    payload = {"stencil_count": len(stencils), "master_count": len(records), "masters": records}
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote: {output}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
