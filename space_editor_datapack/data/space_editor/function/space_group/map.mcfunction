scoreboard players set #map_ok se.v 0
data remove storage space_editor:runtime map.result
data remove storage space_editor:runtime map.source
data remove storage space_editor:runtime map.target
$data modify storage space_editor:runtime map.source set from storage space_editor:document regions[{id:$(source),spaceLinkGroupId:$(groupId)}]
$data modify storage space_editor:runtime map.target set from storage space_editor:document regions[{id:$(target),spaceLinkGroupId:$(groupId)}]
execute unless data storage space_editor:runtime map.source.id run return 0
execute unless data storage space_editor:runtime map.target.id run return 0
function space_editor:space_group/load with storage space_editor:runtime map.source
execute unless score #sg_ok se.v matches 1 run return 0
$execute unless data storage space_editor:runtime sg.before.regions[{id:$(source)}] run return 0
$execute unless data storage space_editor:runtime sg.before.regions[{id:$(target)}] run return 0
function space_editor:mapping/position
