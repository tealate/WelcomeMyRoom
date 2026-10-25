scoreboard players set #best se.v 2147483647
scoreboard players set #face se.v 0
execute store result score #edge se.v run data get storage space_editor:runtime hit.x1m 1
scoreboard players operation #dist se.v = #px se.v
scoreboard players operation #dist se.v -= #edge se.v
execute if score #dist se.v < #best se.v run scoreboard players set #face se.v 0
scoreboard players operation #best se.v < #dist se.v
execute store result score #edge se.v run data get storage space_editor:runtime hit.x2m 1
scoreboard players operation #dist se.v = #edge se.v
scoreboard players operation #dist se.v -= #px se.v
execute if score #dist se.v < #best se.v run scoreboard players set #face se.v 1
scoreboard players operation #best se.v < #dist se.v
execute store result score #edge se.v run data get storage space_editor:runtime hit.y1m 1
scoreboard players operation #dist se.v = #py se.v
scoreboard players operation #dist se.v -= #edge se.v
execute if score #dist se.v < #best se.v run scoreboard players set #face se.v 2
scoreboard players operation #best se.v < #dist se.v
execute store result score #edge se.v run data get storage space_editor:runtime hit.y2m 1
scoreboard players operation #dist se.v = #edge se.v
scoreboard players operation #dist se.v -= #py se.v
execute if score #dist se.v < #best se.v run scoreboard players set #face se.v 3
scoreboard players operation #best se.v < #dist se.v
execute store result score #edge se.v run data get storage space_editor:runtime hit.z1m 1
scoreboard players operation #dist se.v = #pz se.v
scoreboard players operation #dist se.v -= #edge se.v
execute if score #dist se.v < #best se.v run scoreboard players set #face se.v 4
scoreboard players operation #best se.v < #dist se.v
execute store result score #edge se.v run data get storage space_editor:runtime hit.z2m 1
scoreboard players operation #dist se.v = #edge se.v
scoreboard players operation #dist se.v -= #pz se.v
execute if score #dist se.v < #best se.v run scoreboard players set #face se.v 5
scoreboard players operation #best se.v < #dist se.v
execute store result storage space_editor:runtime hitFace int 1 run scoreboard players get #face se.v
