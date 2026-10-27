data modify storage space_editor:runtime transformState set value {kind:"fence",north:"false",east:"false",south:"false",west:"false",waterlogged:"false",flipY:0b,x:0,y:0,z:0}
execute if block ~ ~ ~ #space_editor:transform_fences[north=true] run data modify storage space_editor:runtime transformState.north set value "true"
execute if block ~ ~ ~ #space_editor:transform_fences[east=true] run data modify storage space_editor:runtime transformState.east set value "true"
execute if block ~ ~ ~ #space_editor:transform_fences[south=true] run data modify storage space_editor:runtime transformState.south set value "true"
execute if block ~ ~ ~ #space_editor:transform_fences[west=true] run data modify storage space_editor:runtime transformState.west set value "true"
execute if block ~ ~ ~ #space_editor:transform_fences[waterlogged=true] run data modify storage space_editor:runtime transformState.waterlogged set value "true"
execute if block ~ ~ ~ #space_editor:transform_fences[waterlogged=false] run data modify storage space_editor:runtime transformState.waterlogged set value "false"
function space_editor:transform/rotate_connections
data modify storage space_editor:runtime transformState.flipY set from storage space_editor:document job.flipY
data modify storage space_editor:runtime transformState.x set from storage space_editor:document job.blockTargetX
data modify storage space_editor:runtime transformState.y set from storage space_editor:document job.blockTargetY
data modify storage space_editor:runtime transformState.z set from storage space_editor:document job.blockTargetZ
data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension
function space_editor:transform/read_item with storage space_editor:document job
