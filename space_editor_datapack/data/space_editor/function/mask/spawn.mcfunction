$execute in $(dim) positioned 0.0 0.0 0.0 run summon minecraft:block_display ~$(px) ~$(py) ~$(pz) {Tags:["space_editor.mask","space_editor.mask_body","space_editor.mask_new"],block_state:{Name:"minecraft:waxed_oxidized_cut_copper"},transformation:{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},view_range:4f,width:128f,height:128f}
$execute in $(dim) run scoreboard players set @e[type=minecraft:block_display,tag=space_editor.mask_new] se.id $(id)
$execute in $(dim) run tag @e[type=minecraft:block_display,tag=space_editor.mask_new] remove space_editor.mask_new
execute if data storage space_editor:document {editMode:1b} run function space_editor:mask/spawn_guide with storage space_editor:runtime maskRender
