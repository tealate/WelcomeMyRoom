execute store result score #bound pr.v run data get storage space_editor:search candidate.x1m
execute if score #bound pr.v >= #area_x2 pr.v run return 0
execute store result score #bound pr.v run data get storage space_editor:search candidate.x2m
execute if score #bound pr.v <= #area_x1 pr.v run return 0
execute store result score #bound pr.v run data get storage space_editor:search candidate.y1m
execute if score #bound pr.v >= #area_y2 pr.v run return 0
execute store result score #bound pr.v run data get storage space_editor:search candidate.y2m
execute if score #bound pr.v <= #area_y1 pr.v run return 0
execute store result score #bound pr.v run data get storage space_editor:search candidate.z1m
execute if score #bound pr.v >= #area_z2 pr.v run return 0
execute store result score #bound pr.v run data get storage space_editor:search candidate.z2m
execute if score #bound pr.v <= #area_z1 pr.v run return 0
data modify storage space_editor:search building.candidates append from storage space_editor:search candidate
