function prototype:p03/clear
fill ~-12 ~ ~-12 ~27 ~ ~59 minecraft:smooth_stone
fill ~-12 ~ ~-12 ~27 ~ ~-12 minecraft:sea_lantern
summon minecraft:text_display ~5 ~4 ~-9 {Tags:["prototype.entity","prototype.p03"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"03 Two viewpoints"}
summon minecraft:text_display ~5 ~2 ~-10 {Tags:["prototype.entity","prototype.p03"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"/function prototype:goto/hub"}
summon minecraft:marker ~ ~1 ~ {Tags:["prototype.entity","prototype.p03","prototype.origin"]}
fill ~-8 ~ ~7 ~18 ~6 ~23 minecraft:stone_bricks
fill ~-7 ~1 ~8 ~17 ~5 ~22 minecraft:air
fill ~-7 ~ ~8 ~17 ~ ~22 minecraft:smooth_quartz
fill ~-7 ~6 ~8 ~17 ~6 ~22 minecraft:sea_lantern
fill ~-7 ~1 ~7 ~17 ~5 ~7 minecraft:smooth_basalt
fill ~5 ~1 ~8 ~5 ~5 ~22 minecraft:stone_bricks
fill ~-7 ~1 ~22 ~4 ~5 ~22 minecraft:red_concrete
fill ~6 ~1 ~22 ~17 ~5 ~22 minecraft:blue_concrete
fill ~-4 ~1 ~14 ~-2 ~3 ~16 minecraft:gold_block
fill ~11 ~1 ~14 ~13 ~4 ~16 minecraft:diamond_block
summon minecraft:block_display ~-3 ~1 ~6.75 {Tags:["prototype.entity", "prototype.p03", "prototype.mask"],block_state:{Name:"minecraft:waxed_oxidized_cut_copper"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,4f,0.12f],right_rotation:[0f,0f,0f,1f]}}
summon minecraft:block_display ~10 ~1 ~6.75 {Tags:["prototype.entity", "prototype.p03", "prototype.mask"],block_state:{Name:"minecraft:waxed_oxidized_cut_copper"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[3f,4f,0.12f],right_rotation:[0f,0f,0f,1f]}}
fill ~-2 ~ ~1 ~-1 ~ ~3 minecraft:red_concrete
fill ~11 ~ ~1 ~12 ~ ~3 minecraft:blue_concrete
summon minecraft:text_display ~5 ~3 ~-3 {Tags:["prototype.entity","prototype.p03"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Move left/right: red room / blue room"}
summon minecraft:text_display ~5 ~7 ~7 {Tags:["prototype.entity","prototype.p03"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Static paired apertures + solid divider; no view swapping"}
scoreboard players set #p03 proto.state 0
scoreboard players set #p03.built proto.state 1
tellraw @a {"text":"[prototype] p03 ready","color":"green"}
