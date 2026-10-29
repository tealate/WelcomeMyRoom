execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {"text": "[Space Editor] 別プレイヤーが編集中です。終了後に開始してください。", "color": "red"}
tag @s remove space_editor.editing
data modify storage space_editor:document editMode set value 0b
function space_editor:preview/hide
tellraw @s {"text": "[Space Editor] プレイモード。Regionは保存したまま補助表示を隠しました。", "color": "green"}
function space_editor:pair/cancel
