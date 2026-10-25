data modify storage space_editor:runtime candidate set from storage space_editor:runtime candidates[0]
function space_editor:region/check with storage space_editor:runtime candidate
execute if data storage space_editor:runtime hit run return 0
data remove storage space_editor:runtime candidates[0]
execute if data storage space_editor:runtime candidates[0] run function space_editor:region/check_next
