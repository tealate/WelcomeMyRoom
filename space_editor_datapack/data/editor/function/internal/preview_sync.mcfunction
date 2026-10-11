scoreboard players set #clock se 0
execute in minecraft:overworld as @e[tag=editor.selection] unless score @s se.id = #preview_version se run kill @s
execute in minecraft:the_nether as @e[tag=editor.selection] unless score @s se.id = #preview_version se run kill @s
execute in minecraft:the_end as @e[tag=editor.selection] unless score @s se.id = #preview_version se run kill @s
execute in minecraft:overworld if data storage editor:data {guides:0b} as @e[tag=editor.guide] run data merge entity @s {view_range:0f}
execute in minecraft:overworld if data storage editor:data {guides:1b} as @e[tag=editor.guide] run data merge entity @s {view_range:2f}
execute in minecraft:the_nether if data storage editor:data {guides:0b} as @e[tag=editor.guide] run data merge entity @s {view_range:0f}
execute in minecraft:the_nether if data storage editor:data {guides:1b} as @e[tag=editor.guide] run data merge entity @s {view_range:2f}
execute in minecraft:the_end if data storage editor:data {guides:0b} as @e[tag=editor.guide] run data merge entity @s {view_range:0f}
execute in minecraft:the_end if data storage editor:data {guides:1b} as @e[tag=editor.guide] run data merge entity @s {view_range:2f}
