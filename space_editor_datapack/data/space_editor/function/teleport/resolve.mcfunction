data remove storage space_editor:runtime tpTarget
data remove storage space_editor:runtime tpPair
$data modify storage space_editor:runtime tpTarget set from storage space_editor:document regions[{id:$(partnerId)}]
$data modify storage space_editor:runtime tpPair set from storage space_editor:document regionPairs[{id:$(pairId),kind:"teleport"}]
execute unless data storage space_editor:runtime tpTarget.id run return 0
execute unless data storage space_editor:runtime tpPair.id run return 0
execute if data storage space_editor:runtime tpPair{direction:"one_way"} if data storage space_editor:runtime tpHit{side:"B"} run return 0
data modify storage space_editor:runtime map set value {}
data modify storage space_editor:runtime map.source set from storage space_editor:runtime tpHit
data modify storage space_editor:runtime map.target set from storage space_editor:runtime tpTarget
data modify storage space_editor:runtime map.point set from storage space_editor:runtime tpPlayer.point
data modify storage space_editor:runtime map.yaw set from storage space_editor:runtime tpPlayer.rotation[0]
data modify storage space_editor:runtime map.pitch set from storage space_editor:runtime tpPlayer.rotation[1]
function space_editor:mapping/position
scoreboard players set #tp_safe se.v 0
function space_editor:teleport/check_destination with storage space_editor:runtime map.result
execute unless score #tp_safe se.v matches 1 run return 0
scoreboard players set #tp_success se.v 0
function space_editor:teleport/perform with storage space_editor:runtime map.result
execute unless score #tp_success se.v matches 1 run return 0
execute store result score @s se.tp_lock run data get storage space_editor:runtime tpPair.id 1
execute store result score @s se.tp_cd run data get storage space_editor:runtime tpPair.cooldownTicks 1
data modify storage space_editor:runtime transfer set from storage space_editor:runtime tpPlayer
data modify storage space_editor:runtime transfer.pairId set from storage space_editor:runtime tpPair.id
data modify storage space_editor:runtime transfer.sourceRegionId set from storage space_editor:runtime tpHit.id
data modify storage space_editor:runtime transfer.targetRegionId set from storage space_editor:runtime tpTarget.id
data modify storage space_editor:runtime transfer.sourceRoomId set from storage space_editor:runtime tpHit.roomId
data modify storage space_editor:runtime transfer.targetRoomId set from storage space_editor:runtime tpTarget.roomId
data modify storage space_editor:runtime transfer.destination set from storage space_editor:runtime map.result
data modify storage space_editor:runtime transfers append from storage space_editor:runtime transfer
