data remove storage space_editor:projection debugMap
$data modify storage space_editor:projection debugMap set from storage space_editor:document projection.debugMaps[{uuid:$(uuid),targetId:$(targetId)}]
execute unless data storage space_editor:projection debugMap.regionId run return run function space_editor:projection/remove_debug with storage space_editor:projection route
function space_editor:projection/debug_frame with storage space_editor:projection debugMap
