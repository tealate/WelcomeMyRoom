"""Load and validate Space Editor's configurable block assignments."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "space_editor_blocks.json"
PROPERTY_REPORT = ROOT / "build/test-server/block-properties-26.1.tsv"

RESOURCE_ID = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
PALETTE_NAME = re.compile(r"^[a-z0-9_]+$")
DISPLAY_KEYS = {"selection", "guide", "selectionCandidate", "maskBody"}
PALETTE_KEYS = {"normalBlock", "carrierBlock", "sourceTexture"}


class EditorBlockConfigError(ValueError):
    pass


def _expect_keys(value: object, expected: set[str], field: str) -> dict:
    if not isinstance(value, dict):
        raise EditorBlockConfigError(f"{field} must be a JSON object")
    actual = set(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise EditorBlockConfigError(f"{field} is missing keys: {', '.join(missing)}")
    if unknown:
        raise EditorBlockConfigError(f"{field} has unknown keys: {', '.join(unknown)}")
    return value


def _resource_id(value: object, field: str) -> str:
    if not isinstance(value, str) or not RESOURCE_ID.fullmatch(value):
        raise EditorBlockConfigError(f"{field} must be a namespaced resource ID")
    return value


def resource_path(root: Path, resource_id: str, folder: str, suffix: str) -> Path:
    namespace, path = resource_id.split(":", 1)
    return root / "assets" / namespace / folder / f"{path}{suffix}"


def blockstate_relative_path(block_id: str) -> Path:
    namespace, path = block_id.split(":", 1)
    return Path("assets") / namespace / "blockstates" / f"{path}.json"


def _registry_ids() -> set[str] | None:
    if PROPERTY_REPORT.exists():
        return {line.split("\t", 1)[0] for line in PROPERTY_REPORT.read_text(encoding="utf-8").splitlines() if line.strip()}
    ids = {
        f"{namespace.name}:{path.relative_to(namespace / 'blockstates').with_suffix('').as_posix()}"
        for namespace in (ROOT / "assets").iterdir()
        if namespace.is_dir() and (namespace / "blockstates").is_dir()
        for path in (namespace / "blockstates").rglob("*.json")
    } if (ROOT / "assets").is_dir() else set()
    return ids or None


def validate_editor_block_config(raw: object, *, registry_ids: set[str] | None = None,
                                 check_textures: bool = True) -> dict:
    data = _expect_keys(raw, {"schemaVersion", "displayBlocks", "maskablePalettes"}, "root")
    if data["schemaVersion"] != 1:
        raise EditorBlockConfigError("schemaVersion must be 1")

    displays_raw = _expect_keys(data["displayBlocks"], DISPLAY_KEYS, "displayBlocks")
    displays = {name: _resource_id(value, f"displayBlocks.{name}") for name, value in displays_raw.items()}

    palettes_raw = data["maskablePalettes"]
    if not isinstance(palettes_raw, dict) or not palettes_raw:
        raise EditorBlockConfigError("maskablePalettes must be a non-empty JSON object")
    palettes: dict[str, dict[str, str]] = {}
    for name, raw_palette in palettes_raw.items():
        if not isinstance(name, str) or not PALETTE_NAME.fullmatch(name):
            raise EditorBlockConfigError(f"invalid palette name: {name!r}")
        palette = _expect_keys(raw_palette, PALETTE_KEYS, f"maskablePalettes.{name}")
        palettes[name] = {key: _resource_id(value, f"maskablePalettes.{name}.{key}") for key, value in palette.items()}

    assignments: list[tuple[str, str]] = [(f"displayBlocks.{name}", block) for name, block in displays.items()]
    for name, palette in palettes.items():
        assignments += [
            (f"maskablePalettes.{name}.normalBlock", palette["normalBlock"]),
            (f"maskablePalettes.{name}.carrierBlock", palette["carrierBlock"]),
        ]
    by_block: dict[str, list[str]] = {}
    for field, block in assignments:
        by_block.setdefault(block, []).append(field)
    duplicates = {block: fields for block, fields in by_block.items() if len(fields) > 1}
    if duplicates:
        details = "; ".join(f"{block}: {', '.join(fields)}" for block, fields in sorted(duplicates.items()))
        raise EditorBlockConfigError(f"block assignments must be unique; {details}")

    known = _registry_ids() if registry_ids is None else registry_ids
    if known is not None:
        missing = sorted(block for _, block in assignments if block not in known)
        if missing:
            raise EditorBlockConfigError(f"blocks not found in the Minecraft 26.1 registry: {', '.join(missing)}")

    if check_textures:
        missing_textures = []
        for name, palette in palettes.items():
            texture = resource_path(ROOT, palette["sourceTexture"], "textures", ".png")
            if not texture.is_file():
                missing_textures.append(f"{name}: {palette['sourceTexture']} ({texture})")
        if missing_textures:
            raise EditorBlockConfigError("source textures not found: " + "; ".join(missing_textures))

    return {"schemaVersion": 1, "displayBlocks": displays, "maskablePalettes": palettes}


def load_editor_block_config(path: Path = CONFIG_PATH, *, check_textures: bool = True) -> dict:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EditorBlockConfigError(f"block configuration not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EditorBlockConfigError(f"invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    return validate_editor_block_config(raw, check_textures=check_textures)
