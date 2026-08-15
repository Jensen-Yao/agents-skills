#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage a canonical local source image for an exact Visiomaster replica round."
    )
    parser.add_argument("--input", required=True, help="Original source image path.")
    parser.add_argument("--workspace", required=True, help="Reconstruction workspace directory.")
    parser.add_argument("--id", default="figure", help="Figure id recorded in source manifest.")
    parser.add_argument("--output-name", default="original", help="Base filename for staged source image.")
    parser.add_argument("--manifest-name", default="source_manifest.json", help="Manifest filename under source/.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing staged source image.")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists() or not input_path.is_file():
        raise FileNotFoundError(f"Source image does not exist: {input_path}")
    if input_path.suffix.lower() not in IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image extension `{input_path.suffix}` for {input_path}")

    workspace = Path(args.workspace).resolve()
    source_dir = workspace / "source"
    source_dir.mkdir(parents=True, exist_ok=True)
    staged_path = source_dir / f"{args.output_name}{input_path.suffix.lower()}"
    if staged_path.exists() and not args.force:
        existing_hash = sha256_file(staged_path)
        input_hash = sha256_file(input_path)
        if existing_hash != input_hash:
            raise FileExistsError(
                f"Staged source already exists with different hash: {staged_path}. "
                "Use --force to replace it or choose --output-name."
            )
    else:
        shutil.copy2(input_path, staged_path)

    manifest_path = source_dir / args.manifest_name
    manifest = load_json(manifest_path)
    manifest.update(
        {
            "figure_id": args.id,
            "canonical_source_image": str(staged_path),
            "canonical_source_sha256": sha256_file(staged_path),
            "original_input_path": str(input_path),
            "original_input_sha256": sha256_file(input_path),
            "source_dir": str(source_dir),
        }
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Staged source image: {staged_path}")
    print(f"Wrote source manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
