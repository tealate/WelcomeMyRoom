data modify storage editor:data guides set value 0b
execute in minecraft:overworld as @e[tag=editor.guide] run data merge entity @s {view_range:0f}
execute in minecraft:the_nether as @e[tag=editor.guide] run data merge entity @s {view_range:0f}
execute in minecraft:the_end as @e[tag=editor.guide] run data merge entity @s {view_range:0f}
function editor:internal/selection/preview
