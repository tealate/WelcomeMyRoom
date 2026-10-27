function space_editor:preview/hide
execute unless data storage space_editor:document {editMode:1b} run return 0
data modify storage space_editor:runtime renderQueue set from storage space_editor:document regions
execute if data storage space_editor:runtime renderQueue[0] run function space_editor:preview/next
execute if data storage space_editor:runtime selection.a run function space_editor:preview/point
execute if data storage space_editor:runtime hit.id run function space_editor:preview/highlight with storage space_editor:runtime hit
execute if data storage space_editor:runtime pastePending run function space_editor:paste/spawn_preview with storage space_editor:runtime pastePending
function space_editor:mask/rebuild_all
