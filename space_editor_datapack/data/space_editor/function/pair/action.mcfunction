execute store result score #pair_action se.v run data get storage space_editor:document nextActionId 1
data modify storage space_editor:runtime pairAction set value {type:"pair_edit",id:0,order:0}
execute store result storage space_editor:runtime pairAction.id int 1 run scoreboard players get #pair_action se.v
execute store result storage space_editor:runtime pairAction.order int 1 run scoreboard players get #pair_action se.v
data modify storage space_editor:runtime pairAction.operation set from storage space_editor:runtime pairOperation
data modify storage space_editor:runtime pairAction.before set from storage space_editor:runtime pairBefore
data modify storage space_editor:runtime pairAction.after set value {}
data modify storage space_editor:runtime pairAction.after.pair set from storage space_editor:runtime pair
data modify storage space_editor:runtime pairAction.after.a set from storage space_editor:runtime editA
data modify storage space_editor:runtime pairAction.after.b set from storage space_editor:runtime editB
execute if data storage space_editor:runtime {pairOperation:"delete"} run data modify storage space_editor:runtime pairAction.after set value {}
data modify storage space_editor:document actions append from storage space_editor:runtime pairAction
scoreboard players add #pair_action se.v 1
execute store result storage space_editor:document nextActionId int 1 run scoreboard players get #pair_action se.v
