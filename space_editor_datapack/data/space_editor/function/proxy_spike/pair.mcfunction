function space_editor:proxy_spike/spawn
execute rotated ~ 0 positioned ^-1 ^ ^3 run summon minecraft:mannequin ~ ~ ~ {Tags:["space_editor.proxy_spike","sp.reference","sp.new"],immovable:1b,NoGravity:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,hide_description:1b,CustomNameVisible:0b}
scoreboard players operation @e[tag=sp.new,tag=sp.reference,limit=1] sp.owner = @s sp.owner
execute as @e[tag=sp.new,tag=sp.reference,limit=1] run function space_editor:proxy_spike/set_profile with storage space_editor:proxy_spike
tag @e[tag=sp.new,tag=sp.reference] remove sp.new
function space_editor:proxy_spike/flip_on
function space_editor:proxy_spike/name_text_display
function space_editor:proxy_spike/player_tick
