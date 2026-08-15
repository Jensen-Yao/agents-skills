#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any
import re


STYLE_SUFFIXES = (
    "Bold Italic",
    "Bold Oblique",
    "Semibold Italic",
    "SemiBold Italic",
    "Demi Bold Italic",
    "DemiBold Italic",
    "Extra Bold Italic",
    "ExtraBold Italic",
    "Black Italic",
    "Heavy Italic",
    "Light Italic",
    "Medium Italic",
    "Italic",
    "Oblique",
    "Regular",
    "Bold",
    "Semibold",
    "SemiBold",
    "Demi Bold",
    "DemiBold",
    "Extra Bold",
    "ExtraBold",
    "Black",
    "Heavy",
    "Medium",
)

FONT_ALIASES = {
    "times": "Times New Roman",
    "timesnewroman": "Times New Roman",
    "timesnewromanpsmt": "Times New Roman",
    "times new roman ps": "Times New Roman",
    "helvetica": "Arial",
    "helveticaneue": "Arial",
    "arialmt": "Arial",
    "arialpsmt": "Arial",
    "calibribody": "Calibri",
    "calibri body": "Calibri",
    "cambria&cambriamath": "Cambria Math",
    "cambriamath": "Cambria Math",
    "songti": "SimSun",
    "simsun": "SimSun",
    "heiti": "SimHei",
    "simhei": "SimHei",
    "yahei": "Microsoft YaHei",
    "microsoftyaheiui": "Microsoft YaHei UI",
    "microsoftyahei": "Microsoft YaHei",
    "pingfangsc": "Microsoft YaHei UI",
    "sfpro": "Segoe UI",
    "sfprodisplay": "Segoe UI",
    "sfprorounded": "Segoe UI",
}

ROLE_FALLBACKS = {
    "paper_serif": [
        "Times New Roman",
        "Times",
        "Cambria",
        "Georgia",
        "Garamond",
        "Book Antiqua",
        "Palatino Linotype",
    ],
    "serif": [
        "Times New Roman",
        "Cambria",
        "Georgia",
        "Garamond",
        "Book Antiqua",
    ],
    "ui_sans": [
        "Aptos",
        "Calibri",
        "Arial",
        "Segoe UI",
        "Microsoft YaHei UI",
        "Microsoft YaHei",
    ],
    "sans": [
        "Arial",
        "Calibri",
        "Aptos",
        "Segoe UI",
        "Microsoft YaHei UI",
    ],
    "math": [
        "Cambria Math",
        "Cambria",
        "Times New Roman",
        "Euclid Math One",
        "Euclid",
    ],
    "mono": [
        "Consolas",
        "Courier New",
        "Cascadia Mono",
        "Lucida Console",
    ],
    "cjk_sans": [
        "Microsoft YaHei UI",
        "Microsoft YaHei",
        "DengXian",
        "SimHei",
        "Arial Unicode MS",
    ],
    "cjk_serif": [
        "SimSun",
        "FangSong",
        "KaiTi",
        "Microsoft YaHei UI",
        "Microsoft YaHei",
    ],
}

CJK_FONT_NAMES = {"Microsoft YaHei UI", "Microsoft YaHei", "DengXian", "SimHei", "SimSun", "FangSong", "KaiTi"}

GENERIC_ROLE_NAMES = {
    "serif": "serif",
    "sans-serif": "sans",
    "sans": "sans",
    "ui": "ui_sans",
    "ui-sans": "ui_sans",
    "math": "math",
    "monospace": "mono",
    "mono": "mono",
    "cjk": "cjk_sans",
}


@dataclass(frozen=True)
class FontResolution:
    requested: str | None
    resolved: str | None
    role: str | None
    available: bool
    used_fallback: bool
    reason: str


def normalize_font_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(name).lower())


def clean_registry_font_name(name: str) -> str:
    cleaned = re.sub(r"\s*\([^)]*\)\s*$", "", str(name)).strip()
    return re.sub(r"\s+", " ", cleaned)


def strip_style_suffix(name: str) -> str:
    result = str(name).strip()
    changed = True
    while changed:
        changed = False
        for suffix in STYLE_SUFFIXES:
            if result.lower().endswith(" " + suffix.lower()):
                result = result[: -len(suffix)].strip()
                changed = True
                break
    return result


def split_family_aliases(name: str) -> list[str]:
    cleaned = clean_registry_font_name(name)
    values = [cleaned]
    if "&" in cleaned:
        parts = [part.strip() for part in cleaned.split("&") if part.strip()]
        if len(parts) == 2 and parts[0].lower() == "cambria" and "math" in parts[1].lower():
            values.extend(["Cambria", "Cambria Math"])
        else:
            values.extend(parts)
    base = strip_style_suffix(cleaned)
    if base and base not in values:
        values.append(base)
    return [item for item in values if item]


@lru_cache(maxsize=1)
def installed_font_families() -> tuple[str, ...]:
    fonts: set[str] = set()
    try:
        import winreg
    except Exception:
        winreg = None

    if winreg is not None:
        for root, registry_path in (
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"),
        ):
            try:
                with winreg.OpenKey(root, registry_path) as key:
                    index = 0
                    while True:
                        try:
                            value_name, _value, _typ = winreg.EnumValue(key, index)
                        except OSError:
                            break
                        fonts.update(split_family_aliases(value_name))
                        index += 1
            except OSError:
                continue

    fonts_dir = Path(r"C:\Windows\Fonts")
    if not fonts and fonts_dir.exists():
        for path in fonts_dir.glob("*"):
            if path.suffix.lower() in {".ttf", ".otf", ".ttc"}:
                stem = re.sub(r"[-_](bold|italic|regular|light|medium|black|semibold).*$", "", path.stem, flags=re.I)
                if len(stem) > 2:
                    fonts.add(stem)

    return tuple(sorted(fonts, key=str.lower))


