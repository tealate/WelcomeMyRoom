summon minecraft:marker ~ ~ ~ {Tags:["space_editor.ray_sample"]}
data modify storage space_editor:runtime rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_sample,limit=1,sort=nearest] Pos
kill @e[type=minecraft:marker,tag=space_editor.ray_sample]
execute store result score #px se.v run data get storage space_editor:runtime rayPos[0] 1000
execute store result score #py se.v run data get storage space_editor:runtime rayPos[1] 1000
execute store result score #pz se.v run data get storage space_editor:runtime rayPos[2] 1000
scoreboard players set #paste_hit se.v 0
execute if data storage space_editor:runtime pastePending if data storage space_editor:runtime {activeTool:"delete"} store result score #paste_hit se.v run function space_editor:paste/check_preview_hit with storage space_editor:runtime pastePending
execute if data storage space_editor:runtime pastePending if data storage space_editor:runtime {activeTool:"move"} store result score #paste_hit se.v run function space_editor:paste/check_preview_hit with storage space_editor:runtime pastePending
execute if score #paste_hit se.v matches 1 run return run function space_editor:paste/apply_preview_hit
data modify storage space_editor:runtime candidates set from storage space_editor:document regions
execute if data storage space_editor:runtime candidates[0] run function space_editor:region/check_next
execute if data storage space_editor:runtime hit run return run function space_editor:region/apply_hit
scoreboard players add #region_ray se.v 1
execute if score #region_ray se.v matches ..512 positioned ^ ^ ^0.025 run return run function space_editor:region/ray
tellraw @s {"text": "[Space Editor] 視線上12.8ブロック以内にRegionがありません。", "color": "red"}
