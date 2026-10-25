execute store success score #dim_changed se.v run data modify storage space_editor:runtime selection.dimension set from storage space_editor:runtime clickDimension
execute if score #dim_changed se.v matches 1 run return run function space_editor:selection/dimension_error
data modify storage space_editor:runtime selection.b set value [I;0,0,0]
execute store result storage space_editor:runtime selection.b[0] int 1 run data get storage space_editor:runtime clickPos[0] 1
execute store result storage space_editor:runtime selection.b[1] int 1 run data get storage space_editor:runtime clickPos[1] 1
execute store result storage space_editor:runtime selection.b[2] int 1 run data get storage space_editor:runtime clickPos[2] 1
function space_editor:region/create
