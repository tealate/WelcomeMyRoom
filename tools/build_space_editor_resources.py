"""Generate and synchronize rendering assets used by the current Space Editor.

The resource namespace remains ``editor`` for compatibility with the live
resource pack.  Runtime functions and storage belong to ``space_editor``.
"""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import re
import shutil

from editor_block_config import (
    EditorBlockConfigError,
    blockstate_relative_path,
    load_editor_block_config,
    resource_path,
)

ROOT = Path(__file__).resolve().parents[1]
RP = ROOT / "space_editor_resources"
MANIFEST = ROOT / "space_editor_generated_manifest.json"

TOOL_MODELS = {
    "region": "minecraft:block/cyan_concrete",
    "resize_all": "minecraft:block/yellow_concrete",
    "resize_face": "minecraft:block/orange_concrete",
    "move": "minecraft:block/lime_concrete",
    "delete": "minecraft:block/red_concrete",
    "region_visibility": "minecraft:block/magenta_concrete",
    "copy": "minecraft:block/green_concrete",
    "paste": "minecraft:block/purple_concrete",
    "fill": "minecraft:block/gold_block",
    "mask": "minecraft:block/pink_concrete",
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def _config() -> dict:
    return load_editor_block_config()


def managed_blockstates(config: dict | None = None) -> dict[Path, str]:
    config = config or _config()
    displays = config["displayBlocks"]
    collisions = config["collisionCarriers"]
    managed = {
        blockstate_relative_path(displays["maskBody"]): "editor:block/mask_body",
        blockstate_relative_path(displays["selection"]): "editor:block/selection",
        blockstate_relative_path(displays["guide"]): "editor:block/guide",
        blockstate_relative_path(displays["selectionCandidate"]): "editor:block/selection_candidate",
    }
    managed.update({
        blockstate_relative_path(palette["carrierBlock"]): f"editor:block/{name}_maskable"
        for name, palette in config["maskablePalettes"].items()
    })
    managed.update({
        blockstate_relative_path(collisions["fence"]): "editor:block/collision_fence",
        blockstate_relative_path(collisions["wall"]): "editor:block/collision_wall",
    })
    return managed


def _read_manifest() -> dict[str, dict[str, str | None]]:
    if not MANIFEST.exists():
        return {}
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schemaVersion") != 2 or not isinstance(value.get("managedBlockstates"), dict):
        raise ValueError(f"Invalid generated blockstate manifest: {MANIFEST}")
    result: dict[str, dict[str, str | None]] = {}
    for relative, entry in value["managedBlockstates"].items():
        parts = Path(relative).parts
        if len(parts) < 4 or parts[0] != "assets" or parts[2] != "blockstates" or Path(relative).suffix != ".json" or ".." in parts:
            raise ValueError(f"Unsafe path in generated blockstate manifest: {relative}")
        if not isinstance(entry, dict) or set(entry) != {"generatedHash", "originalBase64"}:
            raise ValueError(f"Invalid entry in generated blockstate manifest: {relative}")
        digest = entry["generatedHash"]
        original = entry["originalBase64"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"Invalid hash in generated blockstate manifest: {relative}")
        if original is not None:
            if not isinstance(original, str):
                raise ValueError(f"Invalid original content in generated blockstate manifest: {relative}")
            base64.b64decode(original, validate=True)
        result[relative] = {"generatedHash": digest, "originalBase64": original}
    return result


def _blockstate_bytes(model: str) -> bytes:
    return (json.dumps({"variants": {"": {"model": model}}}, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _validate_destinations(root: Path, desired: dict[Path, str], *, allow_original: bool) -> None:
    previous = _read_manifest()
    for relative, model in desired.items():
        target = root / relative
        if not target.exists() or target.read_bytes() == _blockstate_bytes(model):
            continue
        entry = previous.get(relative.as_posix())
        if entry is None:
            if allow_original:
                continue
            raise RuntimeError(f"Refusing to overwrite unmanaged blockstate: {target}")
        if hashlib.sha256(target.read_bytes()).hexdigest() != entry["generatedHash"]:
            raise RuntimeError(f"Refusing to overwrite modified managed blockstate: {target}")


def _remove_stale(root: Path, desired: set[str], *, restore_original: bool) -> int:
    removed = 0
    for relative, entry in _read_manifest().items():
        if relative in desired:
            continue
        target = root / relative
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != entry["generatedHash"]:
            raise RuntimeError(f"Refusing to remove modified managed blockstate: {target}")
        original = entry["originalBase64"] if restore_original else None
        if original is not None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(base64.b64decode(original, validate=True))
        elif target.exists():
            target.unlink()
        removed += 1
    return removed


def _preview_model(name: str) -> dict:
    outer = {"from": [0, 0, 0], "to": [16, 16, 16], "shade": False,
             "faces": {face: {"texture": "#all", "uv": [0, 0, 16, 16]} for face in ("north", "south", "east", "west", "up", "down")}}
    planes = (
        ([0, 0, 0], [16, 16, 0.01], "south"), ([0, 0, 15.99], [16, 16, 16], "north"),
        ([0, 0, 0], [0.01, 16, 16], "east"), ([15.99, 0, 0], [16, 16, 16], "west"),
        ([0, 0, 0], [16, 0.01, 16], "up"), ([0, 15.99, 0], [16, 16, 16], "down"),
    )
    elements = [outer] + [
        {"from": start, "to": end, "shade": False, "faces": {face: {"texture": "#all", "uv": [0, 0, 16, 16]}}}
        for start, end, face in planes
    ]
    return {
        "textures": {"particle": f"editor:block/{name}", "all": f"editor:block/{name}"},
        "elements": elements,
    }


def _tool_box(start: list[float], end: list[float], texture: str = "#accent", *, rotation: dict | None = None) -> dict:
    faces = {
        face: {"texture": texture}
        for face in ("north", "south", "east", "west", "up", "down")
    }
    result = {"from": start, "to": end, "faces": faces}
    if rotation is not None:
        result["rotation"] = rotation
    return result


def _tool_model(name: str, accent: str) -> dict:
    # A common dark handle keeps the set visually related.  The coloured head
    # has a different silhouette per action so tools remain distinguishable in
    # the hotbar even when their Japanese names are not visible.
    elements = [_tool_box([7, 0, 7], [9, 10, 9], "#handle")]
    if name == "region":
        elements += [_tool_box([3, 10, 7], [13, 12, 9]), _tool_box([7, 8, 7], [9, 16, 9])]
    elif name == "resize_all":
        elements += [_tool_box([2, 11, 7], [14, 13, 9]), _tool_box([7, 8, 7], [9, 16, 9]),
                     _tool_box([2, 10, 7], [5, 14, 9]), _tool_box([11, 10, 7], [14, 14, 9])]
    elif name == "resize_face":
        elements += [_tool_box([2, 9, 7], [7, 15, 9]), _tool_box([7, 11, 7], [14, 13, 9])]
    elif name == "move":
        elements += [_tool_box([7, 8, 7], [9, 15, 9]), _tool_box([4, 11, 7], [12, 13, 9]),
                     _tool_box([6, 13, 7], [10, 16, 9])]
    elif name == "delete":
        elements += [
            _tool_box([3, 11, 7], [13, 13, 9], rotation={"origin": [8, 12, 8], "axis": "z", "angle": 45, "rescale": True}),
            _tool_box([3, 11, 7], [13, 13, 9], rotation={"origin": [8, 12, 8], "axis": "z", "angle": -45, "rescale": True}),
        ]
    elif name == "region_visibility":
        elements += [_tool_box([2, 10, 7], [14, 14, 9]), _tool_box([6, 9, 6], [10, 15, 10], "#detail")]
    elif name == "copy":
        elements += [_tool_box([3, 9, 7], [10, 15, 8]), _tool_box([6, 11, 8], [13, 16, 9], "#detail")]
    elif name == "paste":
        elements += [_tool_box([7, 10, 7], [9, 16, 9]), _tool_box([4, 10, 7], [12, 12, 9]),
                     _tool_box([6, 8, 7], [10, 11, 9])]
    elif name == "fill":
        elements += [_tool_box([3, 9, 6], [13, 15, 10]), _tool_box([5, 11, 5], [11, 16, 6], "#detail")]
    elif name == "mask":
        elements += [_tool_box([3, 9, 7], [13, 11, 9]), _tool_box([3, 14, 7], [13, 16, 9]),
                     _tool_box([3, 11, 7], [5, 14, 9]), _tool_box([11, 11, 7], [13, 14, 9])]
    return {
        "parent": "minecraft:item/handheld",
        "textures": {
            "handle": "minecraft:block/stripped_dark_oak_log",
            "accent": accent,
            "detail": "minecraft:block/white_concrete",
            "particle": accent,
        },
        "elements": elements,
    }


def build_tool_resources() -> None:
    for name, accent in TOOL_MODELS.items():
        write_json(RP / f"assets/editor/models/item/tool_{name}.json", _tool_model(name, accent))
        write_json(RP / f"assets/editor/items/tool_{name}.json", {
            "model": {
                "type": "minecraft:model",
                "model": f"editor:item/tool_{name}",
            }
        })


def build_preview_resources() -> None:
    from PIL import Image

    for name, (color, border) in {
        "selection": ((70, 220, 255, 255), 2),
        "guide": ((240, 210, 50, 255), 1),
    }.items():
        destination = RP / f"assets/editor/textures/block/{name}.png"
        destination.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        for y in range(32):
            for x in range(32):
                if x < border or x >= 32 - border or y < border or y >= 32 - border or x == y or x + y == 31:
                    image.putpixel((x, y), color)
        image.save(destination)
        write_json(RP / f"assets/editor/models/block/{name}.json", _preview_model(name))

    # The selection cursor is a hand-authored live asset.  Validate and mirror
    # it, but never regenerate it, so LibreSprite edits remain authoritative.
    live_candidate = ROOT / "assets/editor/textures/block/selection_candidate.png"
    if not live_candidate.is_file():
        raise FileNotFoundError(
            "Missing authored cursor texture: assets/editor/textures/block/selection_candidate.png"
        )
    with Image.open(live_candidate) as image:
        rgba = image.convert("RGBA")
        alpha = set(rgba.getchannel("A").getdata())
        if rgba.size != (32, 32) or not {0, 255}.issubset(alpha):
            raise ValueError(
                "selection_candidate.png must be 32x32 with transparent and opaque pixels"
            )
    candidate = RP / "assets/editor/textures/block/selection_candidate.png"
    candidate.parent.mkdir(parents=True, exist_ok=True)
    if not candidate.exists() or candidate.read_bytes() != live_candidate.read_bytes():
        shutil.copyfile(live_candidate, candidate)
    write_json(RP / "assets/editor/models/block/selection_candidate.json", _preview_model("selection_candidate"))


def build_resources() -> None:
    from PIL import Image
    from mark_textures_translucent import process_png

    config = _config()
    for name, palette in config["maskablePalettes"].items():
        destination = RP / f"assets/editor/textures/block/{name}_maskable.png"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(resource_path(ROOT, palette["sourceTexture"], "textures", ".png"), destination)
        print(f"{process_png(destination, False)}: {destination.relative_to(ROOT)}")
        if process_png(destination, True) != "already-translucent":
            raise RuntimeError("Translucency verification failed")
        write_json(RP / f"assets/editor/models/block/{name}_maskable.json", {
            "parent": "minecraft:block/cube_all", "textures": {"all": f"editor:block/{name}_maskable"}
        })
    # mask_body.png is an authored, live resource.  LibreSprite edits belong in
    # ROOT/assets and must never be replaced by a generator default.  Keep the
    # auxiliary resource tree as a mirror so inspections there see the same
    # bytes Minecraft actually loads.
    live_mask = ROOT / "assets/editor/textures/block/mask_body.png"
    if not live_mask.is_file():
        raise FileNotFoundError(
            "Missing authored mask texture: assets/editor/textures/block/mask_body.png"
        )
    with Image.open(live_mask) as image:
        image.verify()
    mask = RP / "assets/editor/textures/block/mask_body.png"
    mask.parent.mkdir(parents=True, exist_ok=True)
    if not mask.exists() or mask.read_bytes() != live_mask.read_bytes():
        shutil.copyfile(live_mask, mask)
    write_json(RP / "assets/editor/models/block/mask_body.json", {
        "textures": {"particle": "editor:block/mask_body", "all": "editor:block/mask_body"},
        "elements": [{"from": [0, 0, 0], "to": [16, 16, 16], "shade": False,
                      "faces": {face: {"texture": "#all", "uv": [0, 0, 16, 16]} for face in ("north", "south", "east", "west", "up", "down")}}],
    })
    build_preview_resources()
    build_tool_resources()
    write_json(RP / "assets/editor/models/block/collision_fence.json", {"textures": {"particle": "minecraft:block/cherry_planks"}, "elements": []})
    write_json(RP / "assets/editor/models/block/collision_wall.json", {"textures": {"particle": "minecraft:block/sandstone"}, "elements": []})
    desired = managed_blockstates(config)
    _validate_destinations(RP, desired, allow_original=False)
    _remove_stale(RP, {path.as_posix() for path in desired}, restore_original=False)
    for relative, model in desired.items():
        write_json(RP / relative, {"variants": {"": {"model": model}}})


def sync_live_resources() -> None:
    config = _config()
    desired = managed_blockstates(config)
    desired_names = {path.as_posix() for path in desired}
    _validate_destinations(ROOT, desired, allow_original=True)
    previous = _read_manifest()
    originals: dict[str, str | None] = {}
    for relative, model in desired.items():
        name = relative.as_posix()
        if name in previous:
            originals[name] = previous[name]["originalBase64"]
        else:
            target = ROOT / relative
            originals[name] = base64.b64encode(target.read_bytes()).decode("ascii") if target.exists() and target.read_bytes() != _blockstate_bytes(model) else None
    removed = _remove_stale(ROOT, desired_names, restore_original=True)
    files: list[Path] = []
    for name in config["maskablePalettes"]:
        files += [
            RP / f"assets/editor/models/block/{name}_maskable.json",
            RP / f"assets/editor/textures/block/{name}_maskable.png",
        ]
    # mask_body.png is intentionally omitted: ROOT/assets is its source of
    # truth. build_resources() mirrors it in the auxiliary tree, never the
    # other way around.
    files += [RP / "assets/editor/models/block/mask_body.json"]
    files += [RP / "assets/editor/models/block/selection_candidate.json"]
    files += [RP / f"assets/editor/models/item/tool_{name}.json" for name in TOOL_MODELS]
    files += [RP / f"assets/editor/items/tool_{name}.json" for name in TOOL_MODELS]
    for name in ("selection", "guide"):
        files += [
            RP / f"assets/editor/models/block/{name}.json",
            RP / f"assets/editor/textures/block/{name}.png",
        ]
    files += [
        RP / "assets/editor/models/block/collision_fence.json",
        RP / "assets/editor/models/block/collision_wall.json",
    ]
    files += [RP / path for path in desired]
    for source in files:
        relative = source.relative_to(RP)
        destination = ROOT / relative
        if source.suffix == ".json":
            json.loads(source.read_text(encoding="utf-8"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or source.read_bytes() != destination.read_bytes():
            shutil.copyfile(source, destination)
        if source.read_bytes() != destination.read_bytes():
            raise RuntimeError(f"Live asset verification failed: {relative}")
    write_json(MANIFEST, {"schemaVersion": 2, "managedBlockstates": {
        relative: {"generatedHash": hashlib.sha256((RP / relative).read_bytes()).hexdigest(), "originalBase64": originals[relative]}
        for relative in sorted(desired_names)
    }})
    print(f"Live resource pack: {len(files)} assets synchronized to {ROOT}; stale blockstates removed={removed}")


def main() -> None:
    build_resources()
    sync_live_resources()


if __name__ == "__main__":
    try:
        main()
    except (EditorBlockConfigError, OSError, RuntimeError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from None
