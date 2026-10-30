data remove storage space_editor:runtime map.target
$data modify storage space_editor:runtime map.target set from storage space_editor:document regions[{id:$(regionId)}]
execute unless data storage space_editor:runtime map.target.id run return run function space_editor:projection/remove_debug with storage space_editor:projection route
data modify storage space_editor:runtime map.source set from storage space_editor:projection sourceFrame
data modify storage space_editor:runtime map.point set from entity @s Pos
data modify storage space_editor:runtime map.yaw set from entity @s Rotation[0]
data modify storage space_editor:runtime map.pitch set from entity @s Rotation[1]
function space_editor:mapping/position
data modify storage space_editor:projection render set from storage space_editor:projection route
data modify storage space_editor:projection render.result set from storage space_editor:runtime map.result
data modify storage space_editor:projection render.debug set value 1
function space_editor:projection/prepare_render
function space_editor:projection/render_debug with storage space_editor:projection render
