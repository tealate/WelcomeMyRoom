$data modify storage space_editor:runtime sgConfig set from storage space_editor:document regionPairs[{id:$(id)}]
$data modify storage space_editor:runtime sgConfig.groupId set value $(groupId)
$data modify storage space_editor:runtime sgConfig.roomA set value "$(roomA)"
$data modify storage space_editor:runtime sgConfig.roomB set value "$(roomB)"
execute store result score #sg_cfg se.v run data get storage space_editor:runtime sgConfig.groupId
execute unless score #sg_cfg se.v matches 0.. run return 0
$execute if score #sg_cfg se.v matches 1.. if data storage space_editor:document linkGroups[{id:$(groupId)}] unless data storage space_editor:document linkGroups[{id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}] run return 0
$execute if score #sg_cfg se.v matches 1.. unless data storage space_editor:document linkGroups[{id:$(groupId)}] run data modify storage space_editor:document linkGroups append value {id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}
function space_editor:space_group/configure_rooms with storage space_editor:runtime sgConfig
$data modify storage space_editor:document regionPairs[{id:$(id)}] set from storage space_editor:runtime sgConfig
function space_editor:link/clean_groups
function space_editor:link/validate_groups
