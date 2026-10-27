data modify storage space_editor:document settings.regionsVisible set value 1b
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] 全Region枠・ラベル・Maskガイドを表示しました。", "color": "green"}
