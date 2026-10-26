execute store result score #px se.v run data get storage space_editor:runtime hover.x 1000
execute store result score #py se.v run data get storage space_editor:runtime hover.y 1000
execute store result score #pz se.v run data get storage space_editor:runtime hover.z 1000
scoreboard players add #px se.v 500
scoreboard players add #py se.v 500
scoreboard players add #pz se.v 500
data modify storage space_editor:runtime candidates set from storage space_editor:document regions
execute if data storage space_editor:runtime candidates[0] run function space_editor:region/check_next
execute if data storage space_editor:runtime hit run return run function space_editor:region/apply_hit
tellraw @s {"text": "[Space Editor] 選択予定位置を含むRegionがありません。", "color": "red"}
