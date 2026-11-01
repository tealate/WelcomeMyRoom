scoreboard players set @s se.use 0
execute if score @s se.mode_gap matches 1.. run return run scoreboard players set @s se.mode_gap 8
scoreboard players set @s se.mode_gap 8
scoreboard players set @s se.cd 5
execute if entity @s[tag=space_editor.editing] run return run function space_editor:play
function space_editor:start
