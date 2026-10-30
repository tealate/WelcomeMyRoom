$execute in minecraft:overworld as @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.owner=$(id)}] run function space_editor:projection/delete/start
$execute in minecraft:overworld run kill @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.owner=$(id)}]
$execute in minecraft:the_nether as @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.owner=$(id)}] run function space_editor:projection/delete/start
$execute in minecraft:the_nether run kill @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.owner=$(id)}]
$execute in minecraft:the_end as @e[type=minecraft:mannequin,tag=space_editor.proxy,scores={pr.owner=$(id)}] run function space_editor:projection/delete/start
$execute in minecraft:the_end run kill @e[type=minecraft:text_display,tag=space_editor.proxy,scores={pr.owner=$(id)}]
