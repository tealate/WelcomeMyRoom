execute in minecraft:overworld run kill @e[type=minecraft:block_display,tag=space_editor.mask]
execute in minecraft:the_nether run kill @e[type=minecraft:block_display,tag=space_editor.mask]
execute in minecraft:the_end run kill @e[type=minecraft:block_display,tag=space_editor.mask]
data modify storage space_editor:runtime maskQueue set from storage space_editor:document masks
execute if data storage space_editor:runtime maskQueue[0] run function space_editor:mask/rebuild_next
