$execute unless data storage space_editor:document projection.visual.$(pose) run return 0
$data modify storage space_editor:projection visualInput set value $(pivot)
execute store result score #pivot pr.v run data get storage space_editor:projection visualInput 1000
execute unless score #pivot pr.v matches 0..4000 run return 0
$execute store result storage space_editor:document projection.visual.$(pose) int 1 run scoreboard players get #pivot pr.v
