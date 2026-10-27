function space_editor:preview/hide
execute unless data storage space_editor:document {editMode:1b} run return 0
execute if data storage space_editor:document settings{regionsVisible:1b} run function space_editor:preview/render_regions
execute if data storage space_editor:runtime selection.a run function space_editor:preview/point
execute if data storage space_editor:document settings{regionsVisible:1b} if data storage space_editor:runtime hit.id run function space_editor:preview/highlight with storage space_editor:runtime hit
execute if data storage space_editor:runtime pastePending run function space_editor:paste/spawn_preview with storage space_editor:runtime pastePending
function space_editor:mask/rebuild_all
