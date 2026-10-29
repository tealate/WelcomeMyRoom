scoreboard players set #pair_ok se.v 0
data remove storage space_editor:runtime sgDelete
$data modify storage space_editor:runtime sgDelete set from storage space_editor:document regions[{id:$(id)}]
function space_editor:space_group/load with storage space_editor:runtime sgDelete
execute unless score #sg_ok se.v matches 1 run return 0
data modify storage space_editor:runtime sg.before.masks set value []
$data modify storage space_editor:runtime sg.before.masks append from storage space_editor:document masks[{regionId:$(id)}]
data modify storage space_editor:runtime sg.before.compatibilityPairs set value []
$data modify storage space_editor:runtime sg.before.compatibilityPairs append from storage space_editor:document regionPairs[{kind:"space_link",a:$(id)}]
$data modify storage space_editor:runtime sg.before.compatibilityPairs append from storage space_editor:document regionPairs[{kind:"space_link",b:$(id)}]
execute unless data storage space_editor:document retiredSpaceLinkPairs run data modify storage space_editor:document retiredSpaceLinkPairs set value []
data modify storage space_editor:document retiredSpaceLinkPairs append from storage space_editor:runtime sg.before.compatibilityPairs[]
data modify storage space_editor:runtime sg.after set from storage space_editor:runtime sg.before.regions
$data remove storage space_editor:runtime sg.after[{id:$(id)}]
data modify storage space_editor:runtime sg.group.members set value []
data modify storage space_editor:runtime sg.queue set from storage space_editor:runtime sg.after
function space_editor:space_group/member_ids
execute store result score #sg_left se.v run data get storage space_editor:runtime sg.after
execute if score #sg_left se.v matches 1 run function space_editor:space_group/dissolve
execute if score #sg_left se.v matches 2.. run function space_editor:space_group/store
$data remove storage space_editor:document regions[{id:$(id)}]
$data remove storage space_editor:document masks[{regionId:$(id)}]
$data remove storage space_editor:document regionPairs[{kind:"space_link",a:$(id)}]
$data remove storage space_editor:document regionPairs[{kind:"space_link",b:$(id)}]
$data remove storage space_editor:runtime spaceLinkContacts[{sourceRegionId:$(id)}]
$data remove storage space_editor:runtime spaceLinkContacts[{targetRegionId:$(id)}]
data modify storage space_editor:runtime sg.operation set value "delete"
function space_editor:space_group/action
function space_editor:pair/cancel
data remove storage space_editor:runtime hit
data modify storage space_editor:document selectedId set value ""
function space_editor:link/clean_groups
function space_editor:link/validate_groups
function space_editor:preview/resync
scoreboard players set #pair_ok se.v 1
