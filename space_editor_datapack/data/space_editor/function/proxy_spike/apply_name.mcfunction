function space_editor:proxy_spike/select
team join sp_body @e[tag=sp.selected,type=minecraft:mannequin]
data modify entity @e[tag=sp.selected,tag=sp.main,limit=1] CustomNameVisible set value 0b
data modify entity @e[tag=sp.selected,tag=sp.main,limit=1] hide_description set value 1b
execute if score @s sp.name matches 1 run team join sp_hidden @e[tag=sp.selected,type=minecraft:mannequin]
execute if score @s sp.name matches 3 run team join sp_hidden @e[tag=sp.selected,type=minecraft:mannequin]
execute if score @s sp.name matches 2 run function space_editor:proxy_spike/name_description_apply
execute unless score @s sp.name matches 3 run kill @e[tag=sp.selected,type=minecraft:text_display]
execute if entity @e[tag=sp.selected,tag=sp.main] if score @s sp.name matches 3 run function space_editor:proxy_spike/name_text_apply
