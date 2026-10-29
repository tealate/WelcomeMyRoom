execute if data storage space_editor:document {editMode:1b} run return 0
execute if entity @s[tag=space_editor.editing] run return 0
execute if entity @s[gamemode=spectator] run return 0
execute unless entity @s[nbt={DeathTime:0s}] run return 0
function space_editor:teleport/read_snapshot
execute unless data storage space_editor:runtime tpPlayer.point run return 0
scoreboard players set #still_locked se.v 0
data remove storage space_editor:runtime tpHit
data modify storage space_editor:runtime tpQueue set from storage space_editor:document regions
execute if data storage space_editor:runtime tpQueue[0] run function space_editor:teleport/scan
execute if score #still_locked se.v matches 0 run scoreboard players set @s se.tp_lock 0
execute if score @s se.tp_lock matches 1.. run return 0
execute if score @s se.tp_cd matches 1.. run return 0
execute unless data storage space_editor:runtime tpHit run return 0
function space_editor:teleport/resolve with storage space_editor:runtime tpHit
