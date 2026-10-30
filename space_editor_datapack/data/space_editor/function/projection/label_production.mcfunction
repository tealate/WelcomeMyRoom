$execute in $(dimension) positioned 0.0 0.0 0.0 run summon minecraft:text_display ~$(x) ~$(nameY) ~$(z) {Tags:["space_editor.proxy","pr.production","pr.new"],billboard:"center",background:1073741824,view_range:0.5f,teleport_duration:3,shadow:0b,see_through:0b,text:{selector:"@a[nbt={UUID:$(uuid)}]"}}
$execute in $(dimension) run scoreboard players set @e[type=minecraft:text_display,tag=pr.new,limit=1] pr.id $(id)
$execute in $(dimension) run scoreboard players set @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production,scores={pr.id=$(id)},limit=1] pr.owner $(owner)
$execute in $(dimension) run scoreboard players operation @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production,scores={pr.id=$(id)},limit=1] pr.epoch = #epoch pr.epoch
$execute in $(dimension) run tag @e[type=minecraft:text_display,tag=space_editor.proxy,tag=pr.production,scores={pr.id=$(id)},limit=1] remove pr.new
