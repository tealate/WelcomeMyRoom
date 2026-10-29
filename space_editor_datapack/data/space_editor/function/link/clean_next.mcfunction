function space_editor:link/clean_one with storage space_editor:runtime cleanGroups[0]
data remove storage space_editor:runtime cleanGroups[0]
execute if data storage space_editor:runtime cleanGroups[0] run function space_editor:link/clean_next
