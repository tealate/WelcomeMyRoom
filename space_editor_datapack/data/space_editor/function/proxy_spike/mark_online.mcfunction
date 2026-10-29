function space_editor:proxy_spike/select
execute unless entity @e[tag=sp.selected,tag=sp.main] run kill @e[tag=sp.selected,tag=sp.label]
execute unless entity @e[tag=sp.selected,tag=sp.reference] run kill @e[tag=sp.selected,tag=sp.label_reference]
tag @e[tag=sp.selected,tag=space_editor.proxy_spike] add sp.online
