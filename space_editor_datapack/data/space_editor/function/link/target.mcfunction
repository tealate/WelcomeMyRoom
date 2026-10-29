$execute if data storage space_editor:runtime contactSource{id:$(id)} run return 0
$execute if data storage space_editor:runtime contactSeen[{id:$(id)}] run return 0
$data modify storage space_editor:runtime contactSeen append value {id:$(id)}
data modify storage space_editor:runtime map set value {}
data modify storage space_editor:runtime map.source set from storage space_editor:runtime contactSource
$data modify storage space_editor:runtime map.target set from storage space_editor:document regions[{id:$(id),spaceLinkGroupId:$(groupId),kind:"space_link"}]
execute unless data storage space_editor:runtime map.target.id run return run function space_editor:link/invalid_target with storage space_editor:runtime contactRef
data modify storage space_editor:runtime sg.group.localSize set from storage space_editor:runtime contactGroup.localSize
scoreboard players set #sg_ok se.v 1
data modify storage space_editor:runtime frame set from storage space_editor:runtime map.target
function space_editor:space_group/validate_frame
execute unless score #sg_ok se.v matches 1 run return run function space_editor:link/invalid_target with storage space_editor:runtime contactRef
data modify storage space_editor:runtime map.point set from storage space_editor:runtime tpPlayer.point
data modify storage space_editor:runtime map.vector set from storage space_editor:runtime tpPlayer.vector
data modify storage space_editor:runtime map.yaw set from storage space_editor:runtime tpPlayer.rotation[0]
data modify storage space_editor:runtime map.pitch set from storage space_editor:runtime tpPlayer.rotation[1]
function space_editor:mapping/position
data modify storage space_editor:runtime linkContact set from storage space_editor:runtime tpPlayer
$data modify storage space_editor:runtime linkContact.spaceLinkGroupId set value $(groupId)
$data modify storage space_editor:runtime linkContact.sourceRegionId set value $(sourceId)
$data modify storage space_editor:runtime linkContact.targetRegionId set value $(id)
data modify storage space_editor:runtime linkContact.sourceRoomId set from storage space_editor:runtime contactSource.roomId
data modify storage space_editor:runtime linkContact.targetRoomId set from storage space_editor:runtime map.target.roomId
data modify storage space_editor:runtime linkContact.destination set from storage space_editor:runtime map.result
$data modify storage space_editor:runtime linkContact.projectionPathId set value {spaceLinkGroupId:$(groupId),sourceRegionId:$(sourceId),targetRegionId:$(id)}
data modify storage space_editor:runtime linkContact.projectionPathId.uuid set from storage space_editor:runtime tpPlayer.uuid
data modify storage space_editor:runtime linkContact.projectionPathId.instanceId set from storage space_editor:runtime tpPlayer.instanceId
data modify storage space_editor:runtime spaceLinkContacts append from storage space_editor:runtime linkContact
