execute in minecraft:overworld run kill @e[tag=space_editor.paste_preview]
execute in minecraft:the_nether run kill @e[tag=space_editor.paste_preview]
execute in minecraft:the_end run kill @e[tag=space_editor.paste_preview]
$execute in $(targetDimension) positioned $(x) $(y) $(z) run summon minecraft:block_display ~ ~ ~ {Tags:["space_editor.preview","space_editor.paste_preview"],block_state:{Name:"minecraft:magenta_glazed_terracotta"},transformation:{translation:[-0.5f,0f,-0.5f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:3f,width:64f,height:64f}
