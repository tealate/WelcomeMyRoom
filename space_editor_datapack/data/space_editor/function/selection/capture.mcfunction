data modify storage space_editor:runtime clickDimension set from storage space_editor:runtime hover.dimension
data modify storage space_editor:runtime clickPos set from storage space_editor:runtime hover.pos
execute unless data storage space_editor:runtime selection.a run return run function space_editor:selection/set_a
function space_editor:selection/set_b
