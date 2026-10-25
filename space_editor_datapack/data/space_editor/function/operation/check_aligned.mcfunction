scoreboard players set #aligned se.v 1
execute store result score #x1m se.v run data get storage space_editor:runtime hit.x1m 1
execute store result score #x2m se.v run data get storage space_editor:runtime hit.x2m 1
scoreboard players operation #rem se.v = #x1m se.v
scoreboard players operation #rem se.v %= #1000 se.v
execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0
scoreboard players operation #rem se.v = #x2m se.v
scoreboard players operation #rem se.v %= #1000 se.v
execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0
execute store result score #y1m se.v run data get storage space_editor:runtime hit.y1m 1
execute store result score #y2m se.v run data get storage space_editor:runtime hit.y2m 1
scoreboard players operation #rem se.v = #y1m se.v
scoreboard players operation #rem se.v %= #1000 se.v
execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0
scoreboard players operation #rem se.v = #y2m se.v
scoreboard players operation #rem se.v %= #1000 se.v
execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0
execute store result score #z1m se.v run data get storage space_editor:runtime hit.z1m 1
execute store result score #z2m se.v run data get storage space_editor:runtime hit.z2m 1
scoreboard players operation #rem se.v = #z1m se.v
scoreboard players operation #rem se.v %= #1000 se.v
execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0
scoreboard players operation #rem se.v = #z2m se.v
scoreboard players operation #rem se.v %= #1000 se.v
execute unless score #rem se.v matches 0 run scoreboard players set #aligned se.v 0
execute if score #aligned se.v matches 0 run return 0
scoreboard players operation #x1 se.v = #x1m se.v
scoreboard players operation #x1 se.v /= #1000 se.v
scoreboard players operation #x2 se.v = #x2m se.v
scoreboard players operation #x2 se.v /= #1000 se.v
scoreboard players operation #sx se.v = #x2 se.v
scoreboard players operation #sx se.v -= #x1 se.v
scoreboard players operation #y1 se.v = #y1m se.v
scoreboard players operation #y1 se.v /= #1000 se.v
scoreboard players operation #y2 se.v = #y2m se.v
scoreboard players operation #y2 se.v /= #1000 se.v
scoreboard players operation #sy se.v = #y2 se.v
scoreboard players operation #sy se.v -= #y1 se.v
scoreboard players operation #z1 se.v = #z1m se.v
scoreboard players operation #z1 se.v /= #1000 se.v
scoreboard players operation #z2 se.v = #z2m se.v
scoreboard players operation #z2 se.v /= #1000 se.v
scoreboard players operation #sz se.v = #z2 se.v
scoreboard players operation #sz se.v -= #z1 se.v
return 1
