function space_editor:mask/prepare
$execute in minecraft:overworld run kill @e[tag=space_editor.mask_body,scores={se.id=$(id)}]
$execute in minecraft:overworld run kill @e[tag=space_editor.mask_guide,scores={se.id=$(id)}]
$execute in minecraft:the_nether run kill @e[tag=space_editor.mask_body,scores={se.id=$(id)}]
$execute in minecraft:the_nether run kill @e[tag=space_editor.mask_guide,scores={se.id=$(id)}]
$execute in minecraft:the_end run kill @e[tag=space_editor.mask_body,scores={se.id=$(id)}]
$execute in minecraft:the_end run kill @e[tag=space_editor.mask_guide,scores={se.id=$(id)}]
execute if score #mask_valid se.v matches 1 run function space_editor:mask/spawn with storage space_editor:runtime maskRender
