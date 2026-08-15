#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

from scene_validate import (
    CONTAINER_TYPES,
    edge_endpoint_node_id,
    edge_endpoint_role,
    edge_point,
    endpoint_position,
    endpoint_side,
    node_box,
    node_center,
    node_semantic_text,
    point_in_box,
    scene_looks_like_gan_tfr,
    text_has_raw_loss_subscript,
)


def load_scene(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def node_maps(scene: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    nodes_by_id = {node["id"]: node for node in scene.get("nodes", []) if node.get("id")}
    node_types_by_id = {node["id"]: node.get("type", "") for node in scene.get("nodes", []) if node.get("id")}
    return nodes_by_id, node_types_by_id


def change(changes: list[str], message: str) -> None:
    if message not in changes:
        changes.append(message)


def record_recipe_application(scene: dict[str, Any], recipe: str, changes: list[str], applied_by: str) -> None:
    metadata = scene.setdefault("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
        scene["metadata"] = metadata
    history = metadata.get("autofix_history")
    if not isinstance(history, list):
        history = []
    entry = {
        "recipe": recipe,
        "applied_by": applied_by,
        "change_count": len(changes),
        "changes": list(changes),
    }
    if not history or canonical_json(history[-1]) != canonical_json(entry):
        history.append(entry)
    metadata["autofix_history"] = history
    metadata["last_autofix_recipe"] = recipe
    metadata["last_autofix_applied_by"] = applied_by


def endpoint_node_id(endpoint: Any) -> str | None:
    if not isinstance(endpoint, str):
        return None
    return endpoint.split(":", 1)[0]


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def format_ratio(value: float) -> str:
    return f"{clamp(value):.3f}".rstrip("0").rstrip(".")


def canonical_value(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 3)
    if isinstance(value, int):
        return float(value)
    if isinstance(value, list):
        return [canonical_value(item) for item in value]
    if isinstance(value, dict):
        return {key: canonical_value(value[key]) for key in sorted(value)}
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(canonical_value(value), sort_keys=True, ensure_ascii=False)


def endpoint_suffix(endpoint: str) -> str:
    if ":" not in endpoint:
        return ""
    return ":" + endpoint.split(":", 1)[1]


def resolve_endpoint_point(
    endpoint: Any,
    nodes_by_id: dict[str, dict[str, Any]],
    peer: tuple[float, float] | None = None,
) -> tuple[float, float] | None:
    if not isinstance(endpoint, str):
        return None
    node_id = endpoint_node_id(endpoint)
    if not node_id or node_id not in nodes_by_id:
        return None
    node = nodes_by_id[node_id]
    if not all(isinstance(node.get(key), (int, float)) for key in ("x", "y", "w", "h")):
        return None
    x1, y1, x2, y2 = node_box(node)
    side = endpoint_side(endpoint)
    if side is None and peer is not None:
        cx, cy = node_center(node)
        dx = peer[0] - cx
        dy = peer[1] - cy
        side = "right" if abs(dx) >= abs(dy) and dx >= 0 else "left" if abs(dx) >= abs(dy) else "bottom" if dy >= 0 else "top"
    side = side or "center"
    pos = endpoint_position(endpoint)
    if side == "left":
        return x1, y1 + (y2 - y1) * (0.5 if pos is None else pos)
    if side == "right":
        return x2, y1 + (y2 - y1) * (0.5 if pos is None else pos)
    if side == "top":
        return x1 + (x2 - x1) * (0.5 if pos is None else pos), y1
    if side == "bottom":
        return x1 + (x2 - x1) * (0.5 if pos is None else pos), y2
    return (x1 + x2) / 2, (y1 + y2) / 2


def node_text(node: dict[str, Any]) -> str:
    return str(node.get("text", node.get("title", ""))).strip()


def normalize_caption_text(text: str) -> str:
    cleaned = str(text).replace("Ўъ", "→").replace("->", "→")
    cleaned = cleaned.replace("=>", "→")
    return " ".join(cleaned.split())


def normalize_loss_formula_text(text: str) -> str:
    def replace_loss(match: re.Match[str]) -> str:
        return f"L_{match.group(1).lower()}"

    return re.sub(r"\bL\s*_?\s*(adv|rec)\b", replace_loss, str(text), flags=re.IGNORECASE)


def normalize_formula_fields(node: dict[str, Any], changes: list[str]) -> None:
    changed = False
    if isinstance(node.get("text"), str):
        normalized = normalize_loss_formula_text(node["text"])
        if normalized != node["text"]:
            node["text"] = normalized
            changed = True
    for key in ("formulas", "lines"):
        value = node.get(key)
        if isinstance(value, str):
            normalized = normalize_loss_formula_text(value)
            if normalized != value:
                node[key] = normalized
                changed = True
        elif isinstance(value, list):
            normalized_items = [normalize_loss_formula_text(item) for item in value]
            if normalized_items != value:
                node[key] = normalized_items
                changed = True
    if changed:
        change(changes, f"normalized loss formulas in `{node.get('id')}`")


def child_nodes_inside(parent: dict[str, Any], nodes: list[dict[str, Any]], tolerance: float = 0.01) -> list[dict[str, Any]]:
    box = node_box(parent)
    children: list[dict[str, Any]] = []
    for node in nodes:
        if node is parent or not all(isinstance(node.get(key), (int, float)) for key in ("x", "y", "w", "h")):
            continue
        if point_in_box(node_center(node), box, tolerance=tolerance):
            children.append(node)
    return children


def rewrite_consumed_endpoints(
    scene: dict[str, Any],
    consumed_to_parent: dict[str, tuple[str, str]],
) -> None:
    for edge in scene.get("edges", []):
        for endpoint_name in ("from", "to"):
            endpoint = edge.get(endpoint_name)
            child_id = endpoint_node_id(endpoint)
            if child_id not in consumed_to_parent:
                continue
            parent_id, fallback_suffix = consumed_to_parent[child_id]
            suffix = endpoint_suffix(endpoint) if isinstance(endpoint, str) and ":" in endpoint else fallback_suffix
            edge[endpoint_name] = f"{parent_id}{suffix}"


def apply_tfr_panel_compaction_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    nodes = scene.get("nodes", [])
    nodes_by_id, _ = node_maps(scene)
    if not scene_looks_like_gan_tfr(scene, nodes_by_id):
        return

    consumed_to_parent: dict[str, tuple[str, str]] = {}
    remove_ids: set[str] = set()
    remove_edge_ids: set[str] = set()

    for panel in list(nodes):
        if panel.get("type") not in {"rounded_process", "process_box"}:
            continue
        if str(panel.get("text", "")).strip():
            continue
        children = child_nodes_inside(panel, nodes, tolerance=0.03)
        grid = next((node for node in children if node.get("type") == "grid_matrix"), None)
        if grid is None:
            continue

        text_children = [
            node
            for node in children
            if node.get("type") in {"text_block", "math_text"} and node_text(node)
        ]
        if not any(str(node_text(node)).strip().lower() == "input" for node in text_children):
            continue
        title_nodes = [
            node
            for node in sorted(text_children, key=lambda item: (float(item.get("y", 0)), float(item.get("x", 0))))
            if str(node_text(node)).strip().lower() != "input"
        ]
        title_texts = [node_text(node) for node in title_nodes]
        combined = " ".join(title_texts).lower()
        if not any(token in combined for token in {"real", "generated", "tfr", "reconstructed"}):
            continue

        input_node = next(node for node in text_children if str(node_text(node)).strip().lower() == "input")
        panel["type"] = "tfr_panel"
        if title_texts:
            panel["title"] = title_texts[0]
        if len(title_texts) > 1:
            panel["subtitle"] = title_texts[1]
        panel["input_label"] = node_text(input_node) or "Input"
        panel["rows"] = int(grid.get("rows", 4))
        panel["cols"] = int(grid.get("cols", 5))
        if grid.get("colored_cells") is not None:
            panel["colored_cells"] = grid.get("colored_cells")
        elif grid.get("cells") is not None:
            panel["colored_cells"] = grid.get("cells")
        for source_key, target_key in (
            ("x", "grid_x"),
            ("y", "grid_y"),
            ("w", "grid_w"),
            ("h", "grid_h"),
        ):
            panel[target_key] = grid.get(source_key)
        panel["input_y"] = input_node.get("y")

        style = panel.setdefault("style", {})
        for node, key in ((title_nodes[0], "title_font_size_pt") if title_nodes else ({}, ""), (input_node, "input_font_size_pt")):
            if key and isinstance(node, dict):
                font_size = (node.get("style") or {}).get("font_size_pt")
                if font_size is not None:
                    style.setdefault(key, font_size)
        if len(title_nodes) > 1:
            subtitle_font = (title_nodes[1].get("style") or {}).get("font_size_pt")
            if subtitle_font is not None:
                style.setdefault("subtitle_font_size_pt", subtitle_font)

        panel_id = str(panel.get("id"))
        consumed = [grid, input_node, *title_nodes]
        for child in consumed:
            child_id = str(child.get("id"))
            if not child_id:
                continue
            remove_ids.add(child_id)
            fallback = ":bottom@0.5" if child is input_node else ":center"
            consumed_to_parent[child_id] = (panel_id, fallback)

        px1, py1, px2, py2 = node_box(panel)
        panel_margin = max(float(panel.get("w", 0)) * 0.04, float(panel.get("h", 0)) * 0.04, 0.04)
        for edge in scene.get("edges", []):
            edge_id = str(edge.get("id", ""))
            if edge.get("type") not in {"arrow_connector", "lane_arrow", "line_segment"}:
                continue
            start = edge_point(edge, "from")
            end = edge_point(edge, "to")
            if start is None or end is None:
                continue
            inside_x = px1 - panel_margin <= start[0] <= px2 + panel_margin and px1 - panel_margin <= end[0] <= px2 + panel_margin
            inside_y = py1 - panel_margin <= start[1] <= py2 + panel_margin and py1 - panel_margin <= end[1] <= py2 + panel_margin
            vertical = abs(start[0] - end[0]) <= max(0.04, float(panel.get("w", 0)) * 0.05)
            if inside_x and inside_y and vertical and ("input" in edge_id.lower() or edge.get("type") == "line_segment"):
                panel["input_arrow"] = True
                remove_edge_ids.add(edge_id)
                change(changes, f"absorbed `{edge_id}` as internal tfr_panel input_arrow")
        change(changes, f"compacted `{panel_id}` children into editable tfr_panel")

    if remove_ids:
        rewrite_consumed_endpoints(scene, consumed_to_parent)
        scene["nodes"] = [node for node in nodes if str(node.get("id")) not in remove_ids]
    if remove_edge_ids:
        scene["edges"] = [edge for edge in scene.get("edges", []) if str(edge.get("id")) not in remove_edge_ids]


def apply_loss_region_compaction_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    nodes = scene.get("nodes", [])
    nodes_by_id, _ = node_maps(scene)
    if not scene_looks_like_gan_tfr(scene, nodes_by_id):
        return

    remove_ids: set[str] = set()
    consumed_to_parent: dict[str, tuple[str, str]] = {}
    for region in list(nodes):
        if region.get("type") not in {"dashed_region", "process_box"}:
            continue
        children = child_nodes_inside(region, nodes, tolerance=0.04)
        formula_node = next(
            (
                node
                for node in children
                if node.get("type") in {"text_block", "math_text"}
                and any(token in node_text(node).lower() for token in {"loss", "penalty", "l_adv", "l_rec"})
            ),
            None,
        )
        if formula_node is None:
            continue

        x1, y1, x2, _ = node_box(region)
        nearby_captions = []
        for node in nodes:
            if node is region or node is formula_node or node.get("type") != "text_block" or not node_text(node):
                continue
            cx, cy = node_center(node)
            text = node_text(node).lower()
            if x1 - float(region.get("w", 0)) * 0.4 <= cx <= x2 + float(region.get("w", 0)) * 0.4 and y1 - float(region.get("h", 0)) * 0.8 <= cy <= y1 + 0.05:
                if "forward" in text or "discriminator" in text or "evaluation" in text:
                    nearby_captions.append(node)

        region["type"] = "loss_region"
        if nearby_captions:
            caption = min(nearby_captions, key=lambda item: abs(node_center(item)[0] - node_center(region)[0]))
            region["title"] = normalize_caption_text(node_text(caption))
            remove_ids.add(str(caption.get("id")))
            consumed_to_parent[str(caption.get("id"))] = (str(region.get("id")), ":top@0.5")
        else:
            region.setdefault("title", "Forward Reconstruction → Discriminator Evaluation")
        region["formulas"] = [normalize_loss_formula_text(line.strip()) for line in node_text(formula_node).splitlines() if line.strip()]
        style = region.setdefault("style", {})
        style.setdefault("fill", "none")
        style.setdefault("line_dash", "dash")
        formula_font = (formula_node.get("style") or {}).get("font_size_pt")
        if formula_font is not None:
            style.setdefault("font_size_pt", formula_font)
        remove_ids.add(str(formula_node.get("id")))
        consumed_to_parent[str(formula_node.get("id"))] = (str(region.get("id")), ":center")
        change(changes, f"compacted `{region.get('id')}` into editable loss_region")

    if remove_ids:
        rewrite_consumed_endpoints(scene, consumed_to_parent)
        scene["nodes"] = [node for node in nodes if str(node.get("id")) not in remove_ids]


def find_update_label(scene: dict[str, Any]) -> str | None:
    candidates: list[tuple[int, str]] = []
    for node in scene.get("nodes", []):
        if node.get("type") != "text_block":
            continue
        text = str(node.get("text", "")).lower()
        node_id = str(node.get("id", ""))
        if "alternating" in text or "update" in text:
            candidates.append((0, node_id))
        elif "backprop" in text or "loss" in text:
            candidates.append((1, node_id))
    if not candidates:
        return None
    return sorted(candidates)[0][1]


def endpoint_point(
    edge: dict[str, Any],
    endpoint_name: str,
    nodes_by_id: dict[str, dict[str, Any]],
    peer: tuple[float, float] | None = None,
) -> tuple[float, float] | None:
    explicit = edge_point(edge, endpoint_name)
    if explicit is not None:
        return explicit
    return resolve_endpoint_point(edge.get(endpoint_name), nodes_by_id, peer)


def ensure_terminal_tangent(edge: dict[str, Any], nodes_by_id: dict[str, dict[str, Any]], changes: list[str]) -> None:
    if edge.get("end_tangent_point"):
        return
    start = endpoint_point(edge, "from", nodes_by_id)
    end = endpoint_point(edge, "to", nodes_by_id, start)
    if end is None:
        return
    controls = [
        (float(point[0]), float(point[1]))
        for point in edge.get("points", []) or []
        if isinstance(point, list) and len(point) == 2
    ]
    previous = controls[-1] if controls else start
    if previous is None:
        return
    dx = end[0] - previous[0]
    dy = end[1] - previous[1]
    if math.hypot(dx, dy) <= 1e-9:
        return
    tangent = [previous[0] + dx * 0.58, previous[1] + dy * 0.58]
    edge["end_tangent_point"] = [round(tangent[0], 3), round(tangent[1], 3)]
    change(changes, f"added end_tangent_point to `{edge.get('id')}` for smoother loop arrowhead")


def apply_math_text_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    for node in scene.get("nodes", []):
        if node.get("type") in {"text_block", "math_text", "loss_region"}:
            normalize_formula_fields(node, changes)
        if node.get("type") == "text_block" and text_has_raw_loss_subscript(str(node.get("text", ""))):
            node["type"] = "math_text"
            style = node.setdefault("style", {})
            style.setdefault("line", "none")
            style.setdefault("fill", "none")
            change(changes, f"converted `{node.get('id')}` from text_block to math_text")


def apply_outer_loop_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    label_id = find_update_label(scene)
    nodes_by_id, _ = node_maps(scene)
    for edge in scene.get("edges", []):
        edge_id = str(edge.get("id", "")).lower()
        if edge.get("type") == "loop_arrow" and any(token in edge_id for token in {"outer", "loop", "cycle"}):
            if edge.get("curve_mode") != "smooth":
                edge["curve_mode"] = "smooth"
                change(changes, f"set `{edge.get('id')}` curve_mode to smooth")
            if not edge.get("semantic_role"):
                edge["semantic_role"] = "outer_update_loop"
                change(changes, f"set `{edge.get('id')}` semantic_role to outer_update_loop")
            if label_id and not (edge.get("label_id") or edge.get("loop_label_id")):
                edge["label_id"] = label_id
                change(changes, f"bound `{edge.get('id')}` to update label `{label_id}`")
            ensure_terminal_tangent(edge, nodes_by_id, changes)


def reverse_edge(edge: dict[str, Any]) -> None:
    edge["from"], edge["to"] = edge.get("to"), edge.get("from")
    if "from" in edge and edge["from"] is None:
        edge.pop("from", None)
    if "to" in edge and edge["to"] is None:
        edge.pop("to", None)
    edge["from_point"], edge["to_point"] = edge.get("to_point"), edge.get("from_point")
    if edge.get("from_point") is None:
        edge.pop("from_point", None)
    if edge.get("to_point") is None:
        edge.pop("to_point", None)
    if isinstance(edge.get("points"), list):
        edge["points"] = list(reversed(edge["points"]))


def apply_gan_direction_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    nodes_by_id, node_types_by_id = node_maps(scene)
    if not scene_looks_like_gan_tfr(scene, nodes_by_id):
        return
    used_ids = {str(edge.get("id")) for edge in scene.get("edges", [])}
    for edge in scene.get("edges", []):
        from_role = edge_endpoint_role(edge, "from", nodes_by_id, node_types_by_id)
        to_role = edge_endpoint_role(edge, "to", nodes_by_id, node_types_by_id)
        if from_role == "discriminator" and to_role == "generated":
            old_id = str(edge.get("id", "edge"))
            reverse_edge(edge)
            if "discriminator_to_generated" in old_id:
                new_id = old_id.replace("discriminator_to_generated", "generated_to_discriminator")
                if new_id not in used_ids:
                    edge["id"] = new_id
            edge.setdefault("route", "horizontal")
            change(changes, f"reversed GAN/TFR main edge `{old_id}`")


def apply_feedback_edge_type_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    nodes_by_id, _ = node_maps(scene)
    if not scene_looks_like_gan_tfr(scene, nodes_by_id):
        return
    feedback_tokens = {"loss", "backprop", "feedback", "gradient", "penalty", "adv", "rec"}
    for edge in scene.get("edges", []):
        edge_type = edge.get("type")
        if edge_type not in {"arrow_connector", "dynamic_connector", "line_segment"}:
            continue
        edge_id = str(edge.get("id", "")).lower()
        if not isinstance(edge.get("style"), dict):
            edge["style"] = {}
        style = edge["style"]
        dashed = str(style.get("line_dash", "")).lower() in {"dash", "dot", "long_dash"}
        feedback_like = dashed or any(token in edge_id for token in feedback_tokens)
        if not feedback_like:
            continue
        if edge_type == "line_segment" and str(style.get("end_arrow", "none")).lower() in {"", "none"} and any(token in edge_id for token in {"bus", "baseline", "frame"}):
            continue
        edge["type"] = "dashed_feedback_path"
        style.setdefault("line_dash", "dash")
        if "allow_diagonal" in edge:
            edge.pop("allow_diagonal", None)
        if edge.get("route") == "straight":
            edge["route"] = "orthogonal"
        change(changes, f"converted `{edge.get('id')}` to dashed_feedback_path")


def containing_region(point: tuple[float, float] | None, nodes: list[dict[str, Any]]) -> dict[str, Any] | None:
    if point is None:
        return None
    regions = [
        node
        for node in nodes
        if node.get("type") in {"dashed_region", "loss_region"}
        and all(isinstance(node.get(key), (int, float)) for key in ("x", "y", "w", "h"))
        and point_in_box(point, node_box(node), tolerance=0.04)
    ]
    if not regions:
        return None
    return min(regions, key=lambda node: float(node["w"]) * float(node["h"]))


def source_region_for_feedback_edge(
    edge: dict[str, Any],
    nodes: list[dict[str, Any]],
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    source_id = endpoint_node_id(edge.get("from"))
    if source_id and source_id in nodes_by_id and nodes_by_id[source_id].get("type") in {"dashed_region", "loss_region"}:
        return nodes_by_id[source_id]
    return containing_region(edge_point(edge, "from"), nodes)


def position_values(count: int) -> list[float]:
    if count <= 1:
        return [0.5]
    if count == 2:
        return [0.36, 0.64]
    margin = 0.24
    step = (1.0 - margin * 2) / max(1, count - 1)
    return [margin + step * index for index in range(count)]


def apply_loss_region_exit_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    nodes = scene.get("nodes", [])
    nodes_by_id, node_types_by_id = node_maps(scene)
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}

    for edge in scene.get("edges", []):
        if edge.get("type") != "dashed_feedback_path":
            continue
        region = source_region_for_feedback_edge(edge, nodes, nodes_by_id)
        if region is None or region.get("type") != "loss_region":
            continue
        target_id = endpoint_node_id(edge.get("to")) or edge_endpoint_node_id(edge, "to", nodes_by_id, node_types_by_id)
        if not target_id or target_id not in nodes_by_id:
            continue
        target = nodes_by_id[target_id]
        if target.get("type") in CONTAINER_TYPES | {"text_block", "junction_point", "boundary_port", "merge_bus"}:
            continue
        rx1, ry1, rx2, ry2 = node_box(region)
        tx1, ty1, tx2, ty2 = node_box(target)
        overlap_x = max(0.0, min(rx2, tx2) - max(rx1, tx1))
        overlap_y = max(0.0, min(ry2, ty2) - max(ry1, ty1))
        rcx, rcy = node_center(region)
        tcx, tcy = node_center(target)
        if overlap_x >= min(rx2 - rx1, tx2 - tx1) * 0.25:
            direction = "down" if tcy >= rcy else "up"
            grouped.setdefault((str(region["id"]), target_id, direction), []).append(edge)
        elif overlap_y >= min(ry2 - ry1, ty2 - ty1) * 0.25:
            direction = "right" if tcx >= rcx else "left"
            grouped.setdefault((str(region["id"]), target_id, direction), []).append(edge)

    for (region_id, target_id, direction), edges in grouped.items():
        region = nodes_by_id[region_id]
        target = nodes_by_id[target_id]
        rx1, ry1, rx2, ry2 = node_box(region)
        tx1, ty1, tx2, ty2 = node_box(target)
        positions = position_values(len(edges))
        for edge, position in zip(edges, positions):
            before = canonical_json(edge)
            if direction in {"down", "up"}:
                span_left = max(rx1, tx1)
                span_right = min(rx2, tx2)
                if span_right <= span_left:
                    span_left, span_right = tx1, tx2
                x = span_left + (span_right - span_left) * position
                y = ry2 if direction == "down" else ry1
                side = "top" if direction == "down" else "bottom"
                target_ratio = (x - tx1) / max(1e-9, tx2 - tx1)
                edge["from_point"] = [round(x, 3), round(y, 3)]
                edge["to"] = f"{target_id}:{side}@{format_ratio(target_ratio)}"
                edge["route"] = "vertical"
            else:
                span_top = max(ry1, ty1)
                span_bottom = min(ry2, ty2)
                if span_bottom <= span_top:
                    span_top, span_bottom = ty1, ty2
                y = span_top + (span_bottom - span_top) * position
                x = rx2 if direction == "right" else rx1
                side = "left" if direction == "right" else "right"
                target_ratio = (y - ty1) / max(1e-9, ty2 - ty1)
                edge["from_point"] = [round(x, 3), round(y, 3)]
                edge["to"] = f"{target_id}:{side}@{format_ratio(target_ratio)}"
                edge["route"] = "horizontal"
            edge.pop("from", None)
            edge.pop("to_point", None)
            edge.pop("points", None)
            edge["allow_cross_container"] = True
            edge["allow_direct_cross_container"] = True
            if canonical_json(edge) != before:
                change(changes, f"rerouted `{edge.get('id')}` as a clean `{region_id}` boundary stub to `{target_id}`")


def apply_backprop_bundle_recipe(scene: dict[str, Any], changes: list[str]) -> None:
    nodes_by_id, node_types_by_id = node_maps(scene)
    if not scene_looks_like_gan_tfr(scene, nodes_by_id):
        return
    verticals: list[dict[str, Any]] = []
    for edge in scene.get("edges", []):
        edge_id = str(edge.get("id", "")).lower()
        if edge.get("type") != "dashed_feedback_path":
            continue
        if not any(token in edge_id for token in {"backprop", "bottom", "disc", "loss"}):
            continue
        start = endpoint_point(edge, "from", nodes_by_id)
        end = endpoint_point(edge, "to", nodes_by_id, start)
        if not start or not end:
            continue
        if abs(start[0] - end[0]) <= 0.03 and abs(start[1] - end[1]) > 0.35:
            if edge_endpoint_role(edge, "to", nodes_by_id, node_types_by_id) == "discriminator" or "disc" in edge_id:
                verticals.append(edge)
    if len(verticals) < 3:
        return
    for edge in verticals:
        if not edge.get("bundle_id"):
            edge["bundle_id"] = "disc_backprop_bundle"
            change(changes, f"assigned `{edge.get('id')}` to disc_backprop_bundle")


def apply_gan_tfr_recipes(scene: dict[str, Any]) -> list[str]:
    changes: list[str] = []
    apply_tfr_panel_compaction_recipe(scene, changes)
    apply_loss_region_compaction_recipe(scene, changes)
    apply_math_text_recipe(scene, changes)
    apply_outer_loop_recipe(scene, changes)
    apply_gan_direction_recipe(scene, changes)
    apply_feedback_edge_type_recipe(scene, changes)
    apply_loss_region_exit_recipe(scene, changes)
    apply_backprop_bundle_recipe(scene, changes)
    return changes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply deterministic visiomaster scene recipes before Visio rendering.")
    parser.add_argument("scene", help="Input scene.json")
    parser.add_argument("--output", help="Output scene.json. Defaults to in-place only with --in-place.")
    parser.add_argument("--in-place", action="store_true", help="Overwrite the input scene.")
    parser.add_argument("--recipe", choices=["gan-tfr"], default="gan-tfr")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    scene_path = Path(args.scene).resolve()
    scene = load_scene(scene_path)
    changes = apply_gan_tfr_recipes(scene)

    if changes:
        print("Applied recipes:")
        for item in changes:
            print(f"- {item}")
    else:
        print("No recipe changes needed.")

    if args.dry_run:
        return 0
    if args.in_place:
        output_path = scene_path
    elif args.output:
        output_path = Path(args.output).resolve()
    else:
        raise ValueError("Use --output, --in-place, or --dry-run.")

    if changes:
        record_recipe_application(scene, args.recipe, changes, "visiomaster.scene_autofix")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(scene, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote scene: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
