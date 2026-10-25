scoreboard players set #current_dim se.v 0
execute if dimension minecraft:the_nether run scoreboard players set #current_dim se.v 1
execute if dimension minecraft:the_end run scoreboard players set #current_dim se.v 2
execute unless score @s se.dim = #current_dim se.v run function space_editor:preview/resync
scoreboard players operation @s se.dim = #current_dim se.v
