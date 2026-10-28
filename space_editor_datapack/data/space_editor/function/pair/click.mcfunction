scoreboard players set @s se.cd 5
execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} if data storage space_editor:runtime pairSession.selected run return run function space_editor:pair/gesture
execute if data storage space_editor:runtime pairPending run return run function space_editor:pair/confirm
data modify storage space_editor:runtime activeTool set value "pair_select"
data remove storage space_editor:runtime hit
scoreboard players set #region_ray se.v 0
execute anchored eyes positioned ^ ^ ^ run function space_editor:region/ray
