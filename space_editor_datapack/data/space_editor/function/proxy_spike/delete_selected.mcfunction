function space_editor:proxy_spike/select
execute as @e[type=minecraft:mannequin,tag=sp.selected] run function space_editor:proxy_spike/delete_start
kill @e[type=minecraft:text_display,tag=sp.selected]
