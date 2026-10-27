scoreboard players set #special_water se.v 0
execute if entity @s[tag=space_editor.special_water] run scoreboard players set #special_water se.v 1
execute if score #special_water se.v matches 1 run setblock ~ ~ ~ minecraft:water
execute unless score #special_water se.v matches 1 run setblock ~ ~ ~ minecraft:air
function space_editor:special/sync_neighbors
function space_editor:special/remove_entity
