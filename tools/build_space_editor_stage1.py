"""Generate the stage-1 Space Editor datapack for Minecraft Java 26.1."""
from __future__ import annotations

import json
from pathlib import Path

from editor_block_config import EditorBlockConfigError, load_editor_block_config
import build_space_editor_resources as resources

ROOT = Path(__file__).resolve().parents[1]
DP = ROOT / "space_editor_datapack"
F = DP / "data/space_editor/function"
try:
    BLOCK_CONFIG = load_editor_block_config()
    DISPLAY_BLOCKS = BLOCK_CONFIG["displayBlocks"]
except EditorBlockConfigError as error:
    raise SystemExit(f"Error: {error}") from None


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def fn(name: str, lines: list[str] | str) -> None:
    write(F / f"{name}.mcfunction", "\n".join(lines) if isinstance(lines, list) else lines)


def js(path: Path, value: object) -> None:
    write(path, json.dumps(value, ensure_ascii=False, indent=2))


def message(text: str, color: str = "aqua", target: str = "@s") -> str:
    return f"tellraw {target} " + json.dumps({"text": f"[Space Editor] {text}", "color": color}, ensure_ascii=False)


def dimensions(command: str) -> list[str]:
    return [f"execute in minecraft:{d} run {command}" for d in ("overworld", "the_nether", "the_end")]


