data modify storage space_editor:projection render.pose set from storage space_editor:projection pose
data modify storage space_editor:projection render.dimension set from storage space_editor:projection render.result.dimension
data modify storage space_editor:projection render.x set from storage space_editor:projection render.result.x
data modify storage space_editor:projection render.y set from storage space_editor:projection render.result.y
data modify storage space_editor:projection render.z set from storage space_editor:projection render.result.z
data modify storage space_editor:projection render.yaw set from storage space_editor:projection render.result.yaw
data modify storage space_editor:projection render.pitch set from storage space_editor:projection render.result.pitch
scoreboard players set #flip pr.v 0
execute if data storage space_editor:projection sourceFrame{flipY:1b} run scoreboard players add #flip pr.v 1
execute if data storage space_editor:runtime map.target{flipY:1b} run scoreboard players add #flip pr.v 1
execute if score #flip pr.v matches 2 run scoreboard players set #flip pr.v 0
execute store result storage space_editor:projection render.flip int 1 run scoreboard players get #flip pr.v
function space_editor:projection/height with storage space_editor:projection render
