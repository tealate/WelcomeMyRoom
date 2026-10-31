execute unless entity @s[type=minecraft:player] run return 0
execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {text:"別プレイヤーの編集終了後に実行してください",color:"red"}
execute if data storage space_editor:document projection.demo run return run function space_editor:projection/demo/status
data modify storage space_editor:projection demo set value {ids:[]}
data modify storage space_editor:projection demo.uuid set from entity @s UUID
execute if dimension minecraft:overworld run data modify storage space_editor:projection demo.dimension set value "minecraft:overworld"
execute if dimension minecraft:the_nether run data modify storage space_editor:projection demo.dimension set value "minecraft:the_nether"
execute if dimension minecraft:the_end run data modify storage space_editor:projection demo.dimension set value "minecraft:the_end"
execute store result score #demo_x pr.v run data get entity @s Pos[0]
execute store result storage space_editor:projection demo.x int 1 run scoreboard players get #demo_x pr.v
execute store result score #demo_y pr.v run data get entity @s Pos[1]
execute store result storage space_editor:projection demo.y int 1 run scoreboard players get #demo_y pr.v
execute store result score #demo_z pr.v run data get entity @s Pos[2]
execute store result storage space_editor:projection demo.z int 1 run scoreboard players get #demo_z pr.v
execute unless score #demo_x pr.v matches -499996..499968 run return run tellraw @s {text:"検証配置は座標範囲内の平地で実行してください",color:"red"}
execute unless score #demo_z pr.v matches -500000..499980 run return run tellraw @s {text:"検証配置は座標範囲内の平地で実行してください",color:"red"}
execute unless score #demo_y pr.v matches -60..246 run return run tellraw @s {text:"検証配置は座標範囲内の平地で実行してください",color:"red"}
function space_editor:start
data modify storage space_editor:projection demo.a set from storage space_editor:document nextId
data modify storage space_editor:runtime selection set value {a:[I;0,0,0],b:[I;0,0,0]}
data modify storage space_editor:runtime selection.dimension set from storage space_editor:projection demo.dimension
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 0
execute store result storage space_editor:runtime selection.a[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 0
execute store result storage space_editor:runtime selection.a[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 4
execute store result storage space_editor:runtime selection.a[2] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 3
execute store result storage space_editor:runtime selection.b[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 3
execute store result storage space_editor:runtime selection.b[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 7
execute store result storage space_editor:runtime selection.b[2] int 1 run scoreboard players get #demo_tmp pr.v
function space_editor:region/create
function space_editor:projection/demo/remember_a with storage space_editor:projection demo
function space_editor:projection/demo/group with storage space_editor:projection demo
data modify storage space_editor:projection demo.ea set from storage space_editor:document nextId
data modify storage space_editor:runtime selection set value {a:[I;0,0,0],b:[I;0,0,0]}
data modify storage space_editor:runtime selection.dimension set from storage space_editor:projection demo.dimension
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players remove #demo_tmp pr.v 4
execute store result storage space_editor:runtime selection.a[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players remove #demo_tmp pr.v 4
execute store result storage space_editor:runtime selection.a[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 0
execute store result storage space_editor:runtime selection.a[2] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 7
execute store result storage space_editor:runtime selection.b[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 9
execute store result storage space_editor:runtime selection.b[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 11
execute store result storage space_editor:runtime selection.b[2] int 1 run scoreboard players get #demo_tmp pr.v
function space_editor:region/create
function space_editor:projection/demo/remember_ea with storage space_editor:projection demo
data modify storage space_editor:projection demo.eb set from storage space_editor:document nextId
data modify storage space_editor:runtime selection set value {a:[I;0,0,0],b:[I;0,0,0]}
data modify storage space_editor:runtime selection.dimension set from storage space_editor:projection demo.dimension
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 8
execute store result storage space_editor:runtime selection.a[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players remove #demo_tmp pr.v 4
execute store result storage space_editor:runtime selection.a[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 0
execute store result storage space_editor:runtime selection.a[2] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 19
execute store result storage space_editor:runtime selection.b[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 9
execute store result storage space_editor:runtime selection.b[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 11
execute store result storage space_editor:runtime selection.b[2] int 1 run scoreboard players get #demo_tmp pr.v
function space_editor:region/create
function space_editor:projection/demo/remember_eb with storage space_editor:projection demo
data modify storage space_editor:projection demo.ec set from storage space_editor:document nextId
data modify storage space_editor:runtime selection set value {a:[I;0,0,0],b:[I;0,0,0]}
data modify storage space_editor:runtime selection.dimension set from storage space_editor:projection demo.dimension
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 20
execute store result storage space_editor:runtime selection.a[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players remove #demo_tmp pr.v 4
execute store result storage space_editor:runtime selection.a[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 0
execute store result storage space_editor:runtime selection.a[2] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 31
execute store result storage space_editor:runtime selection.b[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 9
execute store result storage space_editor:runtime selection.b[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 11
execute store result storage space_editor:runtime selection.b[2] int 1 run scoreboard players get #demo_tmp pr.v
function space_editor:region/create
function space_editor:projection/demo/remember_ec with storage space_editor:projection demo
data modify storage space_editor:projection demo.db set from storage space_editor:document nextId
data modify storage space_editor:runtime selection set value {a:[I;0,0,0],b:[I;0,0,0]}
data modify storage space_editor:runtime selection.dimension set from storage space_editor:projection demo.dimension
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 12
execute store result storage space_editor:runtime selection.a[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 0
execute store result storage space_editor:runtime selection.a[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 16
execute store result storage space_editor:runtime selection.a[2] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 15
execute store result storage space_editor:runtime selection.b[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 3
execute store result storage space_editor:runtime selection.b[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 19
execute store result storage space_editor:runtime selection.b[2] int 1 run scoreboard players get #demo_tmp pr.v
function space_editor:region/create
function space_editor:projection/demo/remember_db with storage space_editor:projection demo
data modify storage space_editor:projection demo.dc set from storage space_editor:document nextId
data modify storage space_editor:runtime selection set value {a:[I;0,0,0],b:[I;0,0,0]}
data modify storage space_editor:runtime selection.dimension set from storage space_editor:projection demo.dimension
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 24
execute store result storage space_editor:runtime selection.a[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 0
execute store result storage space_editor:runtime selection.a[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 16
execute store result storage space_editor:runtime selection.a[2] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 27
execute store result storage space_editor:runtime selection.b[0] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_y pr.v
scoreboard players add #demo_tmp pr.v 3
execute store result storage space_editor:runtime selection.b[1] int 1 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_z pr.v
scoreboard players add #demo_tmp pr.v 19
execute store result storage space_editor:runtime selection.b[2] int 1 run scoreboard players get #demo_tmp pr.v
function space_editor:region/create
function space_editor:projection/demo/remember_dc with storage space_editor:projection demo
function space_editor:projection/demo/configure with storage space_editor:projection demo
data modify storage space_editor:document projection.demo set from storage space_editor:projection demo
function space_editor:projection/enable
function space_editor:projection/demo/status
