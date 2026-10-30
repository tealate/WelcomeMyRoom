execute if entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] unless entity @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_main,limit=1] run function space_editor:proxy_spike/apply_name
execute if entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] unless entity @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_reference,limit=1] run function space_editor:proxy_spike/apply_name
function space_editor:proxy_spike/sync
execute store result storage space_editor:proxy_spike x double 0.001 run scoreboard players get @s sp.x
execute store result storage space_editor:proxy_spike y double 0.001 run scoreboard players get @s sp.y
execute store result storage space_editor:proxy_spike z double 0.001 run scoreboard players get @s sp.z
scoreboard players operation #y sp.v = @s sp.y
execute if score @s sp.flip matches 1 run scoreboard players operation #y sp.v += @s sp.fy
execute store result storage space_editor:proxy_spike my double 0.001 run scoreboard players get #y sp.v
scoreboard players operation #x sp.v = @s sp.x
scoreboard players add #x sp.v 2000
execute store result storage space_editor:proxy_spike rx double 0.001 run scoreboard players get #x sp.v
function space_editor:proxy_spike/move with storage space_editor:proxy_spike
function space_editor:proxy_spike/update_labels
execute if score @s sp.demo matches 1.. run scoreboard players remove @s sp.demo 1
execute if score @s sp.demo matches 0 run return 0
execute if score @s sp.demo matches 1 run function space_editor:proxy_spike/swing_demo_pulse
