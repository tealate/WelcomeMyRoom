execute if data storage space_editor:runtime pairPending run return run function space_editor:pair/cancel
scoreboard players set @s se.cd 5
data modify storage space_editor:runtime activeTool set value "delete"
data remove storage space_editor:runtime hit
scoreboard players set #region_ray se.v 0
execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray
