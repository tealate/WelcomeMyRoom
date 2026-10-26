data modify storage space_editor:runtime transformState set value {kind:"axis_waterlogged",axis:"y",waterlogged:"false",x:0,y:0,z:0}
execute if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis=x] run data modify storage space_editor:runtime transformState.axis set value "x"
execute if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis=y] run data modify storage space_editor:runtime transformState.axis set value "y"
execute if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis=z] run data modify storage space_editor:runtime transformState.axis set value "z"
execute if score #rotation se.v matches 90 if data storage space_editor:runtime transformState{axis:"x"} run data modify storage space_editor:runtime transformState.axis set value "z"
execute if score #rotation se.v matches 90 if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis=z] run data modify storage space_editor:runtime transformState.axis set value "x"
execute if score #rotation se.v matches 270 if data storage space_editor:runtime transformState{axis:"x"} run data modify storage space_editor:runtime transformState.axis set value "z"
execute if score #rotation se.v matches 270 if block ~ ~ ~ #space_editor:transform_axis_waterlogged[axis=z] run data modify storage space_editor:runtime transformState.axis set value "x"
execute if block ~ ~ ~ #space_editor:transform_axis_waterlogged[waterlogged=true] run data modify storage space_editor:runtime transformState.waterlogged set value "true"
execute if block ~ ~ ~ #space_editor:transform_axis_waterlogged[waterlogged=false] run data modify storage space_editor:runtime transformState.waterlogged set value "false"
data modify storage space_editor:runtime transformState.x set from storage space_editor:document job.blockTargetX
data modify storage space_editor:runtime transformState.y set from storage space_editor:document job.blockTargetY
data modify storage space_editor:runtime transformState.z set from storage space_editor:document job.blockTargetZ
data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension
function space_editor:transform/read_item with storage space_editor:document job
