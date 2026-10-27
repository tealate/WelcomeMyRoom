execute in minecraft:overworld as @e[type=minecraft:block_display,tag=space_editor.special] at @s unless block ~ ~ ~ #space_editor:special_collision run function space_editor:special/orphan
execute in minecraft:the_nether as @e[type=minecraft:block_display,tag=space_editor.special] at @s unless block ~ ~ ~ #space_editor:special_collision run function space_editor:special/orphan
execute in minecraft:the_end as @e[type=minecraft:block_display,tag=space_editor.special] at @s unless block ~ ~ ~ #space_editor:special_collision run function space_editor:special/orphan
schedule function space_editor:special/cleanup 1s replace
