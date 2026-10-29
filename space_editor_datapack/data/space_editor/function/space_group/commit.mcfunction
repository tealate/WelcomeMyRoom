function space_editor:space_group/store
function space_editor:space_group/action
data modify storage space_editor:runtime sgPreviewQueue set from storage space_editor:runtime sg.after
function space_editor:space_group/preview_scan
execute if data storage space_editor:runtime hit.id run function space_editor:preview/reload_hit with storage space_editor:runtime hit
function space_editor:link/validate_groups
scoreboard players set #pair_ok se.v 1
