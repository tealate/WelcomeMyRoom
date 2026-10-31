$execute unless score @s se.instance matches $(currentInstanceId) run return 0
$execute unless data storage space_editor:document spaceLinkGroups[{id:$(groupId),members:[$(sourceId),$(targetId)]}] run return 0
data modify storage space_editor:runtime map set value {}
$data modify storage space_editor:runtime map.source set from storage space_editor:document regions[{id:$(sourceId),kind:"space_link",spaceLinkGroupId:$(groupId)}]
$data modify storage space_editor:runtime map.target set from storage space_editor:document regions[{id:$(targetId),kind:"space_link",spaceLinkGroupId:$(groupId)}]
execute unless data storage space_editor:runtime map.source.id run return 0
execute unless data storage space_editor:runtime map.target.id run return 0
execute if data storage space_editor:projection route{suspended:1b} run return run function space_editor:projection/suspended with storage space_editor:projection route
function space_editor:projection/source_dimension with storage space_editor:runtime map.source
execute unless score #dimension pr.v matches 1 run return 0
data modify storage space_editor:runtime map.point set from entity @s Pos
data modify storage space_editor:runtime map.yaw set from entity @s Rotation[0]
data modify storage space_editor:runtime map.pitch set from entity @s Rotation[1]
$data modify storage space_editor:runtime map.result set from storage space_editor:runtime spaceLinkContacts[{uuid:$(uuid),sourceRegionId:$(sourceId),targetRegionId:$(targetId)}].destination
execute unless data storage space_editor:runtime map.result run function space_editor:mapping/position
data modify storage space_editor:projection route.point set from storage space_editor:runtime map.result.point
data modify storage space_editor:projection route.roomId set from storage space_editor:runtime map.target.roomId
data modify storage space_editor:projection route.dimension set from storage space_editor:runtime map.target.dimension
data modify storage space_editor:projection route.targetInstanceId set value 0
execute if data storage space_editor:runtime map.target.instanceId run data modify storage space_editor:projection route.targetInstanceId set from storage space_editor:runtime map.target.instanceId
data modify storage space_editor:projection exists set value []
function space_editor:projection/existence_lookup with storage space_editor:projection route
scoreboard players set #exists pr.v 0
data modify storage space_editor:runtime projectionPoint set from storage space_editor:projection route.point
execute store result score #spx se.v run data get storage space_editor:runtime projectionPoint[0] 2000
scoreboard players operation #quant_next se.v = #spx se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime projectionPoint[0]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #spx se.v = #quant_next se.v
execute store result score #spy se.v run data get storage space_editor:runtime projectionPoint[1] 2000
scoreboard players operation #quant_next se.v = #spy se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime projectionPoint[1]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #spy se.v = #quant_next se.v
execute store result score #spz se.v run data get storage space_editor:runtime projectionPoint[2] 2000
scoreboard players operation #quant_next se.v = #spz se.v
scoreboard players add #quant_next se.v 1
execute store result storage space_editor:runtime quantized double 0.0005 run scoreboard players get #quant_next se.v
execute store success score #quant_diff se.v run data modify storage space_editor:runtime quantized set from storage space_editor:runtime projectionPoint[2]
execute if score #quant_diff se.v matches 0 run scoreboard players operation #spz se.v = #quant_next se.v
function space_editor:projection/existence_scan
execute unless score #exists pr.v matches 1 run return 0
scoreboard players set #valid pr.v 1
data modify storage space_editor:projection sourceFrame set from storage space_editor:runtime map.source
data modify storage space_editor:projection targetFrame set from storage space_editor:runtime map.target
function space_editor:projection/appearance
data modify storage space_editor:projection render set from storage space_editor:projection route
data modify storage space_editor:projection render.result set from storage space_editor:runtime map.result
data modify storage space_editor:projection render.debug set value 0
function space_editor:projection/prepare_render
function space_editor:projection/render_production with storage space_editor:projection render
execute if score @s pr.debug matches 1 run function space_editor:projection/debug_resolve with storage space_editor:projection route
execute unless score @s pr.debug matches 1 run function space_editor:projection/remove_debug with storage space_editor:projection route
