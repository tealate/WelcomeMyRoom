"""Stage 06-1: isolated, vanilla mannequin experiment (also emitted by Stage 05)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F = ROOT / "space_editor_datapack/data/space_editor/function"
P = F / "proxy_spike"
S = "storage space_editor:proxy_spike"
DIMS = ("overworld", "the_nether", "the_end")
TYPES = ("mannequin", "text_display")
BODY = '@e[type=minecraft:mannequin,tag=sp.selected]'
LABEL = '@e[type=minecraft:text_display,tag=sp.selected]'


def put(name, *lines):
    path = P / (name + ".mcfunction")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def append_once(path, line):
    content = path.read_text(encoding="utf-8")
    if line not in content.splitlines():
        path.write_bytes((content + line + "\n").encode("utf-8"))


def target(role):
    typ = "text_display" if role.startswith("label_") else "mannequin"
    return f'@e[type=minecraft:{typ},tag=sp.selected,tag=sp.{role},limit=1]'


def generate():
    append_once(F / "load.mcfunction", "function space_editor:proxy_spike/load")
    append_once(F / "tick.mcfunction", "function space_editor:proxy_spike/tick")
    objectives = ("owner", "follow", "flip", "name", "epoch", "seen", "x", "y", "z", "fy", "normal", "inverted", "demo", "remove", "v")
    put("load", *[f"scoreboard objectives add sp.{o} dummy" for o in objectives],
        "scoreboard objectives add sp.leave minecraft.custom:minecraft.leave_game",
        "scoreboard players add #next sp.owner 0",
        "scoreboard players add #epoch sp.epoch 1",
        "team add sp_hidden", "team modify sp_hidden nametagVisibility never",
        "team modify sp_hidden collisionRule never",
        "team add sp_body", "team modify sp_body nametagVisibility always",
        "team modify sp_body collisionRule never",
        "function space_editor:proxy_spike/clear_all",
        f'data modify {S} note set value "Transient Stage06-1 scratch; document untouched"')
    put("clear_all", "scoreboard players add #epoch sp.epoch 1",
        *[f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] run function space_editor:proxy_spike/delete_start" for dim in DIMS],
        *[f"execute in minecraft:{dim} run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike]" for dim in DIMS],
        "scoreboard players set @a sp.follow 0", "tag @a remove sp.active")
    # Sweep only the two managed entity types, once per dimension; never recurse over projections.
    put("tick",
        *[line for dim,y in (("overworld",-63),("the_nether",1),("the_end",1)) for line in (
            f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=sp.removing,scores={{sp.remove=1..}}] at @s if dimension minecraft:{dim} run scoreboard players remove @s sp.remove 1",
            f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=sp.removing,scores={{sp.remove=4}}] at @s if dimension minecraft:{dim} run tp @s ~ {y} ~",
            f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=sp.removing,scores={{sp.remove=..0}}] at @s if dimension minecraft:{dim} run kill @s",
        )],
        *[f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run function space_editor:proxy_spike/delete_start" for dim in DIMS],
        *[f"execute in minecraft:{dim} as @e[type=minecraft:text_display,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s" for dim in DIMS],
        *[f"execute in minecraft:{dim} run tag @e[type=minecraft:{typ},tag=space_editor.proxy_spike] remove sp.online" for dim in DIMS for typ in TYPES],
        "execute as @a[tag=sp.active] at @s run function space_editor:proxy_spike/owner_tick",
        *[line for dim in DIMS for line in (
            f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=!sp.online] run function space_editor:proxy_spike/delete_start",
            f"execute in minecraft:{dim} run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=!sp.online]",
        )])
    put("owner_tick",
        "execute unless score @s sp.epoch = #epoch sp.epoch run return run function space_editor:proxy_spike/stop",
        "execute unless score @s sp.seen = @s sp.leave run return run function space_editor:proxy_spike/stop",
        "function space_editor:proxy_spike/mark_online",
        "execute if score @s sp.follow matches 1 run function space_editor:proxy_spike/update_selected")
    put("select", "execute unless entity @s[type=minecraft:player] run return 0",
        *[f"tag @e[type=minecraft:{typ},tag=space_editor.proxy_spike,tag=sp.selected] remove sp.selected" for typ in TYPES],
        f"execute store result {S} owner int 1 run scoreboard players get @s sp.owner",
        f"function space_editor:proxy_spike/select_owner with {S}")
    put("select_owner", *[
        f'$tag @e[type=minecraft:{typ},tag=space_editor.proxy_spike,tag=sp.{role},scores={{sp.owner=$(owner)}},limit=1] add sp.selected'
        for typ, role in (("mannequin", "main"), ("mannequin", "reference"), ("text_display", "label_main"), ("text_display", "label_reference"))])
    put("mark_online", "function space_editor:proxy_spike/select",
        *[f"execute unless entity {target(role)} run kill {target('label_' + role)}" for role in ("main", "reference")],
        f"tag {BODY} add sp.online", f"tag {LABEL} add sp.online")
    put("ensure_owner", "scoreboard players add @s sp.owner 0")
    put("spawn", "execute unless entity @s[type=minecraft:player] run return 0",
        "execute at @s unless loaded ~ ~ ~3 run return run tellraw @s {text:'[06-1] 生成先チャンクが未ロードです',color:'yellow'}",
        "function space_editor:proxy_spike/stop",
        "scoreboard players add #next sp.owner 1", "scoreboard players operation @s sp.owner = #next sp.owner",
        "scoreboard players add @s sp.leave 0", "scoreboard players operation @s sp.seen = @s sp.leave",
        "scoreboard players operation @s sp.epoch = #epoch sp.epoch",
        "tag @s add sp.active",
        *[f"scoreboard players set @s sp.{key} {value}" for key, value in
          dict(flip=0, name=3, follow=1, x=0, y=0, z=3000, fy=0, normal=2100, inverted=-300, demo=0).items()],
        "execute at @s run function space_editor:proxy_spike/spawn_main",
        "execute at @s run function space_editor:proxy_spike/player_tick")
    for role, x in (("main", 0), ("reference", 2)):
        put("spawn_" + role,
            f'execute positioned ~{x} ~ ~3 run summon minecraft:mannequin ~ ~ ~ {{Tags:["space_editor.proxy_spike","sp.{role}","sp.new"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hidden_layers:[],hide_description:1b,CustomNameVisible:0b}}',
            f"function space_editor:proxy_spike/initialize_new",
            f"data modify {S} uuid set from entity @s UUID",
            f"execute as @e[type=minecraft:mannequin,tag=sp.new,limit=1] run function space_editor:proxy_spike/set_profile with {S}",
            "tag @e[type=minecraft:mannequin,tag=sp.new] remove sp.new",
            "function space_editor:proxy_spike/apply_name")
    put("initialize_new", *[
        f"scoreboard players operation @e[type=minecraft:{typ},tag=space_editor.proxy_spike,tag=sp.new,limit=1] sp.{obj} = {src} sp.{obj}"
        for typ in TYPES for obj, src in (("owner", "@s"), ("epoch", "#epoch"))],
        *[f"tag @e[type=minecraft:{typ},tag=space_editor.proxy_spike,tag=sp.new] add sp.online" for typ in TYPES])
    put("set_profile", '$data modify entity @s profile set value {id:$(uuid)}')
    put("pair", "function space_editor:proxy_spike/spawn",
        "execute unless entity @s[tag=sp.active] run return 0",
        "execute at @s if loaded ~2 ~ ~3 run function space_editor:proxy_spike/spawn_reference",
        "function space_editor:proxy_spike/flip_on", "execute at @s run function space_editor:proxy_spike/player_tick")
    put("start", "function space_editor:proxy_spike/pair")
    put("delete_start",
        "scoreboard players operation #delete_owner sp.owner = @s sp.owner",
        f"execute if entity @s[tag=sp.main] as @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=sp.label_main] if score @s sp.owner = #delete_owner sp.owner run kill @s",
        f"execute if entity @s[tag=sp.reference] as @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=sp.label_reference] if score @s sp.owner = #delete_owner sp.owner run kill @s",
        "tag @s add sp.removing", "tag @s remove space_editor.proxy_spike",
        "tag @s remove sp.main", "tag @s remove sp.reference", "tag @s remove sp.selected", "tag @s remove sp.online", "tag @s remove sp.new",
        "effect give @s minecraft:invisibility infinite 0 true",
        *[f"item replace entity @s {slot} with minecraft:air" for slot in ("armor.head","armor.chest","armor.legs","armor.feet","weapon.mainhand","weapon.offhand")],
        "scoreboard players set @s sp.remove 6")
    put("delete_selected", "function space_editor:proxy_spike/select", f"execute as {BODY} run function space_editor:proxy_spike/delete_start", f"kill {LABEL}")
    put("stop", "execute unless entity @s[type=minecraft:player] run return 0",
        "function space_editor:proxy_spike/delete_selected", "scoreboard players set @s sp.follow 0",
        "scoreboard players set @s sp.owner 0", "tag @s remove sp.active")
    put("delete", "function space_editor:proxy_spike/stop")
    put("follow_on", "function space_editor:proxy_spike/select",
        f"execute unless entity {BODY} run return run tellraw @s {{text:'[06-1] spawn / pair で生成してください',color:'yellow'}}",
        "scoreboard players set @s sp.follow 1", "execute at @s run function space_editor:proxy_spike/player_tick")
    put("follow_off", "scoreboard players set @s sp.follow 0")
    for name, value, text in (("flip_on", 1, "Dinnerbone"), ("flip_grumm", 1, "Grumm"), ("flip_off", 0, None)):
        put(name, f"scoreboard players set @s sp.flip {value}", "function space_editor:proxy_spike/select",
            (f'data modify entity {target("main")} CustomName set value {{text:"{text}"}}' if text else f'data remove entity {target("main")} CustomName'),
            "function space_editor:proxy_spike/apply_name", "function space_editor:proxy_spike/update_labels")
    # Labels are reused and made invisible in native comparison modes. Their resolved text
    # also supplies description: Mannequin does NOT resolve selector components itself.
    for mode, name in enumerate(("custom_hidden", "team_hidden", "description", "text_display", "native_visible")):
        put("name_" + name, f"scoreboard players set @s sp.name {mode}", "function space_editor:proxy_spike/apply_name")
    put("apply_name", "function space_editor:proxy_spike/select", "function space_editor:proxy_spike/name_text_apply",
        f"team join sp_body {BODY}",
        f"execute as {BODY} run data merge entity @s {{CustomNameVisible:0b,hide_description:1b}}",
        *[f"execute if score @s sp.name matches {mode} run team join sp_hidden {BODY}" for mode in (1, 3)],
        f"execute as {LABEL} run data modify entity @s view_range set value 0f",
        f"execute if score @s sp.name matches 3 as {LABEL} run data modify entity @s view_range set value 0.5f",
        f"execute if score @s sp.name matches 4 as {BODY} run data modify entity @s CustomNameVisible set value 1b",
        "execute if score @s sp.name matches 2 run function space_editor:proxy_spike/name_description_apply",
        "function space_editor:proxy_spike/update_labels")
    put("name_description_apply", *[line for role in ("main", "reference") for line in (
        f"data modify entity {target(role)} hide_description set value 0b",
        f"data modify entity {target(role)} description set from entity {target('label_' + role)} text")])
    put("name_text_apply", *[line for role in ("main", "reference") for line in (
        f'execute if entity {target(role)} unless entity {target("label_" + role)} at {target(role)} run summon minecraft:text_display ~ ~2.1 ~ {{Tags:["space_editor.proxy_spike","sp.label","sp.label_{role}","sp.new"],billboard:"center",background:1073741824,see_through:0b,shadow:0b,teleport_duration:3,view_range:0.5f,text:{{text:""}}}}',
        "function space_editor:proxy_spike/initialize_new",
        f"data modify {S} uuid set from entity @s UUID",
        f"execute as @e[type=minecraft:text_display,tag=sp.new,limit=1] run function space_editor:proxy_spike/set_label with {S}",
        "tag @e[type=minecraft:text_display,tag=sp.new] remove sp.new",
        "function space_editor:proxy_spike/select")])
    put("set_label", '$data modify entity @s text set value {selector:"@a[nbt={UUID:$(uuid)}]"}')
    put("player_tick", "function space_editor:proxy_spike/select", "function space_editor:proxy_spike/update_selected")
    put("update_selected",
        *[f"execute if entity {target(role)} unless entity {target('label_' + role)} run function space_editor:proxy_spike/apply_name" for role in ("main", "reference")],
        "function space_editor:proxy_spike/sync",
        *[f"execute store result {S} {k} double 0.001 run scoreboard players get @s sp.{k}" for k in ("x", "y", "z")],
        "scoreboard players operation #y sp.v = @s sp.y",
        "execute if score @s sp.flip matches 1 run scoreboard players operation #y sp.v += @s sp.fy",
        f"execute store result {S} my double 0.001 run scoreboard players get #y sp.v",
        "scoreboard players operation #x sp.v = @s sp.x", "scoreboard players add #x sp.v 2000",
        f"execute store result {S} rx double 0.001 run scoreboard players get #x sp.v",
        f"function space_editor:proxy_spike/move with {S}",
        "function space_editor:proxy_spike/update_labels",
        "execute if score @s sp.demo matches 1.. run scoreboard players remove @s sp.demo 1",
        "execute if score @s sp.demo matches 0 run return 0",
        "execute if score @s sp.demo matches 1 run function space_editor:proxy_spike/swing_demo_pulse")
    put("move", *[
        f'$execute positioned ~$({x}) ~$({y}) ~$(z) if loaded ~ ~ ~ run tp {target(role)} ~ ~ ~ ~ ~'
        for role, x, y in (("main", "x", "my"), ("reference", "rx", "y"))])
    # Change pose only when needed: avoid repeated full NBT reloads (and standing/crouch
    # transitions in a single tick), then TP LAST to preserve head/body yaw updates.
    put("sync", f'data modify {S} pose set value "standing"',
        *[f'execute if predicate space_editor:proxy_spike/{pose} run data modify {S} pose set value "{pose}"' for pose in ("crouching", "swimming", "fall_flying")],
        f'execute if data entity @s sleeping_pos run data modify {S} pose set value "sleeping"',
        f"execute as {BODY} run function space_editor:proxy_spike/set_pose with {S}",
        *[f"item replace entity {BODY} {slot} from entity @s {slot}" for slot in ("armor.head", "armor.chest", "armor.legs", "armor.feet", "weapon.mainhand", "weapon.offhand")])
    put("set_pose", '$execute unless data entity @s {pose:"$(pose)"} run data modify entity @s pose set value "$(pose)"')
    put("update_labels",
        f"execute if score @s sp.flip matches 1 as {target('label_main')} run data merge entity @s {{transformation:{{left_rotation:[0f,0f,1f,0f]}}}}",
        f"execute if score @s sp.flip matches 0 as {target('label_main')} run data merge entity @s {{transformation:{{left_rotation:[0f,0f,0f,1f]}}}}",
        f"execute as {target('label_reference')} run data merge entity @s {{transformation:{{left_rotation:[0f,0f,0f,1f]}}}}",
        *[line for role in ("main", "reference") for line in (
        "scoreboard players operation #height sp.v = @s sp.normal",
        *( ["execute if score @s sp.flip matches 1 run scoreboard players operation #height sp.v = @s sp.inverted"] if role == "main" else [] ),
        f'execute if data entity {target(role)} {{pose:"crouching"}} run scoreboard players remove #height sp.v 300',
        f'execute if data entity {target(role)} {{pose:"swimming"}} run scoreboard players remove #height sp.v 1200',
        f'execute if data entity {target(role)} {{pose:"fall_flying"}} run scoreboard players remove #height sp.v 1200',
        f'execute if data entity {target(role)} {{pose:"sleeping"}} run scoreboard players remove #height sp.v 1600',
        f"execute store result {S} height double 0.001 run scoreboard players get #height sp.v",
        f"execute at {target(role)} run function space_editor:proxy_spike/label_{role}_position with {S}")])
    for role in ("main", "reference"):
        put(f"label_{role}_position", f'$tp {target("label_" + role)} ~ ~$(height) ~')
    # Milliblock settings make bounded numeric input and inspection simple.
    for name, params in (("offset", ("x", "y", "z")), ("flip_height", ("fy",)), ("label_height", ("normal", "inverted"))):
        put(name, *[line for k in params for line in (
            f'$data modify {S} input set value $({k})',
            f"execute store result score @s sp.{k} run data get {S} input 1000",
            f"execute if score @s sp.{k} matches ..-16001 run scoreboard players set @s sp.{k} -16000",
            f"execute if score @s sp.{k} matches 16001.. run scoreboard players set @s sp.{k} 16000")],
            "function space_editor:proxy_spike/select", "function space_editor:proxy_spike/update_labels")
    put("label_style", "function space_editor:proxy_spike/select",
        '$data modify storage space_editor:proxy_spike input set value $(scale)',
        f"execute store result score #scale sp.v run data get {S} input 1000",
        "execute if score #scale sp.v matches ..99 run return 0", "execute if score #scale sp.v matches 3001.. run return 0",
        f'$execute as {LABEL} run data merge entity @s {{background:$(background),transformation:{{scale:[$(scale)f,$(scale)f,$(scale)f]}}}}')
    for hand in ("main", "off"):
        put("swing_" + hand, "function space_editor:proxy_spike/select", f"swing {BODY} {hand}hand")
    put("swing_demo_on", "scoreboard players set @s sp.demo 2")
    put("swing_demo_off", "scoreboard players set @s sp.demo 0")
    put("swing_demo_pulse", f"swing {BODY} mainhand", "scoreboard players set @s sp.demo 11")
    put("attack", "advancement revoke @s only space_editor:proxy_spike/attack",
        "execute if entity @s[tag=sp.active,scores={sp.follow=1}] at @s run function space_editor:proxy_spike/swing_main")
    put("profile", "function space_editor:proxy_spike/select", "fetchprofile entity @s", f"fetchprofile entity {target('main')}")
    put("status", "function space_editor:proxy_spike/select",
        'tellraw @s [{text:"[06-1] owner="},{score:{name:"@s",objective:"sp.owner"}},{text:" follow="},{score:{name:"@s",objective:"sp.follow"}},{text:" flip="},{score:{name:"@s",objective:"sp.flip"}},{text:" name(0..4)="},{score:{name:"@s",objective:"sp.name"}}]',
        'tellraw @s [{text:"offset / flip Y / label height (milliblocks): "},' + ','.join(f'{{score:{{name:"@s",objective:"sp.{k}"}}}},{{text:" / "}}' for k in ("x", "y", "z", "fy", "normal", "inverted")) + ']',
        f"data get entity {target('main')}")
    put("help", *['tellraw @s ' + json.dumps({"text": text, "color": "aqua"}, ensure_ascii=False) for text in (
        "[06-1] /function space_editor:proxy_spike/<操作>（本人で実行）",
        "pair: 通常＋Dinnerbone比較 / spawn: 1体 / follow_on・follow_off: 追従・一時停止",
        "flip_on・flip_off・flip_grumm / name_custom_hidden・name_team_hidden・name_description・name_text_display・name_native_visible",
        "swing_main・swing_off / swing_demo_on・swing_demo_off: 連続腕振り / profile・status",
        'offset {x:0,y:0,z:3} / flip_height {fy:0} / label_height {normal:2.1,inverted:-0.3}',
        'label_style {scale:1.0,background:1073741824} / stop・delete: 自分を全削除 / clear_all: 全員分削除',
        "/reload 後は pair / spawn で再開。見た目は未検証。詳細 docs/stage06-1-mannequin.md" )])
    data = ROOT / "space_editor_datapack/data/space_editor"
    for pose, flag in (("crouching", "is_sneaking"), ("swimming", "is_swimming"), ("fall_flying", "is_fall_flying")):
        path = data / f"predicate/proxy_spike/{pose}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((json.dumps({"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"flags": {flag: True}}}, separators=(",", ":")) + "\n").encode("utf-8"))
    path = data / "advancement/proxy_spike/attack.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps({"criteria": {"hit": {"trigger": "minecraft:player_hurt_entity", "conditions": {"damage": {"type": {"direct_entity": {"type": "minecraft:player"}}}}}}, "rewards": {"function": "space_editor:proxy_spike/attack"}}) + "\n").encode("utf-8"))


def build():
    import build_space_editor_stage5 as stage5
    stage5.main()  # Stage 05 calls generate(), keeping either build entry safe.


if __name__ == "__main__":
    build()
