"""Generate stage-4 persistent Mask objects on top of Space Editor stage 3."""
from __future__ import annotations

import json
from pathlib import Path

import build_space_editor_stage3 as stage3

ROOT = Path(__file__).resolve().parents[1]
DP = ROOT / "space_editor_datapack"
F = DP / "data/space_editor/function"
DISPLAY_BLOCKS = stage3.stage2.stage1.BLOCK_CONFIG["displayBlocks"]
PALETTES = stage3.stage2.stage1.BLOCK_CONFIG["maskablePalettes"]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def fn(name: str, lines: list[str] | str) -> None:
    write(F / f"{name}.mcfunction", "\n".join(lines) if isinstance(lines, list) else lines)


def message(text: str, color: str = "aqua", target: str = "@s") -> str:
    return f"tellraw {target} " + json.dumps({"text": f"[Space Editor] {text}", "color": color}, ensure_ascii=False)


def dimensions(command: str) -> list[str]:
    return [f"execute in minecraft:{dimension} run {command}" for dimension in ("overworld", "the_nether", "the_end")]


def insert_before(path: Path, needle: str, additions: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    at = next(index for index, line in enumerate(lines) if needle in line)
    lines[at:at] = additions
    write(path, "\n".join(lines))


def append(path: Path, additions: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines.extend(additions)
    write(path, "\n".join(lines))


def main() -> None:
    stage3.main()

    # Additive schema migration. Masks reference Region IDs; their display
    # entities are disposable projections rebuilt from this persistent list.
    insert_before(F / "load.mcfunction", "execute if entity @a[tag=space_editor.editing]", [
        "execute unless data storage space_editor:document masks run data modify storage space_editor:document masks set value []",
        "execute unless data storage space_editor:document nextMaskId run data modify storage space_editor:document nextMaskId set value 1",
        "function space_editor:mask/rebuild_all",
    ])
    append(F / "load.mcfunction", [message("第4段階: Mask生成・編集・可視化を読み込みました。", target="@a")])

    insert_before(F / "tick.mcfunction", "scoreboard players set @a[scores={se.use=1..}]", [
        'execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"mask"}}] run function space_editor:input/mask',
    ])
    insert_before(F / "start.mcfunction", "function space_editor:preview/resync", [
        'execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"mask"}},minecraft:item_model="editor:tool_mask"] run clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"mask"}}]',
        'execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"mask"}}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={space_editor:{tool:"mask"}},minecraft:item_model="editor:tool_mask",minecraft:custom_name={text:"Mask棒",color:"light_purple",italic:false},minecraft:lore=[{text:"Regionを右クリック: Mask生成",italic:false},{text:"削除棒はMaskを先に削除",color:"gray",italic:false}]]',
    ])

    # Mask creation uses the existing Region ray/AABB selection flow.
    fn("input/mask", [
        "scoreboard players set @s se.cd 5",
        'data modify storage space_editor:runtime activeTool set value "mask_create"',
        "data remove storage space_editor:runtime hit",
        "scoreboard players set #region_ray se.v 0",
        "execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray",
    ])
    insert_before(F / "region/apply_hit.mcfunction", 'execute if data storage space_editor:runtime {activeTool:"delete"}', [
        'execute if data storage space_editor:runtime {activeTool:"mask_create"} run return run function space_editor:mask/create_selected',
        "scoreboard players set #mask_deleted se.v 0",
        'execute if data storage space_editor:runtime {activeTool:"delete"} store result score #mask_deleted se.v run function space_editor:mask/delete_attached with storage space_editor:runtime hit',
        "execute if score #mask_deleted se.v matches 1 run return 0",
    ])

    fn("mask/create_selected", [
        "execute unless data storage space_editor:runtime hit.id run return run " + message("Regionを取得できませんでした。", "red"),
        "function space_editor:mask/create_from_region with storage space_editor:runtime hit",
    ])
    fn("mask/create_from_region", [
        "data remove storage space_editor:runtime existingMask",
        '$data modify storage space_editor:runtime existingMask set from storage space_editor:document masks[{regionId:$(id)}]',
        "execute if data storage space_editor:runtime existingMask.id run return run " + message("このRegionにはすでにMaskがあります。", "yellow"),
        "execute store result score #mask_id se.v run data get storage space_editor:document nextMaskId 1",
        'data modify storage space_editor:runtime currentMask set value {id:0,idText:"",type:"mask",name:"",regionId:0,regionIdText:"",material:"mask_default",offset:[I;0,0,0],expand:[I;0,0,0],followsRegionResize:1b,visible:1b}',
        "execute store result storage space_editor:runtime currentMask.id int 1 run scoreboard players get #mask_id se.v",
        '$data modify storage space_editor:runtime currentMask.regionId set value $(id)',
        '$data modify storage space_editor:runtime currentMask.regionIdText set value "$(idText)"',
        "function space_editor:mask/set_id_text with storage space_editor:runtime currentMask",
        "data modify storage space_editor:document masks append from storage space_editor:runtime currentMask",
        "scoreboard players add #mask_id se.v 1",
        "execute store result storage space_editor:document nextMaskId int 1 run scoreboard players get #mask_id se.v",
        'data modify storage space_editor:runtime maskActionType set value "mask_create"',
        'data modify storage space_editor:runtime maskActionOperation set value "create"',
        "data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask",
        "function space_editor:mask/action_append",
        "function space_editor:mask/refresh",
        message("Maskを生成しました。Regionの変更へ自動追従します。", "green"),
    ])
    fn("mask/set_id_text", ['$data modify storage space_editor:runtime currentMask.idText set value "mask_$(id)"'])

    # Rebuild both the persistent, nearly invisible body and the edit-only guide.
    # The body is deliberately not tagged as a preview, so play mode keeps it.
    fn("mask/rebuild_all", [
        *dimensions("kill @e[type=minecraft:block_display,tag=space_editor.mask]"),
        "data modify storage space_editor:runtime maskQueue set from storage space_editor:document masks",
        "execute if data storage space_editor:runtime maskQueue[0] run function space_editor:mask/rebuild_next",
    ])
    fn("mask/refresh", [
        "execute unless data storage space_editor:document {editMode:1b} run return run function space_editor:mask/rebuild_all",
        "function space_editor:preview/resync",
    ])
    fn("mask/rebuild_next", [
        "data modify storage space_editor:runtime currentMask set from storage space_editor:runtime maskQueue[0]",
        "function space_editor:mask/prepare",
        "execute if score #mask_valid se.v matches 1 run function space_editor:mask/spawn with storage space_editor:runtime maskRender",
        "execute unless score #mask_region_found se.v matches 1 run function space_editor:mask/remove_orphan with storage space_editor:runtime currentMask",
        "data remove storage space_editor:runtime maskQueue[0]",
        "execute if data storage space_editor:runtime maskQueue[0] run function space_editor:mask/rebuild_next",
    ])
    fn("mask/load_region", [
        '$data modify storage space_editor:runtime maskRegion set from storage space_editor:document regions[{id:$(regionId)}]',
    ])
    prepare = [
        "scoreboard players set #mask_valid se.v 1",
        "scoreboard players set #mask_region_found se.v 0",
        "data remove storage space_editor:runtime maskRegion",
        "function space_editor:mask/load_region with storage space_editor:runtime currentMask",
        "execute if data storage space_editor:runtime maskRegion.id run scoreboard players set #mask_region_found se.v 1",
        "execute unless score #mask_region_found se.v matches 1 run return run scoreboard players set #mask_valid se.v 0",
        "data modify storage space_editor:runtime maskRender set from storage space_editor:runtime currentMask",
        "data modify storage space_editor:runtime maskRender.dimension set from storage space_editor:runtime maskRegion.dimension",
        "data modify storage space_editor:runtime maskRender.dim set from storage space_editor:runtime maskRegion.dimension",
        "data modify storage space_editor:runtime maskRender.pos set value [0.0d,0.0d,0.0d]",
        "data modify storage space_editor:runtime maskRender.scale set value [1.0f,1.0f,1.0f]",
    ]
    for index, axis in enumerate("xyz"):
        prepare += [
            f"data modify storage space_editor:runtime maskRender.{axis}1 set from storage space_editor:runtime maskRegion.{axis}1",
            f"execute store result score #mask_pos se.v run data get storage space_editor:runtime maskRegion.{axis}1m 1",
            f"execute store result score #mask_size se.v run data get storage space_editor:runtime maskRegion.s{axis}m 1",
            f"execute store result score #mask_offset se.v run data get storage space_editor:runtime currentMask.offset[{index}] 1",
            f"execute store result score #mask_expand se.v run data get storage space_editor:runtime currentMask.expand[{index}] 1",
            "scoreboard players operation #mask_pos se.v += #mask_offset se.v",
            "scoreboard players operation #mask_pos se.v -= #mask_expand se.v",
            "scoreboard players operation #mask_size se.v += #mask_expand se.v",
            "scoreboard players operation #mask_size se.v += #mask_expand se.v",
            "execute unless score #mask_size se.v matches 1..128000 run scoreboard players set #mask_valid se.v 0",
            f"execute store result storage space_editor:runtime maskRender.p{axis} double 0.001 run scoreboard players get #mask_pos se.v",
            f"execute store result storage space_editor:runtime maskRender.s{axis} double 0.001 run scoreboard players get #mask_size se.v",
            f"execute store result storage space_editor:runtime maskRender.pos[{index}] double 0.001 run scoreboard players get #mask_pos se.v",
            f"execute store result storage space_editor:runtime maskRender.scale[{index}] float 0.001 run scoreboard players get #mask_size se.v",
        ]
    fn("mask/prepare", prepare)
    fn("mask/spawn", [
        '$execute in $(dim) positioned 0.0 0.0 0.0 run summon minecraft:block_display ~$(px) ~$(py) ~$(pz) {Tags:["space_editor.mask","space_editor.mask_body","space_editor.mask_new"],block_state:{Name:"' + DISPLAY_BLOCKS["maskBody"] + '"},transformation:{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},view_range:4f,width:128f,height:128f}',
        '$execute in $(dim) run scoreboard players set @e[type=minecraft:block_display,tag=space_editor.mask_new] se.id $(id)',
        '$execute in $(dim) run tag @e[type=minecraft:block_display,tag=space_editor.mask_new] remove space_editor.mask_new',
        "execute if data storage space_editor:document {editMode:1b} if data storage space_editor:document settings{regionsVisible:1b} run function space_editor:mask/spawn_guide with storage space_editor:runtime maskRender",
    ])
    fn("mask/spawn_guide", [
        '$execute in $(dim) positioned 0.0 0.0 0.0 run summon minecraft:block_display ~$(px) ~$(py) ~$(pz) {Tags:["space_editor.preview","space_editor.mask_guide","space_editor.mask_guide_new"],block_state:{Name:"' + DISPLAY_BLOCKS["guide"] + '"},transformation:{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:3f,width:128f,height:128f}',
        '$execute in $(dim) run scoreboard players set @e[type=minecraft:block_display,tag=space_editor.mask_guide_new] se.id $(id)',
        '$execute in $(dim) run tag @e[type=minecraft:block_display,tag=space_editor.mask_guide_new] remove space_editor.mask_guide_new',
    ])
    fn("mask/remove_orphan", ['$data remove storage space_editor:document masks[{id:$(id)}]'])
    append(F / "preview/resync.mcfunction", ["function space_editor:mask/rebuild_all"])

    # Exact 1/1000 block corrections. Values are clamped to a useful ±16
    # range and expand is rejected if any resulting axis becomes non-positive.
    fn("mask/set_offset", [
        '$data modify storage space_editor:runtime maskEdit set value {id:$(id),values:[$(x),$(y),$(z)],fixed:[I;0,0,0]}',
        "function space_editor:mask/read_edit_values",
        "execute unless score #mask_input_valid se.v matches 1 run return run " + message("offsetは各軸-16〜16で指定してください。", "red"),
        "function space_editor:mask/load_edit_target with storage space_editor:runtime maskEdit",
        "execute unless data storage space_editor:runtime currentMask.id run return run " + message("Mask IDが見つかりません。", "red"),
        "data modify storage space_editor:runtime currentMask.offset set from storage space_editor:runtime maskEdit.fixed",
        "function space_editor:mask/commit_offset with storage space_editor:runtime currentMask",
        'data modify storage space_editor:runtime maskActionType set value "mask_update"',
        'data modify storage space_editor:runtime maskActionOperation set value "offset"',
        "data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask",
        "function space_editor:mask/action_append",
        "function space_editor:mask/refresh",
        message("Mask offsetを更新しました。", "green"),
    ])
    fn("mask/set_expand", [
        '$data modify storage space_editor:runtime maskEdit set value {id:$(id),values:[$(x),$(y),$(z)],fixed:[I;0,0,0]}',
        "function space_editor:mask/read_edit_values",
        "execute unless score #mask_input_valid se.v matches 1 run return run " + message("expandは各軸-16〜16で指定してください。", "red"),
        "function space_editor:mask/load_edit_target with storage space_editor:runtime maskEdit",
        "execute unless data storage space_editor:runtime currentMask.id run return run " + message("Mask IDが見つかりません。", "red"),
        "data modify storage space_editor:runtime currentMask.expand set from storage space_editor:runtime maskEdit.fixed",
        "function space_editor:mask/prepare",
        "execute unless score #mask_valid se.v matches 1 run return run " + message("expand後の各辺は0より大きく128以下にしてください。", "red"),
        "function space_editor:mask/commit_expand with storage space_editor:runtime currentMask",
        'data modify storage space_editor:runtime maskActionType set value "mask_update"',
        'data modify storage space_editor:runtime maskActionOperation set value "expand"',
        "data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask",
        "function space_editor:mask/action_append",
        "function space_editor:mask/refresh",
        message("Mask expandを更新しました。", "green"),
    ])
    fn("mask/read_edit_values", [
        "scoreboard players set #mask_input_valid se.v 1",
        *[line for index, axis in enumerate("xyz") for line in (
            f"execute store result score #mask_input_{axis} se.v run data get storage space_editor:runtime maskEdit.values[{index}] 1000",
            f"execute unless score #mask_input_{axis} se.v matches -16000..16000 run scoreboard players set #mask_input_valid se.v 0",
            f"execute store result storage space_editor:runtime maskEdit.fixed[{index}] int 1 run scoreboard players get #mask_input_{axis} se.v",
        )],
    ])
    fn("mask/load_edit_target", [
        "data remove storage space_editor:runtime currentMask",
        '$data modify storage space_editor:runtime currentMask set from storage space_editor:document masks[{id:$(id)}]',
    ])
    fn("mask/commit_offset", ['$data modify storage space_editor:document masks[{id:$(id)}].offset set from storage space_editor:runtime currentMask.offset'])
    fn("mask/commit_expand", ['$data modify storage space_editor:document masks[{id:$(id)}].expand set from storage space_editor:runtime currentMask.expand'])
    fn("mask/rename", [
        '$data modify storage space_editor:runtime maskEdit set value {id:$(id),name:"$(name)"}',
        "function space_editor:mask/load_edit_target with storage space_editor:runtime maskEdit",
        "execute unless data storage space_editor:runtime currentMask.id run return run " + message("Mask IDが見つかりません。", "red"),
        '$data modify storage space_editor:runtime currentMask.name set value "$(name)"',
        "function space_editor:mask/commit_name with storage space_editor:runtime currentMask",
        'data modify storage space_editor:runtime maskActionType set value "mask_update"',
        'data modify storage space_editor:runtime maskActionOperation set value "rename"',
        "data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask",
        "function space_editor:mask/action_append",
        message("Mask名を更新しました。", "green"),
    ])
    fn("mask/commit_name", ['$data modify storage space_editor:document masks[{id:$(id)}].name set from storage space_editor:runtime currentMask.name'])

    fn("mask/delete", [
        '$data modify storage space_editor:runtime maskEdit set value {id:$(id)}',
        "function space_editor:mask/load_edit_target with storage space_editor:runtime maskEdit",
        "execute unless data storage space_editor:runtime currentMask.id run return run " + message("Mask IDが見つかりません。", "red"),
        "function space_editor:mask/delete_loaded",
    ])
    fn("mask/delete_attached", [
        "data remove storage space_editor:runtime currentMask",
        '$data modify storage space_editor:runtime currentMask set from storage space_editor:document masks[{regionId:$(id)}]',
        "execute unless data storage space_editor:runtime currentMask.id run return 0",
        "function space_editor:mask/delete_loaded",
        "return 1",
    ])
    fn("mask/delete_loaded", [
        'data modify storage space_editor:runtime maskActionType set value "mask_delete"',
        'data modify storage space_editor:runtime maskActionOperation set value "delete"',
        "data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask",
        "function space_editor:mask/action_append",
        "function space_editor:mask/remove_loaded with storage space_editor:runtime currentMask",
        "function space_editor:mask/refresh",
        message("Maskを削除しました。Regionは残しています。", "yellow"),
    ])
    fn("mask/remove_loaded", ['$data remove storage space_editor:document masks[{id:$(id)}]'])

    # Semantic actions retain a full Mask snapshot for later undo/replay work.
    fn("mask/action_append", [
        "execute store result score #action se.v run data get storage space_editor:document nextActionId 1",
        'data modify storage space_editor:runtime maskAction set value {id:0,type:"",operation:"",mask:{},order:0}',
        "execute store result storage space_editor:runtime maskAction.id int 1 run scoreboard players get #action se.v",
        "execute store result storage space_editor:runtime maskAction.order int 1 run scoreboard players get #action se.v",
        "data modify storage space_editor:runtime maskAction.type set from storage space_editor:runtime maskActionType",
        "data modify storage space_editor:runtime maskAction.operation set from storage space_editor:runtime maskActionOperation",
        "data modify storage space_editor:runtime maskAction.mask set from storage space_editor:runtime maskActionRecord",
        "data modify storage space_editor:document actions append from storage space_editor:runtime maskAction",
        "scoreboard players add #action se.v 1",
        "execute store result storage space_editor:document nextActionId int 1 run scoreboard players get #action se.v",
    ])
    fn("mask/record_region_sync", [
        "data remove storage space_editor:runtime currentMask",
        '$data modify storage space_editor:runtime currentMask set from storage space_editor:document masks[{regionId:$(id)}]',
        "execute unless data storage space_editor:runtime currentMask.id run return 0",
        'data modify storage space_editor:runtime maskActionType set value "mask_update"',
        'data modify storage space_editor:runtime maskActionOperation set value "region_sync"',
        "data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask",
        "function space_editor:mask/action_append",
    ])
    insert_before(F / "region/save_resize.mcfunction", "function space_editor:preview/resync", [
        "function space_editor:mask/record_region_sync with storage space_editor:runtime hit",
    ])

    # Convenient target-material items for Stage-2 Fill. The custom data keeps
    # the logical palette name even though placement uses the configured carrier.
    for name, palette in PALETTES.items():
        fn(f"mask/give_target_{name}", [
            f'give @s {palette["carrierBlock"]}[minecraft:custom_data={{space_editor:{{maskable:"{name}"}}}},minecraft:custom_name={{text:"Mask対象: {name}",color:"light_purple",italic:false}}]',
            message(f"Mask対象素材 {name} を渡しました。Fill棒のオフハンドで使用できます。", "green"),
        ])
    fn("mask/help", [
        message("Mask棒でRegionを右クリックするとMaskを生成します。"),
        message("補正: /function space_editor:mask/set_offset {id:1,x:0,y:0,z:-0.01}"),
        message("拡張: /function space_editor:mask/set_expand {id:1,x:0.1,y:0,z:0}"),
        message('名前: /function space_editor:mask/rename {id:1,name:"entrance"}'),
        message("削除棒は同じRegionのMaskを先に削除し、次のクリックでRegionを削除します。"),
        message("Mask対象素材: /function space_editor:mask/give_target_stone など。Fill棒のオフハンドで使用します。"),
        message("実体確認: /function space_editor:mask/debug/show（解除は debug/hide）"),
    ])
    fn("mask/debug/show", [
        *dimensions('execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:1b,glow_color_override:16711935,view_range:16f}'),
        message("Mask本体を発光輪郭・view_range 16で表示します。テクスチャとMask方式は変更しません。", "yellow"),
    ])
    fn("mask/debug/hide", [
        *dimensions('execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:0b,view_range:4f}'),
        *dimensions('execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data remove entity @s glow_color_override'),
        message("Mask本体のデバッグ表示を解除しました。", "green"),
    ])
    fn("mask/debug/status", [
        'tellraw @s [{text:"Document Masks: ",color:"light_purple"},{nbt:"masks",storage:"space_editor:document",interpret:false}]',
        'execute unless entity @e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1] run ' + message("現在のdimensionにMask本体がありません。", "red"),
        'execute if entity @e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1] run tellraw @s [{text:"Mask body: ",color:"light_purple"},{text:"block="},{nbt:"block_state.Name",entity:"@e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1]"},{text:", pos="},{nbt:"Pos",entity:"@e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1]"},{text:", scale="},{nbt:"transformation.scale",entity:"@e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1]"},{text:", view_range="},{nbt:"view_range",entity:"@e[type=minecraft:block_display,tag=space_editor.mask_body,limit=1]"}]',
    ])
    append(F / "menu.mcfunction", [message("Mask: Mask棒でRegionを右クリック / 詳細: /function space_editor:mask/help")])
    append(F / "status.mcfunction", [
        'tellraw @s [{text:"Masks: ",color:"light_purple"},{nbt:"masks",storage:"space_editor:document",interpret:false}]',
    ])

    print(f"Generated stage-4 Space Editor: {len(list(F.rglob('*.mcfunction')))} functions")


if __name__ == "__main__":
    main()
