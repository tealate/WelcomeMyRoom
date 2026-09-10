function prototype:hub/clear
fill ~-12 ~ ~-12 ~27 ~ ~59 minecraft:smooth_stone
fill ~-12 ~ ~-12 ~27 ~ ~-12 minecraft:sea_lantern
summon minecraft:text_display ~5 ~4 ~-9 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Spatial prototypes / hub"}
summon minecraft:text_display ~5 ~2 ~-10 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"/function prototype:goto/hub"}
summon minecraft:marker ~ ~1 ~ {Tags:["prototype.entity","prototype.hub","prototype.origin"]}
summon minecraft:text_display ~5 ~3 ~ {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"/function prototype:goto/01 ... 05"}
summon minecraft:text_display ~5 ~2 ~2 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"boot: rebuild all / reset: remove experiments"}
summon minecraft:text_display ~5 ~2 ~4 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"Targets: smooth_basalt = smooth stone / calcite = oak"}
fill ~-6 ~ ~8 ~-4 ~ ~10 minecraft:gold_block
summon minecraft:text_display ~-5 ~2 ~9 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"01 / stand on gold"}
fill ~-2 ~ ~8 ~ ~ ~10 minecraft:gold_block
summon minecraft:text_display ~-1 ~2 ~9 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"02 / stand on gold"}
fill ~2 ~ ~8 ~4 ~ ~10 minecraft:gold_block
summon minecraft:text_display ~3 ~2 ~9 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"03 / stand on gold"}
fill ~6 ~ ~8 ~8 ~ ~10 minecraft:gold_block
summon minecraft:text_display ~7 ~2 ~9 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"04 / stand on gold"}
fill ~10 ~ ~8 ~12 ~ ~10 minecraft:gold_block
summon minecraft:text_display ~11 ~2 ~9 {Tags:["prototype.entity","prototype.hub"],billboard:"center",background:1073741824,line_width:280,view_range:1f,text:"05 / stand on gold"}
scoreboard players set #hub proto.state 0
scoreboard players set #hub.built proto.state 1
tellraw @a {"text":"[prototype] hub ready","color":"green"}
