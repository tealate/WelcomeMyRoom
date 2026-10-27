execute store result score #special_id se.v run data get storage space_editor:document nextSpecialId 1
data modify storage space_editor:runtime specialRecord set from storage space_editor:runtime transformState
execute store result storage space_editor:runtime specialRecord.id int 1 run scoreboard players get #special_id se.v
$execute in $(targetDimension) positioned $(x) $(y) $(z) run scoreboard players operation @e[type=minecraft:block_display,tag=space_editor.special_new,distance=..0.1] se.sid = #special_id se.v
$execute if data storage space_editor:runtime transformState{waterlogged:"true"} in $(targetDimension) positioned $(x) $(y) $(z) run tag @e[type=minecraft:block_display,tag=space_editor.special_new,distance=..0.1] add space_editor.special_water
$execute in $(targetDimension) positioned $(x) $(y) $(z) run tag @e[type=minecraft:block_display,tag=space_editor.special_new,distance=..0.1] remove space_editor.special_new
data modify storage space_editor:document specials append from storage space_editor:runtime specialRecord
scoreboard players add #special_id se.v 1
execute store result storage space_editor:document nextSpecialId int 1 run scoreboard players get #special_id se.v
