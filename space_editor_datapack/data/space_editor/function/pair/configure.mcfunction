$execute if data storage space_editor:document regionPairs[{id:$(id)}].spaceLinkGroupId run return run function space_editor:space_group/configure_legacy {id:$(id),groupId:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}
$function space_editor:pair/load {pairId:$(id)}
execute unless data storage space_editor:runtime editA.id run return 0
execute unless data storage space_editor:runtime editB.id run return 0
function space_editor:pair/snapshot
$data modify storage space_editor:runtime pair.groupId set value $(groupId)
$data modify storage space_editor:runtime pair.roomA set value "$(roomA)"
$data modify storage space_editor:runtime pair.roomB set value "$(roomB)"
$data modify storage space_editor:runtime pair.direction set value "$(direction)"
$data modify storage space_editor:runtime pair.cooldownTicks set value $(cooldownTicks)
execute store result score #config_group se.v run data get storage space_editor:runtime pair.groupId 1
execute store result score #config_cool se.v run data get storage space_editor:runtime pair.cooldownTicks 1
execute unless score #config_group se.v matches 0.. run return 0
execute unless score #config_cool se.v matches 0..1200 run return 0
execute unless data storage space_editor:runtime pair{direction:"both"} unless data storage space_editor:runtime pair{direction:"one_way"} run return 0
$execute if score #config_group se.v matches 1.. if data storage space_editor:document linkGroups[{id:$(groupId)}] unless data storage space_editor:document linkGroups[{id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}] run return run tellraw @s {"text": "[Space Editor] GroupのRoom対応が一致しません。", "color": "red"}
$execute if score #config_group se.v matches 1.. unless data storage space_editor:document linkGroups[{id:$(groupId)}] run data modify storage space_editor:document linkGroups append value {id:$(groupId),roomA:"$(roomA)",roomB:"$(roomB)"}
data modify storage space_editor:runtime editA.roomId set from storage space_editor:runtime pair.roomA
data modify storage space_editor:runtime editB.roomId set from storage space_editor:runtime pair.roomB
data modify storage space_editor:runtime pairOperation set value "configure"
function space_editor:pair/commit
function space_editor:link/clean_groups
