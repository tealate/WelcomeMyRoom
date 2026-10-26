data modify storage space_editor:runtime transformState set value {kind:"stairs",facing:"north",half:"bottom",shape:"straight",waterlogged:"false",x:0,y:0,z:0}
execute if score #rotation se.v matches 0 if block ~ ~ ~ #space_editor:transform_stairs[facing=north] run data modify storage space_editor:runtime transformState.facing set value "north"
execute if score #rotation se.v matches 0 if block ~ ~ ~ #space_editor:transform_stairs[facing=east] run data modify storage space_editor:runtime transformState.facing set value "east"
execute if score #rotation se.v matches 0 if block ~ ~ ~ #space_editor:transform_stairs[facing=south] run data modify storage space_editor:runtime transformState.facing set value "south"
execute if score #rotation se.v matches 0 if block ~ ~ ~ #space_editor:transform_stairs[facing=west] run data modify storage space_editor:runtime transformState.facing set value "west"
execute if score #rotation se.v matches 90 if block ~ ~ ~ #space_editor:transform_stairs[facing=north] run data modify storage space_editor:runtime transformState.facing set value "east"
execute if score #rotation se.v matches 90 if block ~ ~ ~ #space_editor:transform_stairs[facing=east] run data modify storage space_editor:runtime transformState.facing set value "south"
execute if score #rotation se.v matches 90 if block ~ ~ ~ #space_editor:transform_stairs[facing=south] run data modify storage space_editor:runtime transformState.facing set value "west"
execute if score #rotation se.v matches 90 if block ~ ~ ~ #space_editor:transform_stairs[facing=west] run data modify storage space_editor:runtime transformState.facing set value "north"
execute if score #rotation se.v matches 180 if block ~ ~ ~ #space_editor:transform_stairs[facing=north] run data modify storage space_editor:runtime transformState.facing set value "south"
execute if score #rotation se.v matches 180 if block ~ ~ ~ #space_editor:transform_stairs[facing=east] run data modify storage space_editor:runtime transformState.facing set value "west"
execute if score #rotation se.v matches 180 if block ~ ~ ~ #space_editor:transform_stairs[facing=south] run data modify storage space_editor:runtime transformState.facing set value "north"
execute if score #rotation se.v matches 180 if block ~ ~ ~ #space_editor:transform_stairs[facing=west] run data modify storage space_editor:runtime transformState.facing set value "east"
execute if score #rotation se.v matches 270 if block ~ ~ ~ #space_editor:transform_stairs[facing=north] run data modify storage space_editor:runtime transformState.facing set value "west"
execute if score #rotation se.v matches 270 if block ~ ~ ~ #space_editor:transform_stairs[facing=east] run data modify storage space_editor:runtime transformState.facing set value "north"
execute if score #rotation se.v matches 270 if block ~ ~ ~ #space_editor:transform_stairs[facing=south] run data modify storage space_editor:runtime transformState.facing set value "east"
execute if score #rotation se.v matches 270 if block ~ ~ ~ #space_editor:transform_stairs[facing=west] run data modify storage space_editor:runtime transformState.facing set value "south"
execute if block ~ ~ ~ #space_editor:transform_stairs[half=top] run data modify storage space_editor:runtime transformState.half set value "top"
execute if block ~ ~ ~ #space_editor:transform_stairs[half=bottom] run data modify storage space_editor:runtime transformState.half set value "bottom"
execute if score #flip se.v matches 1 if data storage space_editor:runtime transformState{half:"top"} run data modify storage space_editor:runtime transformState.half set value "bottom"
execute if score #flip se.v matches 1 if block ~ ~ ~ #space_editor:transform_stairs[half=bottom] run data modify storage space_editor:runtime transformState.half set value "top"
execute if block ~ ~ ~ #space_editor:transform_stairs[shape=straight] run data modify storage space_editor:runtime transformState.shape set value "straight"
execute if block ~ ~ ~ #space_editor:transform_stairs[shape=inner_left] run data modify storage space_editor:runtime transformState.shape set value "inner_left"
execute if block ~ ~ ~ #space_editor:transform_stairs[shape=inner_right] run data modify storage space_editor:runtime transformState.shape set value "inner_right"
execute if block ~ ~ ~ #space_editor:transform_stairs[shape=outer_left] run data modify storage space_editor:runtime transformState.shape set value "outer_left"
execute if block ~ ~ ~ #space_editor:transform_stairs[shape=outer_right] run data modify storage space_editor:runtime transformState.shape set value "outer_right"
execute if block ~ ~ ~ #space_editor:transform_stairs[waterlogged=true] run data modify storage space_editor:runtime transformState.waterlogged set value "true"
execute if block ~ ~ ~ #space_editor:transform_stairs[waterlogged=false] run data modify storage space_editor:runtime transformState.waterlogged set value "false"
data modify storage space_editor:runtime transformState.x set from storage space_editor:document job.blockTargetX
data modify storage space_editor:runtime transformState.y set from storage space_editor:document job.blockTargetY
data modify storage space_editor:runtime transformState.z set from storage space_editor:document job.blockTargetZ
data modify storage space_editor:runtime transformState.targetDimension set from storage space_editor:document job.targetDimension
function space_editor:transform/read_item with storage space_editor:document job
