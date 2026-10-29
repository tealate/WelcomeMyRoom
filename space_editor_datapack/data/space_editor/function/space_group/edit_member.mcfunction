$execute unless data storage space_editor:runtime partner{id:$(id)} unless data storage space_editor:runtime {activeTool:"move"} run function space_editor:pair/sync_bounds
$execute if data storage space_editor:runtime partner{id:$(id)} run data modify storage space_editor:runtime partner set from storage space_editor:runtime hit
data modify storage space_editor:runtime frame set from storage space_editor:runtime partner
function space_editor:space_group/validate_frame
data modify storage space_editor:runtime sg.after append from storage space_editor:runtime frame
