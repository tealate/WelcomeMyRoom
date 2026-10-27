$data modify storage space_editor:runtime maskEdit set value {id:$(id)}
function space_editor:mask/load_edit_target with storage space_editor:runtime maskEdit
execute unless data storage space_editor:runtime currentMask.id run return run tellraw @s {"text": "[Space Editor] Mask IDが見つかりません。", "color": "red"}
function space_editor:mask/delete_loaded