def main() -> None:
    resources.main()
    js(DP / "data/minecraft/tags/function/load.json", {"values": ["space_editor:load"]})
    js(DP / "data/minecraft/tags/function/tick.json", {"values": ["space_editor:tick"]})
    js(DP / "data/space_editor/tags/block/ray_pass.json", {"values": [
        "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:water",
        "minecraft:light", "minecraft:structure_void"
    ]})

    fn("load", [
        "scoreboard objectives add se.v dummy",
        "scoreboard objectives add se.use minecraft.used:minecraft.carrot_on_a_stick",
        "scoreboard objectives add se.cd dummy",
        "scoreboard objectives add se.id dummy",
        "scoreboard objectives add se.dim dummy",
        "scoreboard players set #minus_one se.v -1",
        "scoreboard players set #50 se.v 50",
        "scoreboard players set #100 se.v 100",
        "scoreboard players set #1000 se.v 1000",
        "scoreboard players set #two se.v 2",
        "scoreboard players set #ray_limit se.v 128",
        "execute unless data storage space_editor:document schemaVersion run function space_editor:internal/init",
        "execute unless data storage space_editor:document {schemaVersion:1} run return run " + message("未対応の保存形式です。データは変更していません。", "red", "@a"),
        "execute unless data storage space_editor:document settings.stepMilli run function space_editor:internal/migrate_step",
        "execute unless data storage space_editor:document settings{boundsVersion:3} run function space_editor:internal/migrate_bounds",
        "execute unless data storage space_editor:document settings.regionsVisible run data modify storage space_editor:document settings.regionsVisible set value 1b",
        *dimensions("kill @e[tag=space_editor.preview]"),
        *dimensions("kill @e[tag=space_editor.selection_capture]"),
        "execute if entity @a[tag=space_editor.editing] run function space_editor:preview/resync",
        message("第1段階を読み込みました。/function space_editor:start", target="@a"),
    ])
    fn("internal/init", [
        'data modify storage space_editor:document schemaVersion set value 1',
        'data modify storage space_editor:document regions set value []',
        'data modify storage space_editor:document actions set value []',
        'data modify storage space_editor:document portalLinks set value []',
        'data modify storage space_editor:document nextId set value 1',
        'data modify storage space_editor:document editMode set value 0b',
        'data modify storage space_editor:document selectedId set value ""',
        'data modify storage space_editor:document settings set value {step:0.1d,stepMilli:100,fixedStep:1b,fixedBounds:1b,boundsVersion:3,regionsVisible:1b}',
    ])
    fn("internal/migrate_step", [
        'data modify storage space_editor:document settings.step set value 0.1d',
        'data modify storage space_editor:document settings.stepMilli set value 100',
        'data modify storage space_editor:document settings.fixedStep set value 1b',
    ])
    fn("internal/migrate_bounds", [
        'data modify storage space_editor:runtime migrateQueue set from storage space_editor:document regions',
        'execute if data storage space_editor:runtime migrateQueue[0] run function space_editor:internal/migrate_bounds_next',
        'data modify storage space_editor:document settings.fixedBounds set value 1b',
        'data modify storage space_editor:document settings.boundsVersion set value 3',
    ])
    fn("internal/migrate_bounds_next", [
        'data modify storage space_editor:runtime migrateRegion set from storage space_editor:runtime migrateQueue[0]',
        'function space_editor:internal/migrate_bounds_one',
        'data remove storage space_editor:runtime migrateQueue[0]',
        'execute if data storage space_editor:runtime migrateQueue[0] run function space_editor:internal/migrate_bounds_next',
    ])
    migrate = []
    for axis in "xyz":
        for edge in (1, 2):
            migrate += [
                f'execute store result score #{axis}{edge} se.v run data get storage space_editor:runtime migrateRegion.{axis}{edge} 1000',
                f'scoreboard players set #negative se.v 0',
                f'execute if score #{axis}{edge} se.v matches ..-1 run scoreboard players set #negative se.v 1',
                f'scoreboard players operation #rounded se.v = #{axis}{edge} se.v',
                f'execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v',
                f'scoreboard players operation #rounded se.v += #50 se.v',
                f'scoreboard players operation #rounded se.v /= #100 se.v',
                f'scoreboard players operation #rounded se.v *= #100 se.v',
                f'execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v',
                f'scoreboard players operation #{axis}{edge} se.v = #rounded se.v',
            ]
        migrate += [
            f'scoreboard players operation #size{axis} se.v = #{axis}2 se.v',
            f'scoreboard players operation #size{axis} se.v -= #{axis}1 se.v',
            f'execute store result storage space_editor:runtime migrateRegion.{axis}1m int 1 run scoreboard players get #{axis}1 se.v',
            f'execute store result storage space_editor:runtime migrateRegion.{axis}2m int 1 run scoreboard players get #{axis}2 se.v',
            f'execute store result storage space_editor:runtime migrateRegion.s{axis}m int 1 run scoreboard players get #size{axis} se.v',
            f'execute store result storage space_editor:runtime migrateRegion.{axis}1 double 0.001 run scoreboard players get #{axis}1 se.v',
            f'execute store result storage space_editor:runtime migrateRegion.{axis}2 double 0.001 run scoreboard players get #{axis}2 se.v',
            f'execute store result storage space_editor:runtime migrateRegion.s{axis} double 0.001 run scoreboard players get #size{axis} se.v',
            f'execute store result storage space_editor:runtime migrateRegion.min[{"xyz".index(axis)}] double 0.001 run scoreboard players get #{axis}1 se.v',
            f'execute store result storage space_editor:runtime migrateRegion.maxExclusive[{"xyz".index(axis)}] double 0.001 run scoreboard players get #{axis}2 se.v',
        ]
    migrate += ['function space_editor:internal/store_migrated with storage space_editor:runtime migrateRegion']
    fn("internal/migrate_bounds_one", migrate)
    fn("internal/store_migrated", ['$data modify storage space_editor:document regions[{id:$(id)}] set from storage space_editor:runtime migrateRegion'])
    fn("tick", [
        "scoreboard players add @a se.cd 0",
        "scoreboard players remove @a[scores={se.cd=1..}] se.cd 1",
        "scoreboard players set #selection_cursor_active se.v 0",
        "execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"region\"}}] run function space_editor:selection/track",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"region\"}}] run function space_editor:input/region",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"resize_all\"}}] run function space_editor:input/resize_all",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"resize_face\"}}] run function space_editor:input/resize_face",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"move\"}}] run function space_editor:input/move",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"delete\"}}] run function space_editor:input/delete",
        "execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"region_visibility\"}}] run function space_editor:input/region_visibility",
        "scoreboard players set @a[scores={se.use=1..}] se.use 0",
        "execute unless score #selection_cursor_active se.v matches 1 run function space_editor:preview/remove_selection_candidate",
        "execute as @a[tag=space_editor.editing] at @s run function space_editor:internal/dimension_tick",
    ])
    fn("internal/dimension_tick", [
        "scoreboard players set #current_dim se.v 0",
        "execute if dimension minecraft:the_nether run scoreboard players set #current_dim se.v 1",
        "execute if dimension minecraft:the_end run scoreboard players set #current_dim se.v 2",
        "execute unless score @s se.dim = #current_dim se.v run function space_editor:preview/resync",
        "scoreboard players operation @s se.dim = #current_dim se.v",
    ])
    fn("start", [
        "execute unless entity @s[type=minecraft:player] run return 0",
        "tag @a remove space_editor.editing",
        "tag @s add space_editor.editing",
        "data modify storage space_editor:document editMode set value 1b",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"region\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"region\"}},minecraft:custom_name={text:\"範囲選択棒\",color:\"aqua\",italic:false},minecraft:lore=[{text:\"右クリック1回目=A / 2回目=B\",italic:false}] ]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"resize_all\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"resize_all\"}},minecraft:custom_name={text:\"全体サイズ変更棒\",color:\"yellow\",italic:false},minecraft:lore=[{text:\"右クリック=拡大 / Shift+右クリック=縮小\",italic:false}] ]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"resize_face\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"resize_face\"}},minecraft:custom_name={text:\"面伸縮棒\",color:\"gold\",italic:false},minecraft:lore=[{text:\"見ている1面を移動 / Shiftで逆方向\",italic:false}] ]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"move\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"move\"}},minecraft:custom_name={text:\"範囲移動棒\",color:\"green\",italic:false},minecraft:lore=[{text:\"見ている面方向へ1ブロック / Shiftで逆方向\",italic:false}] ]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"delete\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"delete\"}},minecraft:custom_name={text:\"削除棒\",color:\"red\",italic:false},minecraft:lore=[{text:\"特殊ブロック・Regionを削除 / Pasteプレビューをキャンセル\",italic:false}] ]",
        "execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:\"region_visibility\"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:\"region_visibility\"}},minecraft:custom_name={text:\"範囲表示切替棒\",color:\"light_purple\",italic:false},minecraft:lore=[{text:\"右クリック: 全Region枠・ラベル・Maskガイドを表示/非表示\",italic:false},{text:\"Mask本体には影響しません\",color:\"gray\",italic:false}]]",
        "function space_editor:preview/resync",
        message("編集モード。範囲棒を2回右クリックしてRegionを作成します。"),
    ])
    fn("play", [
        "tag @s remove space_editor.editing",
        "data modify storage space_editor:document editMode set value 0b",
        "function space_editor:preview/hide",
        message("プレイモード。Regionは保存したまま補助表示を隠しました。", "green"),
    ])
    fn("resume", ["function space_editor:start", message("保存Regionから表示を再同期しました。", "green")])
    fn("selection/clear", [
        "data remove storage space_editor:runtime selection",
        *dimensions("kill @e[tag=space_editor.point]"),
        message("一時Selectionをクリアしました。保存Regionは変更していません。"),
    ])
    fn("set_step", [
        '$data modify storage space_editor:runtime input set value {amount:$(amount)}',
        'execute store result score #step se.v run data get storage space_editor:runtime input.amount 1000',
        'execute unless score #step se.v matches 100..16000 run return run ' + message("増減量は0.1〜16です。", "red"),
        'scoreboard players operation #remainder se.v = #step se.v',
        'scoreboard players operation #remainder se.v %= #100 se.v',
        'execute unless score #remainder se.v matches 0 run return run ' + message("増減量は0.1単位で指定してください。", "red"),
        'execute store result storage space_editor:document settings.step double 0.001 run scoreboard players get #step se.v',
        'execute store result storage space_editor:document settings.stepMilli int 1 run scoreboard players get #step se.v',
        message("増減量を更新しました（0.1単位）。"),
    ])
    fn("status", [
        'tellraw @s [{text:"Document: ",color:"gold"},{nbt:"schemaVersion",storage:"space_editor:document"},{text:" / Regions="},{nbt:"regions",storage:"space_editor:document",interpret:false}]',
        'tellraw @s [{text:"Selection: ",color:"aqua"},{nbt:"selection",storage:"space_editor:runtime"}]',
        'tellraw @s [{text:"Selected: ",color:"yellow"},{nbt:"selectedId",storage:"space_editor:document"},{text:" / step="},{nbt:"settings.step",storage:"space_editor:document"}]',
    ])

    # While the Region wand is held, track a block hit up to three blocks away.
    # If nothing is hit, the block cell containing the point exactly three
    # blocks along the view ray becomes the candidate.  Clicking commits the
    # already-previewed candidate as A or B.
    fn("selection/track", [
        "scoreboard players set #selection_cursor_active se.v 1",
        "execute unless dimension minecraft:overworld in minecraft:overworld run kill @e[tag=space_editor.selection_candidate]",
        "execute unless dimension minecraft:the_nether in minecraft:the_nether run kill @e[tag=space_editor.selection_candidate]",
        "execute unless dimension minecraft:the_end in minecraft:the_end run kill @e[tag=space_editor.selection_candidate]",
        "data remove storage space_editor:runtime hover",
        "scoreboard players set #selection_ray se.v 0",
        "execute anchored eyes positioned ^ ^ ^ run function space_editor:internal/ray_selection",
    ])
    fn("internal/ray_selection", [
        "execute unless block ~ ~ ~ #space_editor:ray_pass run return run execute align xyz run function space_editor:selection/hover_capture",
        "execute if score #selection_ray se.v matches 30 run return run execute align xyz run function space_editor:selection/hover_capture",
        "scoreboard players add #selection_ray se.v 1",
        "execute positioned ^ ^ ^0.1 run return run function space_editor:internal/ray_selection",
    ])
    fn("selection/hover_capture", [
        "data modify storage space_editor:runtime hover set value {dimension:\"\",pos:[I;0,0,0],x:0,y:0,z:0}",
        'execute if dimension minecraft:overworld run data modify storage space_editor:runtime hover.dimension set value "minecraft:overworld"',
        'execute if dimension minecraft:the_nether run data modify storage space_editor:runtime hover.dimension set value "minecraft:the_nether"',
        'execute if dimension minecraft:the_end run data modify storage space_editor:runtime hover.dimension set value "minecraft:the_end"',
        'execute if data storage space_editor:runtime hover{dimension:""} run return run data remove storage space_editor:runtime hover',
        "kill @e[type=minecraft:marker,tag=space_editor.selection_capture]",
        "summon minecraft:marker ~ ~ ~ {Tags:[\"space_editor.selection_capture\"]}",
        *[f"execute store result storage space_editor:runtime hover.pos[{i}] int 1 run data get entity @e[type=minecraft:marker,tag=space_editor.selection_capture,limit=1,sort=nearest] Pos[{i}] 1" for i in range(3)],
        *[f"execute store result storage space_editor:runtime hover.{axis} int 1 run data get storage space_editor:runtime hover.pos[{i}] 1" for i, axis in enumerate("xyz")],
        "kill @e[type=minecraft:marker,tag=space_editor.selection_capture]",
        "function space_editor:preview/selection_candidate with storage space_editor:runtime hover",
    ])

    # Selection input: first click stores A; second click stores B and commits.
    fn("input/region", [
        "scoreboard players set @s se.cd 5",
        "execute unless data storage space_editor:runtime hover.pos run return run " + message("選択予定位置を取得できません。", "red"),
        "function space_editor:selection/capture",
    ])
    fn("selection/capture", [
        "data modify storage space_editor:runtime clickDimension set from storage space_editor:runtime hover.dimension",
        "data modify storage space_editor:runtime clickPos set from storage space_editor:runtime hover.pos",
        "execute unless data storage space_editor:runtime selection.a run return run function space_editor:selection/set_a",
        "function space_editor:selection/set_b",
    ])
    fn("selection/set_a", [
        "data modify storage space_editor:runtime selection set value {a:[I;0,0,0],ax:0,ay:0,az:0}",
        "data modify storage space_editor:runtime selection.dimension set from storage space_editor:runtime clickDimension",
        *[f"execute store result storage space_editor:runtime selection.a[{i}] int 1 run data get storage space_editor:runtime clickPos[{i}] 1" for i in range(3)],
        *[f"execute store result storage space_editor:runtime selection.a{axis} int 1 run data get storage space_editor:runtime clickPos[{i}] 1" for i, axis in enumerate("xyz")],
        "function space_editor:preview/point",
        message("Aを設定しました。次の右クリックでBを設定します。"),
    ])
    fn("selection/set_b", [
        "execute store success score #dim_changed se.v run data modify storage space_editor:runtime selection.dimension set from storage space_editor:runtime clickDimension",
        "execute if score #dim_changed se.v matches 1 run return run function space_editor:selection/dimension_error",
        "data modify storage space_editor:runtime selection.b set value [I;0,0,0]",
        *[f"execute store result storage space_editor:runtime selection.b[{i}] int 1 run data get storage space_editor:runtime clickPos[{i}] 1" for i in range(3)],
        "function space_editor:region/create",
    ])
    fn("selection/dimension_error", [
        "data remove storage space_editor:runtime selection",
        *dimensions("kill @e[tag=space_editor.point]"),
        message("AとBは同じディメンションで指定してください。Selectionをクリアしました。", "red"),
    ])

    # Normalize inclusive A/B into [min, maxExclusive), then persist a Region.
    create = ["scoreboard players set #valid se.v 1"]
    for i, axis in enumerate("xyz"):
        create += [
            f"execute store result score #a{axis} se.v run data get storage space_editor:runtime selection.a[{i}] 1",
            f"execute store result score #b{axis} se.v run data get storage space_editor:runtime selection.b[{i}] 1",
            f"scoreboard players operation #min{axis} se.v = #a{axis} se.v",
            f"scoreboard players operation #min{axis} se.v < #b{axis} se.v",
            f"scoreboard players operation #max{axis} se.v = #a{axis} se.v",
            f"scoreboard players operation #max{axis} se.v > #b{axis} se.v",
            f"scoreboard players add #max{axis} se.v 1",
            f"scoreboard players operation #size{axis} se.v = #max{axis} se.v",
            f"scoreboard players operation #size{axis} se.v -= #min{axis} se.v",
            f"execute unless score #size{axis} se.v matches 1..32 run scoreboard players set #valid se.v 0",
        ]
    create += [
        "execute unless score #valid se.v matches 1 run return run " + message("各辺は1〜32ブロックにしてください。", "red"),
        "execute store result score #next se.v run data get storage space_editor:document nextId 1",
        'data modify storage space_editor:runtime region set value {id:0,idText:"",dimension:"",min:[I;0,0,0],maxExclusive:[I;0,0,0],role:"generic",state:"committed",visible:1b}',
        "execute store result storage space_editor:runtime region.id int 1 run scoreboard players get #next se.v",
        '$data modify storage space_editor:runtime region.idText set value "region_$(id)"',
    ]
    # The idText macro above needs id in macro storage, so assign through a helper.
    create[-1] = "function space_editor:internal/set_region_id_text with storage space_editor:runtime region"
    create += ["data modify storage space_editor:runtime region.dimension set from storage space_editor:runtime selection.dimension"]
    for i, axis in enumerate("xyz"):
        create += [
            f"execute store result storage space_editor:runtime region.min[{i}] int 1 run scoreboard players get #min{axis} se.v",
            f"execute store result storage space_editor:runtime region.maxExclusive[{i}] int 1 run scoreboard players get #max{axis} se.v",
            f"execute store result storage space_editor:runtime region.{axis}1 int 1 run scoreboard players get #min{axis} se.v",
            f"execute store result storage space_editor:runtime region.{axis}2 int 1 run scoreboard players get #max{axis} se.v",
            f"execute store result storage space_editor:runtime region.s{axis} int 1 run scoreboard players get #size{axis} se.v",
            f"scoreboard players operation #{axis}1m se.v = #min{axis} se.v",
            f"scoreboard players operation #{axis}1m se.v *= #1000 se.v",
            f"scoreboard players operation #{axis}2m se.v = #max{axis} se.v",
            f"scoreboard players operation #{axis}2m se.v *= #1000 se.v",
            f"scoreboard players operation #s{axis}m se.v = #size{axis} se.v",
            f"scoreboard players operation #s{axis}m se.v *= #1000 se.v",
            f"execute store result storage space_editor:runtime region.{axis}1m int 1 run scoreboard players get #{axis}1m se.v",
            f"execute store result storage space_editor:runtime region.{axis}2m int 1 run scoreboard players get #{axis}2m se.v",
            f"execute store result storage space_editor:runtime region.s{axis}m int 1 run scoreboard players get #s{axis}m se.v",
        ]
    create += [
        "data modify storage space_editor:document regions append from storage space_editor:runtime region",
        "scoreboard players add #next se.v 1",
        "execute store result storage space_editor:document nextId int 1 run scoreboard players get #next se.v",
        "data remove storage space_editor:runtime selection",
        *dimensions("kill @e[tag=space_editor.point]"),
        "function space_editor:preview/resync",
        message("Regionを保存しました。続けて範囲棒で次のRegionを作れます。", "green"),
    ]
    fn("region/create", create)
    fn("internal/set_region_id_text", ['$data modify storage space_editor:runtime region.idText set value "region_$(id)"'])

    # Preview lifecycle. A single cube model supplies border and diagonal lines.
    fn("preview/hide", dimensions("kill @e[tag=space_editor.preview]"))
    fn("preview/resync", [
        "function space_editor:preview/hide",
        "execute unless data storage space_editor:document {editMode:1b} run return 0",
        "execute if data storage space_editor:document settings{regionsVisible:1b} run function space_editor:preview/render_regions",
        "execute if data storage space_editor:runtime selection.a run function space_editor:preview/point",
        "execute if data storage space_editor:document settings{regionsVisible:1b} if data storage space_editor:runtime hit.id run function space_editor:preview/highlight with storage space_editor:runtime hit",
    ])
    fn("preview/render_regions", [
        "data modify storage space_editor:runtime renderQueue set from storage space_editor:document regions",
        "execute if data storage space_editor:runtime renderQueue[0] run function space_editor:preview/next",
    ])
    fn("input/region_visibility", [
        "scoreboard players set @s se.cd 5",
        "execute if data storage space_editor:document settings{regionsVisible:1b} run return run function space_editor:region/display/hide",
        "function space_editor:region/display/show",
    ])
    fn("region/display/hide", [
        "data modify storage space_editor:document settings.regionsVisible set value 0b",
        *dimensions("kill @e[tag=space_editor.region]"),
        *dimensions("kill @e[tag=space_editor.label]"),
        *dimensions("kill @e[tag=space_editor.mask_guide]"),
        message("全Region枠・ラベル・Maskガイドを非表示にしました。Mask本体は残しています。", "yellow"),
    ])
    fn("region/display/show", [
        "data modify storage space_editor:document settings.regionsVisible set value 1b",
        "function space_editor:preview/resync",
        message("全Region枠・ラベル・Maskガイドを表示しました。", "green"),
    ])
    fn("preview/next", [
        "data modify storage space_editor:runtime renderRegion set from storage space_editor:runtime renderQueue[0]",
        "function space_editor:preview/prepare",
        "function space_editor:preview/spawn with storage space_editor:runtime renderRegion",
        "data remove storage space_editor:runtime renderQueue[0]",
        "execute if data storage space_editor:runtime renderQueue[0] run function space_editor:preview/next",
    ])
    prepare = []
    for axis in "xyz":
        prepare += [
            f"execute store result score #center_a se.v run data get storage space_editor:runtime renderRegion.{axis}1 10",
            f"execute store result score #center_b se.v run data get storage space_editor:runtime renderRegion.{axis}2 10",
            "scoreboard players operation #center_a se.v += #center_b se.v",
            "scoreboard players operation #center_a se.v /= #two se.v",
            f"execute store result storage space_editor:runtime renderRegion.c{axis} double 0.1 run scoreboard players get #center_a se.v",
        ]
    fn("preview/prepare", prepare)
    fn("preview/spawn", [
        '$execute in $(dimension) positioned $(x1) $(y1) $(z1) run summon minecraft:block_display ~ ~ ~ {Tags:["space_editor.preview","space_editor.region","space_editor.new"],block_state:{Name:"' + DISPLAY_BLOCKS["selection"] + '"},transformation:{translation:[-0.5f,0f,-0.5f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:3f,width:64f,height:64f}',
        '$execute in $(dimension) positioned $(cx) $(cy) $(cz) run summon minecraft:text_display ~ ~ ~ {Tags:["space_editor.preview","space_editor.label","space_editor.new"],text:\'{"text":"$(idText)\\n位置: ($(x1), $(y1), $(z1))\\nサイズ: $(sx) × $(sy) × $(sz)","color":"white"}\',billboard:"center",see_through:1b,shadow:1b,background:1073741824,alignment:"center",view_range:3f,width:64f,height:64f}',
        '$execute in $(dimension) run scoreboard players set @e[tag=space_editor.new] se.id $(id)',
        '$execute in $(dimension) run tag @e[tag=space_editor.new] remove space_editor.new',
    ])
    fn("preview/point", [
        "data modify storage space_editor:runtime point set from storage space_editor:runtime selection",
        "function space_editor:preview/spawn_point with storage space_editor:runtime point",
    ])
    fn("preview/spawn_point", [
        *dimensions("kill @e[tag=space_editor.point]"),
        '$execute in $(dimension) positioned $(ax) $(ay) $(az) run summon minecraft:block_display ~ ~ ~ {Tags:["space_editor.preview","space_editor.point"],block_state:{Name:"' + DISPLAY_BLOCKS["guide"] + '"},transformation:{translation:[-0.5f,0f,-0.5f],scale:[1f,1f,1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:2f,width:2f,height:2f}',
    ])
    fn("preview/selection_candidate", [
        '$execute in $(dimension) positioned $(x) $(y) $(z) positioned ~0.5 ~ ~0.5 if entity @e[type=minecraft:block_display,tag=space_editor.selection_candidate,distance=..0.001,limit=1] run return 0',
        '$execute in $(dimension) as @e[type=minecraft:block_display,tag=space_editor.selection_candidate,limit=1] run tp @s $(x) $(y) $(z)',
        '$execute in $(dimension) if entity @e[type=minecraft:block_display,tag=space_editor.selection_candidate,limit=1] run return 0',
        '$execute in $(dimension) positioned $(x) $(y) $(z) run summon minecraft:block_display ~ ~ ~ {Tags:["space_editor.preview","space_editor.selection_candidate"],block_state:{Name:"' + DISPLAY_BLOCKS["selectionCandidate"] + '"},transformation:{translation:[-0.5f,0f,-0.5f],scale:[1f,1f,1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:2f,width:2f,height:2f}',
    ])
    fn("preview/remove_selection_candidate", dimensions("kill @e[tag=space_editor.selection_candidate]"))
    fn("preview/highlight", ['$execute in $(dimension) as @e[tag=space_editor.region,scores={se.id=$(id)}] run data merge entity @s {block_state:{Name:"' + DISPLAY_BLOCKS["guide"] + '"}}'])

    # Ray-march through Region AABBs. The first sample hit wins; list order is
    # the deterministic tie breaker for equal hit distances.
    for tool in ("resize_all", "resize_face", "move"):
        fn(f"input/{tool}", [
            "scoreboard players set @s se.cd 5",
            f'data modify storage space_editor:runtime activeTool set value "{tool}"',
            "data remove storage space_editor:runtime hit",
            "scoreboard players set #region_ray se.v 0",
            "execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray",
        ])
    fn("input/delete", [
        "scoreboard players set @s se.cd 5",
        'data modify storage space_editor:runtime activeTool set value "delete"',
        "data remove storage space_editor:runtime hit",
        "scoreboard players set #region_ray se.v 0",
        "execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray",
    ])
    fn("region/ray", [
        "summon minecraft:marker ~ ~ ~ {Tags:[\"space_editor.ray_sample\"]}",
        "data modify storage space_editor:runtime rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_sample,limit=1,sort=nearest] Pos",
        "kill @e[type=minecraft:marker,tag=space_editor.ray_sample]",
        *[f"execute store result score #p{axis} se.v run data get storage space_editor:runtime rayPos[{i}] 1000" for i, axis in enumerate("xyz")],
        "data modify storage space_editor:runtime candidates set from storage space_editor:document regions",
        "execute if data storage space_editor:runtime candidates[0] run function space_editor:region/check_next",
        "execute if data storage space_editor:runtime hit run return run function space_editor:region/apply_hit",
        "scoreboard players add #region_ray se.v 1",
        "execute if score #region_ray se.v matches ..512 positioned ^ ^ ^0.025 run return run function space_editor:region/ray",
        message("視線上12.8ブロック以内にRegionがありません。", "red"),
    ])
    fn("region/check_next", [
        "data modify storage space_editor:runtime candidate set from storage space_editor:runtime candidates[0]",
        "function space_editor:region/check with storage space_editor:runtime candidate",
        "execute if data storage space_editor:runtime hit run return 0",
        "data remove storage space_editor:runtime candidates[0]",
        "execute if data storage space_editor:runtime candidates[0] run function space_editor:region/check_next",
    ])
    check = ['$execute unless dimension $(dimension) run return 0']
    for i, axis in enumerate("xyz"):
        check += [
            f"execute store result score #lo se.v run data get storage space_editor:runtime candidate.{axis}1m 1",
            f"execute store result score #hi se.v run data get storage space_editor:runtime candidate.{axis}2m 1",
            f"execute if score #p{axis} se.v < #lo se.v run return 0",
            f"execute if score #p{axis} se.v >= #hi se.v run return 0",
        ]
    check += [
        "data modify storage space_editor:runtime hit set from storage space_editor:runtime candidate",
        "function space_editor:region/face",
    ]
    fn("region/check", check)
    face = ["scoreboard players set #best se.v 2147483647", "scoreboard players set #face se.v 0"]
    face_defs = [(0, "x", 0, "min"), (1, "x", 0, "max"), (2, "y", 1, "min"), (3, "y", 1, "max"), (4, "z", 2, "min"), (5, "z", 2, "max")]
    for face_id, axis, idx, side in face_defs:
        face += [f"execute store result score #edge se.v run data get storage space_editor:runtime hit.{axis}{'1m' if side == 'min' else '2m'} 1"]
        if side == "min":
            face += [f"scoreboard players operation #dist se.v = #p{axis} se.v", "scoreboard players operation #dist se.v -= #edge se.v"]
        else:
            face += ["scoreboard players operation #dist se.v = #edge se.v", f"scoreboard players operation #dist se.v -= #p{axis} se.v"]
        face += [f"execute if score #dist se.v < #best se.v run scoreboard players set #face se.v {face_id}", "scoreboard players operation #best se.v < #dist se.v"]
    face += ["execute store result storage space_editor:runtime hitFace int 1 run scoreboard players get #face se.v"]
    fn("region/face", face)
    fn("region/apply_hit", [
        "data modify storage space_editor:document selectedId set from storage space_editor:runtime hit.idText",
        "execute if data storage space_editor:runtime {activeTool:\"delete\"} run return run function space_editor:region/delete_selected",
        "execute if data storage space_editor:runtime {activeTool:\"move\"} run return run function space_editor:region/move",
        "execute if data storage space_editor:runtime {activeTool:\"resize_all\"} run return run function space_editor:region/resize_all",
        "function space_editor:region/resize_face",
    ])

    # Resize using integer block steps. Shift reverses the direction. Bounds are
    # validated before the persistent list item is changed.
    fn("region/load_scores", [
        "execute store result score #id se.v run data get storage space_editor:runtime hit.id 1",
        "execute store result score #step se.v run data get storage space_editor:document settings.stepMilli 1",
        "scoreboard players set #direction se.v 1",
        'execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run scoreboard players set #direction se.v -1',
        "scoreboard players operation #delta se.v = #step se.v",
        "scoreboard players operation #delta se.v *= #direction se.v",
        *[f"execute store result score #{axis}{edge} se.v run data get storage space_editor:runtime hit.{axis}{edge}m 1" for axis in "xyz" for edge in (1, 2)],
    ])
    fn("region/resize_all", [
        "function space_editor:region/load_scores",
        *[line for axis in "xyz" for line in (
            f"scoreboard players operation #{axis}1 se.v -= #delta se.v",
            f"scoreboard players operation #{axis}2 se.v += #delta se.v",
            f"scoreboard players operation #size{axis} se.v = #{axis}2 se.v",
            f"scoreboard players operation #size{axis} se.v -= #{axis}1 se.v",
            f"execute unless score #size{axis} se.v matches 100..32000 run return run " + message("変更後の各辺は0.1〜32ブロックである必要があります。", "red"),
        )],
        "function space_editor:region/save_resize",
    ])
    face_lines = ["function space_editor:region/load_scores"]
    for face_id, axis, _, side in face_defs:
        op = "-=" if side == "min" else "+="
        face_lines += [f"execute if data storage space_editor:runtime {{hitFace:{face_id}}} run scoreboard players operation #{axis}{1 if side == 'min' else 2} se.v {op} #delta se.v"]
    for axis in "xyz":
        face_lines += [
            f"scoreboard players operation #size{axis} se.v = #{axis}2 se.v",
            f"scoreboard players operation #size{axis} se.v -= #{axis}1 se.v",
            f"execute unless score #size{axis} se.v matches 100..32000 run return run " + message("変更後の各辺は0.1〜32ブロックである必要があります。", "red"),
        ]
    face_lines += ["function space_editor:region/save_resize"]
    fn("region/resize_face", face_lines)
    move_lines = [
        "function space_editor:region/load_scores",
        "scoreboard players operation #delta se.v = #1000 se.v",
        "scoreboard players operation #delta se.v *= #direction se.v",
    ]
    for face_id, axis, _, side in face_defs:
        op = "-=" if side == "min" else "+="
        move_lines += [
            f"execute if data storage space_editor:runtime {{hitFace:{face_id}}} run scoreboard players operation #{axis}1 se.v {op} #delta se.v",
            f"execute if data storage space_editor:runtime {{hitFace:{face_id}}} run scoreboard players operation #{axis}2 se.v {op} #delta se.v",
        ]
    for axis in "xyz":
        move_lines += [
            f"scoreboard players operation #size{axis} se.v = #{axis}2 se.v",
            f"scoreboard players operation #size{axis} se.v -= #{axis}1 se.v",
        ]
    move_lines += ["function space_editor:region/save_resize"]
    fn("region/move", move_lines)
    save = []
    for i, axis in enumerate("xyz"):
        save += [
            f"execute store result storage space_editor:runtime hit.{axis}1m int 1 run scoreboard players get #{axis}1 se.v",
            f"execute store result storage space_editor:runtime hit.{axis}2m int 1 run scoreboard players get #{axis}2 se.v",
            f"execute store result storage space_editor:runtime hit.s{axis}m int 1 run scoreboard players get #size{axis} se.v",
            f"execute store result storage space_editor:runtime hit.{axis}1 double 0.001 run scoreboard players get #{axis}1 se.v",
            f"execute store result storage space_editor:runtime hit.{axis}2 double 0.001 run scoreboard players get #{axis}2 se.v",
            f"execute store result storage space_editor:runtime hit.min[{i}] double 0.001 run scoreboard players get #{axis}1 se.v",
            f"execute store result storage space_editor:runtime hit.maxExclusive[{i}] double 0.001 run scoreboard players get #{axis}2 se.v",
            f"execute store result storage space_editor:runtime hit.s{axis} double 0.001 run scoreboard players get #size{axis} se.v",
        ]
    save += [
        'execute if data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y1 se.v matches -64000..319999 run return run ' + message("Overworldの高さ範囲を超えています。", "red"),
        'execute if data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y2 se.v matches -63900..320000 run return run ' + message("Overworldの高さ範囲を超えています。", "red"),
        'execute unless data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y1 se.v matches 0..255999 run return run ' + message("Nether/Endの高さ範囲を超えています。", "red"),
        'execute unless data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y2 se.v matches 100..256000 run return run ' + message("Nether/Endの高さ範囲を超えています。", "red"),
        "function space_editor:region/store_hit with storage space_editor:runtime hit",
        "function space_editor:preview/resync",
        message("Regionを更新しました。", "green"),
    ]
    fn("region/save_resize", save)
    fn("region/store_hit", ['$data modify storage space_editor:document regions[{id:$(id)}] set from storage space_editor:runtime hit'])
    fn("region/delete_selected", [
        "execute unless data storage space_editor:runtime hit.id run return run " + message("先にサイズ変更棒でRegionを選択してください。", "red"),
        "function space_editor:region/delete_hit with storage space_editor:runtime hit",
        'data modify storage space_editor:document selectedId set value ""',
        "data remove storage space_editor:runtime hit",
        "function space_editor:preview/resync",
        message("選択Regionを削除しました。", "yellow"),
    ])
    fn("region/delete_hit", ['$data remove storage space_editor:document regions[{id:$(id)}]'])

    fn("menu", [
        message("開始: /function space_editor:start  プレイ: /function space_editor:play"),
        message("増減量: /function space_editor:set_step {amount:0.1}"),
        message("一時選択解除: /function space_editor:selection/clear  再同期: /function space_editor:resume"),
        message("範囲移動棒: 見ている面方向へ1ブロック移動。Shiftで反対方向。"),
    ])
    print(f"Generated stage-1 Space Editor: {len(list(F.rglob('*.mcfunction')))} functions")


if __name__ == "__main__":
    main()
