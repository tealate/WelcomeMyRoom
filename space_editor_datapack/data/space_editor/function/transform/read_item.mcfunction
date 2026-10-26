$execute in $(sourceDimension) run setblock $(scratchX) $(scratchY) $(scratchZ) minecraft:barrel
$execute in $(sourceDimension) run loot replace block $(scratchX) $(scratchY) $(scratchZ) container.0 1 mine $(blockSourceX) $(blockSourceY) $(blockSourceZ) minecraft:diamond_pickaxe[minecraft:enchantments={"minecraft:silk_touch":1}]
$data modify storage space_editor:runtime transformState.block set from block $(scratchX) $(scratchY) $(scratchZ) Items[{Slot:0b}].id
$execute in $(sourceDimension) run setblock $(scratchX) $(scratchY) $(scratchZ) minecraft:air
