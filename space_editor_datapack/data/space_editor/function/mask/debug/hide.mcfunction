execute in minecraft:overworld run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:0b,view_range:4f}
execute in minecraft:the_nether run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:0b,view_range:4f}
execute in minecraft:the_end run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:0b,view_range:4f}
execute in minecraft:overworld run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data remove entity @s glow_color_override
execute in minecraft:the_nether run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data remove entity @s glow_color_override
execute in minecraft:the_end run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data remove entity @s glow_color_override
tellraw @s {"text": "[Space Editor] Mask本体のデバッグ表示を解除しました。", "color": "green"}
