execute if entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] unless entity @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_main,limit=1] at @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] run summon minecraft:text_display ~ ~2.1 ~ {Tags:["space_editor.proxy_spike","sp.label","sp.label_main","sp.new"],billboard:"center",background:1073741824,see_through:0b,shadow:0b,teleport_duration:1,view_range:0.5f,text:{text:""}}
function space_editor:proxy_spike/initialize_new
data modify storage space_editor:proxy_spike uuid set from entity @s UUID
execute as @e[type=minecraft:text_display,tag=sp.new,limit=1] run function space_editor:proxy_spike/set_label with storage space_editor:proxy_spike
tag @e[type=minecraft:text_display,tag=sp.new] remove sp.new
function space_editor:proxy_spike/select
execute if entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] unless entity @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_reference,limit=1] at @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] run summon minecraft:text_display ~ ~2.1 ~ {Tags:["space_editor.proxy_spike","sp.label","sp.label_reference","sp.new"],billboard:"center",background:1073741824,see_through:0b,shadow:0b,teleport_duration:1,view_range:0.5f,text:{text:""}}
function space_editor:proxy_spike/initialize_new
data modify storage space_editor:proxy_spike uuid set from entity @s UUID
execute as @e[type=minecraft:text_display,tag=sp.new,limit=1] run function space_editor:proxy_spike/set_label with storage space_editor:proxy_spike
tag @e[type=minecraft:text_display,tag=sp.new] remove sp.new
function space_editor:proxy_spike/select
