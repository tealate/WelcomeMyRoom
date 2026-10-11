scoreboard players add #preview_version se 1
execute in minecraft:overworld run kill @e[type=minecraft:block_display,tag=editor.selection]
execute in minecraft:the_nether run kill @e[type=minecraft:block_display,tag=editor.selection]
execute in minecraft:the_end run kill @e[type=minecraft:block_display,tag=editor.selection]
