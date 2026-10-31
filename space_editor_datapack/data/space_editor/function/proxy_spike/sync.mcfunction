data modify storage space_editor:proxy_spike pose set value "standing"
execute if predicate space_editor:proxy_spike/crouching run data modify storage space_editor:proxy_spike pose set value "crouching"
execute if predicate space_editor:proxy_spike/swimming run data modify storage space_editor:proxy_spike pose set value "swimming"
execute if predicate space_editor:proxy_spike/fall_flying run data modify storage space_editor:proxy_spike pose set value "fall_flying"
execute if data entity @s sleeping_pos run data modify storage space_editor:proxy_spike pose set value "sleeping"
execute as @e[type=minecraft:mannequin,tag=sp.selected] run function space_editor:proxy_spike/set_pose with storage space_editor:proxy_spike
item replace entity @e[type=minecraft:mannequin,tag=sp.selected] armor.head from entity @s armor.head
item replace entity @e[type=minecraft:mannequin,tag=sp.selected] armor.chest from entity @s armor.chest
item replace entity @e[type=minecraft:mannequin,tag=sp.selected] armor.legs from entity @s armor.legs
item replace entity @e[type=minecraft:mannequin,tag=sp.selected] armor.feet from entity @s armor.feet
item replace entity @e[type=minecraft:mannequin,tag=sp.selected] weapon.mainhand from entity @s weapon.mainhand
item replace entity @e[type=minecraft:mannequin,tag=sp.selected] weapon.offhand from entity @s weapon.offhand
