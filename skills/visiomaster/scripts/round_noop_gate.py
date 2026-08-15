#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops


INDEX_RE = re.compile(r"\[\d+\]")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_subpath(value: str) -> str:
    return INDEX_RE.sub("[]", value)


def normalize_string_list(value: object) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def matches_pattern(subpath: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if subpath == pattern:
            return True
        if subpath.startswith(pattern + ".") or subpath.startswith(pattern + "[") or subpath.startswith(pattern + "[]"):
            return True
    return False


def diff_values(before: Any, after: Any, path: str, changes: list[dict[str, Any]]) -> None:
    if type(before) is not type(after):
        changes.append({"path": path, "before": before, "after": after})
        return
    if isinstance(before, dict):
        keys = sorted(set(before) | set(after))
        for key in keys:
            child_path = f"{path}.{key}" if path else str(key)
            if key not in before:
                changes.append({"path": child_path, "before": None, "after": after[key]})
            elif key not in after:
                changes.append({"path": child_path, "before": before[key], "after": None})
            else:
                diff_values(before[key], after[key], child_path, changes)
        return
    if isinstance(before, list):
        if (
            path in {"nodes", "edges"}
            and all(isinstance(item, dict) and item.get("id") for item in before)
            and all(isinstance(item, dict) and item.get("id") for item in after)
        ):
            before_map = {str(item["id"]): item for item in before}
            after_map = {str(item["id"]): item for item in after}
            keys = sorted(set(before_map) | set(after_map))
            for key in keys:
                child_path = f"{path}.{key}"
                if key not in before_map:
                    changes.append({"path": child_path, "before": None, "after": after_map[key]})
                elif key not in after_map:
                    changes.append({"path": child_path, "before": before_map[key], "after": None})
                else:
                    diff_values(before_map[key], after_map[key], child_path, changes)
            return
        if len(before) != len(after):
            changes.append({"path": path, "before": before, "after": after})
            return
        for index, (left, right) in enumerate(zip(before, after)):
            diff_values(left, right, f"{path}[{index}]", changes)
        return
    if before != after:
        changes.append({"path": path, "before": before, "after": after})


def load_effective_map(path: Path) -> dict[str, Any]:
    return load_json(path)


def classify_change(change: dict[str, Any], before_scene: dict[str, Any], after_scene: dict[str, Any], field_map: dict[str, Any]) -> tuple[str, str | None]:
    path = str(change["path"])
    defaults = field_map["_defaults"]
    if path.startswith("metadata.") or path == "metadata" or path.startswith("assets.") or path == "assets":
        return "metadata", None
    if path.startswith("page.") or path == "page":
        subpath = normalize_subpath(path.split(".", 1)[1]) if "." in path else ""
        if matches_pattern(subpath, defaults["page_effective_fields"]):
            return "effective", "__page__"
        if matches_pattern(subpath, defaults["page_weak_fields"]):
            return "weak", "__page__"
        return "unknown", "__page__"
    if path.startswith("nodes.") or path == "nodes":
        parts = path.split(".", 2)
        if len(parts) < 2:
            return "effective", None
        node_id = parts[1]
        if len(parts) == 2:
            return "effective", node_id
        subpath = normalize_subpath(parts[2])
        before_node = next((node for node in before_scene.get("nodes", []) if isinstance(node, dict) and str(node.get("id")) == node_id), None)
        after_node = next((node for node in after_scene.get("nodes", []) if isinstance(node, dict) and str(node.get("id")) == node_id), None)
        node_type = str((after_node or before_node or {}).get("type", ""))
        component_map = field_map.get("components", {}).get(node_type, {})
        effective_patterns = defaults["common_node_effective_fields"] + component_map.get("effective_fields", [])
        weak_patterns = defaults["common_node_weak_fields"] + component_map.get("weak_fields", [])
        if matches_pattern(subpath, effective_patterns):
            return "effective", node_id
        if matches_pattern(subpath, weak_patterns):
            return "weak", node_id
        return "unknown", node_id
    if path.startswith("edges.") or path == "edges":
        parts = path.split(".", 2)
        if len(parts) < 2:
            return "effective", None
        edge_id = parts[1]
        if len(parts) == 2:
            return "effective", edge_id
        subpath = normalize_subpath(parts[2])
        if matches_pattern(subpath, defaults["common_edge_effective_fields"]):
            return "effective", edge_id
        if matches_pattern(subpath, defaults["common_edge_weak_fields"]):
            return "weak", edge_id
        return "unknown", edge_id
    return "unknown", None


def pixel_diff_report(before_path: Path, after_path: Path) -> dict[str, Any]:
    before = Image.open(before_path).convert("RGB")
    after = Image.open(after_path).convert("RGB")
    if before.size != after.size:
        return {
            "same_pixels": False,
            "diff_pixels": None,
            "size_changed": True,
            "before_size": list(before.size),
            "after_size": list(after.size),
        }
    diff = ImageChops.difference(before, after)
    bbox = diff.getbbox()
    if bbox is None:
        return {
            "same_pixels": True,
            "diff_pixels": 0,
            "size_changed": False,
            "before_size": list(before.size),
            "after_size": list(after.size),
        }
    diff_pixels = 0
    for pixel in diff.getdata():
        if pixel != (0, 0, 0):
            diff_pixels += 1
    return {
        "same_pixels": False,
        "diff_pixels": diff_pixels,
        "size_changed": False,
        "before_size": list(before.size),
        "after_size": list(after.size),
    }


def load_target_hints(path: Path) -> tuple[str, list[dict[str, Any]]]:
    plan = load_json(path)
    if not isinstance(plan, dict):
        return "unknown", []
    findings_digest = plan.get("findings_digest", [])
    if isinstance(findings_digest, list):
        hints = []
        for finding in findings_digest:
            if not isinstance(finding, dict):
                continue
            hints.append(
                {
                    "finding_id": finding.get("id"),
                    "focus_regions": normalize_string_list(finding.get("focus_regions")),
                    "scene_targets": normalize_string_list(finding.get("likely_scene_ids")),
                    "target_layer": "scene",
                }
            )
        return "rebuild_brief", hints
    tasks = plan.get("tasks", [])
    if isinstance(tasks, list):
        return "legacy_repair_plan", [task for task in tasks if isinstance(task, dict)]
    return "unknown", []


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail the round when the scene/render changes are effectively a no-op.")
    parser.add_argument("--before-scene", required=True)
    parser.add_argument("--after-scene", required=True)
    parser.add_argument("--before-png", required=True)
    parser.add_argument("--after-png", required=True)
    parser.add_argument(
        "--rebuild-brief",
        help="Optional scene_rebuild_brief.json for diagnostic focus-region and legacy-id tracking.",
    )
    parser.add_argument("--repair-plan", help=argparse.SUPPRESS)
    parser.add_argument("--effective-map", help="Optional effective-fields JSON path.")
    parser.add_argument("--output-report", help="Optional JSON report path.")
    args = parser.parse_args()

    before_scene_path = Path(args.before_scene).resolve()
    after_scene_path = Path(args.after_scene).resolve()
    before_png_path = Path(args.before_png).resolve()
    after_png_path = Path(args.after_png).resolve()
    effective_map_path = (
        Path(args.effective_map).resolve()
        if args.effective_map
        else Path(__file__).resolve().parents[1] / "references" / "renderer-effective-fields.json"
    )

    before_scene = load_json(before_scene_path)
    after_scene = load_json(after_scene_path)
    field_map = load_effective_map(effective_map_path)
    before_scene_sha256 = file_sha256(before_scene_path)
    after_scene_sha256 = file_sha256(after_scene_path)

    raw_changes: list[dict[str, Any]] = []
    diff_values(before_scene, after_scene, "", raw_changes)
    raw_changes = [change for change in raw_changes if change["path"]]

    effective_changes: list[str] = []
    weak_changes: list[str] = []
    metadata_changes: list[str] = []
    unknown_changes: list[str] = []
    changed_ids_by_class: dict[str, set[str]] = defaultdict(set)

    for change in raw_changes:
        change_class, target_id = classify_change(change, before_scene, after_scene, field_map)
        if change_class == "effective":
            effective_changes.append(change["path"])
        elif change_class == "weak":
            weak_changes.append(change["path"])
        elif change_class == "metadata":
            metadata_changes.append(change["path"])
        else:
            unknown_changes.append(change["path"])
        if target_id:
            changed_ids_by_class[change_class].add(target_id)

    pixel_report = pixel_diff_report(before_png_path, after_png_path)

    failures: list[str] = []
    if not raw_changes:
        failures.append("Scene JSON did not change at all.")
    if raw_changes and not effective_changes and not weak_changes and metadata_changes:
        failures.append("Scene diff is metadata/assets only; this does not count as a new regeneration round.")
    if raw_changes and not effective_changes and weak_changes and not unknown_changes:
        failures.append("Scene changes touch only weak style fields; no renderer-effective geometry/text/topology fields changed.")
    if raw_changes and not effective_changes and unknown_changes and not weak_changes:
        failures.append("Scene changes do not hit any known renderer-effective fields; update the effective-field map before claiming a new round.")
    if pixel_report["same_pixels"]:
        failures.append("Rendered PNG pixel diff is zero; the round produced no visible change.")

    targeted_checks: list[dict[str, Any]] = []
    target_hint_source_path = args.rebuild_brief or args.repair_plan
    target_hint_source_kind = None
    hint_misses: list[str] = []
    if target_hint_source_path:
        target_hint_source_kind, target_hints = load_target_hints(Path(target_hint_source_path).resolve())
        for task in target_hints:
            target_layer = str(task.get("target_layer", "scene"))
            scene_targets = [str(item) for item in task.get("scene_targets", []) if str(item)]
            if target_layer != "scene":
                continue
            changed_targets = sorted(set(scene_targets) & changed_ids_by_class["effective"])
            targeted_checks.append(
                {
                    "finding_id": task.get("finding_id"),
                    "focus_regions": normalize_string_list(task.get("focus_regions")),
                    "scene_targets": scene_targets,
                    "effective_targets_hit": changed_targets,
                }
            )
            if scene_targets and not changed_targets:
                hint_misses.append(
                    f"Target hints for `{task.get('finding_id')}` did not overlap any renderer-effective changed ids. "
                    "This is diagnostic only because full-scene rebuilds may rename ids."
                )

    report = {
        "before_scene": str(before_scene_path),
        "after_scene": str(after_scene_path),
        "before_png": str(before_png_path),
        "after_png": str(after_png_path),
        "effective_map": str(effective_map_path),
        "scene_hashes": {
            "before_sha256": before_scene_sha256,
            "after_sha256": after_scene_sha256,
            "hash_changed": before_scene_sha256 != after_scene_sha256,
        },
        "change_counts": {
            "raw": len(raw_changes),
            "effective": len(effective_changes),
            "weak": len(weak_changes),
            "metadata": len(metadata_changes),
            "unknown": len(unknown_changes),
        },
        "effective_changes": effective_changes,
        "weak_changes": weak_changes,
        "metadata_changes": metadata_changes,
        "unknown_changes": unknown_changes,
        "changed_ids": {key: sorted(value) for key, value in changed_ids_by_class.items()},
        "pixel_report": pixel_report,
        "target_hint_source": {
            "path": str(Path(target_hint_source_path).resolve()) if target_hint_source_path else None,
            "kind": target_hint_source_kind,
        },
        "target_hint_checks": targeted_checks,
        "target_hint_diagnostics": hint_misses,
        "failures": failures,
        "passed": not failures,
    }

    if args.output_report:
        output_path = Path(args.output_report).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if failures:
        print("ROUND NO-OP GATE FAILED")
        for item in failures:
            print(f"- {item}")
        return 2

    print("ROUND NO-OP GATE PASSED")
    print(f"- effective scene changes: {len(effective_changes)}")
    if pixel_report["size_changed"]:
        print(
            f"- rendered PNG size changed: {pixel_report['before_size'][0]}x{pixel_report['before_size'][1]} -> "
            f"{pixel_report['after_size'][0]}x{pixel_report['after_size'][1]}"
        )
    else:
        print(f"- rendered PNG diff pixels: {pixel_report['diff_pixels']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
