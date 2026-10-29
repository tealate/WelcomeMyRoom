data modify storage space_editor:runtime playerLookup.uuid set from entity @s UUID
data remove storage space_editor:runtime tpPlayer
function space_editor:teleport/find_snapshot with storage space_editor:runtime playerLookup
execute store result score #spx se.v run data get storage space_editor:runtime tpPlayer.point[0] 2000
scoreboard players operation #quant_next se.v = #spx se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime tpPlayer.point[0]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #spx se.v = #quant_next se.v
execute store result score #spy se.v run data get storage space_editor:runtime tpPlayer.point[1] 2000
scoreboard players operation #quant_next se.v = #spy se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime tpPlayer.point[1]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #spy se.v = #quant_next se.v
execute store result score #spz se.v run data get storage space_editor:runtime tpPlayer.point[2] 2000
scoreboard players operation #quant_next se.v = #spz se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime tpPlayer.point[2]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #spz se.v = #quant_next se.v
