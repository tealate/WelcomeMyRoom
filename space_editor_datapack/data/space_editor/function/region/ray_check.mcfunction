$execute unless dimension $(dimension) run return 0
execute if data storage space_editor:runtime {activeTool:"pair_select"} if data storage space_editor:runtime candidate.kind run function space_editor:pair/filter
execute if data storage space_editor:runtime {activeTool:"pair_select"} if data storage space_editor:runtime candidate.kind if score #pair_filter se.v matches 0 run return 0
execute store result score #ray_lo_x se.v run data get storage space_editor:runtime candidate.x1m 1
execute store result score #ray_hi_x se.v run data get storage space_editor:runtime candidate.x2m 1
execute store result score #ray_lo_y se.v run data get storage space_editor:runtime candidate.y1m 1
execute store result score #ray_hi_y se.v run data get storage space_editor:runtime candidate.y2m 1
execute store result score #ray_lo_z se.v run data get storage space_editor:runtime candidate.z1m 1
execute store result score #ray_hi_z se.v run data get storage space_editor:runtime candidate.z2m 1
scoreboard players set #ray_low se.v 0
scoreboard players operation #ray_high se.v = #ray_best se.v
scoreboard players remove #ray_high se.v 1
scoreboard players set #ray_found se.v 513
function space_editor:region/ray_search
execute if score #ray_found se.v < #ray_best se.v run data modify storage space_editor:runtime rayHit set from storage space_editor:runtime candidate
scoreboard players operation #ray_best se.v < #ray_found se.v
