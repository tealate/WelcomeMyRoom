function prototype:p04/clear
fill ~-12 ~ ~-12 ~27 ~ ~59 minecraft:smooth_stone
fill ~-12 ~ ~-12 ~27 ~ ~-12 minecraft:sea_lantern
summon minecraft:text_display ~5 ~4 ~-9 {Tags:["prototype.entity","prototype.p04"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"04 Upside-down room"}
summon minecraft:text_display ~5 ~2 ~-10 {Tags:["prototype.entity","prototype.p04"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"/function prototype:goto/hub"}
summon minecraft:marker ~ ~1 ~ {Tags:["prototype.entity","prototype.p04","prototype.origin"]}
fill ~-4 ~ ~7 ~14 ~9 ~24 minecraft:stone_bricks
fill ~-3 ~1 ~8 ~13 ~8 ~23 minecraft:air
fill ~-3 ~ ~8 ~13 ~ ~23 minecraft:smooth_quartz
fill ~-3 ~9 ~8 ~13 ~9 ~23 minecraft:sea_lantern
fill ~-3 ~1 ~7 ~13 ~7 ~7 minecraft:calcite
summon minecraft:block_display ~ ~1 ~6.75 {Tags:["prototype.entity", "prototype.p04", "prototype.mask"],block_state:{Name:"minecraft:waxed_oxidized_cut_copper"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[10f,6f,0.12f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~11 ~7 ~12 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:oak_planks"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[12f,0.4f,9f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~3 ~6.6 ~14 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:oak_planks"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[3f,0.5f,3f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~1 ~6.1 ~14 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:oak_log"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[0.35f,1.7f,0.35f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~1 ~6.1 ~16 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:oak_log"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[0.35f,1.7f,0.35f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~3 ~6.1 ~14 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:oak_log"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[0.35f,1.7f,0.35f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~3 ~6.1 ~16 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:oak_log"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[0.35f,1.7f,0.35f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~10 ~6.6 ~18 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:red_concrete"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[3f,1f,2f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~10 ~5.6 ~18 {Tags:["prototype.entity", "prototype.p04", "prototype.decor"],block_state:{Name:"minecraft:white_concrete"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,1f,0f],scale:[1f,0.4f,2f],right_rotation:[0f,0f,0f,1f]}}
fill ~4 ~ ~ ~6 ~ ~3 minecraft:gold_block
summon minecraft:text_display ~5 ~3 ~-3 {Tags:["prototype.entity","prototype.p04"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Upside-down furniture beyond masked wall"}
summon minecraft:text_display ~5 ~11 ~12 {Tags:["prototype.entity","prototype.p04"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Visual diorama only / ordinary gravity"}
scoreboard players set #p04 proto.state 0
scoreboard players set #p04.built proto.state 1
tellraw @a {"text":"[prototype] p04 ready","color":"green"}
