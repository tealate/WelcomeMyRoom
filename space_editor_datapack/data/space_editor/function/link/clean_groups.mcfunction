data modify storage space_editor:runtime cleanGroups set from storage space_editor:document linkGroups
execute if data storage space_editor:runtime cleanGroups[0] run function space_editor:link/clean_next
