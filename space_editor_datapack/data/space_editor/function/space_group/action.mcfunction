data modify storage space_editor:runtime sgAction set value {type:"space_link_group_edit",after:{}}
data modify storage space_editor:runtime sgAction.operation set from storage space_editor:runtime sg.operation
data modify storage space_editor:runtime sgAction.before set from storage space_editor:runtime sg.before
data modify storage space_editor:runtime sgAction.after.group set from storage space_editor:runtime sg.group
data modify storage space_editor:runtime sgAction.after.regions set from storage space_editor:runtime sg.after
execute store result score #sg_action se.v run data get storage space_editor:document nextActionId 1
execute store result storage space_editor:runtime sgAction.id int 1 run scoreboard players get #sg_action se.v
execute store result storage space_editor:runtime sgAction.order int 1 run scoreboard players get #sg_action se.v
data modify storage space_editor:document actions append from storage space_editor:runtime sgAction
scoreboard players add #sg_action se.v 1
execute store result storage space_editor:document nextActionId int 1 run scoreboard players get #sg_action se.v
