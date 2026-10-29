data modify entity @e[tag=sp.selected,tag=sp.main,limit=1] hide_description set value 0b
data modify storage space_editor:proxy_spike uuid set from entity @s UUID
execute as @e[tag=sp.selected,tag=sp.main,limit=1] run function space_editor:proxy_spike/set_description with storage space_editor:proxy_spike
