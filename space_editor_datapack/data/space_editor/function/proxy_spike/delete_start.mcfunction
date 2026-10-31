scoreboard players operation #delete_owner sp.owner = @s sp.owner
execute if entity @s[tag=sp.main] as @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=sp.label_main] if score @s sp.owner = #delete_owner sp.owner run kill @s
execute if entity @s[tag=sp.reference] as @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=sp.label_reference] if score @s sp.owner = #delete_owner sp.owner run kill @s
tag @s add sp.removing
tag @s remove space_editor.proxy_spike
tag @s remove sp.main
tag @s remove sp.reference
tag @s remove sp.selected
tag @s remove sp.online
tag @s remove sp.new
effect give @s minecraft:invisibility infinite 0 true
item replace entity @s armor.head with minecraft:air
item replace entity @s armor.chest with minecraft:air
item replace entity @s armor.legs with minecraft:air
item replace entity @s armor.feet with minecraft:air
item replace entity @s weapon.mainhand with minecraft:air
item replace entity @s weapon.offhand with minecraft:air
scoreboard players set @s sp.remove 6
