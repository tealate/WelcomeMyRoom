data modify storage space_editor:runtime lookup.id set from storage space_editor:runtime pastePending.id
data modify storage space_editor:runtime lookup.owner0 set from storage space_editor:runtime pastePending.owner0
data modify storage space_editor:runtime lookup.owner1 set from storage space_editor:runtime pastePending.owner1
data modify storage space_editor:runtime lookup.owner2 set from storage space_editor:runtime pastePending.owner2
data modify storage space_editor:runtime lookup.owner3 set from storage space_editor:runtime pastePending.owner3
data modify storage space_editor:runtime targetDimension set from storage space_editor:runtime pastePending.targetDimension
data modify storage space_editor:runtime targetPos set value [I;0,0,0]
data modify storage space_editor:runtime targetPos[0] set from storage space_editor:runtime pastePending.x
data modify storage space_editor:runtime targetPos[1] set from storage space_editor:runtime pastePending.y
data modify storage space_editor:runtime targetPos[2] set from storage space_editor:runtime pastePending.z
function space_editor:paste/start with storage space_editor:runtime lookup
execute if data storage space_editor:document job{type:"paste",state:"running"} run function space_editor:paste/hide_preview
execute if data storage space_editor:document job{type:"paste",state:"running"} run data remove storage space_editor:runtime pastePending
