scoreboard players add @s sp.owner 0
execute if score @s sp.owner matches 0 run scoreboard players add #next sp.owner 1
execute if score @s sp.owner matches 0 run scoreboard players operation @s sp.owner = #next sp.owner
