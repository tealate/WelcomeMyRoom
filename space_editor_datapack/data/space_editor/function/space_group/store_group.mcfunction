$execute unless data storage space_editor:document spaceLinkGroups[{id:$(id)}] run data modify storage space_editor:document spaceLinkGroups append from storage space_editor:runtime sg.group
$data modify storage space_editor:document spaceLinkGroups[{id:$(id)}] set from storage space_editor:runtime sg.group
execute store result score #sg_id se.v run data get storage space_editor:runtime sg.group.id 1
scoreboard players add #sg_id se.v 1
execute store result score #sg_next se.v run data get storage space_editor:document nextSpaceLinkGroupId 1
execute if score #sg_id se.v > #sg_next se.v store result storage space_editor:document nextSpaceLinkGroupId int 1 run scoreboard players get #sg_id se.v
