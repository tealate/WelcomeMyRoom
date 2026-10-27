execute in minecraft:overworld run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:1b,glow_color_override:16711935,view_range:16f}
execute in minecraft:the_nether run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:1b,glow_color_override:16711935,view_range:16f}
execute in minecraft:the_end run execute as @e[type=minecraft:block_display,tag=space_editor.mask_body] run data merge entity @s {Glowing:1b,glow_color_override:16711935,view_range:16f}
tellraw @s {"text": "[Space Editor] Mask本体を発光輪郭・view_range 16で表示します。テクスチャとMask方式は変更しません。", "color": "yellow"}
