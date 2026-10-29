execute as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value "standing"
execute if predicate space_editor:proxy_spike/crouching as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value "crouching"
execute if predicate space_editor:proxy_spike/swimming as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value "swimming"
execute if predicate space_editor:proxy_spike/fall_flying as @e[tag=sp.selected,type=minecraft:mannequin] run data modify entity @s pose set value "fall_flying"
item replace entity @e[tag=sp.selected,type=minecraft:mannequin] armor.head from entity @s armor.head
item replace entity @e[tag=sp.selected,type=minecraft:mannequin] armor.chest from entity @s armor.chest
item replace entity @e[tag=sp.selected,type=minecraft:mannequin] armor.legs from entity @s armor.legs
item replace entity @e[tag=sp.selected,type=minecraft:mannequin] armor.feet from entity @s armor.feet
item replace entity @e[tag=sp.selected,type=minecraft:mannequin] weapon.mainhand from entity @s weapon.mainhand
item replace entity @e[tag=sp.selected,type=minecraft:mannequin] weapon.offhand from entity @s weapon.offhand
