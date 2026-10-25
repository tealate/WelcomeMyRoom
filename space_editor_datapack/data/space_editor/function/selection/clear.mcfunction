data remove storage space_editor:runtime selection
execute in minecraft:overworld run kill @e[tag=space_editor.point]
execute in minecraft:the_nether run kill @e[tag=space_editor.point]
execute in minecraft:the_end run kill @e[tag=space_editor.point]
tellraw @s {"text": "[Space Editor] 一時Selectionをクリアしました。保存Regionは変更していません。", "color": "aqua"}
