execute store result score #map_px se.v run data get storage space_editor:runtime map.vector[0] 2000
execute store result score #map_py se.v run data get storage space_editor:runtime map.vector[1] 2000
execute store result score #map_pz se.v run data get storage space_editor:runtime map.vector[2] 2000
function space_editor:mapping/vector_scores
execute store result storage space_editor:runtime map.result.vector[0] double 0.0005 run scoreboard players get #map_ox se.v
execute store result storage space_editor:runtime map.result.vector[1] double 0.0005 run scoreboard players get #map_oy se.v
execute store result storage space_editor:runtime map.result.vector[2] double 0.0005 run scoreboard players get #map_oz se.v
