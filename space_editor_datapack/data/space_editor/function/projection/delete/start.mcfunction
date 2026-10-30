scoreboard players operation #delete pr.id = @s pr.id
execute if entity @s[tag=pr.production] in minecraft:overworld as @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production] if score @s pr.id = #delete pr.id run kill @s
execute if entity @s[tag=pr.production] in minecraft:the_nether as @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production] if score @s pr.id = #delete pr.id run kill @s
execute if entity @s[tag=pr.production] in minecraft:the_end as @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production] if score @s pr.id = #delete pr.id run kill @s
execute if entity @s[tag=pr.debug] in minecraft:overworld as @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.debug] if score @s pr.id = #delete pr.id run kill @s
execute if entity @s[tag=pr.debug] in minecraft:the_nether as @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.debug] if score @s pr.id = #delete pr.id run kill @s
execute if entity @s[tag=pr.debug] in minecraft:the_end as @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.debug] if score @s pr.id = #delete pr.id run kill @s
tag @s add pr.removing
tag @s remove space_editor.proxy
tag @s remove pr.production
tag @s remove pr.debug
tag @s remove pr.new
effect give @s minecraft:invisibility infinite 0 true
item replace entity @s armor.head with minecraft:air
item replace entity @s armor.chest with minecraft:air
item replace entity @s armor.legs with minecraft:air
item replace entity @s armor.feet with minecraft:air
item replace entity @s weapon.mainhand with minecraft:air
item replace entity @s weapon.offhand with minecraft:air
scoreboard players set @s pr.remove 6
