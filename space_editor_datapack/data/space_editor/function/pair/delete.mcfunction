$function space_editor:pair/load {pairId:$(pairId)}
execute unless data storage space_editor:runtime pair.id run return 0
function space_editor:pair/snapshot
data modify storage space_editor:runtime pairBefore.masks set from storage space_editor:document masks
data modify storage space_editor:runtime pairOperation set value "delete"
function space_editor:pair/action
function space_editor:pair/remove with storage space_editor:runtime pair
data remove storage space_editor:runtime hit
data modify storage space_editor:document selectedId set value ""
function space_editor:pair/cancel
function space_editor:preview/resync
