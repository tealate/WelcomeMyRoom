scoreboard players set #selection_cursor_active se.v 1
execute unless dimension minecraft:overworld in minecraft:overworld run kill @e[tag=space_editor.selection_candidate]
execute unless dimension minecraft:the_nether in minecraft:the_nether run kill @e[tag=space_editor.selection_candidate]
execute unless dimension minecraft:the_end in minecraft:the_end run kill @e[tag=space_editor.selection_candidate]
data remove storage space_editor:runtime hover
scoreboard players set #selection_ray se.v 0
execute anchored eyes positioned ^ ^ ^ run function space_editor:internal/ray_selection
