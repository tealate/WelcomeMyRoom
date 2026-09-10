function prototype:p01/clear
fill ~-12 ~ ~-12 ~27 ~ ~59 minecraft:smooth_stone
fill ~-12 ~ ~-12 ~27 ~ ~-12 minecraft:sea_lantern
summon minecraft:text_display ~5 ~4 ~-9 {Tags:["prototype.entity","prototype.p01"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"01 Directional wall"}
summon minecraft:text_display ~5 ~2 ~-10 {Tags:["prototype.entity","prototype.p01"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"/function prototype:goto/hub"}
summon minecraft:marker ~ ~1 ~ {Tags:["prototype.entity","prototype.p01","prototype.origin"]}
fill ~-5 ~ ~8 ~15 ~6 ~22 minecraft:stone_bricks
fill ~-4 ~1 ~9 ~14 ~5 ~21 minecraft:air
fill ~-4 ~ ~9 ~14 ~ ~21 minecraft:smooth_quartz
fill ~-4 ~6 ~9 ~14 ~6 ~21 minecraft:sea_lantern
fill ~-4 ~1 ~8 ~14 ~5 ~8 minecraft:smooth_basalt
summon minecraft:block_display ~2 ~1 ~7.7 {Tags:["prototype.entity", "prototype.p01", "prototype.mask"],block_state:{Name:"minecraft:waxed_oxidized_cut_copper"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,4f,0.12f],right_rotation:[0f,0f,0f,1f]}}
fill ~-1 ~1 ~14 ~1 ~3 ~17 minecraft:red_concrete
fill ~8 ~1 ~17 ~10 ~4 ~19 minecraft:blue_concrete
fill ~4 ~ ~ ~5 ~ ~4 minecraft:gold_block
summon minecraft:text_display ~5 ~2 ~-3 {Tags:["prototype.entity","prototype.p01"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Front gold line: compare center / side / back"}
summon minecraft:text_display ~5 ~7 ~8 {Tags:["prototype.entity","prototype.p01"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Placed wall + thin display in FRONT of wall"}
scoreboard players set #p01 proto.state 0
scoreboard players set #p01.built proto.state 1
tellraw @a {"text":"[prototype] p01 ready","color":"green"}
