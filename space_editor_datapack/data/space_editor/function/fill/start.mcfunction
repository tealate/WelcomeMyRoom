execute unless entity @s[type=minecraft:player] run return 0
data remove storage space_editor:runtime fillBlock
data modify storage space_editor:runtime fillBlock set from entity @s SelectedItem.id
function space_editor:fill/apply
