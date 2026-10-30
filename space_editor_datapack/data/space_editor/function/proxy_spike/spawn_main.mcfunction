execute positioned ~0 ~ ~3 run summon minecraft:mannequin ~ ~ ~ {Tags:["space_editor.proxy_spike","sp.main","sp.new"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hidden_layers:[],hide_description:1b,CustomNameVisible:0b}
function space_editor:proxy_spike/initialize_new
data modify storage space_editor:proxy_spike uuid set from entity @s UUID
execute as @e[type=minecraft:mannequin,tag=sp.new,limit=1] run function space_editor:proxy_spike/set_profile with storage space_editor:proxy_spike
tag @e[type=minecraft:mannequin,tag=sp.new] remove sp.new
function space_editor:proxy_spike/apply_name
