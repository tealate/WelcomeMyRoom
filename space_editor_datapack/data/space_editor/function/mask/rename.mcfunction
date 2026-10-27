$data modify storage space_editor:runtime maskEdit set value {id:$(id),name:"$(name)"}
function space_editor:mask/load_edit_target with storage space_editor:runtime maskEdit
execute unless data storage space_editor:runtime currentMask.id run return run tellraw @s {"text": "[Space Editor] Mask IDが見つかりません。", "color": "red"}
$data modify storage space_editor:runtime currentMask.name set value "$(name)"
function space_editor:mask/commit_name with storage space_editor:runtime currentMask
data modify storage space_editor:runtime maskActionType set value "mask_update"
data modify storage space_editor:runtime maskActionOperation set value "rename"
data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask
function space_editor:mask/action_append
tellraw @s {"text": "[Space Editor] Mask名を更新しました。", "color": "green"}
