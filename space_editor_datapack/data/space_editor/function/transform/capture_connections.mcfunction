data modify storage space_editor:runtime transformState set value {kind:"connections",north:"false",east:"false",south:"false",west:"false",waterlogged:"false",x:0,y:0,z:0}
execute if block ~ ~ ~ #space_editor:transform_connections[north=true] run data modify storage space_editor:runtime transformState.north set value "true"
execute if block ~ ~ ~ #space_editor:transform_connections[north=false] run data modify storage space_editor:runtime transformState.north set value "false"
execute if block ~ ~ ~ #space_editor:transform_connections[east=true] run data modify storage space_editor:runtime transformState.east set value "true"
execute if block ~ ~ ~ #space_editor:transform_connections[east=false] run data modify storage space_editor:runtime transformState.east set value "false"
execute if block ~ ~ ~ #space_editor:transform_connections[south=true] run data modify storage space_editor:runtime transformState.south set value "true"
execute if block ~ ~ ~ #space_editor:transform_connections[south=false] run data modify storage space_editor:runtime transformState.south set value "false"
execute if block ~ ~ ~ #space_editor:transform_connections[west=true] run data modify storage space_editor:runtime transformState.west set value "true"
execute if block ~ ~ ~ #space_editor:transform_connections[west=false] run data modify storage space_editor:runtime transformState.west set value "false"
execute if block ~ ~ ~ #space_editor:transform_connections[waterlogged=true] run data modify storage space_editor:runtime transformState.waterlogged set value "true"
execute if block ~ ~ ~ #space_editor:transform_connections[waterlogged=false] run data modify storage space_editor:runtime transformState.waterlogged set value "false"
function space_editor:transform/rotate_connections
data modify storage space_editor:runtime transformState.x set from storage space_editor:document job.blockTargetX
data modify storage space_editor:runtime transformState.y set from storage space_editor:document job.blockTargetY
data modify storage space_editor:runtime transformState.z set from storage space_editor:document job.blockTargetZ
data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension
function space_editor:transform/read_item with storage space_editor:document job
