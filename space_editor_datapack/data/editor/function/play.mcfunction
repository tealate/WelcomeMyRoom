tag @s remove editor.editing
function editor:preview/hide
tellraw @s {"text": "[Space Editor] プレイ確認モード。TPが有効になります。編集に戻る: /function editor:start", "color": "aqua"}
