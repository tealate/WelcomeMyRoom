execute unless entity @s[type=minecraft:player] run return 0
tag @e[type=minecraft:mannequin,tag=space_editor.proxy_spike,tag=sp.selected] remove sp.selected
tag @e[type=minecraft:text_display,tag=space_editor.proxy_spike,tag=sp.selected] remove sp.selected
execute store result storage space_editor:proxy_spike owner int 1 run scoreboard players get @s sp.owner
function space_editor:proxy_spike/select_owner with storage space_editor:proxy_spike
