
# Position + Rotation
execute as @p at @s rotated ~ 0 positioned ^ ^ ^3 rotated as @s run tp @e[type=minecraft:mannequin,tag=mirror_test,limit=1] ~ ~ ~ ~ ~

# Default standing
execute as @p unless predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} unless predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_swimming:true}}} run data modify entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] pose set value standing

# Crouching
execute as @p if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run data modify entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] pose set value crouching

# Swimming
execute as @p if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_swimming:true}}} run data modify entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] pose set value swimming

# Equipment
execute as @p run item replace entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] weapon.mainhand from entity @s weapon.mainhand
execute as @p run item replace entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] weapon.offhand from entity @s weapon.offhand
execute as @p run item replace entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] armor.head from entity @s armor.head
execute as @p run item replace entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] armor.chest from entity @s armor.chest
execute as @p run item replace entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] armor.legs from entity @s armor.legs
execute as @p run item replace entity @e[type=minecraft:mannequin,tag=mirror_test,limit=1] armor.feet from entity @s armor.feet
