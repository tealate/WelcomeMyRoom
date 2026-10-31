execute if score @s sp.flip matches 1 as @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_main,limit=1] run data merge entity @s {transformation:{left_rotation:[0f,0f,1f,0f]}}
execute if score @s sp.flip matches 0 as @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_main,limit=1] run data merge entity @s {transformation:{left_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_reference,limit=1] run data merge entity @s {transformation:{left_rotation:[0f,0f,0f,1f]}}
scoreboard players operation #height sp.v = @s sp.normal
execute if score @s sp.flip matches 1 run scoreboard players operation #height sp.v = @s sp.inverted
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] {pose:"crouching"} run scoreboard players remove #height sp.v 300
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] {pose:"swimming"} run scoreboard players remove #height sp.v 1200
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] {pose:"fall_flying"} run scoreboard players remove #height sp.v 1200
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] {pose:"sleeping"} run scoreboard players remove #height sp.v 1600
execute store result storage space_editor:proxy_spike height double 0.001 run scoreboard players get #height sp.v
execute at @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] run function space_editor:proxy_spike/label_main_position with storage space_editor:proxy_spike
scoreboard players operation #height sp.v = @s sp.normal
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] {pose:"crouching"} run scoreboard players remove #height sp.v 300
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] {pose:"swimming"} run scoreboard players remove #height sp.v 1200
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] {pose:"fall_flying"} run scoreboard players remove #height sp.v 1200
execute if data entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] {pose:"sleeping"} run scoreboard players remove #height sp.v 1600
execute store result storage space_editor:proxy_spike height double 0.001 run scoreboard players get #height sp.v
execute at @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] run function space_editor:proxy_spike/label_reference_position with storage space_editor:proxy_spike
