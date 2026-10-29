function space_editor:mapping/contains with storage space_editor:runtime spatialRegion
execute unless score #inside se.v matches 1 run return 0
execute store result score #tp_pair se.v run data get storage space_editor:runtime spatialRegion.pairId 1
execute if score @s se.tp_lock = #tp_pair se.v run scoreboard players set #still_locked se.v 1
execute unless data storage space_editor:runtime tpHit run data modify storage space_editor:runtime tpHit set from storage space_editor:runtime spatialRegion
