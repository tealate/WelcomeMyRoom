data remove storage space_editor:runtime hit
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(id)}]
execute if data storage space_editor:runtime hit.id run function space_editor:region/delete_selected
$data remove storage space_editor:document projection.debugMaps[{targetId:$(id)}]
data modify storage space_editor:projection demoPaths set value []
$data modify storage space_editor:projection demoPaths append from storage space_editor:projection active[{sourceId:$(id)}]
$data modify storage space_editor:projection demoPaths append from storage space_editor:projection active[{targetId:$(id)}]
function space_editor:projection/demo/purge_scan
