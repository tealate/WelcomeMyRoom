execute unless entity @e[tag=sp.selected,tag=sp.label_main] rotated ~ 0 positioned ^ ^2.3 ^3 run summon minecraft:text_display ~ ~ ~ {Tags:["space_editor.proxy_spike","sp.label","sp.label_main","sp.new"],billboard:"center",background:1073741824,see_through:0b,shadow:1b,text:{text:""}}
execute if entity @e[tag=sp.new,tag=sp.label_main] run scoreboard players operation @e[tag=sp.new,tag=sp.label_main,limit=1] sp.owner = @s sp.owner
tag @e[tag=sp.new,tag=sp.label_main] remove sp.new
function space_editor:proxy_spike/select
execute if entity @e[tag=sp.selected,tag=sp.reference] unless entity @e[tag=sp.selected,tag=sp.label_reference] rotated ~ 0 positioned ^-1 ^2.3 ^3 run summon minecraft:text_display ~ ~ ~ {Tags:["space_editor.proxy_spike","sp.label","sp.label_reference","sp.new"],billboard:"center",background:1073741824,see_through:0b,shadow:1b,text:{text:""}}
execute if entity @e[tag=sp.new,tag=sp.label_reference] run scoreboard players operation @e[tag=sp.new,tag=sp.label_reference,limit=1] sp.owner = @s sp.owner
tag @e[tag=sp.new,tag=sp.label_reference] remove sp.new
function space_editor:proxy_spike/select
data modify storage space_editor:proxy_spike uuid set from entity @s UUID
execute as @e[tag=sp.selected,tag=sp.label] run function space_editor:proxy_spike/set_label with storage space_editor:proxy_spike
