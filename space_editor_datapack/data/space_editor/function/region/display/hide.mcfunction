data modify storage space_editor:document settings.regionsVisible set value 0b
execute in minecraft:overworld run kill @e[tag=space_editor.region]
execute in minecraft:the_nether run kill @e[tag=space_editor.region]
execute in minecraft:the_end run kill @e[tag=space_editor.region]
execute in minecraft:overworld run kill @e[tag=space_editor.label]
execute in minecraft:the_nether run kill @e[tag=space_editor.label]
execute in minecraft:the_end run kill @e[tag=space_editor.label]
execute in minecraft:overworld run kill @e[tag=space_editor.mask_guide]
execute in minecraft:the_nether run kill @e[tag=space_editor.mask_guide]
execute in minecraft:the_end run kill @e[tag=space_editor.mask_guide]
tellraw @s {"text": "[Space Editor] 全Region枠・ラベル・Maskガイドを非表示にしました。Mask本体は残しています。", "color": "yellow"}
