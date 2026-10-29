"""Regenerate the isolated Stage 06-1 mannequin spike after Stage 05."""
from pathlib import Path
import build_space_editor_stage5 as stage5

ROOT = Path(__file__).resolve().parents[1]
F = ROOT / "space_editor_datapack/data/space_editor/function"
P = F / "proxy_spike"


def put(name, *lines):
    path = P / (name + ".mcfunction")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_once(path, line):
    content = path.read_text(encoding="utf-8")
    if line not in content.splitlines():
        path.write_bytes((content + line + "\n").encode("utf-8"))


def build():
    stage5.main()
    append_once(F / "load.mcfunction", "function space_editor:proxy_spike/load")
    append_once(F / "tick.mcfunction", "function space_editor:proxy_spike/tick")
    put("load",
        "scoreboard objectives add sp.owner dummy",
        "scoreboard objectives add sp.follow dummy",
        "scoreboard objectives add sp.flip dummy",
        "scoreboard objectives add sp.name dummy",
        "scoreboard players add #next sp.owner 0",
        "team add sp_hidden",
        "team modify sp_hidden nametagVisibility never",
        "team modify sp_hidden collisionRule never",
        "team add sp_body",
        "team modify sp_body collisionRule never",
        "execute in minecraft:overworld run kill @e[tag=space_editor.proxy_spike]",
        "execute in minecraft:the_nether run kill @e[tag=space_editor.proxy_spike]",
        "execute in minecraft:the_end run kill @e[tag=space_editor.proxy_spike]",
        "scoreboard players set @a sp.follow 0")
    put("tick",
        "tag @e[tag=space_editor.proxy_spike] remove sp.online",
        "execute in minecraft:the_nether run tag @e[tag=space_editor.proxy_spike] remove sp.online",
        "execute in minecraft:the_end run tag @e[tag=space_editor.proxy_spike] remove sp.online",
        "execute as @a at @s if score @s sp.owner matches 1.. run function space_editor:proxy_spike/mark_online",
        "execute as @a[scores={sp.follow=1}] at @s run function space_editor:proxy_spike/player_tick",
        "execute in minecraft:overworld run kill @e[tag=space_editor.proxy_spike,tag=!sp.online]",
        "execute in minecraft:the_nether run kill @e[tag=space_editor.proxy_spike,tag=!sp.online]",
        "execute in minecraft:the_end run kill @e[tag=space_editor.proxy_spike,tag=!sp.online]")
    put("select",
        "scoreboard players operation #owner sp.owner = @s sp.owner",
        "tag @e[tag=space_editor.proxy_spike] remove sp.selected",
        "execute as @e[tag=space_editor.proxy_spike] if score @s sp.owner = #owner sp.owner run tag @s add sp.selected")
    put("mark_online", "function space_editor:proxy_spike/select",
        "execute unless entity @e[tag=sp.selected,tag=sp.main] run kill @e[tag=sp.selected,tag=sp.label]",
        "execute unless entity @e[tag=sp.selected,tag=sp.reference] run kill @e[tag=sp.selected,tag=sp.label_reference]",
        "tag @e[tag=sp.selected,tag=space_editor.proxy_spike] add sp.online")
    put("ensure_owner",
        "scoreboard players add @s sp.owner 0",
        "execute if score @s sp.owner matches 0 run scoreboard players add #next sp.owner 1",
        "execute if score @s sp.owner matches 0 run scoreboard players operation @s sp.owner = #next sp.owner")
    put("spawn",
        "function space_editor:proxy_spike/ensure_owner",
        "function space_editor:proxy_spike/delete_selected",
        "scoreboard players set @s sp.flip 0",
        "scoreboard players set @s sp.name 0",
        "execute rotated ~ 0 positioned ^ ^ ^3 run summon minecraft:mannequin ~ ~ ~ {Tags:[\"space_editor.proxy_spike\",\"sp.main\",\"sp.new\"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hide_description:1b,CustomNameVisible:0b}",
        "scoreboard players operation @e[tag=sp.new,tag=sp.main,limit=1] sp.owner = @s sp.owner",
        "data modify storage space_editor:proxy_spike uuid set from entity @s UUID",
        "execute as @e[tag=sp.new,tag=sp.main,limit=1] run function space_editor:proxy_spike/set_profile with storage space_editor:proxy_spike",
        "tag @e[tag=sp.new,tag=sp.main] remove sp.new",
        "scoreboard players set @s sp.follow 1",
        "function space_editor:proxy_spike/player_tick")
    put("set_profile", '$data modify entity @s profile set value {id:$(uuid)}')
    put("pair",
        "function space_editor:proxy_spike/spawn",
        "execute rotated ~ 0 positioned ^-1 ^ ^3 run summon minecraft:mannequin ~ ~ ~ {Tags:[\"space_editor.proxy_spike\",\"sp.reference\",\"sp.new\"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hide_description:1b,CustomNameVisible:0b}",
        "scoreboard players operation @e[tag=sp.new,tag=sp.reference,limit=1] sp.owner = @s sp.owner",
        "execute as @e[tag=sp.new,tag=sp.reference,limit=1] run function space_editor:proxy_spike/set_profile with storage space_editor:proxy_spike",
        "tag @e[tag=sp.new,tag=sp.reference] remove sp.new",
        "function space_editor:proxy_spike/flip_on",
        "function space_editor:proxy_spike/name_text_display",
        "function space_editor:proxy_spike/player_tick")
    put("delete_selected",
        "function space_editor:proxy_spike/select",
        "kill @e[tag=sp.selected,tag=space_editor.proxy_spike]")
    put("delete",
        "function space_editor:proxy_spike/delete_selected",
        "scoreboard players set @s sp.follow 0")
    put("follow_on", "function space_editor:proxy_spike/select",
        "execute if entity @e[tag=sp.selected,tag=sp.main] run scoreboard players set @s sp.follow 1",
        "execute if entity @e[tag=sp.selected,tag=sp.main] run function space_editor:proxy_spike/player_tick",
        'execute unless entity @e[tag=sp.selected,tag=sp.main] run tellraw @s {text:"[06-1] /function space_editor:proxy_spike/spawn を先に実行してください",color:"yellow"}')
    put("follow_off", "scoreboard players set @s sp.follow 0")
    put("flip_on", "scoreboard players set @s sp.flip 1", "function space_editor:proxy_spike/select", "data modify entity @e[tag=sp.selected,tag=sp.main,limit=1] CustomName set value {text:\"Dinnerbone\"}", "function space_editor:proxy_spike/apply_name")
    put("flip_off", "scoreboard players set @s sp.flip 0", "function space_editor:proxy_spike/select", "data remove entity @e[tag=sp.selected,tag=sp.main,limit=1] CustomName", "function space_editor:proxy_spike/apply_name")
    for mode, label in enumerate(("custom_hidden", "team_hidden", "description", "text_display")):
        put("name_" + label, f"scoreboard players set @s sp.name {mode}", "function space_editor:proxy_spike/apply_name")
    put("apply_name",
        "function space_editor:proxy_spike/select",
        "team join sp_body @e[tag=sp.selected,type=minecraft:mannequin]",
        "data modify entity @e[tag=sp.selected,tag=sp.main,limit=1] CustomNameVisible set value 0b",
        "data modify entity @e[tag=sp.selected,tag=sp.main,limit=1] hide_description set value 1b",
        "execute if score @s sp.name matches 1 run team join sp_hidden @e[tag=sp.selected,type=minecraft:mannequin]",
        "execute if score @s sp.name matches 3 run team join sp_hidden @e[tag=sp.selected,type=minecraft:mannequin]",
        "execute if score @s sp.name matches 2 run function space_editor:proxy_spike/name_description_apply",
        "execute unless score @s sp.name matches 3 run kill @e[tag=sp.selected,type=minecraft:text_display]",
        "execute if entity @e[tag=sp.selected,tag=sp.main] if score @s sp.name matches 3 run function space_editor:proxy_spike/name_text_apply")
    put("name_description_apply",
        "data modify entity @e[tag=sp.selected,tag=sp.main,limit=1] hide_description set value 0b",
        "data modify storage space_editor:proxy_spike uuid set from entity @s UUID",
        "execute as @e[tag=sp.selected,tag=sp.main,limit=1] run function space_editor:proxy_spike/set_description with storage space_editor:proxy_spike")
    put("set_description", '$data modify entity @s description set value {selector:"@a[nbt={UUID:$(uuid)}]"}')
    put("name_text_apply",
        "execute unless entity @e[tag=sp.selected,tag=sp.label_main] rotated ~ 0 positioned ^ ^2.3 ^3 run summon minecraft:text_display ~ ~ ~ {Tags:[\"space_editor.proxy_spike\",\"sp.label\",\"sp.label_main\",\"sp.new\"],billboard:\"center\",background:1073741824,see_through:0b,shadow:1b,text:{text:\"\"}}",
        "execute if entity @e[tag=sp.new,tag=sp.label_main] run scoreboard players operation @e[tag=sp.new,tag=sp.label_main,limit=1] sp.owner = @s sp.owner",
        "tag @e[tag=sp.new,tag=sp.label_main] remove sp.new",
        "function space_editor:proxy_spike/select",
        "execute if entity @e[tag=sp.selected,tag=sp.reference] unless entity @e[tag=sp.selected,tag=sp.label_reference] rotated ~ 0 positioned ^-1 ^2.3 ^3 run summon minecraft:text_display ~ ~ ~ {Tags:[\"space_editor.proxy_spike\",\"sp.label\",\"sp.label_reference\",\"sp.new\"],billboard:\"center\",background:1073741824,see_through:0b,shadow:1b,text:{text:\"\"}}",
        "execute if entity @e[tag=sp.new,tag=sp.label_reference] run scoreboard players operation @e[tag=sp.new,tag=sp.label_reference,limit=1] sp.owner = @s sp.owner",
        "tag @e[tag=sp.new,tag=sp.label_reference] remove sp.new",
        "function space_editor:proxy_spike/select",
        "data modify storage space_editor:proxy_spike uuid set from entity @s UUID",
        "execute as @e[tag=sp.selected,tag=sp.label] run function space_editor:proxy_spike/set_label with storage space_editor:proxy_spike")
    put("set_label", '$data modify entity @s text set value {selector:"@a[nbt={UUID:$(uuid)}]"}')
    put("player_tick",
        "function space_editor:proxy_spike/select",
        "tag @e[tag=sp.selected,tag=space_editor.proxy_spike] add sp.online",
        "execute if entity @e[tag=sp.selected,tag=sp.main] rotated ~ 0 positioned ^ ^ ^3 rotated as @s as @e[tag=sp.selected,tag=sp.main,limit=1] run tp @s ~ ~ ~ ~ ~",
        "execute if entity @e[tag=sp.selected,tag=sp.reference] rotated ~ 0 positioned ^-1 ^ ^3 rotated as @s as @e[tag=sp.selected,tag=sp.reference,limit=1] run tp @s ~ ~ ~ ~ ~",
        "execute if entity @e[tag=sp.selected,tag=sp.label_main] if score @s sp.flip matches 1 rotated ~ 0 positioned ^ ^0.7 ^3 as @e[tag=sp.selected,tag=sp.label_main,limit=1] run tp @s ~ ~ ~",
        "execute if entity @e[tag=sp.selected,tag=sp.label_main] unless score @s sp.flip matches 1 rotated ~ 0 positioned ^ ^2.3 ^3 as @e[tag=sp.selected,tag=sp.label_main,limit=1] run tp @s ~ ~ ~",
        "execute if entity @e[tag=sp.selected,tag=sp.label_reference] rotated ~ 0 positioned ^-1 ^2.3 ^3 as @e[tag=sp.selected,tag=sp.label_reference,limit=1] run tp @s ~ ~ ~",
        "function space_editor:proxy_spike/sync")
    sync = ["execute as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value \"standing\"",
            "execute if predicate space_editor:proxy_spike/crouching as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value \"crouching\"",
            "execute if predicate space_editor:proxy_spike/swimming as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value \"swimming\"",
            "execute if predicate space_editor:proxy_spike/fall_flying as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value \"fall_flying\""]
    for slot in ("armor.head", "armor.chest", "armor.legs", "armor.feet", "weapon.mainhand", "weapon.offhand"):
        sync.append(f"item replace entity @e[tag=sp.selected,type=minecraft:mannequin] {slot} from entity @s {slot}")
    put("sync", *sync)
    put("swing_main", "function space_editor:proxy_spike/select", "swing @e[tag=sp.selected,type=minecraft:mannequin] mainhand")
    put("swing_off", "function space_editor:proxy_spike/select", "swing @e[tag=sp.selected,type=minecraft:mannequin] offhand")
    put("status",
        "function space_editor:proxy_spike/ensure_owner",
        "scoreboard players add @s sp.follow 0",
        "scoreboard players add @s sp.flip 0",
        "scoreboard players add @s sp.name 0",
        "function space_editor:proxy_spike/select",
        'tellraw @s [{text:"[06-1] owned mannequins: "},{selector:"@e[tag=sp.selected,type=minecraft:mannequin]"},{text:" | follow="},{score:{name:"@s",objective:"sp.follow"}},{text:" flip="},{score:{name:"@s",objective:"sp.flip"}},{text:" name mode="},{score:{name:"@s",objective:"sp.name"}}]')
    predicate_dir = ROOT / "space_editor_datapack/data/space_editor/predicate/proxy_spike"
    predicate_dir.mkdir(parents=True, exist_ok=True)
    for name, flag in (("crouching", "is_sneaking"), ("swimming", "is_swimming"), ("fall_flying", "is_fall_flying")):
        (predicate_dir / (name + ".json")).write_text(
            '{"condition":"minecraft:entity_properties","entity":"this","predicate":{"flags":{"' + flag + '":true}}}\n',
            encoding="utf-8",
        )


if __name__ == "__main__":
    build()
