execute if data storage space_editor:runtime highlightedRegion run function space_editor:preview/clear_highlight with storage space_editor:runtime highlightedRegion
function space_editor:preview/update_region with storage space_editor:runtime hit
execute if data storage space_editor:document {editMode:1b} if data storage space_editor:document settings{regionsVisible:1b} run function space_editor:preview/highlight with storage space_editor:runtime hit
