data modify storage editor:data guides set value 1b
execute in minecraft:overworld as @e[tag=editor.guide] run data merge entity @s {view_range:2f}
execute in minecraft:the_nether as @e[tag=editor.guide] run data merge entity @s {view_range:2f}
execute in minecraft:the_end as @e[tag=editor.guide] run data merge entity @s {view_range:2f}
function editor:internal/selection/preview
