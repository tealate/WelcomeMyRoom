execute store result score #action se.v run data get storage space_editor:document nextActionId 1
data modify storage space_editor:runtime maskAction set value {id:0,type:"",operation:"",mask:{},order:0}
execute store result storage space_editor:runtime maskAction.id int 1 run scoreboard players get #action se.v
execute store result storage space_editor:runtime maskAction.order int 1 run scoreboard players get #action se.v
data modify storage space_editor:runtime maskAction.type set from storage space_editor:runtime maskActionType
data modify storage space_editor:runtime maskAction.operation set from storage space_editor:runtime maskActionOperation
data modify storage space_editor:runtime maskAction.mask set from storage space_editor:runtime maskActionRecord
data modify storage space_editor:document actions append from storage space_editor:runtime maskAction
scoreboard players add #action se.v 1
execute store result storage space_editor:document nextActionId int 1 run scoreboard players get #action se.v
