data remove storage space_editor:runtime contactGroup
$data modify storage space_editor:runtime contactGroup set from storage space_editor:document spaceLinkGroups[{id:$(spaceLinkGroupId)}]
execute unless data storage space_editor:runtime contactGroup.id run return 0
data modify storage space_editor:runtime contactSource set from storage space_editor:runtime spatialRegion
data modify storage space_editor:runtime sg.group.localSize set from storage space_editor:runtime contactGroup.localSize
data modify storage space_editor:runtime frame set from storage space_editor:runtime contactSource
scoreboard players set #sg_ok se.v 1
function space_editor:space_group/validate_frame
execute unless score #sg_ok se.v matches 1 run return 0
execute store result score #contact_count se.v run data get storage space_editor:runtime contactGroup.members
execute unless score #contact_count se.v matches 2..4096 run return 0
data modify storage space_editor:runtime contactMembers set from storage space_editor:runtime contactGroup.members
scoreboard players set #source_member se.v 0
function space_editor:link/source_scan
execute unless score #source_member se.v matches 1 run return 0
data modify storage space_editor:runtime contactMembers set from storage space_editor:runtime contactGroup.members
data modify storage space_editor:runtime contactSeen set value []
function space_editor:link/target_scan
