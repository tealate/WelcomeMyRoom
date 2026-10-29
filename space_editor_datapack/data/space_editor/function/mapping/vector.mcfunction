execute store result score #map_px se.v run data get storage space_editor:runtime map.vector[0] 2000
scoreboard players operation #quant_next se.v = #map_px se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime map.vector[0]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #map_px se.v = #quant_next se.v
execute store result score #map_py se.v run data get storage space_editor:runtime map.vector[1] 2000
scoreboard players operation #quant_next se.v = #map_py se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime map.vector[1]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #map_py se.v = #quant_next se.v
execute store result score #map_pz se.v run data get storage space_editor:runtime map.vector[2] 2000
scoreboard players operation #quant_next se.v = #map_pz se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime map.vector[2]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #map_pz se.v = #quant_next se.v
function space_editor:mapping/vector_scores
execute store result storage space_editor:runtime map.result.vector[0] double 0.0005 run scoreboard players get #map_ox se.v
execute store result storage space_editor:runtime map.result.vector[1] double 0.0005 run scoreboard players get #map_oy se.v
execute store result storage space_editor:runtime map.result.vector[2] double 0.0005 run scoreboard players get #map_oz se.v
