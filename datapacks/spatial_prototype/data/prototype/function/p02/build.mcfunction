function prototype:p02/clear
fill ~-12 ~ ~-12 ~27 ~ ~59 minecraft:smooth_stone
fill ~-12 ~ ~-12 ~27 ~ ~-12 minecraft:sea_lantern
summon minecraft:text_display ~5 ~4 ~-9 {Tags:["prototype.entity","prototype.p02"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"02 Bigger inside"}
summon minecraft:text_display ~5 ~2 ~-10 {Tags:["prototype.entity","prototype.p02"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"/function prototype:goto/hub"}
summon minecraft:marker ~ ~1 ~ {Tags:["prototype.entity","prototype.p02","prototype.origin"]}
fill ~-5 ~ ~8 ~15 ~7 ~25 minecraft:stone_bricks
fill ~-4 ~1 ~9 ~14 ~6 ~24 minecraft:air
fill ~-4 ~ ~9 ~14 ~ ~24 minecraft:smooth_quartz
fill ~-4 ~7 ~9 ~14 ~7 ~24 minecraft:sea_lantern
fill ~2 ~ ~2 ~8 ~5 ~8 minecraft:calcite
fill ~3 ~1 ~3 ~7 ~4 ~7 minecraft:air
fill ~3 ~ ~3 ~7 ~ ~7 minecraft:smooth_quartz
fill ~3 ~5 ~3 ~7 ~5 ~7 minecraft:sea_lantern
fill ~4 ~1 ~2 ~6 ~3 ~2 minecraft:air
summon minecraft:block_display ~3 ~1 ~6.7 {Tags:["prototype.entity", "prototype.p02", "prototype.mask"],block_state:{Name:"minecraft:waxed_oxidized_cut_copper"},brightness:{block:15,sky:15},view_range:2f,width:64f,height:32f,transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[5f,4f,0.15f],right_rotation:[0f,0f,0f,1f]}}
fill ~4 ~ ~3 ~6 ~ ~7 minecraft:gold_block
fill ~4 ~1 ~8 ~6 ~3 ~8 minecraft:air
fill ~-5 ~ ~40 ~15 ~7 ~57 minecraft:stone_bricks
fill ~-4 ~1 ~41 ~14 ~6 ~56 minecraft:air
fill ~-4 ~ ~41 ~14 ~ ~56 minecraft:smooth_quartz
fill ~-4 ~7 ~41 ~14 ~7 ~56 minecraft:sea_lantern
fill ~4 ~1 ~40 ~6 ~3 ~40 minecraft:air
fill ~-2 ~1 ~12 ~-2 ~5 ~12 minecraft:quartz_pillar
fill ~-2 ~1 ~21 ~-2 ~5 ~21 minecraft:quartz_pillar
fill ~12 ~1 ~12 ~12 ~5 ~12 minecraft:quartz_pillar
fill ~12 ~1 ~21 ~12 ~5 ~21 minecraft:quartz_pillar
fill ~3 ~1 ~23 ~7 ~2 ~23 minecraft:emerald_block
fill ~-2 ~1 ~44 ~-2 ~5 ~44 minecraft:quartz_pillar
fill ~-2 ~1 ~53 ~-2 ~5 ~53 minecraft:quartz_pillar
fill ~12 ~1 ~44 ~12 ~5 ~44 minecraft:quartz_pillar
fill ~12 ~1 ~53 ~12 ~5 ~53 minecraft:quartz_pillar
fill ~3 ~1 ~55 ~7 ~2 ~55 minecraft:emerald_block
summon minecraft:text_display ~5 ~3 ~-3 {Tags:["prototype.entity","prototype.p02"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Small shell -> gold threshold -> full-size hall"}
summon minecraft:text_display ~5 ~3 ~45 {Tags:["prototype.entity","prototype.p02"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Return through front door / preserves position and look"}
scoreboard players set #p02 proto.state 0
scoreboard players set #p02.built proto.state 1
tellraw @a {"text":"[prototype] p02 ready","color":"green"}
