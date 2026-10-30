scoreboard players add @s pr.owner 0
scoreboard players add @s pr.leave 0
scoreboard players add @s pr.debug 0
execute if score @s pr.owner matches 0 run scoreboard players add #owner pr.owner 1
execute if score @s pr.owner matches 0 run scoreboard players operation @s pr.owner = #owner pr.owner
execute store result storage space_editor:projection actor.id int 1 run scoreboard players get @s pr.owner
execute store result storage space_editor:projection actor.leave int 1 run scoreboard players get @s pr.leave
data modify storage space_editor:projection actor.uuid set from entity @s UUID
function space_editor:projection/register_actor with storage space_editor:projection actor
