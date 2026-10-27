data remove storage space_editor:runtime currentMask
$data modify storage space_editor:runtime currentMask set from storage space_editor:document masks[{regionId:$(id)}]
execute unless data storage space_editor:runtime currentMask.id run return 0
function space_editor:mask/delete_loaded
return 1
