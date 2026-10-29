function space_editor:proxy_spike/ensure_owner
function space_editor:proxy_spike/delete_selected
scoreboard players set @s sp.flip 0
scoreboard players set @s sp.name 0
execute rotated ~ 0 positioned ^ ^ ^3 run summon minecraft:mannequin ~ ~ ~ {Tags:["space_editor.proxy_spike","sp.main","sp.new"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hide_description:1b,CustomNameVisible:0b}
scoreboard players operation @e[tag=sp.new,tag=sp.main,limit=1] sp.owner = @s sp.owner
data modify storage space_editor:proxy_spike uuid set from entity @s UUID
execute as @e[tag=sp.new,tag=sp.main,limit=1] run function space_editor:proxy_spike/set_profile with storage space_editor:proxy_spike
tag @e[tag=sp.new,tag=sp.main] remove sp.new
scoreboard players set @s sp.follow 1
function space_editor:proxy_spike/player_tick
