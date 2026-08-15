#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def image_size(path: str | None) -> tuple[int, int] | None:
    if not path:
        return None
    try:
        from PIL import Image

        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def page_from_args(args: argparse.Namespace) -> dict:
    size = image_size(args.image)
    if args.pixel_page and size:
        width, height = size
        page = {
            "width": width,
            "height": height,
            "units": "px",
            "origin": "top-left",
            "target_width_in": args.target_width_in,
            "background": "#FFFFFF",
        }
        if args.target_height_in:
            page["target_height_in"] = args.target_height_in
        return page

    return {
        "width": args.page_width,
        "height": args.page_height,
        "units": "in",
        "origin": "top-left",
        "background": "#FFFFFF",
    }


def build_blank_scene(args: argparse.Namespace) -> dict:
    assets = []
    if args.image:
        assets.append(
            {
                "id": "source-image",
                "kind": "source_image",
                "path": str(Path(args.image).resolve()),
            }
        )
    if args.style_ref:
        assets.append(
            {
                "id": "style-reference",
                "kind": "style_reference",
                "path": str(Path(args.style_ref).resolve()),
            }
        )

    metadata = {
        "title": args.title,
        "created_by": "visiomaster.image_to_scene",
        "style_profile": args.style_profile,
        "fidelity": args.fidelity,
        "region_strategy": args.region_strategy,
        "source_image": str(Path(args.image).resolve()) if args.image else None,
        "style_reference": str(Path(args.style_ref).resolve()) if args.style_ref else None,
        "starter_mode": "blank_source_inventory",
        "notes": [
            "Starter scene only. Replace nodes and edges after visual analysis.",
            "Coordinates use top-left page origin and inches.",
            "Prefer editable reconstruction over full-image embedding.",
            "Record typography intent with source_font_family, font_family_candidates, and font_role when the source has distinctive fonts.",
        ],
    }
    if args.fidelity == "exact":
        metadata["replica_review_mode"] = "strict_replica"
        metadata["replica_stage"] = "layout_topology"

    return {
        "version": "0.1",
        "metadata": metadata,
        "page": page_from_args(args),
        "nodes": [],
        "edges": [],
        "assets": assets,
    }


TEMPLATE_FILES = {
    "basic-flow": "basic_flow",
    "gan-tfr": "gan_tfr_full",
}


def load_template(template_name: str) -> dict:
    filename = TEMPLATE_FILES.get(template_name, template_name)
    template_path = (
        Path(__file__).resolve().parents[1]
        / "templates"
        / "examples"
        / f"{filename}.scene.json"
    )
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return json.loads(template_path.read_text(encoding="utf-8"))


def merge_source_metadata(scene: dict, args: argparse.Namespace) -> dict:
    metadata = scene.setdefault("metadata", {})
    assets = scene.setdefault("assets", [])

    metadata["title"] = args.title or metadata.get("title") or "VisioMaster Scene"
    metadata["created_by"] = "visiomaster.image_to_scene"
    metadata["style_profile"] = args.style_profile or metadata.get("style_profile") or "paper_white"
    metadata["fidelity"] = args.fidelity or metadata.get("fidelity")
    metadata["region_strategy"] = args.region_strategy or metadata.get("region_strategy")
    metadata["starter_mode"] = "template_seed"
    metadata["starter_template"] = args.template
    metadata["starter_template_bootstrap_only"] = True

    if args.image:
        image_path = str(Path(args.image).resolve())
        metadata["source_image"] = image_path
        assets.append({"id": "source-image", "kind": "source_image", "path": image_path})

    if args.style_ref:
        style_path = str(Path(args.style_ref).resolve())
        metadata["style_reference"] = style_path
        assets.append({"id": "style-reference", "kind": "style_reference", "path": style_path})

    return scene


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a starter scene.json for visiomaster.",
    )
    parser.add_argument("--image", help="Optional source image path.")
    parser.add_argument("--style-ref", help="Optional style reference image path.")
    parser.add_argument(
        "--template",
        choices=["blank", "basic-flow", "gan-tfr"],
        default="blank",
        help="Starter template.",
    )
    parser.add_argument(
        "--preserve-template-page",
        action="store_true",
        help="Keep the page definition from the selected template instead of overriding it from CLI/page defaults.",
    )
    parser.add_argument("--title", default="VisioMaster Scene")
    parser.add_argument("--page-width", type=float, default=13.333)
    parser.add_argument("--page-height", type=float, default=7.5)
    parser.add_argument(
        "--pixel-page",
        action="store_true",
        help="Use the source image pixel width/height as page coordinates. Recommended for exact large-figure replicas.",
    )
    parser.add_argument("--target-width-in", type=float, default=13.333)
    parser.add_argument("--target-height-in", type=float, help="Optional rendered page height when using --pixel-page.")
    parser.add_argument(
        "--fidelity",
        choices=["draft", "clean", "exact"],
        default="exact",
        help="Reconstruction fidelity hint stored in metadata.",
    )
    parser.add_argument(
        "--region-strategy",
        choices=["", "region_first", "tiled_subscenes", "module_first", "section_first"],
        default="",
        help="Large-figure build strategy stored in metadata.",
    )
    parser.add_argument(
        "--style-profile",
        choices=["paper_white", "clean_white"],
        default="paper_white",
    )
    parser.add_argument("--output", required=True, help="Output scene.json path.")
    parser.add_argument(
        "--allow-template-seed-in-exact",
        action="store_true",
        help="Allow a template seed even when --fidelity exact is selected. This is bootstrap-only metadata and is not valid as strict capability proof.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output file if it exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = Path(args.output).resolve()
    if output_path.exists() and not args.overwrite:
        raise FileExistsError(f"Output already exists: {output_path}")
    if args.pixel_page and args.template != "blank":
        raise ValueError("--pixel-page is only supported with --template blank because built-in templates define their own coordinate systems.")
    if args.fidelity == "exact" and args.template != "blank" and not args.allow_template_seed_in_exact:
        raise ValueError(
            "Strict/exact starter scenes must begin from a blank source-driven scene. "
            "Use --template only for draft/clean bootstrap work, or pass --allow-template-seed-in-exact when you intentionally want a non-final bootstrap scene."
        )

    if args.template == "blank":
        scene = build_blank_scene(args)
    else:
        scene = merge_source_metadata(load_template(args.template), args)
        if not args.preserve_template_page and args.template != "gan-tfr":
            scene["page"] = page_from_args(args)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(scene, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote starter scene: {output_path}")
    print("Next steps:")
    print("1. Edit nodes, edges, and styles.")
    print("2. Validate with scene_validate.py.")
    print("3. Render with scene_to_visio.py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
