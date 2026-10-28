execute unless data storage space_editor:runtime map.pitch run data modify storage space_editor:runtime map.pitch set value 0f
execute store result score #map_yaw se.v run data get storage space_editor:runtime map.yaw 1000
scoreboard players operation #quant_next se.v = #map_yaw se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized float 0.001 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime map.yaw
execute if score #quant_diff se.v matches 0 run scoreboard players operation #map_yaw se.v = #quant_next se.v
execute store result score #map_pitch se.v run data get storage space_editor:runtime map.pitch 1000
scoreboard players operation #quant_next se.v = #map_pitch se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized float 0.001 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime map.pitch
execute if score #quant_diff se.v matches 0 run scoreboard players operation #map_pitch se.v = #quant_next se.v
execute store result score #map_angle se.v run data get storage space_editor:runtime map.source.rotationY 1000
scoreboard players operation #map_yaw se.v -= #map_angle se.v
execute store result score #map_angle se.v run data get storage space_editor:runtime map.target.rotationY 1000
scoreboard players operation #map_yaw se.v += #map_angle se.v
scoreboard players set #map_circle se.v 360000
scoreboard players add #map_yaw se.v 180000
scoreboard players operation #map_yaw se.v %= #map_circle se.v
scoreboard players remove #map_yaw se.v 180000
execute if data storage space_editor:runtime map.source{flipY:1b} run scoreboard players operation #map_pitch se.v *= #minus_one se.v
execute if data storage space_editor:runtime map.target{flipY:1b} run scoreboard players operation #map_pitch se.v *= #minus_one se.v
execute store result storage space_editor:runtime map.result.yaw float 0.001 run scoreboard players get #map_yaw se.v
execute store result storage space_editor:runtime map.result.pitch float 0.001 run scoreboard players get #map_pitch se.v
