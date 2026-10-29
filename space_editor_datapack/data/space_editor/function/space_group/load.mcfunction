data modify storage space_editor:runtime sg set value {before:{regions:[]},after:[]}
scoreboard players set #sg_ok se.v 0
data modify storage space_editor:runtime sgUnique set value []
$data modify storage space_editor:runtime sgUnique append from storage space_editor:document spaceLinkGroups[{id:$(spaceLinkGroupId)}]
execute store result score #sg_n se.v run data get storage space_editor:runtime sgUnique
execute unless score #sg_n se.v matches 1 run return 0
$data modify storage space_editor:runtime sg.group set from storage space_editor:document spaceLinkGroups[{id:$(spaceLinkGroupId)}]
data modify storage space_editor:runtime sg.before.group set from storage space_editor:runtime sg.group
scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime sg.group.id run return 0
execute store result score #sg_count se.v run data get storage space_editor:runtime sg.group.members
execute unless score #sg_count se.v matches 2..4096 run return 0
scoreboard players set #sg_ok se.v 1
data modify storage space_editor:runtime sg.queue set from storage space_editor:runtime sg.group.members
function space_editor:space_group/load_scan
