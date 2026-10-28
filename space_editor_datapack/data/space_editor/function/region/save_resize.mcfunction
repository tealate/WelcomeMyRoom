execute store result storage space_editor:runtime hit.x1m int 1 run scoreboard players get #x1 se.v
execute store result storage space_editor:runtime hit.x2m int 1 run scoreboard players get #x2 se.v
execute store result storage space_editor:runtime hit.sxm int 1 run scoreboard players get #sizex se.v
execute store result storage space_editor:runtime hit.x1 double 0.001 run scoreboard players get #x1 se.v
execute store result storage space_editor:runtime hit.x2 double 0.001 run scoreboard players get #x2 se.v
execute store result storage space_editor:runtime hit.min[0] double 0.001 run scoreboard players get #x1 se.v
execute store result storage space_editor:runtime hit.maxExclusive[0] double 0.001 run scoreboard players get #x2 se.v
execute store result storage space_editor:runtime hit.sx double 0.001 run scoreboard players get #sizex se.v
execute store result storage space_editor:runtime hit.y1m int 1 run scoreboard players get #y1 se.v
execute store result storage space_editor:runtime hit.y2m int 1 run scoreboard players get #y2 se.v
execute store result storage space_editor:runtime hit.sym int 1 run scoreboard players get #sizey se.v
execute store result storage space_editor:runtime hit.y1 double 0.001 run scoreboard players get #y1 se.v
execute store result storage space_editor:runtime hit.y2 double 0.001 run scoreboard players get #y2 se.v
execute store result storage space_editor:runtime hit.min[1] double 0.001 run scoreboard players get #y1 se.v
execute store result storage space_editor:runtime hit.maxExclusive[1] double 0.001 run scoreboard players get #y2 se.v
execute store result storage space_editor:runtime hit.sy double 0.001 run scoreboard players get #sizey se.v
execute store result storage space_editor:runtime hit.z1m int 1 run scoreboard players get #z1 se.v
execute store result storage space_editor:runtime hit.z2m int 1 run scoreboard players get #z2 se.v
execute store result storage space_editor:runtime hit.szm int 1 run scoreboard players get #sizez se.v
execute store result storage space_editor:runtime hit.z1 double 0.001 run scoreboard players get #z1 se.v
execute store result storage space_editor:runtime hit.z2 double 0.001 run scoreboard players get #z2 se.v
execute store result storage space_editor:runtime hit.min[2] double 0.001 run scoreboard players get #z1 se.v
execute store result storage space_editor:runtime hit.maxExclusive[2] double 0.001 run scoreboard players get #z2 se.v
execute store result storage space_editor:runtime hit.sz double 0.001 run scoreboard players get #sizez se.v
execute if data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y1 se.v matches -64000..319999 run return run tellraw @s {"text": "[Space Editor] Overworldの高さ範囲を超えています。", "color": "red"}
execute if data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y2 se.v matches -63900..320000 run return run tellraw @s {"text": "[Space Editor] Overworldの高さ範囲を超えています。", "color": "red"}
execute unless data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y1 se.v matches 0..255999 run return run tellraw @s {"text": "[Space Editor] Nether/Endの高さ範囲を超えています。", "color": "red"}
execute unless data storage space_editor:runtime hit{dimension:"minecraft:overworld"} unless score #y2 se.v matches 100..256000 run return run tellraw @s {"text": "[Space Editor] Nether/Endの高さ範囲を超えています。", "color": "red"}
execute if data storage space_editor:runtime hit.pairId run return run function space_editor:pair/edit_bounds
function space_editor:region/store_hit with storage space_editor:runtime hit
function space_editor:mask/record_region_sync with storage space_editor:runtime hit
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] Regionを更新しました。", "color": "green"}
