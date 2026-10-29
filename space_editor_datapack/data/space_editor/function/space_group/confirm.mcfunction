data remove storage space_editor:runtime pairCandidate.pairId
data remove storage space_editor:runtime pairCandidate.side
function space_editor:space_group/add with storage space_editor:runtime pairPending
execute unless score #pair_ok se.v matches 1 run return 0
data modify storage space_editor:runtime pairSession.groupId set from storage space_editor:runtime sg.group.id
function space_editor:space_group/start_add
