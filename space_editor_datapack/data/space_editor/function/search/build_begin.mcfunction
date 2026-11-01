data modify storage space_editor:search building set from storage space_editor:search buildAreas[0]
data modify storage space_editor:search building.candidates set value []
data modify storage space_editor:search buildCandidates set value []
function space_editor:search/build_dimension with storage space_editor:search building
execute store result score #area_x1 pr.v run data get storage space_editor:search building.x1m
execute store result score #area_x2 pr.v run data get storage space_editor:search building.x2m
execute store result score #area_y1 pr.v run data get storage space_editor:search building.y1m
execute store result score #area_y2 pr.v run data get storage space_editor:search building.y2m
execute store result score #area_z1 pr.v run data get storage space_editor:search building.z1m
execute store result score #area_z2 pr.v run data get storage space_editor:search building.z2m
