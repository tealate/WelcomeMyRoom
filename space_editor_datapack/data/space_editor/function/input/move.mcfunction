scoreboard players set @s se.cd 5
data modify storage space_editor:runtime activeTool set value "move"
data remove storage space_editor:runtime hit
scoreboard players set #region_ray se.v 0
execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray
