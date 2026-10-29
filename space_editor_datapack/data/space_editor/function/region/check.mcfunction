$execute unless dimension $(dimension) run return 0
execute if data storage space_editor:runtime {activeTool:"pair_select"} if data storage space_editor:runtime candidate.kind run function space_editor:pair/filter
execute if data storage space_editor:runtime {activeTool:"pair_select"} if data storage space_editor:runtime candidate.kind if score #pair_filter se.v matches 0 run return 0
execute store result score #lo se.v run data get storage space_editor:runtime candidate.x1m 1
execute store result score #hi se.v run data get storage space_editor:runtime candidate.x2m 1
execute if score #px se.v < #lo se.v run return 0
execute if score #px se.v >= #hi se.v run return 0
execute store result score #lo se.v run data get storage space_editor:runtime candidate.y1m 1
execute store result score #hi se.v run data get storage space_editor:runtime candidate.y2m 1
execute if score #py se.v < #lo se.v run return 0
execute if score #py se.v >= #hi se.v run return 0
execute store result score #lo se.v run data get storage space_editor:runtime candidate.z1m 1
execute store result score #hi se.v run data get storage space_editor:runtime candidate.z2m 1
execute if score #pz se.v < #lo se.v run return 0
execute if score #pz se.v >= #hi se.v run return 0
data modify storage space_editor:runtime hit set from storage space_editor:runtime candidate
function space_editor:region/face
