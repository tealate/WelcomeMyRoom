function editor:internal/render/sweep with storage editor:runtime work
$execute in $(dim) positioned 0.0 0.0 0.0 run summon minecraft:block_display ~$(px) ~$(py) ~$(pz) {Tags:["editor.object","editor.mask","editor.new"],block_state:{Name:"minecraft:waxed_oxidized_cut_copper"},transformation:{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},view_range:4f,width:128f,height:128f}
$execute in $(dim) positioned 0.0 0.0 0.0 run summon minecraft:block_display ~$(px) ~$(py) ~$(pz) {Tags:["editor.object","editor.guide","editor.new"],block_state:{Name:"minecraft:lime_glazed_terracotta"},transformation:{translation:[0f,0f,0f],scale:[$(sx)f,$(sy)f,$(sz)f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]},brightness:{block:15,sky:15},view_range:2f,width:128f,height:128f}
$execute in $(dim) run scoreboard players set @e[tag=editor.new] se.id $(id)
$execute in $(dim) run scoreboard players operation @e[tag=editor.new] se.gen = #epoch se.gen
$execute in $(dim) if data storage editor:data {guides:0b} as @e[tag=editor.new,tag=editor.guide] run data merge entity @s {view_range:0f}
$execute in $(dim) run tag @e[tag=editor.new] remove editor.new
