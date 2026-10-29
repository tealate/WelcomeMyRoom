function space_editor:proxy_spike/select
tag @e[tag=sp.selected,tag=space_editor.proxy_spike] add sp.online
execute if entity @e[tag=sp.selected,tag=sp.main] rotated ~ 0 positioned ^ ^ ^3 rotated as @s as @e[tag=sp.selected,tag=sp.main,limit=1] run tp @s ~ ~ ~ ~ ~
execute if entity @e[tag=sp.selected,tag=sp.reference] rotated ~ 0 positioned ^-1 ^ ^3 rotated as @s as @e[tag=sp.selected,tag=sp.reference,limit=1] run tp @s ~ ~ ~ ~ ~
execute if entity @e[tag=sp.selected,tag=sp.label_main] if score @s sp.flip matches 1 rotated ~ 0 positioned ^ ^0.7 ^3 as @e[tag=sp.selected,tag=sp.label_main,limit=1] run tp @s ~ ~ ~
execute if entity @e[tag=sp.selected,tag=sp.label_main] unless score @s sp.flip matches 1 rotated ~ 0 positioned ^ ^2.3 ^3 as @e[tag=sp.selected,tag=sp.label_main,limit=1] run tp @s ~ ~ ~
execute if entity @e[tag=sp.selected,tag=sp.label_reference] rotated ~ 0 positioned ^-1 ^2.3 ^3 as @e[tag=sp.selected,tag=sp.label_reference,limit=1] run tp @s ~ ~ ~
function space_editor:proxy_spike/sync
