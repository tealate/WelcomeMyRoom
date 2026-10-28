execute unless entity @s[nbt={DeathTime:0s}] run return 0
function space_editor:teleport/read_snapshot
data modify storage space_editor:runtime linkQueue set from storage space_editor:document regions
execute if data storage space_editor:runtime linkQueue[0] run function space_editor:link/scan
