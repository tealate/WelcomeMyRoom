data modify storage space_editor:runtime pairSession.mode set value "add"
data modify storage space_editor:runtime pairPending set value {kind:"space_link"}
data modify storage space_editor:runtime pairPending.source set from storage space_editor:runtime pairSession.selected
function space_editor:space_group/refresh_source with storage space_editor:runtime pairPending
function space_editor:pair/track
