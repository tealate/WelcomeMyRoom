$data modify storage space_editor:runtime pairPending.frame set from storage space_editor:document regions[{id:$(source)}]
data modify storage space_editor:runtime frame set from storage space_editor:runtime pairPending.frame
function space_editor:pair/frame
data modify storage space_editor:runtime pairPending.frame set from storage space_editor:runtime frame
data remove storage space_editor:runtime pairPending.frame.spaceLinkGroupId
data remove storage space_editor:runtime pairPending.frame.legacyPairId
data remove storage space_editor:runtime pairPending.frame.pairId
data remove storage space_editor:runtime pairPending.frame.partnerId
data remove storage space_editor:runtime pairPending.frame.side
