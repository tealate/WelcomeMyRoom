execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=1..}] at @s if dimension minecraft:overworld run scoreboard players remove @s pr.remove 1
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=4}] at @s if dimension minecraft:overworld run tp @s ~ -63 ~
execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=..0}] at @s if dimension minecraft:overworld run kill @s
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=1..}] at @s if dimension minecraft:the_nether run scoreboard players remove @s pr.remove 1
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=4}] at @s if dimension minecraft:the_nether run tp @s ~ 1 ~
execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=..0}] at @s if dimension minecraft:the_nether run kill @s
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=1..}] at @s if dimension minecraft:the_end run scoreboard players remove @s pr.remove 1
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=4}] at @s if dimension minecraft:the_end run tp @s ~ 1 ~
execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=pr.removing,scores={pr.remove=..0}] at @s if dimension minecraft:the_end run kill @s
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
