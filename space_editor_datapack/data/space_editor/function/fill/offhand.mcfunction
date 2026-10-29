data modify storage space_editor:runtime fillBlock set value "minecraft:air"
execute if items entity @s weapon.offhand * run data modify storage space_editor:runtime fillBlock set from entity @s equipment.offhand.id
execute if items entity @s weapon.offhand minecraft:water_bucket run data modify storage space_editor:runtime fillBlock set value "minecraft:water"
execute if items entity @s weapon.offhand minecraft:lava_bucket run data modify storage space_editor:runtime fillBlock set value "minecraft:lava"
function space_editor:fill/apply
