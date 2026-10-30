function space_editor:proxy_spike/select
function space_editor:proxy_spike/name_text_apply
team join sp_body @e[type=minecraft:mannequin,tag=sp.selected]
execute as @e[type=minecraft:mannequin,tag=sp.selected] run data merge entity @s {CustomNameVisible:0b,hide_description:1b}
execute if score @s sp.name matches 1 run team join sp_hidden @e[type=minecraft:mannequin,tag=sp.selected]
execute if score @s sp.name matches 3 run team join sp_hidden @e[type=minecraft:mannequin,tag=sp.selected]
execute as @e[type=minecraft:text_display,tag=sp.selected] run data modify entity @s view_range set value 0f
execute if score @s sp.name matches 3 as @e[type=minecraft:text_display,tag=sp.selected] run data modify entity @s view_range set value 0.5f
execute if score @s sp.name matches 4 as @e[type=minecraft:mannequin,tag=sp.selected] run data modify entity @s CustomNameVisible set value 1b
execute if score @s sp.name matches 2 run function space_editor:proxy_spike/name_description_apply
function space_editor:proxy_spike/update_labels
