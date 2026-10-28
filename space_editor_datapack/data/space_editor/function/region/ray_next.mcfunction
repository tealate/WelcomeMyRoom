data modify storage space_editor:runtime candidate set from storage space_editor:runtime rayQueue[0]
function space_editor:region/ray_check with storage space_editor:runtime candidate
data remove storage space_editor:runtime rayQueue[0]
execute if score #ray_best se.v matches 1.. if data storage space_editor:runtime rayQueue[0] run function space_editor:region/ray_next
