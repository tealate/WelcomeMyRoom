"""Generate phase-3 rotation and vertical-mirror support for Space Editor.

Phase 2 remains the fast path for an untransformed paste.  A transformed paste
first scans the archived template, then clones one block at a time using a
persisted linear cursor.  The scan accepts full collision cubes and the state
families implemented below; unsupported blocks are warned about and skipped.
"""
from __future__ import annotations

import json
from pathlib import Path

import build_space_editor_stage2 as stage2

ROOT = Path(__file__).resolve().parents[1]
DP = ROOT / "space_editor_datapack"
F = DP / "data/space_editor/function"
PROPERTY_REPORT = ROOT / "build/test-server/block-properties-26.1.tsv"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def fn(name: str, lines: list[str] | str) -> None:
    write(F / f"{name}.mcfunction", "\n".join(lines) if isinstance(lines, list) else lines)


def js(path: Path, value: object) -> None:
    write(path, json.dumps(value, ensure_ascii=False, indent=2))


def message(text: str, color: str = "aqua", target: str = "@s") -> str:
    return f"tellraw {target} " + json.dumps({"text": f"[Space Editor] {text}", "color": color}, ensure_ascii=False)


def insert_before(path: Path, needle: str, additions: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    at = next(i for i, line in enumerate(lines) if needle in line)
    lines[at:at] = additions
    write(path, "\n".join(lines))


def append(path: Path, additions: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines.extend(additions)
    write(path, "\n".join(lines))


def build_transform_tags() -> None:
    tag_root = DP / "data/space_editor/tags/block"
    names = {
        "allowed": tag_root / "transform_allowed.json",
        "stairs": tag_root / "transform_stairs.json",
        "slabs": tag_root / "transform_slabs.json",
        "connections": tag_root / "transform_connections.json",
        "walls": tag_root / "transform_walls.json",
        "axis": tag_root / "transform_axis.json",
        "axis_waterlogged": tag_root / "transform_axis_waterlogged.json",
        "vertical_unsupported": tag_root / "transform_vertical_unsupported.json",
    }
    if not PROPERTY_REPORT.exists():
        missing = [str(path) for path in names.values() if not path.exists()]
        if missing:
            raise FileNotFoundError("26.1 block classification is unavailable: " + ", ".join(missing))
        return

    sensitive = {
        "attached", "attachment", "axis", "bottom", "copper_golem_pose", "down",
        "east", "face", "facing", "half", "hanging", "hinge", "inverted",
        "north", "orientation", "part", "rotation", "shape", "side_chain", "south",
        "thickness", "tilt", "tip", "type", "up", "vertical_direction", "west",
    }
    groups: dict[str, list[str]] = {key: [] for key in names if key not in {"allowed", "vertical_unsupported"}}
    safe_cubes: list[str] = []
    for raw in PROPERTY_REPORT.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        block_id, props, full_cube = (raw.split("\t") + ["", ""])[:3]
        prop_names = {part.split("=", 1)[0] for part in props.split(",") if part}
        signature = tuple(sorted(prop_names))
        if signature == ("facing", "half", "shape", "waterlogged"):
            groups["stairs"].append(block_id)
        elif signature == ("type", "waterlogged"):
            groups["slabs"].append(block_id)
        elif signature == ("east", "north", "south", "waterlogged", "west"):
            groups["connections"].append(block_id)
        elif signature == ("east", "north", "south", "up", "waterlogged", "west"):
            groups["walls"].append(block_id)
        elif signature == ("axis",):
            groups["axis"].append(block_id)
        elif signature == ("axis", "waterlogged"):
            groups["axis_waterlogged"].append(block_id)
        elif full_cube == "true" and not (prop_names & sensitive):
            safe_cubes.append(block_id)

    allowed = sorted(set(safe_cubes + ["minecraft:air", "minecraft:cave_air", "minecraft:void_air"] +
                         sum(groups.values(), [])))
    for key, values in groups.items():
        js(names[key], {"replace": False, "values": sorted(set(values))})
    js(names["allowed"], {"replace": False, "values": allowed})
    js(names["vertical_unsupported"], {
        "replace": False,
        "values": sorted(set(groups["connections"] + groups["walls"])),
    })


def main() -> None:
    stage2.main()
    for obsolete in ("transform/reject_unsupported.mcfunction", "transform/reject_vertical.mcfunction"):
        (F / obsolete).unlink(missing_ok=True)
    build_transform_tags()

    insert_before(F / "load.mcfunction", "第2段階:", [
        "scoreboard objectives add se.ph dummy",
        "scoreboard objectives add se.pyaw dummy",
        "scoreboard objectives add se.pitch dummy",
        "scoreboard objectives add se.rot dummy",
        "scoreboard objectives add se.flip dummy",
        "scoreboard objectives add se.intent dummy",
    ])
    append(F / "load.mcfunction", [message("第3段階: 水平回転 / FlipY変換を読み込みました。", target="@a")])

    # A paste-wand hold is one transform-control session. Re-equipping resets
    # rotation and FlipY, captures a new baseline yaw, then keeps the chosen
    # state stable while the player looks elsewhere.
    insert_before(F / "tick.mcfunction", "tool:\"paste\"", [
        "scoreboard players add @a se.ph 0",
        "scoreboard players add @a se.rot 0",
        "scoreboard players add @a se.flip 0",
        "scoreboard players add @a se.intent 0",
        "execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"paste\"}}] run function space_editor:paste_mode/held_tick",
        "execute as @a[scores={se.ph=1..}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"paste\"}}] run scoreboard players set @s se.ph 0",
    ])
    fn("paste_mode/held_tick", [
        "execute if score @s se.ph matches 0 run function space_editor:paste_mode/begin",
        "function space_editor:paste_mode/read_intent",
        "function space_editor:paste_mode/actionbar",
    ])
    fn("paste_mode/begin", [
        "execute store result score @s se.pyaw run data get entity @s Rotation[0] 1",
        "scoreboard players set @s se.rot 0",
        "scoreboard players set @s se.flip 0",
        "scoreboard players set @s se.ph 1",
    ])
    fn("paste_mode/read_intent", [
        "scoreboard players set @s se.intent 0",
        "execute store result score @s se.pitch run data get entity @s Rotation[1] 1",
        "scoreboard players operation #pitch_abs se.v = @s se.pitch",
        "execute if score #pitch_abs se.v matches ..-1 run scoreboard players operation #pitch_abs se.v *= #minus_one se.v",
        "execute if score #pitch_abs se.v matches 45.. run scoreboard players set @s se.intent 3",
        "execute if score @s se.intent matches 3 run return 0",
        "execute store result score #view_yaw se.v run data get entity @s Rotation[0] 1",
        "scoreboard players operation #yaw_delta se.v = #view_yaw se.v",
        "scoreboard players operation #yaw_delta se.v -= @s se.pyaw",
        "execute if score #yaw_delta se.v matches ..-181 run scoreboard players add #yaw_delta se.v 360",
        "execute if score #yaw_delta se.v matches 180.. run scoreboard players remove #yaw_delta se.v 360",
        "execute if score #yaw_delta se.v matches -135..-45 run scoreboard players set @s se.intent 1",
        "execute if score #yaw_delta se.v matches 45..135 run scoreboard players set @s se.intent 2",
    ])
    for flip, label in ((0, "OFF"), (1, "ON")):
        for intent, text in ((0, "対象なし"), (1, "左回転"), (2, "右回転"), (3, "上下反転")):
            fn(f"paste_mode/actionbar_{flip}_{intent}", [
                f'title @s actionbar [{{"text":"Rot: ","color":"light_purple"}},{{"score":{{"name":"@s","objective":"se.rot"}}}},{{"text":" / FlipY: {label} / {text}","color":"aqua"}}]'
            ])
    fn("paste_mode/actionbar", [
        *[f"execute if score @s se.flip matches {flip} if score @s se.intent matches {intent} run function space_editor:paste_mode/actionbar_{flip}_{intent}"
          for flip in (0, 1) for intent in range(4)],
    ])
    fn("paste_mode/apply", [
        "execute if score @s se.intent matches 1 run function space_editor:paste_mode/rotate_left",
        "execute if score @s se.intent matches 2 run function space_editor:paste_mode/rotate_right",
        "execute if score @s se.intent matches 3 run function space_editor:paste_mode/toggle_flip",
        "execute if data storage space_editor:runtime pastePending run function space_editor:paste/update_pending_transform",
        "function space_editor:paste_mode/actionbar",
    ])
    fn("paste_mode/rotate_left", [
        "scoreboard players remove @s se.rot 90",
        "execute if score @s se.rot matches ..-1 run scoreboard players set @s se.rot 270",
    ])
    fn("paste_mode/rotate_right", [
        "scoreboard players add @s se.rot 90",
        "execute if score @s se.rot matches 360.. run scoreboard players set @s se.rot 0",
    ])
    fn("paste_mode/toggle_flip", [
        "execute if score @s se.flip matches 0 run return run scoreboard players set @s se.flip 1",
        "scoreboard players set @s se.flip 0",
    ])

    # Shift-click controls the transform and never confirms/cancels a paste.
    # A normal click keeps the phase-2 two-click preview/confirm workflow.
    fn("input/paste", [
        "scoreboard players set @s se.cd 5",
        'execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run return run function space_editor:paste_mode/apply',
        "execute if data storage space_editor:runtime pastePending run return run function space_editor:paste/confirm",
        "execute if data storage space_editor:document job{state:\"running\"} run return run " + message("別のCopy/Paste Jobが実行中です。", "red"),
        "data remove storage space_editor:runtime pasteItem",
        "data modify storage space_editor:runtime pasteItem set from entity @s equipment.offhand",
        "execute unless data storage space_editor:runtime pasteItem.components.\"minecraft:custom_data\".space_editor{kind:\"template\"} run return run " + message("オフハンドにTemplateアイテムを持ってください。", "red"),
        "data modify storage space_editor:runtime lookup set value {id:0}",
        "execute store result storage space_editor:runtime lookup.id int 1 run data get storage space_editor:runtime pasteItem.components.\"minecraft:custom_data\".space_editor.templateId 1",
        *[f"execute store result storage space_editor:runtime lookup.owner{i} int 1 run data get entity @s UUID[{i}] 1" for i in range(4)],
        "execute unless data storage space_editor:runtime hover.pos run return run " + message("選択予定位置を取得できません。", "red"),
        "function space_editor:paste/capture",
    ])
    fn("paste/preview", [
        '$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]',
        "execute unless data storage space_editor:runtime template.id run return run " + message("TemplateIDがDocumentにありません。", "red"),
        'data modify storage space_editor:runtime pastePending set value {id:0,version:1,targetDimension:"",x:0,y:0,z:0,w:0,h:0,d:0,sx:0,sy:0,sz:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}',
        "data modify storage space_editor:runtime pastePending.id set from storage space_editor:runtime template.id",
        "data modify storage space_editor:runtime pastePending.version set from storage space_editor:runtime template.version",
        "data modify storage space_editor:runtime pastePending.targetDimension set from storage space_editor:runtime targetDimension",
        *[f"execute store result storage space_editor:runtime pastePending.{axis} int 1 run data get storage space_editor:runtime targetPos[{i}] 1" for i, axis in enumerate("xyz")],
        *[f"data modify storage space_editor:runtime pastePending.{name} set from storage space_editor:runtime template.size[{i}]" for i, name in enumerate(("w", "h", "d"))],
        *[f"data modify storage space_editor:runtime pastePending.owner{i} set from storage space_editor:runtime lookup.owner{i}" for i in range(4)],
        "function space_editor:paste/update_pending_transform",
        message("Paste範囲を表示しました。通常右クリックで確定、Shift＋右クリックで変換。", "yellow"),
    ])
    fn("paste/update_pending_transform", [
        "scoreboard players add @s se.rot 0",
        "scoreboard players add @s se.flip 0",
        "execute store result storage space_editor:runtime pastePending.rotation int 1 run scoreboard players get @s se.rot",
        "execute store result storage space_editor:runtime pastePending.flipY byte 1 run scoreboard players get @s se.flip",
        "data modify storage space_editor:runtime pastePending.sx set from storage space_editor:runtime pastePending.w",
        "data modify storage space_editor:runtime pastePending.sy set from storage space_editor:runtime pastePending.h",
        "data modify storage space_editor:runtime pastePending.sz set from storage space_editor:runtime pastePending.d",
        "execute if score @s se.rot matches 90 if data storage space_editor:runtime pastePending run function space_editor:paste/swap_preview_xz",
        "execute if score @s se.rot matches 270 if data storage space_editor:runtime pastePending run function space_editor:paste/swap_preview_xz",
        "function space_editor:preview/resync",
    ])
    fn("paste/swap_preview_xz", [
        "data modify storage space_editor:runtime swap set from storage space_editor:runtime pastePending.sx",
        "data modify storage space_editor:runtime pastePending.sx set from storage space_editor:runtime pastePending.sz",
        "data modify storage space_editor:runtime pastePending.sz set from storage space_editor:runtime swap",
    ])
    fn("paste/confirm", [
        "data modify storage space_editor:runtime lookup.id set from storage space_editor:runtime pastePending.id",
        *[f"data modify storage space_editor:runtime lookup.owner{i} set from storage space_editor:runtime pastePending.owner{i}" for i in range(4)],
        "data modify storage space_editor:runtime targetDimension set from storage space_editor:runtime pastePending.targetDimension",
        "data modify storage space_editor:runtime targetPos set value [I;0,0,0]",
        *[f"data modify storage space_editor:runtime targetPos[{i}] set from storage space_editor:runtime pastePending.{axis}" for i, axis in enumerate("xyz")],
        'data modify storage space_editor:runtime pasteTransform set value {rotation:0,flipY:0b}',
        "data modify storage space_editor:runtime pasteTransform.rotation set from storage space_editor:runtime pastePending.rotation",
        "data modify storage space_editor:runtime pasteTransform.flipY set from storage space_editor:runtime pastePending.flipY",
        "function space_editor:paste/start with storage space_editor:runtime lookup",
        'execute if data storage space_editor:document job{type:"paste",state:"running"} run function space_editor:paste/hide_preview',
        'execute if data storage space_editor:document job{type:"paste",state:"running"} run data remove storage space_editor:runtime pastePending',
    ])

    fn("paste/start", [
        '$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]',
        "execute unless data storage space_editor:runtime template.id run return run " + message("TemplateIDがDocumentにありません。", "red"),
        'execute unless data storage space_editor:runtime pasteTransform run data modify storage space_editor:runtime pasteTransform set value {rotation:0,flipY:0b}',
        'data modify storage space_editor:document job set value {type:"paste",state:"running",mode:"fast",phase:"place",id:0,version:1,sourceDimension:"",targetDimension:"",sourceX:0,sourceY:0,sourceZ:0,targetX:0,targetY:0,targetZ:0,targetX2:0,targetZ2:0,scratchX:0,scratchY:0,scratchZ:0,sx:0,sy:0,sz:0,outSx:0,outSy:0,outSz:0,cursorX:0,cursor:0,totalBlocks:0,completedChunks:0,completedBlocks:0,unsupportedBlocks:0,skippedBlocks:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}',
        "data modify storage space_editor:document job.id set from storage space_editor:runtime template.id",
        "data modify storage space_editor:document job.version set from storage space_editor:runtime template.version",
        "data modify storage space_editor:document job.sourceDimension set from storage space_editor:runtime template.archive.dimension",
        *[f"data modify storage space_editor:document job.source{axis.upper()} set from storage space_editor:runtime template.archive.{axis}" for axis in "xyz"],
        "data modify storage space_editor:document job.targetDimension set from storage space_editor:runtime targetDimension",
        *[f"execute store result storage space_editor:document job.target{axis.upper()} int 1 run data get storage space_editor:runtime targetPos[{i}] 1" for i, axis in enumerate("xyz")],
        *[f"data modify storage space_editor:document job.s{axis} set from storage space_editor:runtime template.size[{i}]" for i, axis in enumerate("xyz")],
        "data modify storage space_editor:document job.outSx set from storage space_editor:runtime template.size[0]",
        "data modify storage space_editor:document job.outSy set from storage space_editor:runtime template.size[1]",
        "data modify storage space_editor:document job.outSz set from storage space_editor:runtime template.size[2]",
        "data modify storage space_editor:document job.rotation set from storage space_editor:runtime pasteTransform.rotation",
        "data modify storage space_editor:document job.flipY set from storage space_editor:runtime pasteTransform.flipY",
        *[f"data modify storage space_editor:document job.owner{i} set from storage space_editor:runtime lookup.owner{i}" for i in range(4)],
        "execute store result score #rotation se.v run data get storage space_editor:document job.rotation 1",
        "execute if score #rotation se.v matches 90 run function space_editor:paste/swap_job_xz",
        "execute if score #rotation se.v matches 270 run function space_editor:paste/swap_job_xz",
        *[f"execute store result score #{name} se.v run data get storage space_editor:document job.{name} 1" for name in ("sx", "sy", "sz", "outSx", "outSz")],
        "scoreboard players operation #total se.v = #sx se.v",
        "scoreboard players operation #total se.v *= #sy se.v",
        "scoreboard players operation #total se.v *= #sz se.v",
        "execute store result storage space_editor:document job.totalBlocks int 1 run scoreboard players get #total se.v",
        "execute store result score #target_x2 se.v run data get storage space_editor:document job.targetX 1",
        "scoreboard players operation #target_x2 se.v += #outSx se.v",
        "scoreboard players remove #target_x2 se.v 1",
        "execute store result score #target_z2 se.v run data get storage space_editor:document job.targetZ 1",
        "scoreboard players operation #target_z2 se.v += #outSz se.v",
        "scoreboard players remove #target_z2 se.v 1",
        "execute store result storage space_editor:document job.targetX2 int 1 run scoreboard players get #target_x2 se.v",
        "execute store result storage space_editor:document job.targetZ2 int 1 run scoreboard players get #target_z2 se.v",
        "data modify storage space_editor:document job.archiveDimension set from storage space_editor:runtime template.archive.dimension",
        "data modify storage space_editor:document job.archiveX1 set from storage space_editor:runtime template.archive.x",
        "data modify storage space_editor:document job.archiveZ1 set from storage space_editor:runtime template.archive.z",
        "execute store result score #archive_x2 se.v run data get storage space_editor:runtime template.archive.x 1",
        "execute store result score #archive_z2 se.v run data get storage space_editor:runtime template.archive.z 1",
        "scoreboard players operation #archive_x2 se.v += #sx se.v",
        "scoreboard players remove #archive_x2 se.v 1",
        "scoreboard players operation #archive_z2 se.v += #sz se.v",
        "scoreboard players remove #archive_z2 se.v 1",
        "execute store result storage space_editor:document job.archiveX2 int 1 run scoreboard players get #archive_x2 se.v",
        "execute store result storage space_editor:document job.archiveZ2 int 1 run scoreboard players get #archive_z2 se.v",
        "data modify storage space_editor:document job.scratchX set from storage space_editor:document job.sourceX",
        "data modify storage space_editor:document job.scratchZ set from storage space_editor:document job.sourceZ",
        "execute store result score #scratch_y se.v run data get storage space_editor:document job.sourceY 1",
        "scoreboard players add #scratch_y se.v 48",
        "execute store result storage space_editor:document job.scratchY int 1 run scoreboard players get #scratch_y se.v",
        "execute store result score #flip se.v run data get storage space_editor:document job.flipY 1",
        'execute unless score #rotation se.v matches 0 run data modify storage space_editor:document job.mode set value "transformed"',
        'execute unless score #rotation se.v matches 0 run data modify storage space_editor:document job.phase set value "preflight"',
        'execute if score #flip se.v matches 1 run data modify storage space_editor:document job.mode set value "transformed"',
        'execute if score #flip se.v matches 1 run data modify storage space_editor:document job.phase set value "preflight"',
        "function space_editor:job/forceload_archive with storage space_editor:document job",
        "function space_editor:job/forceload_target with storage space_editor:document job",
        message("Paste Jobを開始しました。変換ありは事前走査後、1ブロックずつ配置します。", "green"),
    ])
    fn("paste/swap_job_xz", [
        "data modify storage space_editor:runtime swap set from storage space_editor:document job.outSx",
        "data modify storage space_editor:document job.outSx set from storage space_editor:document job.outSz",
        "data modify storage space_editor:document job.outSz set from storage space_editor:runtime swap",
    ])
    fn("job/forceload_target", ['$execute in $(targetDimension) run forceload add $(targetX) $(targetZ) $(targetX2) $(targetZ2)'])
    fn("job/unforceload_target", ['$execute in $(targetDimension) run forceload remove $(targetX) $(targetZ) $(targetX2) $(targetZ2)'])

    # Preserve the phase-2 strip clone as the fast path.
    original_tick = (F / "job/tick.mcfunction").read_text(encoding="utf-8").strip()
    fn("job/fast_tick", original_tick)
    fn("job/tick", [
        'execute if data storage space_editor:document job{type:"paste",mode:"transformed"} run return run function space_editor:job/transformed_tick',
        "function space_editor:job/fast_tick",
    ])
    fn("job/transformed_tick", [
        "execute store result score #cursor se.v run data get storage space_editor:document job.cursor 1",
        "execute store result score #total se.v run data get storage space_editor:document job.totalBlocks 1",
        "execute if score #cursor se.v >= #total se.v run return run function space_editor:job/transformed_phase_done",
        "scoreboard players set #budget se.v 64",
        "function space_editor:job/transformed_loop",
    ])
    fn("job/transformed_loop", [
        "execute if score #cursor se.v >= #total se.v run return run function space_editor:job/transformed_phase_done",
        "function space_editor:job/prepare_block",
        'execute if data storage space_editor:document job{phase:"preflight"} run function space_editor:transform/preflight',
        'execute if data storage space_editor:document job{phase:"place"} run function space_editor:transform/clone_one',
        'execute unless data storage space_editor:document job{state:"running"} run return 0',
        "scoreboard players add #cursor se.v 1",
        "execute store result storage space_editor:document job.cursor int 1 run scoreboard players get #cursor se.v",
        "scoreboard players remove #budget se.v 1",
        "execute if score #budget se.v matches 1.. run function space_editor:job/transformed_loop",
    ])
    fn("job/transformed_phase_done", [
        'execute if data storage space_editor:document job{phase:"preflight"} run return run function space_editor:job/start_transform_place',
        "function space_editor:job/finish",
    ])
    fn("job/start_transform_place", [
        'data modify storage space_editor:document job.phase set value "place"',
        "data modify storage space_editor:document job.cursor set value 0",
        "execute store result score #unsupported se.v run data get storage space_editor:document job.unsupportedBlocks 1",
        'execute if score #unsupported se.v matches 1.. run tellraw @a [{"text":"[Space Editor] 警告: 未対応ブロック ","color":"yellow"},{"score":{"name":"#unsupported","objective":"se.v"}},{"text":" 個は変更せずスキップします。残りの配置を続行します。"}]',
        message("変換Pasteの事前走査が完了しました。配置を開始します。", "green", "@a"),
    ])
    fn("job/prepare_block", [
        *[f"execute store result score #{name} se.v run data get storage space_editor:document job.{name} 1" for name in ("sx", "sy", "sz")],
        "scoreboard players operation #rx se.v = #cursor se.v",
        "scoreboard players operation #rx se.v %= #sx se.v",
        "scoreboard players operation #work se.v = #cursor se.v",
        "scoreboard players operation #work se.v /= #sx se.v",
        "scoreboard players operation #rz se.v = #work se.v",
        "scoreboard players operation #rz se.v %= #sz se.v",
        "scoreboard players operation #ry se.v = #work se.v",
        "scoreboard players operation #ry se.v /= #sz se.v",
        *[f"execute store result score #src{axis} se.v run data get storage space_editor:document job.source{axis.upper()} 1" for axis in "xyz"],
        *[f"execute store result score #dst{axis} se.v run data get storage space_editor:document job.target{axis.upper()} 1" for axis in "xyz"],
        "scoreboard players operation #srcx se.v += #rx se.v",
        "scoreboard players operation #srcy se.v += #ry se.v",
        "scoreboard players operation #srcz se.v += #rz se.v",
        "scoreboard players operation #tx se.v = #rx se.v",
        "scoreboard players operation #ty se.v = #ry se.v",
        "scoreboard players operation #tz se.v = #rz se.v",
        "execute store result score #rotation se.v run data get storage space_editor:document job.rotation 1",
        "execute store result score #flip se.v run data get storage space_editor:document job.flipY 1",
        "execute if score #rotation se.v matches 90 run function space_editor:transform/coord_90",
        "execute if score #rotation se.v matches 180 run function space_editor:transform/coord_180",
        "execute if score #rotation se.v matches 270 run function space_editor:transform/coord_270",
        "execute if score #flip se.v matches 1 run function space_editor:transform/coord_flip_y",
        "scoreboard players operation #dstx se.v += #tx se.v",
        "scoreboard players operation #dsty se.v += #ty se.v",
        "scoreboard players operation #dstz se.v += #tz se.v",
        *[f"execute store result storage space_editor:document job.blockSource{axis.upper()} int 1 run scoreboard players get #src{axis} se.v" for axis in "xyz"],
        *[f"execute store result storage space_editor:document job.blockTarget{axis.upper()} int 1 run scoreboard players get #dst{axis} se.v" for axis in "xyz"],
    ])
    fn("transform/coord_90", [
        "scoreboard players operation #tx se.v = #sz se.v",
        "scoreboard players remove #tx se.v 1",
        "scoreboard players operation #tx se.v -= #rz se.v",
        "scoreboard players operation #tz se.v = #rx se.v",
    ])
    fn("transform/coord_180", [
        "scoreboard players operation #tx se.v = #sx se.v",
        "scoreboard players remove #tx se.v 1",
        "scoreboard players operation #tx se.v -= #rx se.v",
        "scoreboard players operation #tz se.v = #sz se.v",
        "scoreboard players remove #tz se.v 1",
        "scoreboard players operation #tz se.v -= #rz se.v",
    ])
    fn("transform/coord_270", [
        "scoreboard players operation #tx se.v = #rz se.v",
        "scoreboard players operation #tz se.v = #sx se.v",
        "scoreboard players remove #tz se.v 1",
        "scoreboard players operation #tz se.v -= #rx se.v",
    ])
    fn("transform/coord_flip_y", [
        "scoreboard players operation #ty se.v = #sy se.v",
        "scoreboard players remove #ty se.v 1",
        "scoreboard players operation #ty se.v -= #ry se.v",
    ])
    fn("transform/preflight", [
        "function space_editor:transform/preflight_macro with storage space_editor:document job",
    ])
    fn("transform/preflight_macro", [
        '$execute in $(sourceDimension) unless block $(blockSourceX) $(blockSourceY) $(blockSourceZ) #space_editor:transform_allowed run function space_editor:transform/record_unsupported',
        '$execute if data storage space_editor:document job{flipY:1b} in $(sourceDimension) if block $(blockSourceX) $(blockSourceY) $(blockSourceZ) #space_editor:transform_vertical_unsupported run function space_editor:transform/record_unsupported',
    ])
    fn("transform/record_unsupported", [
        "execute store result score #unsupported se.v run data get storage space_editor:document job.unsupportedBlocks 1",
        "scoreboard players add #unsupported se.v 1",
        "execute store result storage space_editor:document job.unsupportedBlocks int 1 run scoreboard players get #unsupported se.v",
    ])

    fn("transform/clone_one", [
        "scoreboard players set #skip se.v 0",
        "function space_editor:transform/skip_check with storage space_editor:document job",
        "execute if score #skip se.v matches 1 run return 0",
        'data modify storage space_editor:runtime transformState set value {kind:"none"}',
        "function space_editor:transform/state_capture with storage space_editor:document job",
        'execute unless data storage space_editor:runtime transformState{kind:"none"} unless data storage space_editor:runtime transformState.block run return run function space_editor:transform/fail_state_item',
        "execute store success score #clone_ok se.v run function space_editor:transform/clone_one_macro with storage space_editor:document job",
        "execute unless score #clone_ok se.v matches 1 run return run function space_editor:transform/fail_clone",
        'execute unless data storage space_editor:runtime transformState{kind:"none"} run function space_editor:transform/clear_target with storage space_editor:runtime transformState',
        "scoreboard players set #state_ok se.v 1",
        'execute if data storage space_editor:runtime transformState{kind:"stairs"} store success score #state_ok se.v run function space_editor:transform/apply_stairs with storage space_editor:runtime transformState',
        'execute if data storage space_editor:runtime transformState{kind:"slab"} store success score #state_ok se.v run function space_editor:transform/apply_slab with storage space_editor:runtime transformState',
        'execute if data storage space_editor:runtime transformState{kind:"connections"} store success score #state_ok se.v run function space_editor:transform/apply_connections with storage space_editor:runtime transformState',
        'execute if data storage space_editor:runtime transformState{kind:"wall"} store success score #state_ok se.v run function space_editor:transform/apply_wall with storage space_editor:runtime transformState',
        'execute if data storage space_editor:runtime transformState{kind:"axis"} store success score #state_ok se.v run function space_editor:transform/apply_axis with storage space_editor:runtime transformState',
        'execute if data storage space_editor:runtime transformState{kind:"axis_waterlogged"} store success score #state_ok se.v run function space_editor:transform/apply_axis_waterlogged with storage space_editor:runtime transformState',
        "execute unless score #state_ok se.v matches 1 run return run function space_editor:transform/fail_state_apply",
        "execute store result score #done se.v run data get storage space_editor:document job.completedBlocks 1",
        "scoreboard players add #done se.v 1",
        "execute store result storage space_editor:document job.completedBlocks int 1 run scoreboard players get #done se.v",
    ])
    fn("transform/skip_check", [
        '$execute in $(sourceDimension) unless block $(blockSourceX) $(blockSourceY) $(blockSourceZ) #space_editor:transform_allowed run return run function space_editor:transform/record_skipped',
        '$execute if data storage space_editor:document job{flipY:1b} in $(sourceDimension) if block $(blockSourceX) $(blockSourceY) $(blockSourceZ) #space_editor:transform_vertical_unsupported run return run function space_editor:transform/record_skipped',
    ])
    fn("transform/record_skipped", [
        "scoreboard players set #skip se.v 1",
        "execute store result score #skipped se.v run data get storage space_editor:document job.skippedBlocks 1",
        "scoreboard players add #skipped se.v 1",
        "execute store result storage space_editor:document job.skippedBlocks int 1 run scoreboard players get #skipped se.v",
    ])
    fn("transform/clone_one_macro", [
        '$return run clone from $(sourceDimension) $(blockSourceX) $(blockSourceY) $(blockSourceZ) $(blockSourceX) $(blockSourceY) $(blockSourceZ) to $(targetDimension) $(blockTargetX) $(blockTargetY) $(blockTargetZ) strict replace force',
    ])
    fn("transform/fail_state_item", [
        'data modify storage space_editor:document job.state set value "error"',
        'data modify storage space_editor:document job.error set value "state_block_item_unavailable"',
        message("BlockState変換用のブロックID取得に失敗しました。Jobを停止しました。", "red", "@a"),
    ])
    fn("transform/fail_clone", [
        'data modify storage space_editor:document job.state set value "error"',
        'data modify storage space_editor:document job.error set value "single_block_clone_failed"',
        message("1ブロックCloneに失敗しました。Jobを停止しました。", "red", "@a"),
    ])
    fn("transform/fail_state_apply", [
        'data modify storage space_editor:document job.state set value "error"',
        'data modify storage space_editor:document job.error set value "block_state_apply_failed"',
        message("BlockState補正に失敗しました。Jobを停止しました。", "red", "@a"),
    ])

    fn("transform/state_capture", [
        '$execute in $(sourceDimension) positioned $(blockSourceX) $(blockSourceY) $(blockSourceZ) if block ~ ~ ~ #space_editor:transform_stairs run function space_editor:transform/capture_stairs with storage space_editor:document job',
        '$execute in $(sourceDimension) positioned $(blockSourceX) $(blockSourceY) $(blockSourceZ) if block ~ ~ ~ #space_editor:transform_slabs run function space_editor:transform/capture_slab with storage space_editor:document job',
        '$execute in $(sourceDimension) positioned $(blockSourceX) $(blockSourceY) $(blockSourceZ) if block ~ ~ ~ #space_editor:transform_connections run function space_editor:transform/capture_connections with storage space_editor:document job',
        '$execute in $(sourceDimension) positioned $(blockSourceX) $(blockSourceY) $(blockSourceZ) if block ~ ~ ~ #space_editor:transform_walls run function space_editor:transform/capture_wall with storage space_editor:document job',
        '$execute in $(sourceDimension) positioned $(blockSourceX) $(blockSourceY) $(blockSourceZ) if block ~ ~ ~ #space_editor:transform_axis run function space_editor:transform/capture_axis with storage space_editor:document job',
        '$execute in $(sourceDimension) positioned $(blockSourceX) $(blockSourceY) $(blockSourceZ) if block ~ ~ ~ #space_editor:transform_axis_waterlogged run function space_editor:transform/capture_axis_waterlogged with storage space_editor:document job',
    ])
    read_item = [
        '$execute in $(sourceDimension) run setblock $(scratchX) $(scratchY) $(scratchZ) minecraft:barrel',
        '$execute in $(sourceDimension) run loot replace block $(scratchX) $(scratchY) $(scratchZ) container.0 1 mine $(blockSourceX) $(blockSourceY) $(blockSourceZ) minecraft:diamond_pickaxe[minecraft:enchantments={"minecraft:silk_touch":1}]',
        '$data modify storage space_editor:runtime transformState.block set from block $(scratchX) $(scratchY) $(scratchZ) Items[{Slot:0b}].id',
        '$execute in $(sourceDimension) run setblock $(scratchX) $(scratchY) $(scratchZ) minecraft:air',
    ]
    fn("transform/read_item", read_item)

    def capture_bool(prop: str) -> list[str]:
        return [f'execute if block ~ ~ ~ #space_editor:transform_connections[{prop}=true] run data modify storage space_editor:runtime transformState.{prop} set value "true"',
                f'execute if block ~ ~ ~ #space_editor:transform_connections[{prop}=false] run data modify storage space_editor:runtime transformState.{prop} set value "false"']

    facing_lines: list[str] = []
    maps = {
        0: {"north": "north", "east": "east", "south": "south", "west": "west"},
        90: {"north": "east", "east": "south", "south": "west", "west": "north"},
        180: {"north": "south", "east": "west", "south": "north", "west": "east"},
        270: {"north": "west", "east": "north", "south": "east", "west": "south"},
    }
    for rotation, mapping in maps.items():
        for source, target in mapping.items():
            facing_lines.append(f'execute if score #rotation se.v matches {rotation} if block ~ ~ ~ #space_editor:transform_stairs[facing={source}] run data modify storage space_editor:runtime transformState.facing set value "{target}"')

    fn("transform/capture_stairs", [
        'data modify storage space_editor:runtime transformState set value {kind:"stairs",facing:"north",half:"bottom",shape:"straight",waterlogged:"false",x:0,y:0,z:0}',
        *facing_lines,
        *[f'execute if block ~ ~ ~ #space_editor:transform_stairs[half={value}] run data modify storage space_editor:runtime transformState.half set value "{value}"' for value in ("top", "bottom")],
        'execute if score #flip se.v matches 1 if data storage space_editor:runtime transformState{half:"top"} run data modify storage space_editor:runtime transformState.half set value "bottom"',
        'execute if score #flip se.v matches 1 if block ~ ~ ~ #space_editor:transform_stairs[half=bottom] run data modify storage space_editor:runtime transformState.half set value "top"',
        *[f'execute if block ~ ~ ~ #space_editor:transform_stairs[shape={value}] run data modify storage space_editor:runtime transformState.shape set value "{value}"' for value in ("straight", "inner_left", "inner_right", "outer_left", "outer_right")],
        *[f'execute if block ~ ~ ~ #space_editor:transform_stairs[waterlogged={value}] run data modify storage space_editor:runtime transformState.waterlogged set value "{value}"' for value in ("true", "false")],
        *[f"data modify storage space_editor:runtime transformState.{axis} set from storage space_editor:document job.blockTarget{axis.upper()}" for axis in "xyz"],
        "data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension",
        "function space_editor:transform/read_item with storage space_editor:document job",
    ])
    fn("transform/capture_slab", [
        'data modify storage space_editor:runtime transformState set value {kind:"slab",type:"bottom",waterlogged:"false",x:0,y:0,z:0}',
        *[f'execute if block ~ ~ ~ #space_editor:transform_slabs[type={value}] run data modify storage space_editor:runtime transformState.type set value "{value}"' for value in ("top", "bottom", "double")],
        'execute if score #flip se.v matches 1 if data storage space_editor:runtime transformState{type:"top"} run data modify storage space_editor:runtime transformState.type set value "bottom"',
        'execute if score #flip se.v matches 1 if block ~ ~ ~ #space_editor:transform_slabs[type=bottom] run data modify storage space_editor:runtime transformState.type set value "top"',
        *[f'execute if block ~ ~ ~ #space_editor:transform_slabs[waterlogged={value}] run data modify storage space_editor:runtime transformState.waterlogged set value "{value}"' for value in ("true", "false")],
        *[f"data modify storage space_editor:runtime transformState.{axis} set from storage space_editor:document job.blockTarget{axis.upper()}" for axis in "xyz"],
        "data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension",
        "function space_editor:transform/read_item with storage space_editor:document job",
    ])
    fn("transform/capture_connections", [
        'data modify storage space_editor:runtime transformState set value {kind:"connections",north:"false",east:"false",south:"false",west:"false",waterlogged:"false",x:0,y:0,z:0}',
        *sum((capture_bool(direction) for direction in ("north", "east", "south", "west")), []),
        *[f'execute if block ~ ~ ~ #space_editor:transform_connections[waterlogged={value}] run data modify storage space_editor:runtime transformState.waterlogged set value "{value}"' for value in ("true", "false")],
        "function space_editor:transform/rotate_connections",
        *[f"data modify storage space_editor:runtime transformState.{axis} set from storage space_editor:document job.blockTarget{axis.upper()}" for axis in "xyz"],
        "data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension",
        "function space_editor:transform/read_item with storage space_editor:document job",
    ])
    fn("transform/capture_wall", [
        'data modify storage space_editor:runtime transformState set value {kind:"wall",north:"none",east:"none",south:"none",west:"none",up:"true",waterlogged:"false",x:0,y:0,z:0}',
        *[f'execute if block ~ ~ ~ #space_editor:transform_walls[{direction}={value}] run data modify storage space_editor:runtime transformState.{direction} set value "{value}"' for direction in ("north", "east", "south", "west") for value in ("none", "low", "tall")],
        *[f'execute if block ~ ~ ~ #space_editor:transform_walls[up={value}] run data modify storage space_editor:runtime transformState.up set value "{value}"' for value in ("true", "false")],
        *[f'execute if block ~ ~ ~ #space_editor:transform_walls[waterlogged={value}] run data modify storage space_editor:runtime transformState.waterlogged set value "{value}"' for value in ("true", "false")],
        "function space_editor:transform/rotate_connections",
        *[f"data modify storage space_editor:runtime transformState.{axis} set from storage space_editor:document job.blockTarget{axis.upper()}" for axis in "xyz"],
        "data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension",
        "function space_editor:transform/read_item with storage space_editor:document job",
    ])
    fn("transform/rotate_connections", [
        "data modify storage space_editor:runtime connectionSource set from storage space_editor:runtime transformState",
        *[f"execute if score #rotation se.v matches {rotation} run function space_editor:transform/connections_{rotation}" for rotation in (90, 180, 270)],
    ])
    connection_maps = {
        90: {"north": "west", "east": "north", "south": "east", "west": "south"},
        180: {"north": "south", "east": "west", "south": "north", "west": "east"},
        270: {"north": "east", "east": "south", "south": "west", "west": "north"},
    }
    for rotation, target_from_source in connection_maps.items():
        fn(f"transform/connections_{rotation}", [
            f"data modify storage space_editor:runtime transformState.{target} set from storage space_editor:runtime connectionSource.{source}"
            for target, source in target_from_source.items()
        ])
    fn("transform/capture_axis", [
        'data modify storage space_editor:runtime transformState set value {kind:"axis",axis:"y",x:0,y:0,z:0}',
        *[f'execute if block ~ ~ ~ #space_editor:transform_axis[axis={value}] run data modify storage space_editor:runtime transformState.axis set value "{value}"' for value in ("x", "y", "z")],
        'execute if score #rotation se.v matches 90 if data storage space_editor:runtime transformState{axis:"x"} run data modify storage space_editor:runtime transformState.axis set value "z"',
        'execute if score #rotation se.v matches 90 if block ~ ~ ~ #space_editor:transform_axis[axis=z] run data modify storage space_editor:runtime transformState.axis set value "x"',
        'execute if score #rotation se.v matches 270 if data storage space_editor:runtime transformState{axis:"x"} run data modify storage space_editor:runtime transformState.axis set value "z"',
        'execute if score #rotation se.v matches 270 if block ~ ~ ~ #space_editor:transform_axis[axis=z] run data modify storage space_editor:runtime transformState.axis set value "x"',
        *[f"data modify storage space_editor:runtime transformState.{axis} set from storage space_editor:document job.blockTarget{axis.upper()}" for axis in "xyz"],
        "data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension",
        "function space_editor:transform/read_item with storage space_editor:document job",
    ])
    fn("transform/capture_axis_waterlogged", [
        'data modify storage space_editor:runtime transformState set value {kind:"axis_waterlogged",axis:"y",waterlogged:"false",x:0,y:0,z:0}',
        *[f'execute if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis={value}] run data modify storage space_editor:runtime transformState.axis set value "{value}"' for value in ("x", "y", "z")],
        'execute if score #rotation se.v matches 90 if data storage space_editor:runtime transformState{axis:"x"} run data modify storage space_editor:runtime transformState.axis set value "z"',
        'execute if score #rotation se.v matches 90 if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis=z] run data modify storage space_editor:runtime transformState.axis set value "x"',
        'execute if score #rotation se.v matches 270 if data storage space_editor:runtime transformState{axis:"x"} run data modify storage space_editor:runtime transformState.axis set value "z"',
        'execute if score #rotation se.v matches 270 if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis=z] run data modify storage space_editor:runtime transformState.axis set value "x"',
        *[f'execute if block ~ ~ ~ #space_editor:transform_axis_waterlogged[waterlogged={value}] run data modify storage space_editor:runtime transformState.waterlogged set value "{value}"' for value in ("true", "false")],
        *[f"data modify storage space_editor:runtime transformState.{axis} set from storage space_editor:document job.blockTarget{axis.upper()}" for axis in "xyz"],
        "data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension",
        "function space_editor:transform/read_item with storage space_editor:document job",
    ])
    fn("transform/apply_stairs", ['$return run execute in $(targetDimension) run setblock $(x) $(y) $(z) $(block)[facing=$(facing),half=$(half),shape=$(shape),waterlogged=$(waterlogged)] strict'])
    fn("transform/apply_slab", ['$return run execute in $(targetDimension) run setblock $(x) $(y) $(z) $(block)[type=$(type),waterlogged=$(waterlogged)] strict'])
    fn("transform/apply_connections", ['$return run execute in $(targetDimension) run setblock $(x) $(y) $(z) $(block)[north=$(north),east=$(east),south=$(south),west=$(west),waterlogged=$(waterlogged)] strict'])
    fn("transform/clear_target", ['$execute in $(targetDimension) run setblock $(x) $(y) $(z) minecraft:air strict'])
    fn("transform/apply_wall", ['$return run execute in $(targetDimension) run setblock $(x) $(y) $(z) $(block)[north=$(north),east=$(east),south=$(south),west=$(west),up=$(up),waterlogged=$(waterlogged)] strict'])
    fn("transform/apply_axis", ['$return run execute in $(targetDimension) run setblock $(x) $(y) $(z) $(block)[axis=$(axis)] strict'])
    fn("transform/apply_axis_waterlogged", ['$return run execute in $(targetDimension) run setblock $(x) $(y) $(z) $(block)[axis=$(axis),waterlogged=$(waterlogged)] strict'])

    fn("job/finish", [
        "function space_editor:job/unforceload_archive with storage space_editor:document job",
        'execute if data storage space_editor:document job{type:"paste"} run function space_editor:job/unforceload_target with storage space_editor:document job',
        'execute if data storage space_editor:document job{type:"copy"} run return run function space_editor:copy/finalize',
        "function space_editor:paste/finalize",
    ])
    fn("job/cancel", [
        'execute if data storage space_editor:document job{state:"running"} run function space_editor:job/unforceload_archive with storage space_editor:document job',
        'execute if data storage space_editor:document job{state:"paused"} run function space_editor:job/unforceload_archive with storage space_editor:document job',
        'execute if data storage space_editor:document job{state:"error"} run function space_editor:job/unforceload_archive with storage space_editor:document job',
        'execute if data storage space_editor:document job{type:"paste",state:"running"} run function space_editor:job/unforceload_target with storage space_editor:document job',
        'execute if data storage space_editor:document job{type:"paste",state:"paused"} run function space_editor:job/unforceload_target with storage space_editor:document job',
        'execute if data storage space_editor:document job{type:"paste",state:"error"} run function space_editor:job/unforceload_target with storage space_editor:document job',
        '$execute if data storage space_editor:document job{type:"paste"} in $(sourceDimension) run setblock $(scratchX) $(scratchY) $(scratchZ) minecraft:air',
        'execute if data storage space_editor:document job{state:"running"} run data modify storage space_editor:document job.state set value "cancelled"',
        'execute if data storage space_editor:document job{state:"paused"} run data modify storage space_editor:document job.state set value "cancelled"',
        'execute if data storage space_editor:document job{state:"error"} run data modify storage space_editor:document job.state set value "cancelled"',
        message("Jobを中断しました。コピー元と既存Templateは変更していません。", "yellow"),
    ])
    fn("paste/finalize", [
        "execute store result score #action se.v run data get storage space_editor:document nextActionId 1",
        'data modify storage space_editor:runtime action set value {id:0,type:"template_paste",templateId:0,version:1,targetDimension:"",origin:[I;0,0,0],rotation:0,flipY:0b,skippedBlocks:0,order:0}',
        "execute store result storage space_editor:runtime action.id int 1 run scoreboard players get #action se.v",
        "data modify storage space_editor:runtime action.templateId set from storage space_editor:document job.id",
        "data modify storage space_editor:runtime action.version set from storage space_editor:document job.version",
        "data modify storage space_editor:runtime action.targetDimension set from storage space_editor:document job.targetDimension",
        *[f"data modify storage space_editor:runtime action.origin[{i}] set from storage space_editor:document job.target{axis.upper()}" for i, axis in enumerate("xyz")],
        "data modify storage space_editor:runtime action.rotation set from storage space_editor:document job.rotation",
        "data modify storage space_editor:runtime action.flipY set from storage space_editor:document job.flipY",
        "data modify storage space_editor:runtime action.skippedBlocks set from storage space_editor:document job.skippedBlocks",
        "execute store result storage space_editor:runtime action.order int 1 run scoreboard players get #action se.v",
        "data modify storage space_editor:document actions append from storage space_editor:runtime action",
        "scoreboard players add #action se.v 1",
        "execute store result storage space_editor:document nextActionId int 1 run scoreboard players get #action se.v",
        "execute store result score #skipped se.v run data get storage space_editor:document job.skippedBlocks 1",
        'execute if score #skipped se.v matches 1.. run tellraw @a [{"text":"[Space Editor] 警告: Paste完了。未対応ブロック ","color":"yellow"},{"score":{"name":"#skipped","objective":"se.v"}},{"text":" 個は配置先を変更せずスキップしました。"}]',
        'data modify storage space_editor:document job.state set value "complete"',
    ])

    append(F / "menu.mcfunction", [
        message("Paste変換: 棒を持った時の正面を基準にShift＋左/右で90度回転、Shift＋上/下でFlipY。"),
        message("変換設定は棒を持ち替えると0度 / FlipY OFFへ戻ります。キャンセル: /function space_editor:paste/cancel"),
    ])
    append(F / "status.mcfunction", [
        'tellraw @s [{text:"Paste transform: Rot=",color:"light_purple"},{score:{name:"@s",objective:"se.rot"}},{text:" / FlipY="},{score:{name:"@s",objective:"se.flip"}}]',
    ])
    print(f"Generated stage-3 Space Editor: {len(list(F.rglob('*.mcfunction')))} functions")


if __name__ == "__main__":
    main()
