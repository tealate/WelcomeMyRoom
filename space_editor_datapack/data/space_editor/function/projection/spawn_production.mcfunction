scoreboard players remove #spawn pr.v 1
$execute in $(dimension) positioned 0.0 0.0 0.0 run summon minecraft:mannequin ~$(x) ~$(y) ~$(z) {Tags:["space_editor.proxy","pr.production","pr.new"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hidden_layers:[],hide_description:1b,CustomNameVisible:0b,profile:{id:$(uuid)}}
$execute in $(dimension) run scoreboard players set @e[type=minecraft:mannequin,tag=pr.new,limit=1] pr.id $(id)
$execute in $(dimension) run scoreboard players set @e[type=minecraft:mannequin,tag=space_editor.proxy,tag=pr.production,scores={pr.id=$(id)},limit=1] pr.owner $(owner)
$execute in $(dimension) run scoreboard players operation @e[type=minecraft:mannequin,tag=space_editor.proxy,tag=pr.production,scores={pr.id=$(id)},limit=1] pr.epoch = #epoch pr.epoch
$execute in $(dimension) run team join pr_hidden @e[type=minecraft:mannequin,tag=space_editor.proxy,tag=pr.production,scores={pr.id=$(id)},limit=1]
$execute in $(dimension) run tag @e[type=minecraft:mannequin,tag=space_editor.proxy,tag=pr.production,scores={pr.id=$(id)},limit=1] remove pr.new
