$data modify storage space_editor:runtime maskEdit set value {id:$(id),values:[$(x),$(y),$(z)],fixed:[I;0,0,0]}
function space_editor:mask/read_edit_values
execute unless score #mask_input_valid se.v matches 1 run return run tellraw @s {"text": "[Space Editor] expandは各軸-16〜16で指定してください。", "color": "red"}
function space_editor:mask/load_edit_target with storage space_editor:runtime maskEdit
execute unless data storage space_editor:runtime currentMask.id run return run tellraw @s {"text": "[Space Editor] Mask IDが見つかりません。", "color": "red"}
data modify storage space_editor:runtime currentMask.expand set from storage space_editor:runtime maskEdit.fixed
function space_editor:mask/prepare
execute unless score #mask_valid se.v matches 1 run return run tellraw @s {"text": "[Space Editor] expand後の各辺は0より大きく128以下にしてください。", "color": "red"}
function space_editor:mask/commit_expand with storage space_editor:runtime currentMask
data modify storage space_editor:runtime maskActionType set value "mask_update"
data modify storage space_editor:runtime maskActionOperation set value "expand"
data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask
function space_editor:mask/action_append
function space_editor:mask/refresh
tellraw @s {"text": "[Space Editor] Mask expandを更新しました。", "color": "green"}
