data modify storage space_editor:runtime map set value {}
data modify storage space_editor:runtime map.source set from storage space_editor:runtime spatialRegion
$data modify storage space_editor:runtime map.target set from storage space_editor:document regions[{id:$(partnerId)}]
execute unless data storage space_editor:runtime map.target.id run return 0
data modify storage space_editor:runtime map.point set from storage space_editor:runtime tpPlayer.point
data modify storage space_editor:runtime map.yaw set from storage space_editor:runtime tpPlayer.rotation[0]
data modify storage space_editor:runtime map.pitch set from storage space_editor:runtime tpPlayer.rotation[1]
function space_editor:mapping/position
data modify storage space_editor:runtime linkContact set from storage space_editor:runtime tpPlayer
$data modify storage space_editor:runtime linkContact.pairId set value $(pairId)
$data modify storage space_editor:runtime linkContact.sourceRegionId set value $(id)
$data modify storage space_editor:runtime linkContact.targetRegionId set value $(partnerId)
data modify storage space_editor:runtime linkContact.sourceRoomId set from storage space_editor:runtime spatialRegion.roomId
data modify storage space_editor:runtime linkContact.targetRoomId set from storage space_editor:runtime map.target.roomId
data modify storage space_editor:runtime linkContact.destination set from storage space_editor:runtime map.result
data modify storage space_editor:runtime spaceLinkContacts append from storage space_editor:runtime linkContact
