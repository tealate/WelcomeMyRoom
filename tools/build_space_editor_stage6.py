"""Stage06 production projections. Reuses Stage05 mapping and Stage06-1 appearance.

No world edits, recursive projection, or pack-specific dimensions. Persistent
configuration lives in document.projection; active paths live in projection storage.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
P = "storage space_editor:projection"
R = "storage space_editor:runtime"
D = "storage space_editor:document"
DIMS = ("overworld", "the_nether", "the_end")


def generate(stage5):
    global fn, F, read_fixed
    F = stage5.F
    fn = lambda name, lines: stage5.fn("projection/" + name, lines)
    read_fixed = stage5.read_fixed
    stage5.append(F / "load.mcfunction", ["function space_editor:projection/load"])
    stage5.insert_before(F / "tick.mcfunction", "function space_editor:teleport/tick", ["function space_editor:projection/maintenance"])
    stage5.insert_before(F / "teleport/tick.mcfunction", "function #space_editor:before_teleport", ["function space_editor:projection/before"])
    stage5.insert_before(F / "teleport/tick.mcfunction", "function #space_editor:after_teleport", ["function space_editor:projection/after"])
    lifecycle()
    contacts()
    routing()
    rendering()
    transfers()
    controls()
    demo()


def drain(name, queue, step, capacity=256):
    fn(name + "_16", [f"execute unless data {P} {queue}[0] run return 0"] +
       [f"execute if data {P} {queue}[0] run function space_editor:projection/{step}"] * 16)
    fn(name, [f"execute if data {P} {queue}[0] run function space_editor:projection/{name}_16"] * ((capacity + 15)//16))


def delete_entities(extra=""):
    """Queue mannequins for hidden disposal; text displays have no death animation."""
    return [line for dim in DIMS for line in (
        f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=space_editor.proxy{extra}] run function space_editor:projection/delete/start",
        f"execute in minecraft:{dim} run kill @e[type=minecraft:text_display,tag=space_editor.proxy{extra}]",
    )]


def lifecycle():
    fn("load", [
        *[f"scoreboard objectives add pr.{n} dummy" for n in ("owner", "id", "epoch", "debug", "gc", "remove", "v")],
        "scoreboard objectives add pr.leave minecraft.custom:minecraft.leave_game",
        "scoreboard players add #owner pr.owner 0", "scoreboard players add #epoch pr.epoch 1",
        "team add pr_hidden", "team modify pr_hidden nametagVisibility never", "team modify pr_hidden collisionRule never",
        f'execute unless data {D} projection run data modify {D} projection set value {{enabled:0b,debugMaps:[],visual:{{standing:1900,crouching:1600,swimming:700,fall_flying:700,sleeping:300}},labelGap:300}}',
        f"execute unless data {P} active run data modify {P} active set value []",
        f"execute unless data {P} players run data modify {P} players set value []",
        f"execute unless data {P} nextId run data modify {P} nextId set value 1",
        f"data modify {P} schema set value 1", *delete_entities(),
    ])
    fn("enable", [f"data modify {D} projection.enabled set value 1b", 'tellraw @s {text:"Stage06 有効: playモードでSpaceLinkへ侵入すると投影します",color:"aqua"}'])
    fn("disable", [f"data modify {D} projection.enabled set value 0b", "function space_editor:projection/clear"])
    fn("clear", [f"data modify {P} active set value []", f"data modify {P} players set value []",
        "scoreboard players add #epoch pr.epoch 1", *delete_entities()])
    fn("maintenance", [
        # Deleting mannequins are detached from projection tags. Two ticks allow
        # invisibility/equipment packets to arrive, then death happens four ticks
        # after a same-chunk teleport to an in-bounds disposal height.
        *[line for dim,y in (("overworld",-63),("the_nether",1),("the_end",1)) for line in (
            f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=pr.removing,scores={{pr.remove=1..}}] at @s if dimension minecraft:{dim} run scoreboard players remove @s pr.remove 1",
            f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=pr.removing,scores={{pr.remove=4}}] at @s if dimension minecraft:{dim} run tp @s ~ {y} ~",
            f"execute in minecraft:{dim} as @e[type=minecraft:mannequin,tag=pr.removing,scores={{pr.remove=..0}}] at @s if dimension minecraft:{dim} run kill @s",
        )],
        # Also cleans late-loaded entities while disabled, editing, or owners offline.
        *[line for dim in DIMS for typ in ("mannequin", "text_display") for line in (
            f"execute in minecraft:{dim} run scoreboard players add @e[type=minecraft:{typ},tag=space_editor.proxy] pr.gc 0",
            f"execute in minecraft:{dim} run scoreboard players remove @e[type=minecraft:{typ},tag=space_editor.proxy,scores={{pr.gc=1..}}] pr.gc 1",
            f"execute in minecraft:{dim} as @e[type=minecraft:{typ},tag=space_editor.proxy,scores={{pr.gc=..0}},limit=16] run function space_editor:projection/gc_entity")],
        f"execute if data {D} {{editMode:1b}} run function space_editor:projection/hide_all",
    ])
    fn("hide_all", delete_entities())
    fn("delete/start", [
        "scoreboard players operation #delete pr.id = @s pr.id",
        *[f"execute if entity @s[tag={tag}] in minecraft:{dim} as @e[type=minecraft:text_display,tag=space_editor.proxy,tag={tag}] if score @s pr.id = #delete pr.id run kill @s"
          for tag in ("pr.production", "pr.debug") for dim in DIMS],
        "tag @s add pr.removing", "tag @s remove space_editor.proxy",
        "tag @s remove pr.production", "tag @s remove pr.debug", "tag @s remove pr.new",
        "effect give @s minecraft:invisibility infinite 0 true",
        *[f"item replace entity @s {slot} with minecraft:air" for slot in ("armor.head","armor.chest","armor.legs","armor.feet","weapon.mainhand","weapon.offhand")],
        "scoreboard players set @s pr.remove 6",
    ])
    fn("delete/self", ["execute if entity @s[type=minecraft:mannequin] run return run function space_editor:projection/delete/start", "kill @s"])
    fn("gc_entity", [
        "scoreboard players set @s pr.gc 40",
        "execute unless score @s pr.epoch = #epoch pr.epoch run return run function space_editor:projection/delete/self",
        f"execute unless data {D} projection{{enabled:1b}} run return run function space_editor:projection/delete/self",
        f"execute store result {P} gc.id int 1 run scoreboard players get @s pr.id",
        f"execute store result {P} gc.owner int 1 run scoreboard players get @s pr.owner",
        f"function space_editor:projection/gc_check with {P} gc",
    ])
    fn("gc_check", [
        f'$execute unless entity @a[scores={{pr.owner=$(owner)}},gamemode=!spectator,nbt={{DeathTime:0s}}] run return run function space_editor:projection/delete/self',
        f'$execute unless data {P} active[{{id:$(id),owner:$(owner)}}] run function space_editor:projection/delete/self',
    ])
    fn("register", [
        "scoreboard players add @s pr.owner 0", "scoreboard players add @s pr.leave 0", "scoreboard players add @s pr.debug 0",
        "execute if score @s pr.owner matches 0 run scoreboard players add #owner pr.owner 1",
        "execute if score @s pr.owner matches 0 run scoreboard players operation @s pr.owner = #owner pr.owner",
        f"execute store result {P} actor.id int 1 run scoreboard players get @s pr.owner",
        f"execute store result {P} actor.leave int 1 run scoreboard players get @s pr.leave",
        f"data modify {P} actor.uuid set from entity @s UUID",
        f"function space_editor:projection/register_actor with {P} actor",
    ])
    fn("register_actor", [
        f'$execute unless data {P} players[{{id:$(id),uuid:$(uuid),leave:$(leave)}}] run function space_editor:projection/remove_owner with {P} actor',
        f'$execute unless data {P} players[{{id:$(id),uuid:$(uuid),leave:$(leave)}}] run data remove {P} active[{{owner:$(id)}}]',
        f'$execute unless data {P} players[{{id:$(id),uuid:$(uuid),leave:$(leave)}}] run data remove {P} players[{{id:$(id)}}]',
        f'$execute unless data {P} players[{{id:$(id)}}] run data modify {P} players append value {{id:$(id),uuid:$(uuid),leave:$(leave),previous:[],next:[]}}',
        f'$data modify {P} players[{{id:$(id)}}].next set value []',
    ])


def contacts():
    fn("before", [
        f"execute unless data {D} projection{{enabled:1b}} run return 0",
        "scoreboard players set #spawn pr.v 8", "scoreboard players set #blocked pr.v 0",
        "execute as @a[gamemode=!spectator,nbt={DeathTime:0s}] at @s run function space_editor:projection/register",
        f"data modify {P} contacts set from {R} spaceLinkContacts",
        "scoreboard players set #updates pr.v 24",
        f"execute store result score #contacts pr.v run data get {P} contacts",
        "execute if score #contacts pr.v matches 64.. run scoreboard players set #updates pr.v 8",
        "execute if score #contacts pr.v matches 64.. if entity @a[scores={pr.debug=1}] run scoreboard players set #updates pr.v 4",
        "function space_editor:projection/contact_scan",
        f"data modify {P} actorQueue set from {P} players", "function space_editor:projection/finish_players",
        f"data modify {P} work set from {P} active", f"data modify {P} done set value []",
        *[f"execute if score #updates pr.v matches {i}.. if data {P} work[0] run function space_editor:projection/route_step" for i in range(1,25)],
        f"data modify {P} active set from {P} work", f"data modify {P} active append from {P} done[]",
    ])
    drain("contact_scan", "contacts", "contact_next", 4096)
    fn("contact_next", [
        f"data modify {P} contact set from {P} contacts[0]", f"data remove {P} contacts[0]",
        f"function space_editor:projection/contact_owner with {P} contact",
    ])
    fn("contact_owner", [
        f'$execute store result {P} contact.owner int 1 run scoreboard players get @a[nbt={{UUID:$(uuid)}},limit=1] pr.owner',
        f"function space_editor:projection/contact with {P} contact",
    ])
    fn("contact", [
        f'$execute unless data {P} players[{{id:$(owner)}}].next[{{groupId:$(spaceLinkGroupId),sourceId:$(sourceRegionId)}}] run data modify {P} players[{{id:$(owner)}}].next append value {{groupId:$(spaceLinkGroupId),sourceId:$(sourceRegionId)}}',
        f'$execute if data {P} players[{{id:$(owner)}}].previous[{{groupId:$(spaceLinkGroupId),sourceId:$(sourceRegionId)}}] run return 0',
        f'$data remove {P} active[{{owner:$(owner),groupId:$(spaceLinkGroupId),entrySourceId:$(sourceRegionId),targetId:$(targetRegionId),sourceInstanceId:$(instanceId),suspended:1b}}]',
        f'$execute if data {P} active[{{owner:$(owner),groupId:$(spaceLinkGroupId),entrySourceId:$(sourceRegionId),targetId:$(targetRegionId),sourceInstanceId:$(instanceId)}}] run return 0',
        f'execute if data {P} contact{{targetRoomId:""}} run return run scoreboard players add #blocked pr.v 1',
        f'$execute unless data {D} regions[{{kind:"proxy_existence",roomId:"$(targetRoomId)"}}] run return run scoreboard players add #blocked pr.v 1',
        f'execute store result score #count pr.v run data get {P} active',
        'execute if score #count pr.v matches 256.. run return run scoreboard players add #blocked pr.v 1',
        f'$data modify {P} new set value {{owner:$(owner),uuid:$(uuid),groupId:$(spaceLinkGroupId),entrySourceId:$(sourceRegionId),sourceId:$(sourceRegionId),targetId:$(targetRegionId),sourceInstanceId:$(instanceId),currentInstanceId:$(instanceId),targetInstanceId:0}}',
        f"data modify {P} new.id set from {P} nextId",
        f"execute store result score #next pr.v run data get {P} nextId", "scoreboard players add #next pr.v 1",
        f"execute store result {P} nextId int 1 run scoreboard players get #next pr.v",
        f"data modify {P} active append from {P} new",
    ])
    drain("finish_players", "actorQueue", "finish_player")
    fn("finish_player", [f"function space_editor:projection/finish_actor with {P} actorQueue[0]", f"data remove {P} actorQueue[0]"])
    fn("finish_actor", [
        f'$execute unless entity @a[scores={{pr.owner=$(id)}},nbt={{UUID:$(uuid),DeathTime:0s}},gamemode=!spectator] run function space_editor:projection/remove_owner with {P} actorQueue[0]',
        f'$execute unless entity @a[scores={{pr.owner=$(id)}},nbt={{UUID:$(uuid),DeathTime:0s}},gamemode=!spectator] run data remove {P} active[{{owner:$(id)}}]',
        f'$execute unless entity @a[scores={{pr.owner=$(id)}},nbt={{UUID:$(uuid),DeathTime:0s}},gamemode=!spectator] run return run data remove {P} players[{{id:$(id)}}]',
        f'$data modify {P} players[{{id:$(id)}}].previous set from {P} players[{{id:$(id)}}].next'])


def routing():
    fn("route_step", [
        f"data modify {P} route set from {P} work[0]", f"data remove {P} work[0]",
        "scoreboard players set #valid pr.v 0", f"function space_editor:projection/route_actor with {P} route",
        f"execute if score #valid pr.v matches 1 run data modify {P} done append from {P} route",
        f"execute unless score #valid pr.v matches 1 run function space_editor:projection/remove_render with {P} route",
    ])
    fn("route_actor", [f'$execute as @a[scores={{pr.owner=$(owner)}},nbt={{UUID:$(uuid),DeathTime:0s}},gamemode=!spectator,limit=1] at @s run function space_editor:projection/update with {P} route'])
    fn("update", [
        f'$execute unless score @s se.instance matches $(currentInstanceId) run return 0',
        f'$execute unless data {D} spaceLinkGroups[{{id:$(groupId),members:[$(sourceId),$(targetId)]}}] run return 0',
        f"data modify {R} map set value {{}}",
        f'$data modify {R} map.source set from {D} regions[{{id:$(sourceId),kind:"space_link",spaceLinkGroupId:$(groupId)}}]',
        f'$data modify {R} map.target set from {D} regions[{{id:$(targetId),kind:"space_link",spaceLinkGroupId:$(groupId)}}]',
        f"execute unless data {R} map.source.id run return 0", f"execute unless data {R} map.target.id run return 0",
        f'execute if data {P} route{{suspended:1b}} run return run function space_editor:projection/suspended with {P} route',
        f"function space_editor:projection/source_dimension with {R} map.source", "execute unless score #dimension pr.v matches 1 run return 0",
        f"data modify {R} map.point set from entity @s Pos", f"data modify {R} map.yaw set from entity @s Rotation[0]", f"data modify {R} map.pitch set from entity @s Rotation[1]",
        # Use the already validated/calculated Stage05 contact while still inside.
        f'$data modify {R} map.result set from {R} spaceLinkContacts[{{uuid:$(uuid),sourceRegionId:$(sourceId),targetRegionId:$(targetId)}}].destination',
        f"execute unless data {R} map.result run function space_editor:mapping/position",
        f"data modify {P} route.point set from {R} map.result.point",
        f"data modify {P} route.roomId set from {R} map.target.roomId",
        f"data modify {P} route.dimension set from {R} map.target.dimension",
        f"data modify {P} route.targetInstanceId set value 0",
        f"execute if data {R} map.target.instanceId run data modify {P} route.targetInstanceId set from {R} map.target.instanceId",
        f"data modify {P} exists set value []", f"function space_editor:projection/existence_lookup with {P} route",
        "scoreboard players set #exists pr.v 0",
        f"data modify {R} projectionPoint set from {P} route.point",
        *[line for i,a in enumerate("xyz") for line in read_fixed(f"projectionPoint[{i}]",f"#sp{a}")],
        "function space_editor:projection/existence_scan", "execute unless score #exists pr.v matches 1 run return 0",
        "scoreboard players set #valid pr.v 1",
        f"data modify {P} sourceFrame set from {R} map.source", f"data modify {P} targetFrame set from {R} map.target",
        "function space_editor:projection/appearance",
        f"data modify {P} render set from {P} route", f"data modify {P} render.result set from {R} map.result",
        f"data modify {P} render.debug set value 0", "function space_editor:projection/prepare_render",
        f"function space_editor:projection/render_production with {P} render",
        f"execute if score @s pr.debug matches 1 run function space_editor:projection/debug_resolve with {P} route",
        f"execute unless score @s pr.debug matches 1 run function space_editor:projection/remove_debug with {P} route",
    ])
    fn("source_dimension", ["scoreboard players set #dimension pr.v 0", '$execute if dimension $(dimension) run scoreboard players set #dimension pr.v 1'])
    fn("suspended", [f'$execute unless data {D} regions[{{kind:"proxy_existence",roomId:"$(roomId)",dimension:"$(dimension)"}}] run return 0',
        "scoreboard players set #valid pr.v 1", f"function space_editor:projection/remove_render with {P} route"])
    fn("existence_lookup", [f'$data modify {P} exists append from {D} regions[{{kind:"proxy_existence",roomId:"$(roomId)",dimension:"$(dimension)"}}]'])
    fn("existence_scan", [
        f"execute unless data {P} exists[0] run return 0", "execute if score #exists pr.v matches 1 run return 0",
        f"data modify {R} spatialRegion set from {P} exists[0]",
        f"function space_editor:projection/existence_check with {P} exists[0]", f"data remove {P} exists[0]",
        f"execute if data {P} exists[0] run function space_editor:projection/existence_scan",
    ])
    fn("existence_check", [f'$execute in $(dimension) run function space_editor:mapping/contains with {R} spatialRegion', "execute if score #inside se.v matches 1 run scoreboard players set #exists pr.v 1"])
    fn("appearance", [
        f'data modify {P} pose set value "standing"',
        *[f'execute if predicate space_editor:proxy_spike/{pose} run data modify {P} pose set value "{pose}"' for pose in ("crouching","swimming","fall_flying")],
        f'execute if data entity @s sleeping_pos run data modify {P} pose set value "sleeping"',
    ])
    fn("prepare_render", [
        f"data modify {P} render.pose set from {P} pose",
        f"data modify {P} render.dimension set from {P} render.result.dimension",
        *[f"data modify {P} render.{k} set from {P} render.result.{k}" for k in ("x","y","z","yaw","pitch")],
        "scoreboard players set #flip pr.v 0",
        f'execute if data {P} sourceFrame{{flipY:1b}} run scoreboard players add #flip pr.v 1',
        f'execute if data {R} map.target{{flipY:1b}} run scoreboard players add #flip pr.v 1',
        "execute if score #flip pr.v matches 2 run scoreboard players set #flip pr.v 0",
        f"execute store result {P} render.flip int 1 run scoreboard players get #flip pr.v",
        f"function space_editor:projection/height with {P} render",
    ])
    fn("height", [
        # Vanilla renderer pivots by getBbHeight()+0.1. Logical point remains unchanged.
        f'$execute store result score #height pr.v run data get {D} projection.visual.$(pose)',
        f"execute store result score #y pr.v run data get {P} render.y 2000",
        "scoreboard players operation #offset pr.v = #height pr.v", "scoreboard players operation #offset pr.v += #height pr.v",
        "execute if score #flip pr.v matches 1 run scoreboard players operation #y pr.v -= #offset pr.v",
        f"execute store result {P} render.y double 0.0005 run scoreboard players get #y pr.v",
        "scoreboard players operation #nameY pr.v = #y pr.v",
        f"execute store result score #gap pr.v run data get {D} projection.labelGap 2",
        "execute if score #flip pr.v matches 0 run scoreboard players operation #nameY pr.v += #offset pr.v",
        "execute if score #flip pr.v matches 0 run scoreboard players remove #nameY pr.v 200",
        "execute if score #flip pr.v matches 0 run scoreboard players operation #nameY pr.v += #gap pr.v",
        "execute if score #flip pr.v matches 1 run scoreboard players operation #nameY pr.v -= #gap pr.v",
        # Rotating text 180 degrees shifts the visible glyph around its baseline.
        # Move only the inverted formal label 0.1 block back toward the head.
        "execute if score #flip pr.v matches 1 run scoreboard players add #nameY pr.v 200",
        f"execute store result {P} render.nameY double 0.0005 run scoreboard players get #nameY pr.v",
    ])
    fn("remove_render", ["$" + line.replace("]", ",scores={pr.id=$(id)}]", 1) for line in delete_entities()])
    fn("remove_debug", ["$" + line.replace("]", ",scores={pr.id=$(id)}]", 1) for line in delete_entities(",tag=pr.debug")])
    fn("remove_owner", ["$" + line.replace("]", ",scores={pr.owner=$(id)}]", 1) for line in delete_entities()])


def rendering():
    for kind, debug in (("production", False), ("debug", True)):
        tag = "pr.debug" if debug else "pr.production"
        body = f'@e[type=minecraft:mannequin,tag=space_editor.proxy,tag={tag},scores={{pr.id=$(id)}},limit=1]'
        label = f'@e[type=minecraft:text_display,tag=space_editor.proxy,tag={tag},scores={{pr.id=$(id)}},limit=1]'
        fn("render_"+kind, [
            *([] if debug else [f'$execute if data {P} route{{sourceId:$(targetId)}} run return run function space_editor:projection/hide_production with {P} route']),
            f'$execute in $(dimension) positioned 0.0 0.0 0.0 positioned ~$(x) ~$(y) ~$(z) unless loaded ~ ~ ~ run return run function space_editor:projection/hide_{kind} with {P} render',
            f'$execute in $(dimension) positioned 0.0 0.0 0.0 positioned ~$(x) ~$(y) ~$(z) unless entity @a[distance=..96] run return run function space_editor:projection/hide_{kind} with {P} render',
            f'$execute in $(dimension) unless entity {body} if score #spawn pr.v matches 1.. run function space_editor:projection/spawn_{kind} with {P} render',
            f'$execute in $(dimension) unless entity {body} run return 0',
            f'$execute in $(dimension) unless entity {label} run function space_editor:projection/label_{kind} with {P} render',
            f'$execute in $(dimension) if data {P} render{{flip:1}} as {label} run data merge entity @s {{transformation:{{left_rotation:[0f,0f,1f,0f]}}}}',
            f'$execute in $(dimension) if data {P} render{{flip:0}} as {label} run data merge entity @s {{transformation:{{left_rotation:[0f,0f,0f,1f]}}}}',
            f'$execute in $(dimension) as {body} run function space_editor:proxy_spike/set_pose with {P} render',
            f'$execute in $(dimension) if data {P} render{{flip:1}} as {body} unless data entity @s {{CustomName:"Dinnerbone"}} run data modify entity @s CustomName set value "Dinnerbone"',
            f'$execute in $(dimension) if data {P} render{{flip:0}} run data remove entity {body} CustomName',
            *[f'$execute in $(dimension) run item replace entity {body} {slot} from entity @s {slot}' for slot in ("armor.head","armor.chest","armor.legs","armor.feet","weapon.mainhand","weapon.offhand")],
            f'$execute in $(dimension) positioned 0.0 0.0 0.0 run tp {body} ~$(x) ~$(y) ~$(z) $(yaw) $(pitch)',
            f'$execute in $(dimension) positioned 0.0 0.0 0.0 run tp {label} ~$(x) ~$(nameY) ~$(z)',
        ])
        fn("spawn_"+kind, [
            "scoreboard players remove #spawn pr.v 1",
            f'$execute in $(dimension) positioned 0.0 0.0 0.0 run summon minecraft:mannequin ~$(x) ~$(y) ~$(z) {{Tags:["space_editor.proxy","{tag}","pr.new"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hidden_layers:[],hide_description:1b,CustomNameVisible:0b,profile:{{id:$(uuid)}}}}',
            f'$execute in $(dimension) run scoreboard players set @e[type=minecraft:mannequin,tag=pr.new,limit=1] pr.id $(id)',
            f'$execute in $(dimension) run scoreboard players set {body} pr.owner $(owner)',
            f'$execute in $(dimension) run scoreboard players operation {body} pr.epoch = #epoch pr.epoch',
            f'$execute in $(dimension) run team join pr_hidden {body}',
            f'$execute in $(dimension) run tag {body} remove pr.new',
        ])
        text = '{selector:"@a[nbt={UUID:$(uuid)}]"}'
        if debug:
            text = '[{selector:"@a[nbt={UUID:$(uuid)}]"},{text:" [G$(groupId) $(entrySourceId)→$(targetId) / #$(id)]",color:"aqua"}]'
        fn("label_"+kind, [
            f'$execute in $(dimension) positioned 0.0 0.0 0.0 run summon minecraft:text_display ~$(x) ~$(nameY) ~$(z) {{Tags:["space_editor.proxy","{tag}","pr.new"],billboard:"center",background:1073741824,view_range:0.5f,teleport_duration:3,shadow:0b,see_through:0b,text:{text}}}',
            f'$execute in $(dimension) run scoreboard players set @e[type=minecraft:text_display,tag=pr.new,limit=1] pr.id $(id)',
            f'$execute in $(dimension) run scoreboard players set {label} pr.owner $(owner)',
            f'$execute in $(dimension) run scoreboard players operation {label} pr.epoch = #epoch pr.epoch',
            f'$execute in $(dimension) run tag {label} remove pr.new',
        ])
        fn("hide_"+kind, ["$" + line.replace("]", ",scores={pr.id=$(id)}]", 1) for line in delete_entities(f",tag={tag}")])
    fn("debug_resolve", [
        f"data remove {P} debugMap", f'$data modify {P} debugMap set from {D} projection.debugMaps[{{uuid:$(uuid),targetId:$(targetId)}}]',
        f"execute unless data {P} debugMap.regionId run return run function space_editor:projection/remove_debug with {P} route",
        f"function space_editor:projection/debug_frame with {P} debugMap",
    ])
    fn("debug_frame", [
        f"data remove {R} map.target", f'$data modify {R} map.target set from {D} regions[{{id:$(regionId)}}]',
        f"execute unless data {R} map.target.id run return run function space_editor:projection/remove_debug with {P} route",
        f"data modify {R} map.source set from {P} sourceFrame", f"data modify {R} map.point set from entity @s Pos",
        f"data modify {R} map.yaw set from entity @s Rotation[0]", f"data modify {R} map.pitch set from entity @s Rotation[1]",
        "function space_editor:mapping/position",
        f"data modify {P} render set from {P} route", f"data modify {P} render.result set from {R} map.result", f"data modify {P} render.debug set value 1",
        "function space_editor:projection/prepare_render", f"function space_editor:projection/render_debug with {P} render",
    ])


def transfers():
    fn("after", [f"execute unless data {D} projection{{enabled:1b}} run return 0",
        f"data modify {P} transfers set from {R} transfers", "function space_editor:projection/transfer_scan"])
    drain("transfer_scan", "transfers", "transfer_next", 64)
    fn("transfer_next", [f"data modify {P} transfer set from {P} transfers[0]", f"data remove {P} transfers[0]",
        f"data modify {P} rebases set value []", f"data modify {P} rebaseQueue set from {P} active", "function space_editor:projection/rebase_scan"])
    drain("rebase_scan", "rebaseQueue", "rebase_next")
    fn("rebase_next", [f"data modify {P} rebase set from {P} rebaseQueue[0]", f"data remove {P} rebaseQueue[0]",
        f"function space_editor:projection/rebase_owner with {P} transfer"])
    fn("rebase_owner", [f'$execute unless data {P} rebase{{uuid:$(uuid)}} run return 0',
        f"function space_editor:projection/rebase_path with {P} rebase"])
    fn("rebase_path", [
        f"data remove {P} resolved", f'$data modify {P} resolved set from {P} rebases[{{groupId:$(groupId),oldSource:$(sourceId)}}]',
        f"execute unless data {P} resolved run function space_editor:projection/rebase_find with {P} rebase",
        f"execute if data {P} resolved.sourceId run function space_editor:projection/rebase_commit with {P} rebase",
        f"execute unless data {P} resolved.sourceId run data modify {P} warning set value \"unresolved_transfer_source: retained path suspended until valid source is known\"",
        f'$execute unless data {P} resolved.sourceId run data modify {P} active[{{id:$(id)}}].suspended set value 1b',
    ])
    fn("rebase_find", [
        f'$data modify {P} resolved set value {{groupId:$(groupId),oldSource:$(sourceId)}}',
        f"data remove {P} oldFrame", f'$data modify {P} oldFrame set from {D} regions[{{id:$(sourceId)}}]',
        f"function space_editor:projection/rebase_basis with {P} transfer",
        f"data modify {P} candidates set value []", f'$data modify {P} candidates append from {D} regions[{{kind:"space_link",spaceLinkGroupId:$(groupId)}}]',
        "function space_editor:projection/candidate_scan",
        f"data modify {P} rebases append from {P} resolved",
    ])
    fn("candidate_scan", [
        f"execute unless data {P} candidates[0] run return 0", f"execute if data {P} resolved.sourceId run return 0",
        f"function space_editor:projection/candidate with {P} candidates[0]", f"data remove {P} candidates[0]",
        f"execute if data {P} candidates[0] run function space_editor:projection/candidate_scan",
    ])
    fn("candidate", [
        f'$execute unless data {P} transfer.destination{{dimension:"$(dimension)"}} run return 0',
        f'execute store result score #candidateRot pr.v run data get {P} candidates[0].rotationY',
        f'execute store result score #candidateFlip pr.v run data get {P} candidates[0].flipY',
        "execute unless score #candidateRot pr.v = #desiredRot pr.v run return 0",
        "execute unless score #candidateFlip pr.v = #desiredFlip pr.v run return 0",
        # Compare inverse mapping of post-TP point to the immutable pre-TP snapshot.
        # This disambiguates multiple anchors with the same RoomID.
        f"data modify {R} map set value {{}}", f"data modify {R} map.source set from {P} candidates[0]",
        f"function space_editor:projection/rebase_old_frame with {P} rebase",
        f"execute unless data {R} map.target.id run return 0",
        f"data modify {R} map.point set from {P} transfer.destination.point",
        "function space_editor:mapping/position",
        f"data modify {R} projectionPrePoint set from {P} transfer.point",
        *[line for i,a in enumerate("xyz") for line in (
            *read_fixed(f"projectionPrePoint[{i}]",f"#pr_pre_{a}"),
            f"scoreboard players operation #pr_pre_{a} se.v -= #map_o{a} se.v",
            f"execute unless score #pr_pre_{a} se.v matches -1..1 run return 0")],
        f'$data modify {P} resolved.sourceId set value $(id)',
    ])
    fn("rebase_basis", [
        f'$data modify {P} tpSource set from {D} regions[{{id:$(sourceRegionId)}}]',
        f'$data modify {P} tpTarget set from {D} regions[{{id:$(targetRegionId)}}]',
        f"execute store result score #desiredRot pr.v run data get {P} oldFrame.rotationY",
        f"execute store result score #basis pr.v run data get {P} tpSource.rotationY", "scoreboard players operation #desiredRot pr.v -= #basis pr.v",
        f"execute store result score #basis pr.v run data get {P} tpTarget.rotationY", "scoreboard players operation #desiredRot pr.v += #basis pr.v",
        "scoreboard players set #circle pr.v 360", "scoreboard players operation #desiredRot pr.v %= #circle pr.v",
        f"execute store result score #desiredFlip pr.v run data get {P} oldFrame.flipY",
        f"execute store result score #basis pr.v run data get {P} tpSource.flipY", "scoreboard players operation #desiredFlip pr.v += #basis pr.v",
        f"execute store result score #basis pr.v run data get {P} tpTarget.flipY", "scoreboard players operation #desiredFlip pr.v += #basis pr.v",
        "scoreboard players set #two pr.v 2", "scoreboard players operation #desiredFlip pr.v %= #two pr.v",
    ])
    fn("rebase_old_frame", [f'$data modify {R} map.target set from {D} regions[{{id:$(sourceId),spaceLinkGroupId:$(groupId)}}]'])
    fn("rebase_commit", [
        f'$data remove {P} active[{{id:$(id)}}].suspended',
        f'$data modify {P} active[{{id:$(id)}}].sourceId set from {P} resolved.sourceId',
        f"data modify {P} arrived.groupId set from {P} resolved.groupId", f"data modify {P} arrived.sourceId set from {P} resolved.sourceId",
        f'$data modify {P} players[{{id:$(owner)}}].previous append from {P} arrived',
    ])


def controls():
    fn("debug/on", ["scoreboard players set @s pr.debug 1", 'tellraw @s {text:"Debug ON: debug/mapで投影先に対応するRegionを指定してください",color:"aqua"}'])
    fn("debug/off", ["scoreboard players set @s pr.debug 0", f"execute store result {P} actor.id int 1 run scoreboard players get @s pr.owner", f"function space_editor:projection/debug/clear_owner with {P} actor"])
    fn("debug/clear_owner", ["$" + line.replace("]", ",scores={pr.owner=$(id)}]", 1) for line in delete_entities(",tag=pr.debug")])
    fn("debug/map", [
        f'$execute unless data {D} regions[{{id:$(target),kind:"space_link"}}] run return 0', f'$execute unless data {D} regions[{{id:$(region)}}] run return 0',
        f'$data modify {P} config set value {{targetId:$(target),regionId:$(region)}}', f"data modify {P} config.uuid set from entity @s UUID",
        f"function space_editor:projection/debug/save with {P} config",
    ])
    fn("debug/save", [f'$data remove {D} projection.debugMaps[{{uuid:$(uuid),targetId:$(targetId)}}]', f"data modify {D} projection.debugMaps append from {P} config"])
    fn("visual", [f'$execute unless data {D} projection.visual.$(pose) run return 0',
        f'$data modify {P} visualInput set value $(pivot)', f"execute store result score #pivot pr.v run data get {P} visualInput 1000",
        "execute unless score #pivot pr.v matches 0..4000 run return 0",
        f'$execute store result {D} projection.visual.$(pose) int 1 run scoreboard players get #pivot pr.v'])
    fn("status", [f"data get {D} projection", f"data get {P} active", 'tellraw @s [{text:"projection blocked entries="},{score:{name:"#blocked",objective:"pr.v"}}]'])
    fn("help", ['tellraw @s ' + json.dumps({"text": t, "color": "aqua"},ensure_ascii=False) for t in (
        "Stage06: /function space_editor:projection/enable → space_editor:play → SpaceLinkへ外から侵入",
        "各SpaceLinkにspace_group/set_room、存在範囲にproxy_existence/set_roomで同じroomIdを設定",
        'projection/debug/map {target:3,region:7} → projection/debug/on / off',
        "projection/status / clear（経路と侵入履歴を初期化、内部でも再生成） / disable",
        'projection/visual {pose:"standing",pivot:1.9} は反転ピボット補正。詳細 docs/stage06-projection.md',
        'projection/demo/setup: 地形変更なしの3部屋検証配置 / demo/teleport: TP追加 / demo/cleanup: この配置だけ削除',
    )])
    fn("swing", [f"execute store result {P} actor.id int 1 run scoreboard players get @s pr.owner", f"function space_editor:projection/swing_owner with {P} actor"])
    fn("swing_owner", [f'$execute in minecraft:{dim} run swing @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={{pr.owner=$(id)}}] mainhand' for dim in DIMS])
    fn("attack", ["advancement revoke @s only space_editor:projection/attack", f"execute if data {D} projection{{enabled:1b}} run function space_editor:projection/swing"])
    path = ROOT / "space_editor_datapack/data/space_editor/advancement/projection/attack.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps({"criteria":{"hit":{"trigger":"minecraft:player_hurt_entity","conditions":{"damage":{"type":{"direct_entity":{"type":"minecraft:player"}}}}}},"rewards":{"function":"space_editor:projection/attack"}})+"\n").encode())


def demo():
    """Optional additive setup through existing Region/group/pair editing APIs."""
    edit_guard = 'execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {text:"別プレイヤーの編集終了後に実行してください",color:"red"}'
    def box(key, bounds):
        lines = [f"data modify {P} demo.{key} set from {D} nextId",
                 f"data modify {R} selection set value {{a:[I;0,0,0],b:[I;0,0,0]}}",
                 f"data modify {R} selection.dimension set from {P} demo.dimension"]
        for end, values in zip(("a","b"), bounds):
            for i,(axis,offset) in enumerate(zip("xyz",values)):
                lines += [f"scoreboard players operation #demo_tmp pr.v = #demo_{axis} pr.v",
                          f"scoreboard players {'add' if offset >= 0 else 'remove'} #demo_tmp pr.v {abs(offset)}",
                          f"execute store result {R} selection.{end}[{i}] int 1 run scoreboard players get #demo_tmp pr.v"]
        lines += ["function space_editor:region/create", f"function space_editor:projection/demo/remember_{key} with {P} demo"]
        return lines
    for key in ("a","b","c","ea","eb","ec","db","dc","ta","tb"):
        fn("demo/remember_"+key, [f'$execute if data {D} regions[{{id:$({key})}}] run data modify {P} demo.ids append value {{id:$({key})}}',
                                f"data modify {D} projection.demo set from {P} demo"])
    setup = ["execute unless entity @s[type=minecraft:player] run return 0",
             edit_guard,
             f"execute if data {D} projection.demo run return run function space_editor:projection/demo/status",
             f"data modify {P} demo set value {{ids:[]}}", f"data modify {P} demo.uuid set from entity @s UUID",
             *[f'execute if dimension minecraft:{dim} run data modify {P} demo.dimension set value "minecraft:{dim}"' for dim in DIMS],
             *[line for i,a in enumerate("xyz") for line in (
                 f"execute store result score #demo_{a} pr.v run data get entity @s Pos[{i}]",
                 f"execute store result {P} demo.{a} int 1 run scoreboard players get #demo_{a} pr.v")],
             *[f'execute unless score #demo_{a} pr.v matches {bounds} run return run tellraw @s {{text:"検証配置は座標範囲内の平地で実行してください",color:"red"}}' for a,bounds in (("x","-499996..499968"),("z","-500000..499980"),("y","-60..246"))],
             "function space_editor:start",
             *box("a", ((0,0,4),(3,3,7))),
             f"function space_editor:projection/demo/group with {P} demo",
             *box("ea", ((-4,-4,0),(7,9,11))),
             *box("eb", ((8,-4,0),(19,9,11))),
             *box("ec", ((20,-4,0),(31,9,11))),
             *box("db", ((12,0,16),(15,3,19))),
             *box("dc", ((24,0,16),(27,3,19))),
             f"function space_editor:projection/demo/configure with {P} demo",
             f"data modify {D} projection.demo set from {P} demo",
             "function space_editor:projection/enable", "function space_editor:projection/demo/status"]
    fn("demo/setup", setup)
    group = []
    for key,offset,rotation in (("b",12,90),("c",24,180)):
        group += [f"data modify {P} demo.{key} set from {D} nextId",
                  f'$data modify {R} pairCandidate set from {D} regions[{{id:$(a)}}]',
                  f"data remove {R} pairCandidate.spaceLinkGroupId", f"data remove {R} pairCandidate.kind",
                  f"data modify {R} pairCandidate.rotationY set value {rotation}", f"data modify {R} pairCandidate.flipY set value 1b"]
        for bound,delta in ((1,offset),(2,offset+4)):
            group += ["scoreboard players operation #demo_tmp pr.v = #demo_x pr.v", f"scoreboard players add #demo_tmp pr.v {delta}",
                      f"execute store result {R} pairCandidate.x{bound}m int 1000 run scoreboard players get #demo_tmp pr.v"]
        group += ["$function space_editor:space_group/add {source:$(a)}",f"function space_editor:projection/demo/remember_{key} with {P} demo"]
    fn("demo/group", group)
    configure=[]
    for k in ("a","b","c"):
        configure += [f'$function space_editor:space_group/set_room {{id:$({k}),roomId:"stage6_demo_$(a)_{k}"}}',
                      f'$data modify {R} hit set from {D} regions[{{id:$(e{k})}}]',
                      "function space_editor:pair/mark_existence",
                      f'$function space_editor:proxy_existence/set_room {{id:$(e{k}),roomId:"stage6_demo_$(a)_{k}"}}']
    configure += ['$function space_editor:projection/debug/map {target:$(b),region:$(db)}',
                  '$function space_editor:projection/debug/map {target:$(c),region:$(dc)}']
    fn("demo/configure", configure)
    fn("demo/status", [f"data get {D} projection.demo", 'tellraw @s {text:"原点はsetup時の足元床座標。A=(X+0..4,Z+4..8)、B=X+12、C=X+24。Debug B/CはZ+16..20。/function space_editor:play 後にAへ歩く。demo/teleportで本人TP追加。",color:"aqua"}'])
    fn("demo/teleport", [edit_guard, f"execute unless data {D} projection.demo run return 0",
        f"execute if data {D} projection.demo.ta run return 0", f"data modify {P} demo set from {D} projection.demo",
        *[f"execute store result score #demo_{a} pr.v run data get {P} demo.{a}" for a in "xyz"],
        *box("ta", ((0,0,4),(3,3,7))), f"function space_editor:projection/demo/tp_pair with {P} demo",
        f"data modify {D} projection.demo set from {P} demo"])
    fn("demo/tp_pair", [f"data modify {P} demo.tb set from {D} nextId",
        f'$data modify {R} pairCandidate set from {D} regions[{{id:$(b)}}]', f"data remove {R} pairCandidate.spaceLinkGroupId", f"data remove {R} pairCandidate.kind",
        '$function space_editor:pair/create {source:$(ta),kind:"teleport"}',
        f"function space_editor:projection/demo/remember_tb with {P} demo",
        f'$data modify {P} tpConfig set from {D} regions[{{id:$(ta)}}]',
        f'$data modify {P} tpConfig.roomA set value "stage6_demo_$(a)_a"', f'$data modify {P} tpConfig.roomB set value "stage6_demo_$(a)_b"',
        f"function space_editor:projection/demo/tp_configure with {P} tpConfig"])
    fn("demo/tp_configure", ['$function space_editor:pair/configure {id:$(id),groupId:0,roomA:"$(roomA)",roomB:"$(roomB)",direction:"both",cooldownTicks:20}'])
    fn("demo/cleanup", [edit_guard, f"execute unless data {D} projection.demo run return 0",
        f"data modify {P} demoDelete set from {D} projection.demo.ids", "function space_editor:projection/demo/delete_scan",
        f"data remove {D} projection.demo", "function space_editor:projection/maintenance"])
    drain("demo/delete_scan", "demoDelete", "demo/delete_next", 16)
    fn("demo/delete_next", [f"function space_editor:projection/demo/delete_one with {P} demoDelete[0]", f"data remove {P} demoDelete[0]"])
    fn("demo/delete_one", [f"data remove {R} hit", f'$data modify {R} hit set from {D} regions[{{id:$(id)}}]',
        f"execute if data {R} hit.id run function space_editor:region/delete_selected",
        f'$data remove {D} projection.debugMaps[{{targetId:$(id)}}]',
        f"data modify {P} demoPaths set value []",
        f'$data modify {P} demoPaths append from {P} active[{{sourceId:$(id)}}]',
        f'$data modify {P} demoPaths append from {P} active[{{targetId:$(id)}}]',
        "function space_editor:projection/demo/purge_scan"])
    drain("demo/purge_scan", "demoPaths", "demo/purge_next", 512)
    fn("demo/purge_next", [f"function space_editor:projection/remove_render with {P} demoPaths[0]",
        f"function space_editor:projection/demo/purge_path with {P} demoPaths[0]", f"data remove {P} demoPaths[0]"])
    fn("demo/purge_path", [f'$data remove {P} active[{{id:$(id)}}]'])


def main():
    import build_space_editor_stage5
    build_space_editor_stage5.main()


if __name__ == "__main__":
    main()
