data remove storage space_editor:runtime currentMask
$data modify storage space_editor:runtime currentMask set from storage space_editor:document masks[{regionId:$(id)}]
execute unless data storage space_editor:runtime currentMask.id run return 0
data modify storage space_editor:runtime maskActionType set value "mask_update"
data modify storage space_editor:runtime maskActionOperation set value "region_sync"
data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask
function space_editor:mask/action_append
