data modify entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] hide_description set value 0b
data modify entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] description set from entity @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_main,limit=1] text
data modify entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] hide_description set value 0b
data modify entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.reference,limit=1] description set from entity @e[type=minecraft:text_display,tag=sp.selected,tag=sp.label_reference,limit=1] text
