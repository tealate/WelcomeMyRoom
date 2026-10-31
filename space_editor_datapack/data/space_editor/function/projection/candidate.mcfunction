$execute unless data storage space_editor:projection transfer.destination{dimension:"$(dimension)"} run return 0
execute store result score #candidateRot pr.v run data get storage space_editor:projection candidates[0].rotationY
execute store result score #candidateFlip pr.v run data get storage space_editor:projection candidates[0].flipY
execute unless score #candidateRot pr.v = #desiredRot pr.v run return 0
execute unless score #candidateFlip pr.v = #desiredFlip pr.v run return 0
data modify storage space_editor:runtime map set value {}
data modify storage space_editor:runtime map.source set from storage space_editor:projection candidates[0]
function space_editor:projection/rebase_old_frame with storage space_editor:projection rebase
execute unless data storage space_editor:runtime map.target.id run return 0
data modify storage space_editor:runtime map.point set from storage space_editor:projection transfer.destination.point
function space_editor:mapping/position
data modify storage space_editor:runtime projectionPrePoint set from storage space_editor:projection transfer.point
execute store result score #pr_pre_x se.v run data get storage space_editor:runtime projectionPrePoint[0] 2000
scoreboard players operation #quant_next se.v = #pr_pre_x se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime projectionPrePoint[0]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #pr_pre_x se.v = #quant_next se.v
scoreboard players operation #pr_pre_x se.v -= #map_ox se.v
execute unless score #pr_pre_x se.v matches -1..1 run return 0
execute store result score #pr_pre_y se.v run data get storage space_editor:runtime projectionPrePoint[1] 2000
scoreboard players operation #quant_next se.v = #pr_pre_y se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime projectionPrePoint[1]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #pr_pre_y se.v = #quant_next se.v
scoreboard players operation #pr_pre_y se.v -= #map_oy se.v
execute unless score #pr_pre_y se.v matches -1..1 run return 0
execute store result score #pr_pre_z se.v run data get storage space_editor:runtime projectionPrePoint[2] 2000
scoreboard players operation #quant_next se.v = #pr_pre_z se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime projectionPrePoint[2]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #pr_pre_z se.v = #quant_next se.v
scoreboard players operation #pr_pre_z se.v -= #map_oz se.v
execute unless score #pr_pre_z se.v matches -1..1 run return 0
$data modify storage space_editor:projection resolved.sourceId set value $(id)
