data remove storage space_editor:runtime hit
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(id)}]
execute unless data storage space_editor:runtime hit.spaceLinkGroupId run return 0
function space_editor:space_group/load with storage space_editor:runtime hit
execute unless score #sg_ok se.v matches 1 run return 0
data modify storage space_editor:runtime sg.after set from storage space_editor:runtime sg.before.regions
$data modify storage space_editor:runtime sg.after[{id:$(id)}].roomId set value "$(roomId)"
data modify storage space_editor:runtime sg.operation set value "room"
function space_editor:space_group/commit
