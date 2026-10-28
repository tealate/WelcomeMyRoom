"""Generate phase-2 Space Editor functions on top of the phase-1 pack.

The archive is a reserved, permanently force-loaded area in the Overworld.  It
avoids adding a worldgen dimension (which would require a server restart) while
still keeping template blocks outside normal play space.  Every clone job is
split along X according to commandModificationBlockLimit and persisted in the
Document before the first block is copied.
"""
from __future__ import annotations

import json
from pathlib import Path

import build_space_editor_stage1 as stage1

ROOT = Path(__file__).resolve().parents[1]
DP = ROOT / "space_editor_datapack"
F = DP / "data/space_editor/function"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def fn(name: str, lines: list[str] | str) -> None:
    write(F / f"{name}.mcfunction", "\n".join(lines) if isinstance(lines, list) else lines)


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


def main() -> None:
    stage1.main()
    (F / "paste/ray.mcfunction").unlink(missing_ok=True)

    # Additive schema migration.  Phase 1 fields are never replaced.
    insert_before(F / "load.mcfunction", "第1段階を読み込みました", [
        "execute unless data storage space_editor:document templates run data modify storage space_editor:document templates set value []",
        "execute unless data storage space_editor:document nextTemplateId run data modify storage space_editor:document nextTemplateId set value 1",
        "execute unless data storage space_editor:document nextActionId run data modify storage space_editor:document nextActionId set value 1",
        "execute unless data storage space_editor:document archive run data modify storage space_editor:document archive set value {dimension:\"minecraft:overworld\",baseX:20000000,baseY:-63,baseZ:20000000,stride:64}",
        "execute if data storage space_editor:document job{state:\"running\"} run " + message("保存中のCopy/Paste Jobを再開します。", "yellow", "@a"),
    ])
    append(F / "load.mcfunction", [message("第2段階: Fill / Copy / Pasteを読み込みました。", target="@a")])
    append(F / "preview/resync.mcfunction", [
        "execute if data storage space_editor:runtime pastePending run function space_editor:paste/spawn_preview with storage space_editor:runtime pastePending",
    ])

    insert_before(F / "tick.mcfunction", "scoreboard players set @a[scores={se.use=1..}]", [
        'execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste"}}] unless data storage space_editor:runtime pastePending run function space_editor:selection/track',
        'execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"fill"}}] run function space_editor:selection/track',
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"copy\"}}] run function space_editor:input/copy",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"paste\"}}] run function space_editor:input/paste",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"fill\"}}] run function space_editor:input/fill",
        "execute if data storage space_editor:document job{state:\"running\"} run function space_editor:job/tick",
        "execute if data storage space_editor:document job{state:\"awaiting_item\"} run function space_editor:copy/try_issue",
        "execute if data storage space_editor:document job{state:\"complete\"} run function space_editor:job/notify_complete",
    ])

    insert_before(F / "region/ray.mcfunction", "data modify storage space_editor:runtime candidates", [
        "scoreboard players set #paste_hit se.v 0",
        'execute if data storage space_editor:runtime pastePending if data storage space_editor:runtime {activeTool:"delete"} store result score #paste_hit se.v run function space_editor:paste/check_preview_hit with storage space_editor:runtime pastePending',
        'execute if data storage space_editor:runtime pastePending if data storage space_editor:runtime {activeTool:"move"} store result score #paste_hit se.v run function space_editor:paste/check_preview_hit with storage space_editor:runtime pastePending',
        "execute if score #paste_hit se.v matches 1 run return run function space_editor:paste/apply_preview_hit",
    ])

    insert_before(F / "start.mcfunction", "function space_editor:preview/resync", [
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"copy\"}},minecraft:item_model=\"editor:tool_copy\"] run clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"copy\"}}]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"copy\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"copy\"}},minecraft:item_model=\"editor:tool_copy\",minecraft:custom_name={text:\"コピー棒\",color:\"green\",italic:false},minecraft:lore=[{text:\"Regionを見て右クリック: Template保存\",italic:false}]]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"paste\"}},minecraft:item_model=\"editor:tool_paste\"] run clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"paste\"}}]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"paste\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"paste\"}},minecraft:item_model=\"editor:tool_paste\",minecraft:custom_name={text:\"ペースト棒\",color:\"light_purple\",italic:false},minecraft:lore=[{text:\"3ブロック先までの候補位置へTemplateを貼付\",italic:false}]]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"fill\"}},minecraft:item_model=\"editor:tool_fill\"] run clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"fill\"}}]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"fill\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"fill\"}},minecraft:item_model=\"editor:tool_fill\",minecraft:custom_name={text:\"Fill棒\",color:\"gold\",italic:false},minecraft:lore=[{text:\"3ブロック先までの候補位置を含むRegionをFill\",italic:false}]]",
    ])

    # Copy selects the nearest Region through the phase-1 AABB ray test.
    fn("input/copy", [
        "scoreboard players set @s se.cd 5",
        'data modify storage space_editor:runtime activeTool set value "copy"',
        "data remove storage space_editor:runtime hit",
        "scoreboard players set #region_ray se.v 0",
        "execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray",
    ])
    fn("region/apply_hit", [
        "data modify storage space_editor:document selectedId set from storage space_editor:runtime hit.idText",
        "execute if data storage space_editor:runtime {activeTool:\"copy\"} run return run function space_editor:copy/start",
        "execute if data storage space_editor:runtime {activeTool:\"fill\"} run return run function space_editor:fill/offhand",
        "execute if data storage space_editor:runtime {activeTool:\"delete\"} run return run function space_editor:region/delete_selected",
        "execute if data storage space_editor:runtime {activeTool:\"move\"} run return run function space_editor:region/move",
        "execute if data storage space_editor:runtime {activeTool:\"resize_all\"} run return run function space_editor:region/resize_all",
        "function space_editor:region/resize_face",
    ])

    # Common block-alignment gate.  Phase-1 regions may have decimal editor
    # bounds, but destructive block operations require exact block boundaries.
    fn("operation/check_aligned", [
        "scoreboard players set #aligned se.v 1",
        *[line for axis in "xyz" for line in (
            f"execute store result score #{axis}1m se.v run data get storage space_editor:runtime hit.{axis}1m 1",
            f"execute store result score #{axis}2m se.v run data get storage space_editor:runtime hit.{axis}2m 1",
            f"scoreboard players operation #rem se.v = #{axis}1m se.v",
            "scoreboard players operation #rem se.v %= #1000 se.v",
            "execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0",
            f"scoreboard players operation #rem se.v = #{axis}2m se.v",
            "scoreboard players operation #rem se.v %= #1000 se.v",
            "execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0",
        )],
        "execute if score #aligned se.v matches 0 run return 0",
        *[line for axis in "xyz" for line in (
            f"scoreboard players operation #{axis}1 se.v = #{axis}1m se.v",
            f"scoreboard players operation #{axis}1 se.v /= #1000 se.v",
            f"scoreboard players operation #{axis}2 se.v = #{axis}2m se.v",
            f"scoreboard players operation #{axis}2 se.v /= #1000 se.v",
            f"scoreboard players operation #s{axis} se.v = #{axis}2 se.v",
            f"scoreboard players operation #s{axis} se.v -= #{axis}1 se.v",
        )],
        "return 1",
    ])

    # Fill uses the same three-block hover cell as the Region wand. The Region
    # containing the center of that cell is selected. The
    # Region is marked fill-only immediately before the operation and removed
    # only when /fill succeeds.
    fn("fill", ["function space_editor:fill/start"])
    fn("fill/start", [
        "execute unless entity @s[type=minecraft:player] run return 0",
        "data remove storage space_editor:runtime fillBlock",
        "data modify storage space_editor:runtime fillBlock set from entity @s SelectedItem.id",
        "function space_editor:fill/apply",
    ])
    fn("input/fill", [
        "scoreboard players set @s se.cd 5",
        'data modify storage space_editor:runtime activeTool set value "fill"',
        "data remove storage space_editor:runtime hit",
        "execute unless data storage space_editor:runtime hover.pos run return run " + message("選択予定位置を取得できません。", "red"),
        "function space_editor:region/from_hover",
    ])
    fn("region/from_hover", [
        *[f"execute store result score #p{axis} se.v run data get storage space_editor:runtime hover.{axis} 1000" for axis in "xyz"],
        *[f"scoreboard players add #p{axis} se.v 500" for axis in "xyz"],
        "data modify storage space_editor:runtime candidates set from storage space_editor:document regions",
        "execute if data storage space_editor:runtime candidates[0] run function space_editor:region/check_next",
        "execute if data storage space_editor:runtime hit run return run function space_editor:region/apply_hit",
        message("選択予定位置を含むRegionがありません。", "red"),
    ])
    fn("fill/offhand", [
        "data remove storage space_editor:runtime fillBlock",
        "data modify storage space_editor:runtime fillBlock set from entity @s equipment.offhand.id",
        "function space_editor:fill/apply",
    ])
    fn("fill/apply", [
        "execute unless data storage space_editor:runtime hit.id run return run " + message("先にRegionを選択してください。", "red"),
        "execute unless data storage space_editor:runtime fillBlock run return run " + message("Fill棒ではオフハンドに素材ブロックを持ってください。", "red"),
        "execute store result score #aligned se.v run function space_editor:operation/check_aligned",
        "execute unless score #aligned se.v matches 1 run return run " + message("Fillはブロック境界に揃ったRegionだけ使用できます。", "red"),
        "data modify storage space_editor:runtime fill set from storage space_editor:runtime hit",
        "data modify storage space_editor:runtime fill.block set from storage space_editor:runtime fillBlock",
        *[f"execute store result storage space_editor:runtime fill.{axis}1 int 1 run scoreboard players get #{axis}1 se.v" for axis in "xyz"],
        *[f"scoreboard players remove #{axis}2 se.v 1" for axis in "xyz"],
        *[f"execute store result storage space_editor:runtime fill.{axis}2 int 1 run scoreboard players get #{axis}2 se.v" for axis in "xyz"],
        "execute store success score #op_ok se.v run function space_editor:fill/run with storage space_editor:runtime fill",
        "execute unless score #op_ok se.v matches 1 run return run " + message("Fillに失敗しました。手持ちが設置可能なブロックか、範囲が読み込まれているか確認してください。", "red"),
        'data modify storage space_editor:runtime hit.role set value "fill"',
        "function space_editor:region/delete_hit with storage space_editor:runtime hit",
        'data modify storage space_editor:document selectedId set value ""',
        "data remove storage space_editor:runtime hit",
        "function space_editor:preview/resync",
        message("Fill完了。Fill専用RegionをDocumentと表示から削除しました。", "green"),
    ])
    fn("fill/run", ['$return run execute in $(dimension) run fill $(x1) $(y1) $(z1) $(x2) $(y2) $(z2) $(block) replace'])

    # Copy job creation and archive allocation.
    fn("copy/start", [
        "execute if data storage space_editor:document job{state:\"running\"} run return run " + message("別のCopy/Paste Jobが実行中です。", "red"),
        "execute store result score #aligned se.v run function space_editor:operation/check_aligned",
        "execute unless score #aligned se.v matches 1 run return run " + message("Copyはブロック境界に揃ったRegionだけ使用できます。", "red"),
        "execute store result score #template se.v run data get storage space_editor:document nextTemplateId 1",
        "scoreboard players operation #archive_x se.v = #template se.v",
        "scoreboard players set #stride se.v 64",
        "scoreboard players operation #archive_x se.v *= #stride se.v",
        "scoreboard players add #archive_x se.v 20000000",
        'data modify storage space_editor:document job set value {type:"copy",state:"running",id:0,version:1,sourceDimension:"",targetDimension:"minecraft:overworld",sourceX:0,sourceY:0,sourceZ:0,targetX:0,targetY:-63,targetZ:20000000,sx:0,sy:0,sz:0,cursorX:0,completedChunks:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}',
        "execute store result storage space_editor:document job.id int 1 run scoreboard players get #template se.v",
        "data modify storage space_editor:document job.sourceDimension set from storage space_editor:runtime hit.dimension",
        *[f"execute store result storage space_editor:document job.source{axis.upper()} int 1 run scoreboard players get #{axis}1 se.v" for axis in "xyz"],
        "execute store result storage space_editor:document job.targetX int 1 run scoreboard players get #archive_x se.v",
        *[f"execute store result storage space_editor:document job.s{axis} int 1 run scoreboard players get #s{axis} se.v" for axis in "xyz"],
        "scoreboard players operation #archive_x2 se.v = #archive_x se.v",
        "scoreboard players operation #archive_x2 se.v += #sx se.v",
        "scoreboard players remove #archive_x2 se.v 1",
        "scoreboard players set #archive_z2 se.v 20000000",
        "scoreboard players operation #archive_z2 se.v += #sz se.v",
        "scoreboard players remove #archive_z2 se.v 1",
        'data modify storage space_editor:document job.archiveDimension set value "minecraft:overworld"',
        "execute store result storage space_editor:document job.archiveX1 int 1 run scoreboard players get #archive_x se.v",
        "data modify storage space_editor:document job.archiveZ1 set value 20000000",
        "execute store result storage space_editor:document job.archiveX2 int 1 run scoreboard players get #archive_x2 se.v",
        "execute store result storage space_editor:document job.archiveZ2 int 1 run scoreboard players get #archive_z2 se.v",
        *[f"execute store result storage space_editor:document job.owner{i} int 1 run data get entity @s UUID[{i}] 1" for i in range(4)],
        "data modify storage space_editor:document job.sourceRegion set from storage space_editor:runtime hit",
        "function space_editor:job/forceload_archive with storage space_editor:document job",
        "scoreboard players add #template se.v 1",
        "execute store result storage space_editor:document nextTemplateId int 1 run scoreboard players get #template se.v",
        message("Copy Jobを開始しました。進捗はDocumentへ保存されます。", "green"),
    ])
    fn("job/forceload_archive", [
        '$execute in $(archiveDimension) run forceload add $(archiveX1) $(archiveZ1) $(archiveX2) $(archiveZ2)',
    ])
    fn("job/unforceload_archive", [
        '$execute in $(archiveDimension) run forceload remove $(archiveX1) $(archiveZ1) $(archiveX2) $(archiveZ2)',
    ])

    # Paste reads a reference-only template item from the offhand and commits
    # the same three-block hover cell used by the Region wand as its origin.
    fn("input/paste", [
        "scoreboard players set @s se.cd 5",
        'execute if data storage space_editor:runtime pastePending if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run return run function space_editor:paste/cancel',
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
    fn("paste/capture", [
        "data modify storage space_editor:runtime targetDimension set from storage space_editor:runtime hover.dimension",
        "data modify storage space_editor:runtime targetPos set from storage space_editor:runtime hover.pos",
        "function space_editor:paste/preview with storage space_editor:runtime lookup",
    ])
    fn("paste/preview", [
        '$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]',
        "execute unless data storage space_editor:runtime template.id run return run " + message("TemplateIDがDocumentにありません。", "red"),
        'data modify storage space_editor:runtime pastePending set value {id:0,version:1,targetDimension:"",x:0,y:0,z:0,sx:0,sy:0,sz:0,owner0:0,owner1:0,owner2:0,owner3:0}',
        "data modify storage space_editor:runtime pastePending.id set from storage space_editor:runtime template.id",
        "data modify storage space_editor:runtime pastePending.version set from storage space_editor:runtime template.version",
        "data modify storage space_editor:runtime pastePending.targetDimension set from storage space_editor:runtime targetDimension",
        *[f"execute store result storage space_editor:runtime pastePending.{axis} int 1 run data get storage space_editor:runtime targetPos[{i}] 1" for i, axis in enumerate("xyz")],
        *[f"data modify storage space_editor:runtime pastePending.s{axis} set from storage space_editor:runtime template.size[{i}]" for i, axis in enumerate("xyz")],
        *[f"data modify storage space_editor:runtime pastePending.owner{i} set from storage space_editor:runtime lookup.owner{i}" for i in range(4)],
        "function space_editor:preview/resync",
        message("Paste範囲を表示しました。もう一度右クリックで確定、Shift＋右クリックでキャンセル。", "yellow"),
    ])
    fn("paste/spawn_preview", [
        "execute in minecraft:overworld run kill @e[tag=space_editor.paste_preview]",
        "execute in minecraft:the_nether run kill @e[tag=space_editor.paste_preview]",
        "execute in minecraft:the_end run kill @e[tag=space_editor.paste_preview]",
        '$execute in $(targetDimension) positioned $(x) $(y) $(z) run summon minecraft:block_display ~ ~ ~ {Tags:["space_editor.preview","space_editor.paste_preview"],block_state:{Name:"' + stage1.DISPLAY_BLOCKS["selection"] + '"},transformation:{translation:[-0.5f,0f,-0.5f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:3f,width:64f,height:64f}',
    ])
    fn("paste/hide_preview", [
        "execute in minecraft:overworld run kill @e[tag=space_editor.paste_preview]",
        "execute in minecraft:the_nether run kill @e[tag=space_editor.paste_preview]",
        "execute in minecraft:the_end run kill @e[tag=space_editor.paste_preview]",
    ])
    fn("paste/cancel", [
        "function space_editor:paste/hide_preview",
        "data remove storage space_editor:runtime pastePending",
        message("Pasteプレビューをキャンセルしました。", "yellow"),
    ])
    preview_hit = ['$execute unless dimension $(targetDimension) run return 0']
    for axis in "xyz":
        preview_hit += [
            f"execute store result score #{axis}1m se.v run data get storage space_editor:runtime pastePending.{axis} 1000",
            f"execute store result score #s{axis}m se.v run data get storage space_editor:runtime pastePending.s{axis} 1000",
            f"scoreboard players operation #{axis}2m se.v = #{axis}1m se.v",
            f"scoreboard players operation #{axis}2m se.v += #s{axis}m se.v",
            f"execute if score #p{axis} se.v < #{axis}1m se.v run return 0",
            f"execute if score #p{axis} se.v >= #{axis}2m se.v run return 0",
        ]
    preview_hit += [
        'data modify storage space_editor:runtime hit set value {kind:"paste_preview",x1m:0,x2m:0,y1m:0,y2m:0,z1m:0,z2m:0}',
        *[f"execute store result storage space_editor:runtime hit.{axis}{edge}m int 1 run scoreboard players get #{axis}{edge}m se.v" for axis in "xyz" for edge in (1, 2)],
        "function space_editor:region/face",
        "return 1",
    ]
    fn("paste/check_preview_hit", preview_hit)
    fn("paste/apply_preview_hit", [
        'execute if data storage space_editor:runtime {activeTool:"delete"} run return run function space_editor:paste/cancel',
        "function space_editor:paste/move_preview",
    ])
    move_preview = [
        "scoreboard players set #direction se.v 1",
        'execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run scoreboard players set #direction se.v -1',
        *[f"execute store result score #{axis} se.v run data get storage space_editor:runtime pastePending.{axis} 1" for axis in "xyz"],
    ]
    for face_id, axis, _, side in ((0, "x", 0, "min"), (1, "x", 0, "max"), (2, "y", 1, "min"), (3, "y", 1, "max"), (4, "z", 2, "min"), (5, "z", 2, "max")):
        op = "remove" if side == "min" else "add"
        move_preview += [f"execute if data storage space_editor:runtime {{hitFace:{face_id}}} run scoreboard players {op} #{axis} se.v 1"]
        if side == "min":
            move_preview += [f"execute if data storage space_editor:runtime {{hitFace:{face_id}}} if score #direction se.v matches -1 run scoreboard players add #{axis} se.v 2"]
        else:
            move_preview += [f"execute if data storage space_editor:runtime {{hitFace:{face_id}}} if score #direction se.v matches -1 run scoreboard players remove #{axis} se.v 2"]
    move_preview += [
        "execute store result score #y2 se.v run data get storage space_editor:runtime pastePending.sy 1",
        "scoreboard players operation #y2 se.v += #y se.v",
        'execute if data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y se.v matches -64..319 run return run ' + message("Overworldの高さ範囲を超えています。", "red"),
        'execute if data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y2 se.v matches -63..320 run return run ' + message("Overworldの高さ範囲を超えています。", "red"),
        'execute unless data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y se.v matches 0..255 run return run ' + message("Nether/Endの高さ範囲を超えています。", "red"),
        'execute unless data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y2 se.v matches 1..256 run return run ' + message("Nether/Endの高さ範囲を超えています。", "red"),
        *[f"execute store result storage space_editor:runtime pastePending.{axis} int 1 run scoreboard players get #{axis} se.v" for axis in "xyz"],
        "data remove storage space_editor:runtime hit",
        "function space_editor:preview/resync",
        message("Pasteプレビューを1ブロック移動しました。", "green"),
    ]
    fn("paste/move_preview", move_preview)
    fn("paste/confirm", [
        "data modify storage space_editor:runtime lookup.id set from storage space_editor:runtime pastePending.id",
        *[f"data modify storage space_editor:runtime lookup.owner{i} set from storage space_editor:runtime pastePending.owner{i}" for i in range(4)],
        "data modify storage space_editor:runtime targetDimension set from storage space_editor:runtime pastePending.targetDimension",
        "data modify storage space_editor:runtime targetPos set value [I;0,0,0]",
        *[f"data modify storage space_editor:runtime targetPos[{i}] set from storage space_editor:runtime pastePending.{axis}" for i, axis in enumerate("xyz")],
        "function space_editor:paste/start with storage space_editor:runtime lookup",
        'execute if data storage space_editor:document job{type:"paste",state:"running"} run function space_editor:paste/hide_preview',
        'execute if data storage space_editor:document job{type:"paste",state:"running"} run data remove storage space_editor:runtime pastePending',
    ])
    fn("paste/start", [
        '$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]',
        "execute unless data storage space_editor:runtime template.id run return run " + message("TemplateIDがDocumentにありません。", "red"),
        'data modify storage space_editor:document job set value {type:"paste",state:"running",id:0,version:1,sourceDimension:"",targetDimension:"",sourceX:0,sourceY:0,sourceZ:0,targetX:0,targetY:0,targetZ:0,sx:0,sy:0,sz:0,cursorX:0,completedChunks:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}',
        "data modify storage space_editor:document job.id set from storage space_editor:runtime template.id",
        "data modify storage space_editor:document job.version set from storage space_editor:runtime template.version",
        "data modify storage space_editor:document job.sourceDimension set from storage space_editor:runtime template.archive.dimension",
        *[f"data modify storage space_editor:document job.source{axis.upper()} set from storage space_editor:runtime template.archive.{axis}" for axis in "xyz"],
        "data modify storage space_editor:document job.targetDimension set from storage space_editor:runtime targetDimension",
        *[f"execute store result storage space_editor:document job.target{axis.upper()} int 1 run data get storage space_editor:runtime targetPos[{i}] 1" for i, axis in enumerate("xyz")],
        *[f"data modify storage space_editor:document job.s{axis} set from storage space_editor:runtime template.size[{i}]" for i, axis in enumerate("xyz")],
        *[f"data modify storage space_editor:document job.owner{i} set from storage space_editor:runtime lookup.owner{i}" for i in range(4)],
        "data modify storage space_editor:document job.archiveDimension set from storage space_editor:runtime template.archive.dimension",
        "data modify storage space_editor:document job.archiveX1 set from storage space_editor:runtime template.archive.x",
        "data modify storage space_editor:document job.archiveZ1 set from storage space_editor:runtime template.archive.z",
        "execute store result score #archive_x2 se.v run data get storage space_editor:runtime template.archive.x 1",
        "execute store result score #archive_z2 se.v run data get storage space_editor:runtime template.archive.z 1",
        "execute store result score #sx se.v run data get storage space_editor:runtime template.size[0] 1",
        "execute store result score #sz se.v run data get storage space_editor:runtime template.size[2] 1",
        "scoreboard players operation #archive_x2 se.v += #sx se.v",
        "scoreboard players remove #archive_x2 se.v 1",
        "scoreboard players operation #archive_z2 se.v += #sz se.v",
        "scoreboard players remove #archive_z2 se.v 1",
        "execute store result storage space_editor:document job.archiveX2 int 1 run scoreboard players get #archive_x2 se.v",
        "execute store result storage space_editor:document job.archiveZ2 int 1 run scoreboard players get #archive_z2 se.v",
        "function space_editor:job/forceload_archive with storage space_editor:document job",
        message("Paste Jobを開始しました（0度・反転なし・airを含む・クリックしたブロック原点）。", "green"),
    ])

    # One persisted X strip per tick.  A strip width is derived from the live
    # commandModificationBlockLimit; a minimum of one prevents deadlock.
    fn("job/tick", [
        "execute store result score #cursor se.v run data get storage space_editor:document job.cursorX 1",
        "execute store result score #sx se.v run data get storage space_editor:document job.sx 1",
        "execute store result score #sy se.v run data get storage space_editor:document job.sy 1",
        "execute store result score #sz se.v run data get storage space_editor:document job.sz 1",
        "scoreboard players operation #remaining se.v = #sx se.v",
        "scoreboard players operation #remaining se.v -= #cursor se.v",
        "execute if score #remaining se.v matches ..0 run return run function space_editor:job/finish",
        "execute store result score #limit se.v run gamerule minecraft:max_block_modifications",
        "scoreboard players operation #area se.v = #sy se.v",
        "scoreboard players operation #area se.v *= #sz se.v",
        "scoreboard players operation #width se.v = #limit se.v",
        "scoreboard players operation #width se.v /= #area se.v",
        "execute if score #width se.v matches ..0 run scoreboard players set #width se.v 1",
        "scoreboard players operation #width se.v < #remaining se.v",
        "function space_editor:job/prepare_chunk",
        "execute store success score #clone_ok se.v run function space_editor:job/clone_chunk with storage space_editor:document job",
        "execute unless score #clone_ok se.v matches 1 run return run function space_editor:job/fail",
        "scoreboard players operation #cursor se.v += #width se.v",
        "execute store result storage space_editor:document job.cursorX int 1 run scoreboard players get #cursor se.v",
        "execute store result score #chunks se.v run data get storage space_editor:document job.completedChunks 1",
        "scoreboard players add #chunks se.v 1",
        "execute store result storage space_editor:document job.completedChunks int 1 run scoreboard players get #chunks se.v",
        "execute if score #cursor se.v >= #sx se.v run function space_editor:job/finish",
    ])
    fn("job/prepare_chunk", [
        *[f"execute store result score #src{axis} se.v run data get storage space_editor:document job.source{axis.upper()} 1" for axis in "xyz"],
        *[f"execute store result score #dst{axis} se.v run data get storage space_editor:document job.target{axis.upper()} 1" for axis in "xyz"],
        "scoreboard players operation #srcx se.v += #cursor se.v",
        "scoreboard players operation #dstx se.v += #cursor se.v",
        "scoreboard players operation #srcx2 se.v = #srcx se.v",
        "scoreboard players operation #srcx2 se.v += #width se.v",
        "scoreboard players remove #srcx2 se.v 1",
        "scoreboard players operation #srcy2 se.v = #srcy se.v",
        "scoreboard players operation #srcy2 se.v += #sy se.v",
        "scoreboard players remove #srcy2 se.v 1",
        "scoreboard players operation #srcz2 se.v = #srcz se.v",
        "scoreboard players operation #srcz2 se.v += #sz se.v",
        "scoreboard players remove #srcz2 se.v 1",
        *[f"execute store result storage space_editor:document job.{name} int 1 run scoreboard players get #{score} se.v" for name, score in (
            ("chunkSourceX1", "srcx"), ("chunkSourceY1", "srcy"), ("chunkSourceZ1", "srcz"),
            ("chunkSourceX2", "srcx2"), ("chunkSourceY2", "srcy2"), ("chunkSourceZ2", "srcz2"),
            ("chunkTargetX", "dstx"), ("chunkTargetY", "dsty"), ("chunkTargetZ", "dstz"),
        )],
    ])
    fn("job/clone_chunk", [
        '$return run clone from $(sourceDimension) $(chunkSourceX1) $(chunkSourceY1) $(chunkSourceZ1) $(chunkSourceX2) $(chunkSourceY2) $(chunkSourceZ2) to $(targetDimension) $(chunkTargetX) $(chunkTargetY) $(chunkTargetZ) strict replace force',
    ])
    fn("job/fail", [
        'data modify storage space_editor:document job.state set value "error"',
        'data modify storage space_editor:document job.error set value "clone_failed_or_chunk_unloaded"',
        message("Clone区画に失敗したためJobを停止しました。/function space_editor:job/retry", "red", "@a"),
    ])
    fn("job/finish", [
        "function space_editor:job/unforceload_archive with storage space_editor:document job",
        "execute if data storage space_editor:document job{type:\"copy\"} run return run function space_editor:copy/finalize",
        "function space_editor:paste/finalize",
    ])
    fn("copy/finalize", [
        'data modify storage space_editor:runtime template set value {id:0,version:1,archive:{dimension:"",x:0,y:0,z:0},size:[I;0,0,0],source:{},rotation:0,flipY:0b}',
        "data modify storage space_editor:runtime template.id set from storage space_editor:document job.id",
        "data modify storage space_editor:runtime template.version set from storage space_editor:document job.version",
        'data modify storage space_editor:runtime template.archive set value {dimension:"",x:0,y:0,z:0}',
        "data modify storage space_editor:runtime template.archive.dimension set from storage space_editor:document job.targetDimension",
        "data modify storage space_editor:runtime template.archive.x set from storage space_editor:document job.targetX",
        "data modify storage space_editor:runtime template.archive.y set from storage space_editor:document job.targetY",
        "data modify storage space_editor:runtime template.archive.z set from storage space_editor:document job.targetZ",
        "data modify storage space_editor:runtime template.size set value [I;0,0,0]",
        "data modify storage space_editor:runtime template.size[0] set from storage space_editor:document job.sx",
        "data modify storage space_editor:runtime template.size[1] set from storage space_editor:document job.sy",
        "data modify storage space_editor:runtime template.size[2] set from storage space_editor:document job.sz",
        "data modify storage space_editor:runtime template.source set from storage space_editor:document job.sourceRegion",
        "data modify storage space_editor:document templates append from storage space_editor:runtime template",
        'data modify storage space_editor:document job.state set value "awaiting_item"',
        "function space_editor:copy/try_issue",
    ])
    fn("copy/try_issue", ["function space_editor:copy/issue_selector with storage space_editor:document job"])
    fn("copy/issue_selector", [
        '$execute as @a[nbt={UUID:[I;$(owner0),$(owner1),$(owner2),$(owner3)]}] run function space_editor:copy/issue with storage space_editor:document job',
    ])
    fn("copy/issue", [
        '$give @s minecraft:paper[minecraft:custom_data={space_editor:{kind:"template",templateId:$(id),version:$(version)}},minecraft:custom_name={text:"Template #$(id)",color:"green",italic:false},minecraft:lore=[{text:"参照アイテム / ブロック本体はTool Archive",color:"gray",italic:false}]]',
        message("Templateアイテムを発行しました。", "green"),
        'data modify storage space_editor:document job.state set value "done"',
    ])
    fn("paste/finalize", [
        "execute store result score #action se.v run data get storage space_editor:document nextActionId 1",
        'data modify storage space_editor:runtime action set value {id:0,type:"template_paste",templateId:0,version:1,targetDimension:"",origin:[I;0,0,0],rotation:0,flipY:0b,order:0}',
        "execute store result storage space_editor:runtime action.id int 1 run scoreboard players get #action se.v",
        "data modify storage space_editor:runtime action.templateId set from storage space_editor:document job.id",
        "data modify storage space_editor:runtime action.version set from storage space_editor:document job.version",
        "data modify storage space_editor:runtime action.targetDimension set from storage space_editor:document job.targetDimension",
        *[f"data modify storage space_editor:runtime action.origin[{i}] set from storage space_editor:document job.target{axis.upper()}" for i, axis in enumerate("xyz")],
        "execute store result storage space_editor:runtime action.order int 1 run scoreboard players get #action se.v",
        "data modify storage space_editor:document actions append from storage space_editor:runtime action",
        "scoreboard players add #action se.v 1",
        "execute store result storage space_editor:document nextActionId int 1 run scoreboard players get #action se.v",
        'data modify storage space_editor:document job.state set value "complete"',
    ])
    fn("job/notify_complete", ["function space_editor:job/notify_selector with storage space_editor:document job"])
    fn("job/notify_selector", [
        '$execute as @a[nbt={UUID:[I;$(owner0),$(owner1),$(owner2),$(owner3)]}] run ' + message("Paste完了。", "green"),
        'data modify storage space_editor:document job.state set value "done"',
    ])

    fn("job/pause", [
        'execute if data storage space_editor:document job{state:"running"} run data modify storage space_editor:document job.state set value "paused"',
        message("Jobを一時停止しました。", "yellow"),
    ])
    fn("job/resume", [
        'execute if data storage space_editor:document job{state:"paused"} run data modify storage space_editor:document job.state set value "running"',
        message("Jobを再開しました。", "green"),
    ])
    fn("job/retry", [
        'execute if data storage space_editor:document job{state:"error"} run data modify storage space_editor:document job.state set value "running"',
        "data remove storage space_editor:document job.error",
        message("失敗した区画からJobを再試行します。", "yellow"),
    ])
    fn("job/cancel", [
        'execute if data storage space_editor:document job{state:"running"} run function space_editor:job/unforceload_archive with storage space_editor:document job',
        'execute if data storage space_editor:document job{state:"paused"} run function space_editor:job/unforceload_archive with storage space_editor:document job',
        'execute if data storage space_editor:document job{state:"error"} run function space_editor:job/unforceload_archive with storage space_editor:document job',
        'execute if data storage space_editor:document job{state:"running"} run data modify storage space_editor:document job.state set value "cancelled"',
        'execute if data storage space_editor:document job{state:"paused"} run data modify storage space_editor:document job.state set value "cancelled"',
        'execute if data storage space_editor:document job{state:"error"} run data modify storage space_editor:document job.state set value "cancelled"',
        message("Jobを中断しました。コピー元と既存Templateは変更していません。", "yellow"),
    ])

    # Manual reissue path for a lost reference item.
    fn("template/reissue", [
        '$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]',
        "execute unless data storage space_editor:runtime template.id run return run " + message("TemplateIDが見つかりません。", "red"),
        "function space_editor:template/give with storage space_editor:runtime template",
    ])
    fn("template/give", [
        '$give @s minecraft:paper[minecraft:custom_data={space_editor:{kind:"template",templateId:$(id),version:$(version)}},minecraft:custom_name={text:"Template #$(id)",color:"green",italic:false},minecraft:lore=[{text:"再発行された参照アイテム",color:"gray",italic:false}]]',
        message("Templateアイテムを再発行しました。", "green"),
    ])

    append(F / "menu.mcfunction", [
        message("Fill: Region選択→ブロックをメインハンド→/function space_editor:fill"),
        message("Fill: Fill棒＋オフハンド素材 / Copy: コピー棒 / Paste: ペースト棒＋オフハンドTemplate"),
        message("Fill/Paste棒は範囲棒と同じ3ブロック候補を使用。ブロックがなければ空中セルを選択します。"),
        message("Pasteは1回目で範囲表示、2回目で確定。キャンセル: /function space_editor:paste/cancel"),
        message("Job: /function space_editor:job/pause | resume | retry | cancel"),
        message("再発行: /function space_editor:template/reissue {id:1}"),
    ])
    append(F / "status.mcfunction", [
        'tellraw @s [{text:"Templates: ",color:"green"},{nbt:"templates",storage:"space_editor:document",interpret:false}]',
        'tellraw @s [{text:"Job: ",color:"light_purple"},{nbt:"job",storage:"space_editor:document",interpret:false}]',
    ])

    print(f"Generated stage-2 Space Editor: {len(list(F.rglob('*.mcfunction')))} functions")


if __name__ == "__main__":
    main()
