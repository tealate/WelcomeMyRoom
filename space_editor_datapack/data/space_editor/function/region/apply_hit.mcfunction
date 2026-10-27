data modify storage space_editor:document selectedId set from storage space_editor:runtime hit.idText
execute if data storage space_editor:runtime {activeTool:"copy"} run return run function space_editor:copy/start
execute if data storage space_editor:runtime {activeTool:"fill"} run return run function space_editor:fill/offhand
execute if data storage space_editor:runtime {activeTool:"mask_create"} run return run function space_editor:mask/create_selected
scoreboard players set #mask_deleted se.v 0
execute if data storage space_editor:runtime {activeTool:"delete"} store result score #mask_deleted se.v run function space_editor:mask/delete_attached with storage space_editor:runtime hit
execute if score #mask_deleted se.v matches 1 run return 0
execute if data storage space_editor:runtime {activeTool:"delete"} run return run function space_editor:region/delete_selected
execute if data storage space_editor:runtime {activeTool:"move"} run return run function space_editor:region/move
execute if data storage space_editor:runtime {activeTool:"resize_all"} run return run function space_editor:region/resize_all
function space_editor:region/resize_face
