data modify storage space_editor:runtime transformState set value {kind:"wall",north:"none",east:"none",south:"none",west:"none",up:"true",waterlogged:"false",flipY:0b,x:0,y:0,z:0}
execute if block ~ ~ ~ #space_editor:transform_walls[north=none] run data modify storage space_editor:runtime transformState.north set value "none"
execute if block ~ ~ ~ #space_editor:transform_walls[north=low] run data modify storage space_editor:runtime transformState.north set value "low"
execute if block ~ ~ ~ #space_editor:transform_walls[north=tall] run data modify storage space_editor:runtime transformState.north set value "tall"
execute if block ~ ~ ~ #space_editor:transform_walls[east=none] run data modify storage space_editor:runtime transformState.east set value "none"
execute if block ~ ~ ~ #space_editor:transform_walls[east=low] run data modify storage space_editor:runtime transformState.east set value "low"
execute if block ~ ~ ~ #space_editor:transform_walls[east=tall] run data modify storage space_editor:runtime transformState.east set value "tall"
execute if block ~ ~ ~ #space_editor:transform_walls[south=none] run data modify storage space_editor:runtime transformState.south set value "none"
execute if block ~ ~ ~ #space_editor:transform_walls[south=low] run data modify storage space_editor:runtime transformState.south set value "low"
execute if block ~ ~ ~ #space_editor:transform_walls[south=tall] run data modify storage space_editor:runtime transformState.south set value "tall"
execute if block ~ ~ ~ #space_editor:transform_walls[west=none] run data modify storage space_editor:runtime transformState.west set value "none"
execute if block ~ ~ ~ #space_editor:transform_walls[west=low] run data modify storage space_editor:runtime transformState.west set value "low"
execute if block ~ ~ ~ #space_editor:transform_walls[west=tall] run data modify storage space_editor:runtime transformState.west set value "tall"
execute if block ~ ~ ~ #space_editor:transform_walls[up=true] run data modify storage space_editor:runtime transformState.up set value "true"
execute if block ~ ~ ~ #space_editor:transform_walls[up=false] run data modify storage space_editor:runtime transformState.up set value "false"
execute if block ~ ~ ~ #space_editor:transform_walls[waterlogged=true] run data modify storage space_editor:runtime transformState.waterlogged set value "true"
execute if block ~ ~ ~ #space_editor:transform_walls[waterlogged=false] run data modify storage space_editor:runtime transformState.waterlogged set value "false"
function space_editor:transform/rotate_connections
data modify storage space_editor:runtime transformState.flipY set from storage space_editor:document job.flipY
data modify storage space_editor:runtime transformState.x set from storage space_editor:document job.blockTargetX
data modify storage space_editor:runtime transformState.y set from storage space_editor:document job.blockTargetY
data modify storage space_editor:runtime transformState.z set from storage space_editor:document job.blockTargetZ
data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension
function space_editor:transform/read_item with storage space_editor:document job
