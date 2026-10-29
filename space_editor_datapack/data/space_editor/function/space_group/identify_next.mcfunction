data modify storage space_editor:runtime frame set from storage space_editor:runtime sg.queue[0]
function space_editor:pair/frame
execute if data storage space_editor:runtime frame.pairId run data modify storage space_editor:runtime frame.legacyPairId set from storage space_editor:runtime frame.pairId
data remove storage space_editor:runtime frame.pairId
data remove storage space_editor:runtime frame.partnerId
data remove storage space_editor:runtime frame.side
data modify storage space_editor:runtime frame.kind set value "space_link"
data modify storage space_editor:runtime frame.spaceLinkGroupId set from storage space_editor:runtime sg.group.id
execute unless data storage space_editor:runtime frame.roomId run data modify storage space_editor:runtime frame.roomId set value ""
data modify storage space_editor:runtime sg.after append from storage space_editor:runtime frame
data remove storage space_editor:runtime sg.queue[0]
