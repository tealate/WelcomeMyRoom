tag @s remove space_editor.editing
data modify storage space_editor:document editMode set value 0b
function space_editor:preview/hide
tellraw @s {"text": "[Space Editor] プレイモード。Regionは保存したまま補助表示を隠しました。", "color": "green"}
function space_editor:pair/cancel
