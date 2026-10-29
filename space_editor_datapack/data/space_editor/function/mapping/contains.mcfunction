scoreboard players set #inside se.v 0
$execute unless dimension $(dimension) run return 0
execute store result score #bound se.v run data get storage space_editor:runtime spatialRegion.x1m 2
execute if score #spx se.v < #bound se.v run return 0
execute store result score #bound se.v run data get storage space_editor:runtime spatialRegion.x2m 2
execute if score #spx se.v >= #bound se.v run return 0
execute store result score #bound se.v run data get storage space_editor:runtime spatialRegion.y1m 2
execute if score #spy se.v < #bound se.v run return 0
execute store result score #bound se.v run data get storage space_editor:runtime spatialRegion.y2m 2
execute if score #spy se.v >= #bound se.v run return 0
execute store result score #bound se.v run data get storage space_editor:runtime spatialRegion.z1m 2
execute if score #spz se.v < #bound se.v run return 0
execute store result score #bound se.v run data get storage space_editor:runtime spatialRegion.z2m 2
execute if score #spz se.v >= #bound se.v run return 0
scoreboard players set #inside se.v 1
