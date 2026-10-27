data modify storage space_editor:runtime maskActionType set value "mask_delete"
data modify storage space_editor:runtime maskActionOperation set value "delete"
data modify storage space_editor:runtime maskActionRecord set from storage space_editor:runtime currentMask
function space_editor:mask/action_append
function space_editor:mask/remove_loaded with storage space_editor:runtime currentMask
function space_editor:mask/refresh
tellraw @s {"text": "[Space Editor] Maskを削除しました。Regionは残しています。", "color": "yellow"}
