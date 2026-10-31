execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=1..}] at @s if dimension minecraft:overworld run scoreboard players remove @s sp.remove 1
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=4}] at @s if dimension minecraft:overworld run tp @s ~ -63 ~
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=..0}] at @s if dimension minecraft:overworld run kill @s
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=1..}] at @s if dimension minecraft:the_nether run scoreboard players remove @s sp.remove 1
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=4}] at @s if dimension minecraft:the_nether run tp @s ~ 1 ~
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=..0}] at @s if dimension minecraft:the_nether run kill @s
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=1..}] at @s if dimension minecraft:the_end run scoreboard players remove @s sp.remove 1
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=4}] at @s if dimension minecraft:the_end run tp @s ~ 1 ~
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=sp.removing,scores={sp.remove=..0}] at @s if dimension minecraft:the_end run kill @s
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run function space_editor:proxy_spike/delete_start
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run function space_editor:proxy_spike/delete_start
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run function space_editor:proxy_spike/delete_start
execute in minecraft:overworld as @e[type=minecraft:text_display,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:the_nether as @e[type=minecraft:text_display,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:the_end as @e[type=minecraft:text_display,tag=space_editor.proxy_spike] unless score @s sp.epoch = #epoch sp.epoch run kill @s
execute in minecraft:overworld run tag @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:overworld run tag @e[type=minecraft:text_display,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_nether run tag @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_nether run tag @e[type=minecraft:text_display,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_end run tag @e[type=minecraft:mannequin,tag=space_editor.proxy_spike] remove sp.online
execute in minecraft:the_end run tag @e[type=minecraft:text_display,tag=space_editor.proxy_spike] remove sp.online
execute as @a[tag=sp.active] at @s run function space_editor:proxy_spike/owner_tick
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=!sp.online] run function space_editor:proxy_spike/delete_start
execute in minecraft:overworld run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=!sp.online] run function space_editor:proxy_spike/delete_start
execute in minecraft:the_nether run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=!sp.online]
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=!sp.online] run function space_editor:proxy_spike/delete_start
execute in minecraft:the_end run kill @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=!sp.online]
