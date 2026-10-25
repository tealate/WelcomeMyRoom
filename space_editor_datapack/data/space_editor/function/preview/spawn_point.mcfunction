execute in minecraft:overworld run kill @e[tag=space_editor.point]
execute in minecraft:the_nether run kill @e[tag=space_editor.point]
execute in minecraft:the_end run kill @e[tag=space_editor.point]
$execute in $(dimension) positioned $(ax) $(ay) $(az) run summon minecraft:block_display ~ ~ ~ {Tags:["space_editor.preview","space_editor.point"],block_state:{Name:"minecraft:lime_glazed_terracotta"},transformation:{translation:[-0.5f,0f,-0.5f],scale:[1f,1f,1f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:2f,width:2f,height:2f}
