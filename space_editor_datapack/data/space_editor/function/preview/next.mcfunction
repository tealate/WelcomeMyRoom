data modify storage space_editor:runtime renderRegion set from storage space_editor:runtime renderQueue[0]
function space_editor:preview/prepare
function space_editor:preview/spawn with storage space_editor:runtime renderRegion
data remove storage space_editor:runtime renderQueue[0]
execute if data storage space_editor:runtime renderQueue[0] run function space_editor:preview/next
