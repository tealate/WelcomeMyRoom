tag @e[tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_nether run tag @e[tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_end run tag @e[tag=space_editor.proxy_spike] remove sp.online
execute as @a at @s if score @s sp.owner matches 1.. run function space_editor:proxy_spike/mark_online
execute as @a[scores={sp.follow=1}] at @s run function space_editor:proxy_spike/player_tick
execute in minecraft:overworld run kill @e[tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_nether run kill @e[tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_end run kill @e[tag=space_editor.proxy_spike,tag=!sp.online]