@lru_cache(maxsize=1)
def installed_font_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for font in installed_font_families():
        lookup.setdefault(normalize_font_key(font), font)
    return lookup


def canonical_font_name(name: Any) -> str | None:
    if not isinstance(name, str):
        return None
    raw = name.strip()
    if not raw:
        return None
    alias = FONT_ALIASES.get(normalize_font_key(raw))
    if alias:
        raw = alias
    lookup = installed_font_lookup()
    return lookup.get(normalize_font_key(raw), raw)


def installed_font_match(name: Any) -> str | None:
    canonical = canonical_font_name(name)
    if not canonical:
        return None
    return installed_font_lookup().get(normalize_font_key(canonical))


def has_cjk_text(text: Any) -> bool:
    return any("\u3400" <= char <= "\u9fff" or "\uf900" <= char <= "\ufaff" for char in str(text or ""))


def has_math_text(text: Any) -> bool:
    value = str(text or "")
    return bool(re.search(r"[_^=∑∏√∞≈≤≥±×÷⊗]", value))


def normalize_role(role: Any, text: Any = "") -> str | None:
    if isinstance(role, str) and role.strip():
        key = role.strip().lower().replace(" ", "_").replace("-", "_")
        key = {
            "paper": "paper_serif",
            "paper_serif": "paper_serif",
            "academic": "paper_serif",
            "academic_serif": "paper_serif",
            "ui": "ui_sans",
            "ui_sans": "ui_sans",
            "cjk": "cjk_sans",
            "cjk_sans": "cjk_sans",
            "cjk_serif": "cjk_serif",
            "mono": "mono",
            "monospace": "mono",
        }.get(key, key)
        if key in ROLE_FALLBACKS:
            if has_cjk_text(text) and key not in {"cjk_sans", "cjk_serif"}:
                return "cjk_sans"
            return key
    if has_cjk_text(text):
        return "cjk_sans"
    if has_math_text(text):
        return "math"
    return None


def listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = [item.strip() for item in value.split(",") if item.strip()]
        return parts or [value.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def role_fallbacks(role: str | None, text: Any = "") -> list[str]:
    normalized_role = normalize_role(role, text)
    fallbacks = list(ROLE_FALLBACKS.get(normalized_role or "", []))
    if has_cjk_text(text):
        for item in ROLE_FALLBACKS["cjk_sans"]:
            if item not in fallbacks:
                fallbacks.append(item)
    return fallbacks


def resolve_font_family(
    requested: Any = None,
    candidates: Any = None,
    role: Any = None,
    text: Any = "",
) -> FontResolution:
    requested_list = listify(requested)
    candidate_list = listify(candidates)
    normalized_role = normalize_role(role, text)

    search: list[str] = []
    first_requested_match = installed_font_match(requested_list[0]) if requested_list else None
    role_first = (
        has_cjk_text(text)
        and normalized_role in {"cjk_sans", "cjk_serif"}
        and (not first_requested_match or first_requested_match not in CJK_FONT_NAMES)
    )
    if role_first:
        for fallback in role_fallbacks(normalized_role, text):
            if fallback not in search:
                search.append(fallback)
    for item in requested_list:
        generic_role = GENERIC_ROLE_NAMES.get(str(item).strip().lower())
        if generic_role:
            for fallback in role_fallbacks(generic_role, text):
                if fallback not in search:
                    search.append(fallback)
            continue
        canonical = canonical_font_name(item)
        if canonical and canonical not in search:
            search.append(canonical)
    if not role_first:
        for fallback in role_fallbacks(normalized_role, text):
            if fallback not in search:
                search.append(fallback)
    for item in candidate_list:
        generic_role = GENERIC_ROLE_NAMES.get(str(item).strip().lower())
        if generic_role:
            for fallback in role_fallbacks(generic_role, text):
                if fallback not in search:
                    search.append(fallback)
            continue
        canonical = canonical_font_name(item)
        if canonical and canonical not in search:
            search.append(canonical)

    requested_name = requested_list[0] if requested_list else None
    lookup = installed_font_lookup()
    if not lookup:
        return FontResolution(requested_name, requested_name or (search[0] if search else None), normalized_role, False, False, "font inventory unavailable")

    for index, item in enumerate(search):
        match = installed_font_match(item)
        if match:
            used_fallback = bool(requested_name and normalize_font_key(match) != normalize_font_key(canonical_font_name(requested_name) or requested_name))
            reason = "requested font available" if index == 0 and not used_fallback else "fallback font selected"
            return FontResolution(requested_name, match, normalized_role, True, used_fallback, reason)

    if requested_name:
        return FontResolution(requested_name, requested_name, normalized_role, False, False, "requested font unavailable and no fallback matched")
    return FontResolution(None, None, normalized_role, False, False, "no font requested and no fallback matched")


def font_resolution_for_style(style: dict[str, Any], text: Any = "") -> FontResolution:
    return resolve_font_family(
        requested=style.get("font_family"),
        candidates=style.get("font_family_candidates", style.get("font_candidates")),
        role=style.get("font_role"),
        text=text,
    )


def font_inventory_summary() -> dict[str, Any]:
    fonts = installed_font_families()
    lookup = installed_font_lookup()
    base_families = tuple(sorted({strip_style_suffix(font) for font in fonts if strip_style_suffix(font)}, key=str.lower))
    return {
        "font_entry_count": len(fonts),
        "font_count": len(base_families),
        "canonical_count": len(lookup),
        "base_families": list(base_families),
        "fonts": list(fonts),
    }
