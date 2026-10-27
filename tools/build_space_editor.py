"""Build Space Editor and apply its rendering assets to the live resource pack.

The generated mcfunctions are intentionally plain text: game-side state and
failure recovery can be inspected without running this generator. No world is
opened or modified by the build.
"""
from __future__ import annotations

import json
import base64
import hashlib
from pathlib import Path
import re
import shutil
import sys
import zipfile

from editor_block_config import EditorBlockConfigError, blockstate_relative_path, load_editor_block_config, resource_path

ROOT = Path(__file__).resolve().parents[1]
DP = ROOT / "space_editor_datapack"
RP = ROOT / "space_editor_resources"
F = DP / "data/editor/function"
try:
    BLOCK_CONFIG = load_editor_block_config()
except EditorBlockConfigError as error:
    raise SystemExit(f"Error: {error}") from None
DISPLAY_BLOCKS = BLOCK_CONFIG["displayBlocks"]
COLLISION_CARRIERS = BLOCK_CONFIG["collisionCarriers"]
PALETTES = {
    name: (palette["normalBlock"], palette["carrierBlock"], palette["sourceTexture"])
    for name, palette in BLOCK_CONFIG["maskablePalettes"].items()
}
MANIFEST = ROOT / "space_editor_generated_manifest.json"


def write(path: Path, value: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")


def js(path: Path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2))


def fn(name: str, body: str | list[str]):
    write(F / (name + ".mcfunction"), "\n".join(body) if isinstance(body, list) else body)


def msg(text: str, color="aqua", target="@s"):
    return "tellraw " + target + " " + json.dumps({"text": "[Space Editor] " + text, "color": color}, ensure_ascii=False)


def button(label: str, command: str, color="aqua", hint="クリックして実行"):
    return {"text": " [" + label + "] ", "color": color,
            "click_event": {"action": "run_command", "command": "/function editor:" + command},
            "hover_event": {"action": "show_text", "value": hint}}


def row(*components):
    return "tellraw @s " + json.dumps(list(components), ensure_ascii=False)


def guard(selection=False):
    lines = ["execute unless score #enabled se = #one se run return 0",
             'execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}']
    if selection:
        lines += ['execute unless data storage editor:data selection.valid run return run tellraw @s {"text":"先にA/Bの2点を選択してください。","color":"red"}']
    return lines


