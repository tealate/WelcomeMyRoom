data modify storage space_editor:runtime sgUnique set value []
$data modify storage space_editor:runtime sgUnique append from storage space_editor:document regions[{id:$(id)}]
execute store result score #sg_n se.v run data get storage space_editor:runtime sgUnique
execute unless score #sg_n se.v matches 1 run return run scoreboard players set #sg_ok se.v 0
data remove storage space_editor:runtime frame
$data modify storage space_editor:runtime frame set from storage space_editor:document regions[{id:$(id),spaceLinkGroupId:$(groupId),kind:"space_link"}]
execute unless data storage space_editor:runtime frame.id run return run scoreboard players set #sg_ok se.v 0
$execute if data storage space_editor:runtime sg.before.regions[{id:$(id)}] run return run scoreboard players set #sg_ok se.v 0
data modify storage space_editor:runtime sg.before.regions append from storage space_editor:runtime frame
function space_editor:space_group/validate_frame
