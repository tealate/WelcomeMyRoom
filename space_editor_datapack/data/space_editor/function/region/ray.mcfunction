data remove storage space_editor:runtime rayHit
scoreboard players set #ray_best se.v 513
summon minecraft:marker ~ ~ ~ {Tags:["space_editor.ray_probe"]}
data modify storage space_editor:runtime rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] Pos
execute store result score #ray_origin_x se.v run data get storage space_editor:runtime rayPos[0] 1000
execute store result score #ray_origin_y se.v run data get storage space_editor:runtime rayPos[1] 1000
execute store result score #ray_origin_z se.v run data get storage space_editor:runtime rayPos[2] 1000
execute positioned ^ ^ ^12.8 run tp @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] ~ ~ ~
data modify storage space_editor:runtime rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] Pos
execute store result score #ray_end_x se.v run data get storage space_editor:runtime rayPos[0] 1000
scoreboard players set #ray_sign_x se.v 1
execute if score #ray_end_x se.v < #ray_origin_x se.v run scoreboard players set #ray_sign_x se.v -1
execute store result score #ray_end_y se.v run data get storage space_editor:runtime rayPos[1] 1000
scoreboard players set #ray_sign_y se.v 1
execute if score #ray_end_y se.v < #ray_origin_y se.v run scoreboard players set #ray_sign_y se.v -1
execute store result score #ray_end_z se.v run data get storage space_editor:runtime rayPos[2] 1000
scoreboard players set #ray_sign_z se.v 1
execute if score #ray_end_z se.v < #ray_origin_z se.v run scoreboard players set #ray_sign_z se.v -1
data modify storage space_editor:runtime rayQueue set from storage space_editor:document regions
execute if data storage space_editor:runtime rayQueue[0] run function space_editor:region/ray_next
kill @e[type=minecraft:marker,tag=space_editor.ray_probe]
function space_editor:region/ray_step
