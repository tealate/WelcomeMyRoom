execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {text:"別プレイヤーの編集終了後に実行してください",color:"red"}
execute unless data storage space_editor:document projection.demo run return 0
execute if data storage space_editor:document projection.demo.ta run return 0
data modify storage space_editor:projection demo set from storage space_editor:document projection.demo
execute store result score #demo_x pr.v run data get storage space_editor:projection demo.x
execute store result score #demo_y pr.v run data get storage space_editor:projection demo.y
execute store result score #demo_z pr.v run data get storage space_editor:projection demo.z
data modify storage space_editor:projection demo.ta set from storage space_editor:document nextId
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
function space_editor:projection/demo/remember_ta with storage space_editor:projection demo
function space_editor:projection/demo/tp_pair with storage space_editor:projection demo
data modify storage space_editor:document projection.demo set from storage space_editor:projection demo
