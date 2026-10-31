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
execute store result score #ray_lo_x se.v run data get storage space_editor:runtime hit.x1m 1
execute store result score #ray_hi_x se.v run data get storage space_editor:runtime hit.x2m 1
execute store result score #ray_end_y se.v run data get storage space_editor:runtime rayPos[1] 1000
scoreboard players set #ray_sign_y se.v 1
execute if score #ray_end_y se.v < #ray_origin_y se.v run scoreboard players set #ray_sign_y se.v -1
execute store result score #ray_lo_y se.v run data get storage space_editor:runtime hit.y1m 1
execute store result score #ray_hi_y se.v run data get storage space_editor:runtime hit.y2m 1
execute store result score #ray_end_z se.v run data get storage space_editor:runtime rayPos[2] 1000
scoreboard players set #ray_sign_z se.v 1
execute if score #ray_end_z se.v < #ray_origin_z se.v run scoreboard players set #ray_sign_z se.v -1
execute store result score #ray_lo_z se.v run data get storage space_editor:runtime hit.z1m 1
execute store result score #ray_hi_z se.v run data get storage space_editor:runtime hit.z2m 1
scoreboard players set #ray_low se.v 0
scoreboard players set #ray_high se.v 512
scoreboard players set #ray_found se.v 513
function space_editor:region/ray_search
execute if score #ray_found se.v matches ..512 run function space_editor:fill/face_found
kill @e[type=minecraft:marker,tag=space_editor.ray_probe]
