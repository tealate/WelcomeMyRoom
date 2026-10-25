execute store result score #center_a se.v run data get storage space_editor:runtime renderRegion.x1 10
execute store result score #center_b se.v run data get storage space_editor:runtime renderRegion.x2 10
scoreboard players operation #center_a se.v += #center_b se.v
scoreboard players operation #center_a se.v /= #two se.v
execute store result storage space_editor:runtime renderRegion.cx double 0.1 run scoreboard players get #center_a se.v
execute store result score #center_a se.v run data get storage space_editor:runtime renderRegion.y1 10
execute store result score #center_b se.v run data get storage space_editor:runtime renderRegion.y2 10
scoreboard players operation #center_a se.v += #center_b se.v
scoreboard players operation #center_a se.v /= #two se.v
execute store result storage space_editor:runtime renderRegion.cy double 0.1 run scoreboard players get #center_a se.v
execute store result score #center_a se.v run data get storage space_editor:runtime renderRegion.z1 10
execute store result score #center_b se.v run data get storage space_editor:runtime renderRegion.z2 10
scoreboard players operation #center_a se.v += #center_b se.v
scoreboard players operation #center_a se.v /= #two se.v
execute store result storage space_editor:runtime renderRegion.cz double 0.1 run scoreboard players get #center_a se.v
