scoreboard players add #epoch sp.epoch 1
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] run function space_editor:proxy_spike/delete_start
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] run function space_editor:proxy_spike/delete_start
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] run function space_editor:proxy_spike/delete_start
execute in minecraft:overworld run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike]
execute in minecraft:the_nether run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike]
execute in minecraft:the_end run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike]
scoreboard players set @a sp.follow 0
tag @a remove sp.active
