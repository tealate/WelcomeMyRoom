execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:overworld as @e[type=minecraft:text_display,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:the_nether as @e[type=minecraft:text_display,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:the_end as @e[type=minecraft:text_display,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:overworld run tag @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:overworld run tag @e[type=minecraft:text_display,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_nether run tag @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_nether run tag @e[type=minecraft:text_display,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_end run tag @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_end run tag @e[type=minecraft:text_display,tag=space_editor.proxy_spike] remove sp.online
execute as @a[tag=sp.active] at @s run function space_editor:proxy_spike/owner_tick
execute in minecraft:overworld run kill @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:overworld run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_nether run kill @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_nether run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_end run kill @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_end run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=!sp.online]
