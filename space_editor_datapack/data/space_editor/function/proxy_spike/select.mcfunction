scoreboard players operation #owner sp.owner = @s sp.owner
tag @e[tag=space_editor.proxy_spike] remove sp.selected
execute as @e[tag=space_editor.proxy_spike] if score @s sp.owner = #owner sp.owner run tag @s add sp.selected
