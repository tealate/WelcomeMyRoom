function space_editor:paste/hide_preview
data remove storage space_editor:runtime pastePending
tellraw @s {"text": "[Space Editor] Pasteプレビューをキャンセルしました。", "color": "yellow"}
