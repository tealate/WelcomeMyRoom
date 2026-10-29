scoreboard players set #pair_ok se.v 0
data remove storage space_editor:runtime hit
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(id)}]
function space_editor:space_group/load with storage space_editor:runtime hit
execute unless score #sg_ok se.v matches 1 run return 0
data modify storage space_editor:runtime frame set from storage space_editor:runtime hit
$data modify storage space_editor:runtime frame.rotationY set value $(rotationY)
$data modify storage space_editor:runtime frame.flipY set value $(flipY)b
execute unless data storage space_editor:runtime frame{rotationY:0} unless data storage space_editor:runtime frame{rotationY:90} unless data storage space_editor:runtime frame{rotationY:180} unless data storage space_editor:runtime frame{rotationY:270} run return 0
execute unless data storage space_editor:runtime frame{flipY:0b} unless data storage space_editor:runtime frame{flipY:1b} run return 0
function space_editor:pair/pose_bounds
execute unless score #frame_ok se.v matches 1 run return 0
data modify storage space_editor:runtime sg.after set from storage space_editor:runtime sg.before.regions
$data modify storage space_editor:runtime sg.after[{id:$(id)}] set from storage space_editor:runtime frame
data modify storage space_editor:runtime sg.operation set value "pose"
function space_editor:space_group/commit
