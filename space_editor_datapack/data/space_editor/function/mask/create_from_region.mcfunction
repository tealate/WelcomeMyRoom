data remove storage space_editor:runtime existingMask
$data modify storage space_editor:runtime existingMask set from storage space_editor:document masks[{regionId:$(id)}]
execute if data storage space_editor:runtime existingMask.id run return run tellraw @s {"text": "[Space Editor] このRegionにはすでにMaskがあります。", "color": "yellow"}
execute store result score #mask_id se.v run data get storage space_editor:document nextMaskId 1
data modify storage space_editor:runtime currentMask set value {id:0,idText:"",type:"mask",name:"",regionId:0,regionIdText:"",material:"mask_default",offset:[I;0,0,0],expand:[I;0,0,0],followsRegionResize:1b,visible:1b}
execute store result storage space_editor:runtime currentMask.id int 1 run scoreboard players get #mask_id se.v
$data modify storage space_editor:runtime currentMask.regionId set value $(id)
$data modify storage space_editor:runtime currentMask.regionIdText set value "$(idText)"
function space_editor:mask/set_id_text with storage space_editor:runtime currentMask
data modify storage space_editor:document masks append from storage space_editor:runtime currentMask
scoreboard players add #mask_id se.v 1
execute store result storage space_editor:document nextMaskId int 1 run scoreboard players get #mask_id se.v
data modify storage space_editor:runtime maskActionType set value "mask_create"
data modify storage space_editor:runtime maskActionOperation set value "create"
data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask
function space_editor:mask/action_append
function space_editor:mask/refresh
tellraw @s {"text": "[Space Editor] Maskを生成しました。Regionの変更へ自動追従します。", "color": "green"}
