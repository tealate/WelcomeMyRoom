execute store result score #action se.v run data get storage space_editor:document nextActionId 1
data modify storage space_editor:runtime action set value {id:0,type:"template_paste",templateId:0,version:1,targetDimension:"",origin:[I;0,0,0],rotation:0,flipY:0b,order:0}
execute store result storage space_editor:runtime action.id int 1 run scoreboard players get #action se.v
data modify storage space_editor:runtime action.templateId set from storage space_editor:document job.id
data modify storage space_editor:runtime action.version set from storage space_editor:document job.version
data modify storage space_editor:runtime action.targetDimension set from storage space_editor:document job.targetDimension
data modify storage space_editor:runtime action.origin[0] set from storage space_editor:document job.targetX
data modify storage space_editor:runtime action.origin[1] set from storage space_editor:document job.targetY
data modify storage space_editor:runtime action.origin[2] set from storage space_editor:document job.targetZ
execute store result storage space_editor:runtime action.order int 1 run scoreboard players get #action se.v
data modify storage space_editor:document actions append from storage space_editor:runtime action
scoreboard players add #action se.v 1
execute store result storage space_editor:document nextActionId int 1 run scoreboard players get #action se.v
data modify storage space_editor:document job.state set value "complete"
