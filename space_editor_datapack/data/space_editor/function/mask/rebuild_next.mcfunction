data modify storage space_editor:runtime currentMask set from storage space_editor:runtime maskQueue[0]
function space_editor:mask/prepare
execute if score #mask_valid se.v matches 1 run function space_editor:mask/spawn with storage space_editor:runtime maskRender
execute unless score #mask_region_found se.v matches 1 run function space_editor:mask/remove_orphan with storage space_editor:runtime currentMask
data remove storage space_editor:runtime maskQueue[0]
execute if data storage space_editor:runtime maskQueue[0] run function space_editor:mask/rebuild_next
