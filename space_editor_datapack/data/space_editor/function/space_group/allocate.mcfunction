execute store result score #sg_id se.v run data get storage space_editor:document nextSpaceLinkGroupId 1
execute unless score #sg_id se.v matches 1..2147483646 run scoreboard players set #sg_id se.v 1
data modify storage space_editor:runtime sgIds set from storage space_editor:document spaceLinkGroups
function space_editor:space_group/id_scan
execute if data storage space_editor:runtime sgIds[0] run scoreboard players set #sg_ok se.v 0
execute unless score #sg_id se.v matches 1..2147483646 run scoreboard players set #sg_ok se.v 0
execute store result storage space_editor:runtime sg.group.id int 1 run scoreboard players get #sg_id se.v
