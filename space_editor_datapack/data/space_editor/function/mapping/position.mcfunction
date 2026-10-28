data remove storage space_editor:runtime map.result
scoreboard players set #map_ok se.v 1
execute unless data storage space_editor:runtime map.source.rotationY run data modify storage space_editor:runtime map.source.rotationY set value 0
execute unless data storage space_editor:runtime map.source.flipY run data modify storage space_editor:runtime map.source.flipY set value 0b
execute store result score #map_source_x se.v run data get storage space_editor:runtime map.source.x1m 1
execute store result score #map_tmp se.v run data get storage space_editor:runtime map.source.x2m 1
scoreboard players operation #map_source_x se.v += #map_tmp se.v
execute store result score #map_source_y se.v run data get storage space_editor:runtime map.source.y1m 1
execute store result score #map_tmp se.v run data get storage space_editor:runtime map.source.y2m 1
scoreboard players operation #map_source_y se.v += #map_tmp se.v
execute store result score #map_source_z se.v run data get storage space_editor:runtime map.source.z1m 1
execute store result score #map_tmp se.v run data get storage space_editor:runtime map.source.z2m 1
scoreboard players operation #map_source_z se.v += #map_tmp se.v
execute unless data storage space_editor:runtime map.target.rotationY run data modify storage space_editor:runtime map.target.rotationY set value 0
execute unless data storage space_editor:runtime map.target.flipY run data modify storage space_editor:runtime map.target.flipY set value 0b
execute store result score #map_target_x se.v run data get storage space_editor:runtime map.target.x1m 1
execute store result score #map_tmp se.v run data get storage space_editor:runtime map.target.x2m 1
scoreboard players operation #map_target_x se.v += #map_tmp se.v
execute store result score #map_target_y se.v run data get storage space_editor:runtime map.target.y1m 1
execute store result score #map_tmp se.v run data get storage space_editor:runtime map.target.y2m 1
scoreboard players operation #map_target_y se.v += #map_tmp se.v
execute store result score #map_target_z se.v run data get storage space_editor:runtime map.target.z1m 1
execute store result score #map_tmp se.v run data get storage space_editor:runtime map.target.z2m 1
scoreboard players operation #map_target_z se.v += #map_tmp se.v
execute store result score #map_px se.v run data get storage space_editor:runtime map.point[0] 2000
scoreboard players operation #map_px se.v -= #map_source_x se.v
execute store result score #map_py se.v run data get storage space_editor:runtime map.point[1] 2000
scoreboard players operation #map_py se.v -= #map_source_y se.v
execute store result score #map_pz se.v run data get storage space_editor:runtime map.point[2] 2000
scoreboard players operation #map_pz se.v -= #map_source_z se.v
function space_editor:mapping/vector_scores
data modify storage space_editor:runtime map.result set value {point:[0d,0d,0d],vector:[0d,0d,0d],yaw:0f,pitch:0f}
data modify storage space_editor:runtime map.result.dimension set from storage space_editor:runtime map.target.dimension
scoreboard players operation #map_ox se.v += #map_target_x se.v
execute store result storage space_editor:runtime map.result.point[0] double 0.0005 run scoreboard players get #map_ox se.v
execute store result storage space_editor:runtime map.result.x double 0.0005 run scoreboard players get #map_ox se.v
scoreboard players operation #map_oy se.v += #map_target_y se.v
execute store result storage space_editor:runtime map.result.point[1] double 0.0005 run scoreboard players get #map_oy se.v
execute store result storage space_editor:runtime map.result.y double 0.0005 run scoreboard players get #map_oy se.v
scoreboard players operation #map_oz se.v += #map_target_z se.v
execute store result storage space_editor:runtime map.result.point[2] double 0.0005 run scoreboard players get #map_oz se.v
execute store result storage space_editor:runtime map.result.z double 0.0005 run scoreboard players get #map_oz se.v
execute if data storage space_editor:runtime map.vector run function space_editor:mapping/vector
execute if data storage space_editor:runtime map.yaw run function space_editor:mapping/look
