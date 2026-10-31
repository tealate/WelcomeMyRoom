$execute unless data storage space_editor:projection players[{id:$(owner)}].next[{groupId:$(spaceLinkGroupId),sourceId:$(sourceRegionId)}] run data modify storage space_editor:projection players[{id:$(owner)}].next append value {groupId:$(spaceLinkGroupId),sourceId:$(sourceRegionId)}
$execute if data storage space_editor:projection players[{id:$(owner)}].previous[{groupId:$(spaceLinkGroupId),sourceId:$(sourceRegionId)}] run return 0
$data remove storage space_editor:projection active[{owner:$(owner),groupId:$(spaceLinkGroupId),entrySourceId:$(sourceRegionId),targetId:$(targetRegionId),sourceInstanceId:$(instanceId),suspended:1b}]
$execute if data storage space_editor:projection active[{owner:$(owner),groupId:$(spaceLinkGroupId),entrySourceId:$(sourceRegionId),targetId:$(targetRegionId),sourceInstanceId:$(instanceId)}] run return 0
execute if data storage space_editor:projection contact{targetRoomId:""} run return run scoreboard players add #blocked pr.v 1
$execute unless data storage space_editor:document regions[{kind:"proxy_existence",roomId:"$(targetRoomId)"}] run return run scoreboard players add #blocked pr.v 1
execute store result score #count pr.v run data get storage space_editor:projection active
execute if score #count pr.v matches 256.. run return run scoreboard players add #blocked pr.v 1
$data modify storage space_editor:projection new set value {owner:$(owner),uuid:$(uuid),groupId:$(spaceLinkGroupId),entrySourceId:$(sourceRegionId),sourceId:$(sourceRegionId),targetId:$(targetRegionId),sourceInstanceId:$(instanceId),currentInstanceId:$(instanceId),targetInstanceId:0}
data modify storage space_editor:projection new.id set from storage space_editor:projection nextId
execute store result score #next pr.v run data get storage space_editor:projection nextId
scoreboard players add #next pr.v 1
execute store result storage space_editor:projection nextId int 1 run scoreboard players get #next pr.v
data modify storage space_editor:projection active append from storage space_editor:projection new
