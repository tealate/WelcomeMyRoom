data modify storage space_editor:runtime frame set from storage space_editor:runtime renderRegion
function space_editor:pair/frame
data modify storage space_editor:runtime frame.pairId set from storage space_editor:runtime frame.spaceLinkGroupId
data modify storage space_editor:runtime frame.side set from storage space_editor:runtime frame.idText
function space_editor:pair/spawn_frame with storage space_editor:runtime frame
function space_editor:pair/direction_points
function space_editor:space_group/spawn_directions with storage space_editor:runtime frame