def main():
    desired_blockstates = managed_blockstates()
    _validate_blockstate_destinations(ROOT, desired_blockstates, allow_original_capture=True)
    _validate_blockstate_destinations(RP, desired_blockstates, allow_original_capture=False)
    js(DP / "pack.mcmeta", {"pack": {"description": "Space Editor 1.0 | Java 26.1", "min_format": [101, 1], "max_format": [101, 1]}})
    js(RP / "pack.mcmeta", {"pack": {"description": "Space Editor 1.0 | Mask + Selection", "min_format": 84, "max_format": 84}})
    js(DP / "data/minecraft/tags/function/load.json", {"values": ["editor:load"]})
    js(DP / "data/minecraft/tags/function/tick.json", {"values": ["editor:tick"]})
    js(DP / "data/editor/tags/block/ray_pass.json", {"values": ["minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:water", "minecraft:light", "minecraft:structure_void"]})
    palette = {name: {"normal": normal, "maskable": masked} for name, (normal, masked, _) in PALETTES.items()}
    palette["air"] = {"normal": "minecraft:air", "maskable": "minecraft:air"}
    fn("load", [
        "scoreboard objectives add se dummy", "scoreboard objectives add se.use minecraft.used:minecraft.carrot_on_a_stick",
        "scoreboard objectives add se.cd dummy", "scoreboard objectives add se.id dummy",
        "scoreboard objectives add se.gen dummy", "scoreboard players add #epoch se.gen 0",
        "scoreboard players set #one se 1", "scoreboard players set #16 se 16", "scoreboard players set #1000 se 1000",
        "scoreboard players add #preview_version se 0", "scoreboard players set #clock se 0",
        "scoreboard players set #enabled se 0",
        "execute unless data storage editor:data document run function editor:internal/init",
        "execute if data storage editor:data document{schema:1} run scoreboard players set #enabled se 1",
        "execute unless score #enabled se matches 1 run return run tellraw @a {text:\"Space Editor: 未対応の保存形式です。データは変更していません。\",color:\"red\"}",
        # A persisted worker owns these force-load tickets; a reload resumes it.
        "execute unless data storage editor:data prefs run function editor:settings/reset",
        "execute if data storage editor:runtime job run data modify storage editor:runtime job.wait set value 0",
        msg("準備完了。/function editor:menu で開始", target="@a")])
    fn("internal/init", [
        'data modify storage editor:data document set value {schema:1,name:"Untitled",objects:[],palettes:' + json.dumps(palette, separators=(",", ":")) + '}',
        'data modify storage editor:data next_id set value 1',
        'data modify storage editor:data revision set value 0',
        'data modify storage editor:data footprints set value []',
        'data modify storage editor:data history set value {past:[],future:[]}',
        'data modify storage editor:data build_state set value "clean"',
        'data modify storage editor:data guides set value 1b',
        'function editor:settings/reset'])
    fn("settings/reset", ['data modify storage editor:data prefs set value {palette:"stone",variant:"normal",ox:0,oy:0,oz:0,ex:0,ey:0,ez:0}', msg("素材=stone / normal、補正=0 に戻しました。")])
    fn("tick", [
        "execute unless score #enabled se matches 1 run return 0",
        *[f'execute in minecraft:{d} as @e[tag=editor.object] unless score @s se.gen = #epoch se.gen run kill @s' for d in ("overworld", "the_nether", "the_end")],
        "execute if data storage editor:runtime job run function editor:internal/job/tick",
        "scoreboard players add #clock se 1",
        "execute if score #clock se matches 20.. run function editor:internal/preview_sync",
        "scoreboard players add @a se.cd 0", "scoreboard players remove @a[scores={se.cd=1..}] se.cd 1",
        "execute as @a[scores={se.use=1..},tag=editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{editor_wand:1b}] run function editor:internal/wand",
        "scoreboard players set @a[scores={se.use=1..}] se.use 0",
        'execute unless data storage editor:runtime job unless data storage editor:data {build_state:"error"} run function editor:internal/teleport/tick'])
    fn("menu", [
        row({"text": "━━ Space Editor ━━", "color": "gold"}, button("編集開始・棒を入手", "start"), button("プレイ", "play", "green")),
        row(button("A:視線", "selection/a"), button("B:視線", "selection/b"), button("A:足元", "selection/a_here"), button("B:足元", "selection/b_here"), button("選択解除", "selection/clear", "gray")),
        row(button("素材", "palette/menu"), button("埋める", "block/place", "green"), button("空洞の箱", "block/hollow", "green"), button("外殻のみ", "block/outline", "green"), button("空気で消去", "block/erase", "red")),
        row(button("Mask生成", "mask/create", "light_purple"), button("TP範囲登録", "teleport/create", "yellow"), button("補正設定", "settings/menu")),
        row(button("Undo", "history/undo", "yellow"), button("Redo", "history/redo", "yellow"), button("選択移動", "selection/menu"), button("登録一覧", "objects/list"), button("ガイド切替", "preview/toggle")),
        row(button("再構築", "build", "gold"), button("状態", "status"), button("書き出し", "export"), button("ヘルプ", "help", "gray")),
        row({"text": "素材: ", "color": "gray"}, {"nbt": "prefs.palette", "storage": "editor:data"}, {"text": " / "}, {"nbt": "prefs.variant", "storage": "editor:data"})])
    fn("start", guard() + ['execute unless entity @s[type=minecraft:player] run return 0',
        'tag @a remove editor.editing', 'tag @s add editor.editing',
        'execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{editor_wand:1b}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={editor_wand:1b},minecraft:custom_name={text:"Space Editor — 選択棒",color:"aqua",italic:false},minecraft:lore=[{text:"右クリック: A / しゃがみ+右クリック: B",italic:false},{text:"/function editor:menu で配置メニュー",italic:false}]]',
        'function editor:preview/show', msg("右クリック=A、しゃがみ+右クリック=B。選択後は /function editor:menu。編集者はTP判定から除外されます。")])
    fn("play", ['tag @s remove editor.editing', 'function editor:preview/hide', msg("プレイ確認モード。TPが有効になります。編集に戻る: /function editor:start")])
    fn("help", [msg("1. start → 選択棒でA/B → menuで素材・配置。棒は12.8ブロック先まで選択。"),
        msg("2. 1回の選択は各辺32以下。負座標・通常3ディメンション対応。"),
        msg("3. 補正はMask/TP用。Blockは整数範囲のまま配置。空気で消す操作も記録します。"),
        msg("4. 一覧の削除・選択・TP接続をクリック。Undo/Redoは20手まで。"),
        msg("5. 再構築は履歴の配置跡を空気に戻し、現在のデータを順番に再生。天然地形の復元はしません。", "yellow"),
        msg("6. 書き出しはログに1件ずつ表示。付属Pythonでワールド保存データから完全JSONも取得できます。")])
    fn("status", [
        'execute if data storage editor:runtime job store result storage editor:runtime remaining int 1 run data get storage editor:runtime job.queue',
        row({"text": "状態: ", "color": "gold"}, {"nbt": "build_state", "storage": "editor:data"}, {"text": " / revision="}, {"nbt": "revision", "storage": "editor:data"}),
        'execute if data storage editor:runtime job run '+row({"text":"残り処理数: ","color":"yellow"},{"nbt":"remaining","storage":"editor:runtime"},{"text":" / "},{"nbt":"work.dim","storage":"editor:runtime"},{"text":" / "},{"nbt":"job.phase","storage":"editor:runtime"}),
        row({"text": "Selection: ", "color": "aqua"}, {"nbt": "selection", "storage": "editor:data"}),
        row({"text": "設定: ", "color": "gray"}, {"nbt": "prefs", "storage": "editor:data"}),
        row(button("停止後に再開", "build/resume", "yellow"), button("メニュー", "menu"))])

    # Input adapters terminate at capture/normalize; renderer never raycasts.
    fn("internal/wand", ['execute if data storage editor:runtime job run return 0',
        'execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run return run function editor:selection/b',
        'function editor:selection/a'])
    for point in "ab":
        fn("selection/" + point, guard() + [f'data modify storage editor:runtime point set value "{point}"', 'scoreboard players set #ray se 0',
            'execute anchored eyes positioned ^ ^ ^ run function editor:internal/ray'])
        fn("selection/" + point + "_here", guard() + [f'data modify storage editor:runtime point set value "{point}"',
            'execute align xyz run function editor:internal/capture'])
    fn("internal/ray", [
        'execute unless block ~ ~ ~ #editor:ray_pass run return run execute align xyz run function editor:internal/capture',
        'scoreboard players add #ray se 1',
        'execute if score #ray se matches ..128 positioned ^ ^ ^0.1 run return run function editor:internal/ray',
        msg("12.8ブロック以内に対象がありません。足元指定や座標指定も使えます。", "yellow")])
    fn("internal/capture", [
        'data remove storage editor:runtime dim',
        *[f'execute if dimension minecraft:{d} run data modify storage editor:runtime dim set value "minecraft:{d}"' for d in ("overworld", "the_nether", "the_end")],
        'execute unless data storage editor:runtime dim run return run tellraw @s {text:"この版は通常の3ディメンションに対応しています。",color:"red"}',
        # Compare with a scratch copy: data modify returns success only on change.
        'data modify storage editor:runtime old_dim set from storage editor:data selection.dim',
        'execute store success score #changed se run data modify storage editor:runtime old_dim set from storage editor:runtime dim',
        'execute if score #changed se matches 1 run data remove storage editor:data selection',
        'data modify storage editor:data selection.dim set from storage editor:runtime dim',
        'kill @e[type=minecraft:marker,tag=editor.capture]',
        'summon minecraft:marker ~ ~ ~ {Tags:["editor.capture"]}',
        'data modify storage editor:runtime pos set from entity @e[type=minecraft:marker,tag=editor.capture,limit=1] Pos',
        'kill @e[type=minecraft:marker,tag=editor.capture]',
        'function editor:internal/capture_point with storage editor:runtime',
        'function editor:internal/selection/normalize'])
    fn("internal/capture_point", [f'$execute store result storage editor:data selection.$(point){axis} int 1 run data get storage editor:runtime pos[{i}] 1' for i, axis in enumerate("xyz")])
    fn("selection/set", guard() + [
        '$data modify storage editor:data selection set value {ax:$(ax),ay:$(ay),az:$(az),bx:$(bx),by:$(by),bz:$(bz),dim:"$(dimension)"}',
        'function editor:internal/selection/normalize'])
    lines = ['data remove storage editor:data selection.valid', 'function editor:internal/selection/kill']
    for p in "ab":
        for a in "xyz":
            lines += [f'execute unless data storage editor:data selection.{p}{a} run return 0', f'execute store result score #{p}{a} se run data get storage editor:data selection.{p}{a} 1',
                      f'execute store result storage editor:data selection.{p}{a} int 1 run scoreboard players get #{p}{a} se']
    lines += ['scoreboard players set #dim_ok se 0']
    for d in ("overworld", "the_nether", "the_end"):
        lines += [f'execute if data storage editor:data selection{{dim:"minecraft:{d}"}} run scoreboard players set #dim_ok se 1']
    lines += ['execute unless score #dim_ok se matches 1 run return run tellraw @s {text:"未対応ディメンションです。",color:"red"}', 'scoreboard players set #volume se 1']
    for a in "xyz":
        lines += [f'scoreboard players operation #{a}1 se = #a{a} se', f'scoreboard players operation #{a}1 se < #b{a} se',
                  f'scoreboard players operation #{a}2 se = #a{a} se', f'scoreboard players operation #{a}2 se > #b{a} se',
                  f'execute unless score #{a}1 se matches -1000000..1000000 run return run tellraw @s {{text:"座標は±1000000以内にしてください。",color:"red"}}',
                  f'execute unless score #{a}2 se matches -1000000..1000000 run return run tellraw @s {{text:"座標は±1000000以内にしてください。",color:"red"}}',
                  f'scoreboard players operation #s{a} se = #{a}2 se', f'scoreboard players operation #s{a} se -= #{a}1 se', f'scoreboard players add #s{a} se 1',
                  f'execute unless score #s{a} se matches 1..32 run return run tellraw @s {{text:"1回の選択は各辺1〜32ブロックです。",color:"red"}}']
        for field in (a + "1", a + "2", "s" + a):
            lines += [f'execute store result storage editor:data selection.{field} int 1 run scoreboard players get #{field} se']
    lines += ['execute unless score #y1 se matches -64..319 run return run tellraw @s {text:"高さが範囲外です。",color:"red"}',
              'execute unless score #y2 se matches -64..319 run return run tellraw @s {text:"高さが範囲外です。",color:"red"}',
              'execute unless data storage editor:data selection{dim:"minecraft:overworld"} unless score #y1 se matches 0..255 run return run tellraw @s {text:"ネザー/エンドの高さは0〜255です。",color:"red"}',
              'execute unless data storage editor:data selection{dim:"minecraft:overworld"} unless score #y2 se matches 0..255 run return run tellraw @s {text:"ネザー/エンドの高さは0〜255です。",color:"red"}',
              'data modify storage editor:data selection.valid set value 1b',
              'function editor:internal/selection/preview', msg("Selectionを更新しました。/function editor:menu から配置できます。")]
    fn("internal/selection/normalize", lines)
    fn("selection/clear", guard() + ['data remove storage editor:data selection', 'function editor:internal/selection/kill', msg("Selectionを解除しました。")])
    fn("selection/move", guard(True) + ['$data modify storage editor:runtime delta set value {x:$(x),y:$(y),z:$(z)}',
        *[f'execute store result score #d{a} se run data get storage editor:runtime delta.{a} 1' for a in "xyz"],
        *[f'execute unless score #d{a} se matches -32..32 run return 0' for a in "xyz"],
        *[line for p in "ab" for a in "xyz" for line in (
            f'execute store result score #coord se run data get storage editor:data selection.{p}{a}',
            f'scoreboard players operation #coord se += #d{a} se',
            f'execute store result storage editor:data selection.{p}{a} int 1 run scoreboard players get #coord se')],
        'function editor:internal/selection/normalize'])
    fn("selection/menu", [row(*[button(label, "selection/"+name) for label,name in (("西 -X","west"),("東 +X","east"),("北 -Z","north"),("南 +Z","south"),("上 +Y","up"),("下 -Y","down"))]),
        msg("選択範囲だけを1ブロック移動します。配置済みオブジェクトは動かしません。"),
        row({"text":"任意移動: /function editor:selection/move {x:1,y:0,z:0}","color":"aqua","click_event":{"action":"suggest_command","command":"/function editor:selection/move {x:1,y:0,z:0}"}})])
    for name, delta in (("west",(-1,0,0)),("east",(1,0,0)),("north",(0,0,-1)),("south",(0,0,1)),("up",(0,1,0)),("down",(0,-1,0))):
        fn("selection/"+name, [f'function editor:selection/move {{x:{delta[0]},y:{delta[1]},z:{delta[2]}}}'])
    fn("internal/selection/kill", ['scoreboard players add #preview_version se 1', *[f'execute in minecraft:{d} run kill @e[type=minecraft:block_display,tag=editor.selection]' for d in ("overworld", "the_nether", "the_end")]])
    fn("internal/selection/preview", ['function editor:internal/selection/kill',
        'execute unless data storage editor:data selection.valid run return 0',
        'execute if data storage editor:data {guides:0b} run return 0',
        'function editor:internal/selection/spawn with storage editor:data selection'])
    fn("internal/selection/spawn", [f'$execute in $(dim) positioned $(x1) $(y1) $(z1) align xyz run summon minecraft:block_display ~ ~ ~ {{Tags:["editor.selection"],block_state:{{Name:"{DISPLAY_BLOCKS["selection"]}"}},transformation:{{translation:[-0.003f,-0.003f,-0.003f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}},brightness:{{block:15,sky:15}},view_range:2f,width:64f,height:64f}}',
        '$execute in $(dim) run scoreboard players operation @e[tag=editor.selection] se.id = #preview_version se'])
    fn("internal/preview_sync", ['scoreboard players set #clock se 0',
        *[f'execute in minecraft:{d} as @e[tag=editor.selection] unless score @s se.id = #preview_version se run kill @s' for d in ("overworld", "the_nether", "the_end")],
        *[f'execute in minecraft:{d} if data storage editor:data {{guides:{value}b}} as @e[tag=editor.guide] run data merge entity @s {{view_range:{view}f}}' for d in ("overworld", "the_nether", "the_end") for value,view in ((0,0),(1,2))]])

    fn("palette/menu", [row(*[button(n, "palette/" + n) for n in PALETTES]), row(button("通常", "palette/normal", "white"), button("Mask対象", "palette/maskable", "light_purple")), msg("素材と通常/Mask対象を選んだ後、メニューのブロック配置を実行してください。")])
    for name in PALETTES:
        fn("palette/" + name, [f'data modify storage editor:data prefs.palette set value "{name}"', msg("素材: " + name)])
    for variant in ("normal", "maskable"):
        fn("palette/" + variant, [f'data modify storage editor:data prefs.variant set value "{variant}"', msg("種類: " + variant)])
    for name, prefix in (("offset", "o"), ("expand", "e")):
        fn("settings/" + name, [f'$data modify storage editor:runtime input set value {{x:$(x),y:$(y),z:$(z)}}', *[
            f'execute store result score #i{a} se run data get storage editor:runtime input.{a} 1000' for a in "xyz"],
            *[f'execute unless score #i{a} se matches -16000..16000 run return run tellraw @s {{text:"補正値は±16以内です。",color:"red"}}' for a in "xyz"],
            *[f'execute store result storage editor:data prefs.{prefix}{a} int 1 run scoreboard players get #i{a} se' for a in "xyz"], msg(name + "を設定しました（1/1000ブロック精度）。")])
    fn("settings/menu", [msg("補正はMask/TPの生成時に保存されます。expandは両端それぞれの増分、負数で縮小。"),
        row({"text": "offset: /function editor:settings/offset {x:0,y:0,z:-0.01}", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function editor:settings/offset {x:0,y:0,z:-0.01}"}}),
        row({"text": "expand: /function editor:settings/expand {x:-0.1,y:-0.1,z:-0.1}", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function editor:settings/expand {x:-0.1,y:-0.1,z:-0.1}"}}),
        row(button("補正リセット", "settings/zero"), button("メニュー", "menu"))])
    fn("settings/zero", [*[f'data modify storage editor:data prefs.{p}{a} set value 0' for p in "oe" for a in "xyz"], msg("生成補正を0に戻しました。")])

    # Document mutation is serialized by the durable job lock. The document is
    # authoritative even if a server stops between recording and world replay.
    fn("internal/history/save", ['data modify storage editor:data history.past append value {}',
        'data modify storage editor:data history.past[-1].objects set from storage editor:data document.objects',
        'execute if data storage editor:data history.past[20] run data remove storage editor:data history.past[0]',
        'data modify storage editor:data history.future set value []'])
    fn("internal/object/base", [
        'data modify storage editor:runtime object set value {label:""}',
        *[f'data modify storage editor:runtime object.{field} set from storage editor:data selection.{field}' for field in ('dim','ax','ay','az','bx','by','bz','x1','y1','z1','x2','y2','z2','sx','sy','sz')],
        'data modify storage editor:runtime object.id set from storage editor:data next_id',
        ])
    for typ, name in (("block_fill", "block/place"), ("mask", "mask/create"), ("teleport_volume", "teleport/create")):
        lines = guard(True) + ['function editor:internal/object/base', f'data modify storage editor:runtime object.type set value "{typ}"']
        if typ == "block_fill":
            lines += ['data modify storage editor:runtime object.mode set value "fill"', 'data modify storage editor:runtime object.palette set from storage editor:data prefs.palette',
                      'data modify storage editor:runtime object.variant set from storage editor:data prefs.variant']
        else:
            lines += ['function editor:internal/object/transform', 'execute unless score #transform_ok se matches 1 run return 0']
            if typ == "mask":
                lines += ['data modify storage editor:runtime object.material set value "mask_default"']
        lines += ['function editor:internal/object/commit']
        fn(name, lines)
    for mode in ("hollow", "outline"):
        fn("block/"+mode, guard(True) + ['function editor:internal/object/base',
            f'data merge storage editor:runtime {{object:{{type:"block_fill",mode:"{mode}"}}}}',
            'data modify storage editor:runtime object.palette set from storage editor:data prefs.palette',
            'data modify storage editor:runtime object.variant set from storage editor:data prefs.variant',
            'function editor:internal/object/commit'])
    fn("block/erase", guard(True) + ['function editor:internal/object/base',
        'data merge storage editor:runtime {object:{type:"block_fill",mode:"fill",palette:"air",variant:"normal"}}', 'function editor:internal/object/commit'])
    lines = ['scoreboard players set #transform_ok se 0']
    for a in "xyz":
        lines += [f'execute store result score #pos se run data get storage editor:runtime object.{a}1 1000',
                  f'execute store result score #size se run data get storage editor:runtime object.s{a} 1000',
                  f'execute store result score #offset se run data get storage editor:data prefs.o{a}',
                  f'execute store result score #expand se run data get storage editor:data prefs.e{a}',
                  'scoreboard players operation #pos se += #offset se', 'scoreboard players operation #pos se -= #expand se',
                  'scoreboard players operation #size se += #expand se', 'scoreboard players operation #size se += #expand se',
                  'execute unless score #size se matches 1..64000 run return run tellraw @s {text:"補正後のサイズは0.001〜64ブロックにしてください。",color:"red"}',
                  f'execute store result storage editor:runtime object.p{a} double 0.001 run scoreboard players get #pos se',
                  f'execute store result storage editor:runtime object.s{a} double 0.001 run scoreboard players get #size se',
                  f'execute store result storage editor:runtime object.lo{a} int 1 run scoreboard players get #pos se',
                  'scoreboard players operation #pos se += #size se',
                  f'execute store result storage editor:runtime object.hi{a} int 1 run scoreboard players get #pos se',
                  f'data modify storage editor:runtime object.o{a} set from storage editor:data prefs.o{a}',
                  f'data modify storage editor:runtime object.e{a} set from storage editor:data prefs.e{a}']
    lines += ['scoreboard players set #transform_ok se 1']
    fn("internal/object/transform", lines)
    fn("internal/object/commit", [
        'execute if data storage editor:data document.objects[511] run return run tellraw @s {text:"この版の登録上限は512件です。",color:"red"}',
        'function editor:internal/history/save',
        'data modify storage editor:data document.objects append from storage editor:runtime object',
        'execute if data storage editor:runtime object{type:"block_fill"} run data modify storage editor:data footprints append from storage editor:runtime object',
        'execute store result score #next se run data get storage editor:data next_id', 'scoreboard players add #next se 1',
        'execute store result storage editor:data next_id int 1 run scoreboard players get #next se',
        'function editor:internal/revision',
        'data modify storage editor:runtime job set value {queue:[],tickets:[],wait:0,phase:"next"}',
        'data modify storage editor:runtime job.queue append from storage editor:runtime object',
        'data modify storage editor:data build_state set value "pending"', msg("配置を記録しました。チャンクを読み込み、ワールドに反映します。")])
    fn("internal/revision", ['execute store result score #revision se run data get storage editor:data revision',
        'scoreboard players add #revision se 1', 'execute store result storage editor:data revision int 1 run scoreboard players get #revision se'])

    for action, src, dst in (("undo", "past", "future"), ("redo", "future", "past")):
        fn("history/" + action, guard() + [f'execute unless data storage editor:data history.{src}[-1] run return run tellraw @s {{text:"対象の履歴がありません。",color:"yellow"}}',
            f'data modify storage editor:data history.{dst} append value {{}}',
            f'data modify storage editor:data history.{dst}[-1].objects set from storage editor:data document.objects',
            f'data modify storage editor:data document.objects set from storage editor:data history.{src}[-1].objects',
            f'data remove storage editor:data history.{src}[-1]', 'function editor:internal/revision', 'function editor:build'])
    fn("objects/delete", guard() + ['$execute unless data storage editor:data document.objects[{id:$(id)}] run return run tellraw @s {text:"IDが見つかりません。",color:"red"}',
        'function editor:internal/history/save', '$data remove storage editor:data document.objects[{id:$(id)}]',
        'function editor:internal/revision', 'function editor:build'])
    fn("objects/select", guard() + ['$execute unless data storage editor:data document.objects[{id:$(id)}] run return 0',
        '$data modify storage editor:runtime selected_object set from storage editor:data document.objects[{id:$(id)}]',
        'data modify storage editor:data selection set value {}',
        *[f'data modify storage editor:data selection.{field} set from storage editor:runtime selected_object.{field}' for field in ('dim','ax','ay','az','bx','by','bz')],
        'function editor:settings/zero',
        *[f'execute if data storage editor:runtime selected_object.{field} run data modify storage editor:data prefs.{field} set from storage editor:runtime selected_object.{field}' for field in ('palette','variant','ox','oy','oz','ex','ey','ez')],
        'function editor:internal/selection/normalize'])
    fn("objects/update", guard(True) + ['$execute unless data storage editor:data document.objects[{id:$(id)}] run return 0',
        '$data modify storage editor:runtime previous set from storage editor:data document.objects[{id:$(id)}]',
        'function editor:internal/object/base',
        *[f'data modify storage editor:runtime object.{field} set from storage editor:runtime previous.{field}' for field in ('id','type','label')],
        'execute if data storage editor:runtime previous.target run data modify storage editor:runtime object.target set from storage editor:runtime previous.target',
        'execute if data storage editor:runtime previous{type:"block_fill"} run function editor:internal/object/update_block',
        'execute unless data storage editor:runtime previous{type:"block_fill"} run function editor:internal/object/transform',
        'execute unless data storage editor:runtime previous{type:"block_fill"} unless score #transform_ok se matches 1 run return 0',
        'execute if data storage editor:runtime previous{type:"mask"} run data modify storage editor:runtime object.material set value "mask_default"',
        'function editor:internal/history/save',
        '$data modify storage editor:data document.objects[{id:$(id)}] set from storage editor:runtime object',
        'function editor:internal/revision', 'function editor:build'])
    fn("internal/object/update_block", ['data modify storage editor:runtime object.mode set value "fill"',
        'execute if data storage editor:runtime previous.mode run data modify storage editor:runtime object.mode set from storage editor:runtime previous.mode',
        'data modify storage editor:runtime object.palette set from storage editor:data prefs.palette',
        'data modify storage editor:runtime object.variant set from storage editor:data prefs.variant'])
    fn("objects/rename", guard() + ['$execute unless data storage editor:data document.objects[{id:$(id)}] run return 0',
        'function editor:internal/history/save', '$data modify storage editor:data document.objects[{id:$(id)}].label set value "$(label)"',
        'function editor:internal/revision', msg("名前を変更しました。")])
    fn("objects/list", ['data modify storage editor:runtime list set from storage editor:data document.objects',
        'execute unless data storage editor:runtime list[0] run return run tellraw @s {text:"登録はまだありません。",color:"gray"}',
        'function editor:internal/list/next'])
    fn("internal/list/next", ['function editor:internal/list/row with storage editor:runtime list[0]',
        'data remove storage editor:runtime list[0]', 'execute if data storage editor:runtime list[0] run function editor:internal/list/next'])
    fn("internal/list/row", ['$tellraw @s [{text:"#$(id) $(type) ",color:"gold"},{nbt:"list[0].label",storage:"editor:runtime"},{text:" [選択]",color:"aqua",click_event:{action:"run_command",command:"/function editor:objects/select {id:$(id)}"}},{text:" [更新]",color:"green",click_event:{action:"suggest_command",command:"/function editor:objects/update {id:$(id)}"}},{text:" [削除]",color:"red",click_event:{action:"suggest_command",command:"/function editor:objects/delete {id:$(id)}"}},{text:" [名前]",color:"gray",click_event:{action:"suggest_command",command:\'/function editor:objects/rename {id:$(id),label:"name"}\'}}]',
        'data modify storage editor:runtime list_item set from storage editor:runtime list[0]',
        '$execute if data storage editor:runtime list_item{type:"teleport_volume"} run tellraw @s [{text:"  [現在地をTP先に設定]",color:"yellow",click_event:{action:"suggest_command",command:"/function editor:teleport/link {id:$(id)}"}}]'])

    # Replay first clears every historical fill footprint, then renders live
    # objects in insertion order. Deleted fills cannot leave ghost terrain.
    fn("build", guard() + [
        'scoreboard players add #epoch se.gen 1',
        'data modify storage editor:runtime job set value {queue:[],tickets:[],wait:0,phase:"next"}',
        'data modify storage editor:runtime clear_list set from storage editor:data footprints',
        'execute if data storage editor:runtime clear_list[0] run function editor:internal/build/clear_list',
        'data modify storage editor:runtime job.queue append from storage editor:data document.objects[]',
        *[f'execute in minecraft:{d} run kill @e[tag=editor.object]' for d in ("overworld", "the_nether", "the_end")],
        # Unloaded entities are also swept per footprint when each job loads it.
        'data modify storage editor:data build_state set value "pending"',
        msg("再構築を開始しました。配置跡を消去してデータを順番に再生します。")])
    fn("internal/build/clear_list", ['data modify storage editor:runtime clear_list[0].type set value "clear"',
        'data modify storage editor:runtime job.queue append from storage editor:runtime clear_list[0]',
        'data remove storage editor:runtime clear_list[0]',
        'execute if data storage editor:runtime clear_list[0] run function editor:internal/build/clear_list'])
    # Keep display tombstones too, so deleting an unloaded mask is durable.
    # Filled below after all functions have been emitted.
    fn("build/resume", ['execute if data storage editor:runtime job run function editor:internal/job/release',
        'data remove storage editor:runtime job', 'function editor:build'])
    fn("internal/job/tick", [
        'execute if data storage editor:runtime job{phase:"error"} run return 0',
        'execute if data storage editor:runtime job{phase:"next"} run return run function editor:internal/job/next',
        'execute if data storage editor:runtime job{phase:"wait"} run function editor:internal/job/wait'])
    fn("internal/job/next", [
        'execute unless data storage editor:runtime job.queue[0] run return run function editor:internal/job/done',
        'data modify storage editor:runtime work set from storage editor:runtime job.queue[0]',
        # Displays belong to their transformed origin chunk, which can differ
        # from the selected block chunk after a negative fractional offset.
        'execute if data storage editor:runtime work.px run function editor:internal/job/display_bounds',
        'data modify storage editor:runtime job.tickets set value []',
        'data modify storage editor:runtime job.wait set value 0',
        'function editor:internal/job/chunks',
        'data modify storage editor:runtime job.phase set value "wait"'])
    fn("internal/job/display_bounds", [
        *[f'execute store result storage editor:runtime work.{a}{edge} int 1 run data get storage editor:runtime work.p{a} 1' for a in "xz" for edge in (1, 2)],
        'data modify storage editor:runtime work.y1 set value 64',
        'data modify storage editor:runtime work.y2 set value 64'])
    # All chunk calculations use integer floor division, including negatives.
    lines = []
    for a in "xz":
        for edge in (1, 2):
            lines += [f'execute store result score #c{a}{edge} se run data get storage editor:runtime work.{a}{edge}',
                      f'scoreboard players operation #c{a}{edge} se /= #16 se', f'scoreboard players operation #c{a}{edge} se *= #16 se']
    lines += ['scoreboard players operation #cx se = #cx1 se', 'function editor:internal/job/chunk_x']
    fn("internal/job/chunks", lines)
    fn("internal/job/chunk_x", ['scoreboard players operation #cz se = #cz1 se', 'function editor:internal/job/chunk_z',
        'scoreboard players add #cx se 16', 'execute if score #cx se <= #cx2 se run function editor:internal/job/chunk_x'])
    fn("internal/job/chunk_z", ['execute store result storage editor:runtime ticket.x int 1 run scoreboard players get #cx se',
        'execute store result storage editor:runtime ticket.z int 1 run scoreboard players get #cz se',
        'data modify storage editor:runtime ticket.dim set from storage editor:runtime work.dim',
        'function editor:internal/job/ticket with storage editor:runtime ticket',
        'scoreboard players add #cz se 16', 'execute if score #cz se <= #cz2 se run function editor:internal/job/chunk_z'])
    fn("internal/job/ticket", ['$execute in $(dim) store success score #exists se run forceload query $(x) $(z)',
        'execute if score #exists se matches 1 run return 0',
        '$execute in $(dim) store success score #added se run forceload add $(x) $(z)',
        'execute if score #added se matches 1 run data modify storage editor:runtime job.tickets append from storage editor:runtime ticket'])
    fn("internal/job/wait", ['scoreboard players set #loaded se 0', 'function editor:internal/job/loaded with storage editor:runtime work',
        'execute if score #loaded se matches 1 run return run function editor:internal/job/apply',
        'execute store result score #wait se run data get storage editor:runtime job.wait', 'scoreboard players add #wait se 1',
        'execute store result storage editor:runtime job.wait int 1 run scoreboard players get #wait se',
        'execute if score #wait se matches 1200.. run function editor:internal/job/error'])
    fn("internal/job/loaded", ['$execute in $(dim) if loaded $(x1) $(y1) $(z1) if loaded $(x1) $(y1) $(z2) if loaded $(x2) $(y2) $(z1) if loaded $(x2) $(y2) $(z2) run scoreboard players set #loaded se 1'])
    fn("internal/job/apply", [
        'execute if data storage editor:runtime work{type:"clear"} run function editor:internal/render/clear with storage editor:runtime work',
        'execute if data storage editor:runtime work{type:"block_fill"} run function editor:internal/render/block with storage editor:runtime work',
        'execute if data storage editor:runtime work{type:"mask"} run function editor:internal/render/mask with storage editor:runtime work',
        'execute if data storage editor:runtime work{type:"teleport_volume"} run function editor:internal/render/teleport with storage editor:runtime work',
        'execute if data storage editor:runtime work{type:"sweep"} run function editor:internal/render/sweep with storage editor:runtime work',
        'function editor:internal/job/release', 'data remove storage editor:runtime job.queue[0]',
        'data modify storage editor:runtime job.phase set value "next"'])
    fn("internal/job/release", ['execute unless data storage editor:runtime job.tickets[0] run return 0',
        'function editor:internal/job/unticket with storage editor:runtime job.tickets[0]',
        'data remove storage editor:runtime job.tickets[0]', 'function editor:internal/job/release'])
    fn("internal/job/unticket", ['$execute in $(dim) run forceload remove $(x) $(z)'])
    fn("internal/job/error", ['function editor:internal/job/release', 'data modify storage editor:runtime job.phase set value "error"',
        'data modify storage editor:data build_state set value "error"',
        msg("チャンク読み込み待ちがタイムアウト。データは保存済みです。status→再開で再構築します。", "red", "@a[tag=editor.editing]")])
    fn("internal/job/done", ['data remove storage editor:runtime job', 'data modify storage editor:data build_state set value "clean"',
        # Once replay succeeds, only current world footprints are needed.
        # Undo first clears those and then replays its restored document.
        'data modify storage editor:data footprints set value []',
        'data modify storage editor:data display_footprints set value []',
        'data modify storage editor:runtime compact set from storage editor:data document.objects',
        'execute if data storage editor:runtime compact[0] run function editor:internal/compact',
        'function editor:internal/selection/preview', msg("ワールドへの反映が完了しました。", "green", "@a[tag=editor.editing]")])
    fn("internal/compact", ['data modify storage editor:runtime compact_item set from storage editor:runtime compact[0]',
        'execute if data storage editor:runtime compact_item{type:"block_fill"} run data modify storage editor:data footprints append from storage editor:runtime compact_item',
        'execute unless data storage editor:runtime compact_item{type:"block_fill"} run data modify storage editor:data display_footprints append from storage editor:runtime compact_item',
        'data remove storage editor:runtime compact[0]', 'execute if data storage editor:runtime compact[0] run function editor:internal/compact'])
    fn("internal/render/clear", ['$execute in $(dim) run fill $(x1) $(y1) $(z1) $(x2) $(y2) $(z2) minecraft:air strict'])
    fn("internal/render/block", ['$data modify storage editor:runtime work.block set from storage editor:data document.palettes.$(palette).$(variant)',
        'function editor:internal/render/fill with storage editor:runtime work'])
    fn("internal/render/fill", [
        '$execute if data storage editor:runtime work{mode:"hollow"} run return run execute in $(dim) run fill $(x1) $(y1) $(z1) $(x2) $(y2) $(z2) $(block) hollow',
        '$execute if data storage editor:runtime work{mode:"outline"} run return run execute in $(dim) run fill $(x1) $(y1) $(z1) $(x2) $(y2) $(z2) $(block) outline',
        '$execute in $(dim) run fill $(x1) $(y1) $(z1) $(x2) $(y2) $(z2) $(block) strict'])
    fn("internal/render/sweep", ['$execute in $(dim) run kill @e[tag=editor.object,scores={se.id=$(id)}]'])
    for typ in ("mask", "teleport"):
        body = ['function editor:internal/render/sweep with storage editor:runtime work']
        if typ == "mask":
            body += ['$execute in $(dim) positioned 0.0 0.0 0.0 run summon minecraft:block_display ~$(px) ~$(py) ~$(pz) {Tags:["editor.object","editor.mask","editor.new"],block_state:{Name:"' + DISPLAY_BLOCKS["maskBody"] + '"},transformation:{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},view_range:4f,width:128f,height:128f}']
        body += ['$execute in $(dim) positioned 0.0 0.0 0.0 run summon minecraft:block_display ~$(px) ~$(py) ~$(pz) {Tags:["editor.object","editor.guide","editor.new"],block_state:{Name:"' + DISPLAY_BLOCKS["guide"] + '"},transformation:{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:2f,width:128f,height:128f}',
            '$execute in $(dim) run scoreboard players set @e[tag=editor.new] se.id $(id)',
            '$execute in $(dim) run scoreboard players operation @e[tag=editor.new] se.gen = #epoch se.gen',
            '$execute in $(dim) if data storage editor:data {guides:0b} as @e[tag=editor.new,tag=editor.guide] run data merge entity @s {view_range:0f}',
            '$execute in $(dim) run tag @e[tag=editor.new] remove editor.new']
        fn("internal/render/" + typ, body)
    fn("preview/toggle", ['execute if data storage editor:data {guides:1b} run return run function editor:preview/hide', 'function editor:preview/show'])
    for action, value, view in (("show", 1, 2), ("hide", 0, 0)):
        fn("preview/" + action, [f'data modify storage editor:data guides set value {value}b',
            *[f'execute in minecraft:{d} as @e[tag=editor.guide] run data merge entity @s {{view_range:{view}f}}' for d in ("overworld", "the_nether", "the_end")],
            'function editor:internal/selection/preview'])

    fn("teleport/link", guard() + ['$execute unless data storage editor:data document.objects[{id:$(id),type:"teleport_volume"}] run return run tellraw @s {text:"TP範囲のIDではありません。",color:"red"}',
        'execute unless entity @s[type=minecraft:player] run return 0',
        'scoreboard players set #dim_ok se 0',
        *[f'execute if dimension minecraft:{d} run scoreboard players set #dim_ok se 1' for d in ("overworld", "the_nether", "the_end")],
        'execute unless score #dim_ok se matches 1 run return run tellraw @s {text:"TP先は通常3ディメンション内にしてください。",color:"red"}',
        *[line for i in range(3) for line in (f'execute store result score #target_coord se run data get entity @s Pos[{i}] 1',
            'execute unless score #target_coord se matches -1000000..1000000 run return run tellraw @s {text:"TP先は±1000000以内にしてください。",color:"red"}')],
        'function editor:internal/history/save',
        '$data modify storage editor:data document.objects[{id:$(id)}].target set value {}',
        '$data modify storage editor:data document.objects[{id:$(id)}].target.pos set from entity @s Pos',
        '$data modify storage editor:data document.objects[{id:$(id)}].target.rotation set from entity @s Rotation',
        *[f'$execute if dimension minecraft:{d} run data modify storage editor:data document.objects[{{id:$(id)}}].target.dim set value "minecraft:{d}"' for d in ("overworld", "the_nether", "the_end")],
        'function editor:internal/revision', msg("現在の足元・向きをTP先として保存しました。playで動作確認できます。")])
    fn("teleport/unlink", guard() + ['function editor:internal/history/save', '$data remove storage editor:data document.objects[{id:$(id)}].target', 'function editor:internal/revision'])
    fn("internal/teleport/tick", ['execute unless entity @a[tag=!editor.editing,scores={se.cd=0}] run return 0',
        'data modify storage editor:runtime volumes set from storage editor:data document.objects',
        'execute if data storage editor:runtime volumes[0] run function editor:internal/teleport/next'])
    fn("internal/teleport/next", ['data modify storage editor:runtime volume_item set from storage editor:runtime volumes[0]',
        'execute if data storage editor:runtime volume_item{type:"teleport_volume"} if data storage editor:runtime volume_item.target run function editor:internal/teleport/check with storage editor:runtime volumes[0]',
        'data remove storage editor:runtime volumes[0]', 'execute if data storage editor:runtime volumes[0] run function editor:internal/teleport/next'])
    fn("internal/teleport/check", ['$execute as @a[tag=!editor.editing,scores={se.cd=0}] at @s if dimension $(dim) run function editor:internal/teleport/player with storage editor:runtime volumes[0]'])
    fn("internal/teleport/player", [*[f'execute store result score #p{a} se run data get entity @s Pos[{i}] 1000' for i, a in enumerate("xyz")],
        *[f'$execute unless score #p{a} se matches $(lo{a}).. run return 0' for a in "xyz"],
        *[f'$execute if score #p{a} se matches $(hi{a}).. run return 0' for a in "xyz"],
        'scoreboard players set @s se.cd 20',
        'data modify storage editor:runtime target set from storage editor:runtime volumes[0].target',
        *[f'execute store result storage editor:runtime target.{a} double 0.001 run data get storage editor:runtime target.pos[{i}] 1000' for i, a in enumerate("xyz")],
        *[f'execute store result storage editor:runtime target.{a} float 0.001 run data get storage editor:runtime target.rotation[{i}] 1000' for i, a in enumerate(("yaw", "pitch"))],
        'function editor:internal/teleport/go with storage editor:runtime target'])
    fn("internal/teleport/go", ['$execute in $(dim) positioned 0.0 0.0 0.0 run tp @s ~$(x) ~$(y) ~$(z) $(yaw) $(pitch)'])

    fn("export", [msg("SE_EXPORT_BEGIN", "gray"),
        'tellraw @s [{text:"SE_META "},{nbt:"document.schema",storage:"editor:data"},{text:" "},{nbt:"revision",storage:"editor:data"}]',
        'data modify storage editor:runtime export set from storage editor:data document.objects',
        'execute if data storage editor:runtime export[0] run function editor:internal/export/next', msg("SE_EXPORT_END", "gray"),
        msg("完全なJSON出力: ワールドを保存して閉じ、付属 editor_data.py export <ワールドフォルダ> を実行してください。")])
    fn("internal/export/next", ['tellraw @s [{text:"SE_OBJECT "},{nbt:"export[0]",storage:"editor:runtime"}]',
        'data remove storage editor:runtime export[0]', 'execute if data storage editor:runtime export[0] run function editor:internal/export/next'])
    # Persist a separate list of every display location, including deleted IDs.
    path = F / "internal/init.mcfunction"
    write(path, path.read_text(encoding="utf-8") + '\ndata modify storage editor:data display_footprints set value []')
    path = F / "internal/object/commit.mcfunction"
    body = path.read_text(encoding="utf-8").replace('function editor:internal/revision', 'execute unless data storage editor:runtime object{type:"block_fill"} run data modify storage editor:data display_footprints append from storage editor:runtime object\nfunction editor:internal/revision')
    write(path, body)
    path = F / "build.mcfunction"
    body = path.read_text(encoding="utf-8").replace('data modify storage editor:runtime job.queue append from storage editor:data document.objects[]',
        'data modify storage editor:runtime sweep_list set from storage editor:data display_footprints\nexecute if data storage editor:runtime sweep_list[0] run function editor:internal/build/sweep_list\ndata modify storage editor:runtime job.queue append from storage editor:data document.objects[]')
    write(path, body)
    fn("internal/build/sweep_list", ['data modify storage editor:runtime sweep_list[0].type set value "sweep"',
        'data modify storage editor:runtime job.queue append from storage editor:runtime sweep_list[0]',
        'data remove storage editor:runtime sweep_list[0]', 'execute if data storage editor:runtime sweep_list[0] run function editor:internal/build/sweep_list'])
    build_resources()
    sync_live_resources()
    print(f"Generated {len(list(F.rglob('*.mcfunction')))} mcfunctions; datapack: {DP}")


def managed_blockstates() -> dict[Path, str]:
    managed = {
        blockstate_relative_path(DISPLAY_BLOCKS["maskBody"]): "editor:block/mask_body",
        blockstate_relative_path(DISPLAY_BLOCKS["selection"]): "editor:block/selection",
        blockstate_relative_path(DISPLAY_BLOCKS["guide"]): "editor:block/guide",
    }
    managed.update({
        blockstate_relative_path(carrier): f"editor:block/{name}_maskable"
        for name, (_, carrier, _) in PALETTES.items()
    })
    managed.update({
        blockstate_relative_path(COLLISION_CARRIERS["fence"]): "editor:block/collision_fence",
        blockstate_relative_path(COLLISION_CARRIERS["wall"]): "editor:block/collision_wall",
    })
    return managed


def _read_generated_manifest() -> dict[str, dict[str, str | None]]:
    if not MANIFEST.exists():
        return {}
    value = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schemaVersion") not in (1, 2) or not isinstance(value.get("managedBlockstates"), dict):
        raise ValueError(f"Invalid generated blockstate manifest: {MANIFEST}")
    result: dict[str, dict[str, str | None]] = {}
    for relative, entry in value["managedBlockstates"].items():
        parts = Path(relative).parts
        if len(parts) < 4 or parts[0] != "assets" or parts[2] != "blockstates" or Path(relative).suffix != ".json" or ".." in parts:
            raise ValueError(f"Unsafe path in generated blockstate manifest: {relative}")
        if value["schemaVersion"] == 1:
            entry = {"generatedHash": entry, "originalBase64": None}
        if not isinstance(entry, dict) or set(entry) != {"generatedHash", "originalBase64"}:
            raise ValueError(f"Invalid entry in generated blockstate manifest: {relative}")
        digest = entry["generatedHash"]
        original = entry["originalBase64"]
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"Invalid hash in generated blockstate manifest: {relative}")
        if original is not None:
            if not isinstance(original, str):
                raise ValueError(f"Invalid original content in generated blockstate manifest: {relative}")
            try:
                base64.b64decode(original, validate=True)
            except ValueError as exc:
                raise ValueError(f"Invalid original content in generated blockstate manifest: {relative}") from exc
        result[relative] = {"generatedHash": digest, "originalBase64": original}
    return result


def _remove_stale_blockstates(root: Path, desired: set[str], *, restore_original: bool) -> int:
    removed = 0
    for relative, entry in _read_generated_manifest().items():
        if relative in desired:
            continue
        target = root / relative
        if not target.exists():
            original = entry["originalBase64"] if restore_original else None
            if original is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(base64.b64decode(original, validate=True))
                removed += 1
            continue
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual_hash != entry["generatedHash"]:
            raise RuntimeError(f"Refusing to remove modified managed blockstate: {target}")
        original = entry["originalBase64"] if restore_original else None
        if original is None:
            target.unlink()
        else:
            target.write_bytes(base64.b64decode(original, validate=True))
        removed += 1
    return removed


def _blockstate_bytes(model: str) -> bytes:
    value = {"variants": {"": {"model": model}}}
    return (json.dumps(value, ensure_ascii=False, indent=2).strip() + "\n").encode("utf-8")


def _validate_blockstate_destinations(root: Path, desired: dict[Path, str], *, allow_original_capture: bool) -> None:
    previously_managed = _read_generated_manifest()
    for relative, model in desired.items():
        target = root / relative
        if not target.exists():
            continue
        current = target.read_bytes()
        expected = _blockstate_bytes(model)
        if current == expected:
            continue
        name = relative.as_posix()
        old_entry = previously_managed.get(name)
        if old_entry is None:
            if allow_original_capture:
                continue
            raise RuntimeError(f"Refusing to overwrite unmanaged blockstate: {target}")
        if hashlib.sha256(current).hexdigest() != old_entry["generatedHash"]:
            raise RuntimeError(f"Refusing to overwrite modified managed blockstate: {target}")


def build_block_assignments() -> None:
    desired = managed_blockstates()
    # Check the active pack first so a conflicting new assignment cannot leave
    # the generated source half-switched before live synchronization fails.
    _validate_blockstate_destinations(ROOT, desired, allow_original_capture=True)
    _validate_blockstate_destinations(RP, desired, allow_original_capture=False)
    _remove_stale_blockstates(RP, {path.as_posix() for path in desired}, restore_original=False)
    for relative, model in desired.items():
        js(RP / relative, {"variants": {"": {"model": model}}})


def sync_live_resources():
    """Update only this tool's declared assets in the active testpack.

    The datapack source is linked from the world's datapacks folder; it needs
    no archive or copy step. Keep the original vanilla texture files intact.
    """
    desired_blockstates = managed_blockstates()
    desired_names = {path.as_posix() for path in desired_blockstates}
    _validate_blockstate_destinations(ROOT, desired_blockstates, allow_original_capture=True)
    previous = _read_generated_manifest()
    original_by_name: dict[str, str | None] = {}
    for relative, model in desired_blockstates.items():
        name = relative.as_posix()
        if name in previous:
            original_by_name[name] = previous[name]["originalBase64"]
            continue
        target = ROOT / relative
        expected = _blockstate_bytes(model)
        original_by_name[name] = (
            base64.b64encode(target.read_bytes()).decode("ascii")
            if target.exists() and target.read_bytes() != expected else None
        )
    removed = _remove_stale_blockstates(ROOT, desired_names, restore_original=True)
    files: list[Path] = []
    for name in PALETTES:
        files += [Path(f"assets/editor/textures/block/{name}_maskable.png"),
                  Path(f"assets/editor/models/block/{name}_maskable.json")]
    for name in ("mask_body", "selection", "guide"):
        files += [Path(f"assets/editor/textures/block/{name}.png"),
                  Path(f"assets/editor/models/block/{name}.json")]
    files += [Path("assets/editor/models/block/collision_fence.json"),
              Path("assets/editor/models/block/collision_wall.json")]
    files += list(desired_blockstates)
    for name in files:
        source, destination = RP / name, ROOT / name
        if source.suffix == ".json":
            json.loads(source.read_text(encoding="utf-8"))
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or source.read_bytes() != destination.read_bytes():
            shutil.copyfile(source, destination)
        if source.read_bytes() != destination.read_bytes():
            raise RuntimeError(f"Live asset verification failed: {name}")
    manifest = {
        "schemaVersion": 2,
        "managedBlockstates": {
            relative: {
                "generatedHash": hashlib.sha256((RP / relative).read_bytes()).hexdigest(),
                "originalBase64": original_by_name[relative],
            }
            for relative in sorted(desired_names)
        },
    }
    js(MANIFEST, manifest)
    print(f"Live resource pack: {len(files)} assets synchronized to {ROOT}; stale blockstates removed={removed}")


def build_preview_resources():
    """Build the binary-alpha, double-sided selection preview assets."""
    from PIL import Image
    preview_styles = {
        "selection": ((70, 220, 255, 255), 2),
        "guide": ((240, 210, 50, 255), 1),
    }
    for name, (color, border) in preview_styles.items():
        dest = RP / f"assets/editor/textures/block/{name}.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        for y in range(32):
            for x in range(32):
                if x < border or x >= 32 - border or y < border or y >= 32 - border or x == y or x + y == 31:
                    im.putpixel((x, y), color)
        im.save(dest)
        outer = {"from": [0, 0, 0], "to": [16, 16, 16], "shade": False,
                 "faces": {face: {"texture": "#all", "uv": [0, 0, 16, 16]} for face in ("north", "south", "east", "west", "up", "down")}}
        elements = [outer]
        # Six thin planes whose visible faces point toward the cube center.
        # The 0.01 model-unit inset prevents overlap with the outward faces.
        inner_planes = (
            ([0, 0, 0], [16, 16, 0.01], "south"),
            ([0, 0, 15.99], [16, 16, 16], "north"),
            ([0, 0, 0], [0.01, 16, 16], "east"),
            ([15.99, 0, 0], [16, 16, 16], "west"),
            ([0, 0, 0], [16, 0.01, 16], "up"),
            ([0, 15.99, 0], [16, 16, 16], "down"),
        )
        elements += [{"from": start, "to": end, "shade": False,
                      "faces": {face: {"texture": "#all", "uv": [0, 0, 16, 16]}}}
                     for start, end, face in inner_planes]
        js(RP / f"assets/editor/models/block/{name}.json", {"textures": {"particle": f"editor:block/{name}", "all": f"editor:block/{name}"}, "elements": elements})


def build_resources():
    from PIL import Image
    from mark_textures_translucent import process_png
    for name, (_, _, tex) in PALETTES.items():
        dest = RP / f"assets/editor/textures/block/{name}_maskable.png"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(resource_path(ROOT, tex, "textures", ".png"), dest)
        print(f"{process_png(dest, False)}: {dest.relative_to(ROOT)}")
        if process_png(dest, True) != "already-translucent":
            raise RuntimeError("Translucency verification failed")
        js(RP / f"assets/editor/models/block/{name}_maskable.json", {"parent": "minecraft:block/cube_all", "textures": {"all": f"editor:block/{name}_maskable"}})
    # These are programmatic rendering primitives, not illustrated textures.
    # A mask must have alpha=1 everywhere; preview lines use only 0 and 255.
    dest = RP / "assets/editor/textures/block/mask_body.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (32, 32), (255, 255, 255, 1)).save(dest)
    js(RP / "assets/editor/models/block/mask_body.json", {"textures": {"particle": "editor:block/mask_body", "all": "editor:block/mask_body"}, "elements": [{"from": [0, 0, 0], "to": [16, 16, 16], "shade": False, "faces": {face: {"texture": "#all", "uv": [0, 0, 16, 16]} for face in ("north", "south", "east", "west", "up", "down")}}]})
    build_preview_resources()
    js(RP / "assets/editor/models/block/collision_fence.json", {
        "textures": {"particle": "minecraft:block/cherry_planks"}, "elements": []})
    js(RP / "assets/editor/models/block/collision_wall.json", {
        "textures": {"particle": "minecraft:block/sandstone"}, "elements": []})
    build_block_assignments()


if __name__ == "__main__":
    try:
        main()
    except (EditorBlockConfigError, OSError, RuntimeError, ValueError) as error:
        raise SystemExit(f"Error: {error}") from None
