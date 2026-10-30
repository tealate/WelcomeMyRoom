execute in minecraft:overworld run scoreboard players add @e[type=minecraft:mannequin,tag=space_editor.proxy] pr.gc 0
execute in minecraft:overworld run scoreboard players remove @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.gc=1..}] pr.gc 1
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.gc=..0},limit=16] run function space_editor:projection/gc_entity
execute in minecraft:overworld run scoreboard players add @e[type=minecraft:text_display,tag=space_editor.proxy] pr.gc 0
execute in minecraft:overworld run scoreboard players remove @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.gc=1..}] pr.gc 1
execute in minecraft:overworld as @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.gc=..0},limit=16] run function space_editor:projection/gc_entity
execute in minecraft:the_nether run scoreboard players add @e[type=minecraft:mannequin,tag=space_editor.proxy] pr.gc 0
execute in minecraft:the_nether run scoreboard players remove @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.gc=1..}] pr.gc 1
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.gc=..0},limit=16] run function space_editor:projection/gc_entity
execute in minecraft:the_nether run scoreboard players add @e[type=minecraft:text_display,tag=space_editor.proxy] pr.gc 0
execute in minecraft:the_nether run scoreboard players remove @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.gc=1..}] pr.gc 1
execute in minecraft:the_nether as @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.gc=..0},limit=16] run function space_editor:projection/gc_entity
execute in minecraft:the_end run scoreboard players add @e[type=minecraft:mannequin,tag=space_editor.proxy] pr.gc 0
execute in minecraft:the_end run scoreboard players remove @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.gc=1..}] pr.gc 1
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.gc=..0},limit=16] run function space_editor:projection/gc_entity
execute in minecraft:the_end run scoreboard players add @e[type=minecraft:text_display,tag=space_editor.proxy] pr.gc 0
execute in minecraft:the_end run scoreboard players remove @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.gc=1..}] pr.gc 1
execute in minecraft:the_end as @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.gc=..0},limit=16] run function space_editor:projection/gc_entity
execute if data storage space_editor:document {editMode:1b} run function space_editor:projection/hide_all
