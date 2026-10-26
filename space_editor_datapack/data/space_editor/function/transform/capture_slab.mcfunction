data modify storage space_editor:runtime transformState set value {kind:"slab",type:"bottom",waterlogged:"false",x:0,y:0,z:0}
execute if block ~ ~ ~ #space_editor:transform_slabs[type=top] run data modify storage space_editor:runtime transformState.type set value "top"
execute if block ~ ~ ~ #space_editor:transform_slabs[type=bottom] run data modify storage space_editor:runtime transformState.type set value "bottom"
execute if block ~ ~ ~ #space_editor:transform_slabs[type=double] run data modify storage space_editor:runtime transformState.type set value "double"
execute if score #flip se.v matches 1 if data storage space_editor:runtime transformState{type:"top"} run data modify storage space_editor:runtime transformState.type set value "bottom"
execute if score #flip se.v matches 1 if block ~ ~ ~ #space_editor:transform_slabs[type=bottom] run data modify storage space_editor:runtime transformState.type set value "top"
execute if block ~ ~ ~ #space_editor:transform_slabs[waterlogged=true] run data modify storage space_editor:runtime transformState.waterlogged set value "true"
execute if block ~ ~ ~ #space_editor:transform_slabs[waterlogged=false] run data modify storage space_editor:runtime transformState.waterlogged set value "false"
data modify storage space_editor:runtime transformState.x set from storage space_editor:document job.blockTargetX
data modify storage space_editor:runtime transformState.y set from storage space_editor:document job.blockTargetY
data modify storage space_editor:runtime transformState.z set from storage space_editor:document job.blockTargetZ
data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension
function space_editor:transform/read_item with storage space_editor:document job
