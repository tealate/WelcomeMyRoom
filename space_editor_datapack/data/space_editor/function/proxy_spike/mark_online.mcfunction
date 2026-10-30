function space_editor:proxy_spike/select
execute unless entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] run kill @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_main,limit=1]
execute unless entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] run kill @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_reference,limit=1]
tag @e[type=minecraft:mannequin,tag=sp.selected] add sp.online
tag @e[type=minecraft:text_display,tag=sp.selected] add sp.online
