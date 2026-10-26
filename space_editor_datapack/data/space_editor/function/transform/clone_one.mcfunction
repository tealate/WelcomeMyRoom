scoreboard players set #skip se.v 0
function space_editor:transform/skip_check with storage space_editor:document job
execute if score #skip se.v matches 1 run return 0
data modify storage space_editor:runtime transformState set value {kind:"none"}
function space_editor:transform/state_capture with storage space_editor:document job
execute unless data storage space_editor:runtime transformState{kind:"none"} unless data storage space_editor:runtime transformState.block run return run function space_editor:transform/fail_state_item
execute store success score #clone_ok se.v run function space_editor:transform/clone_one_macro with storage space_editor:document job
execute unless score #clone_ok se.v matches 1 run return run function space_editor:transform/fail_clone
execute unless data storage space_editor:runtime transformState{kind:"none"} run function space_editor:transform/clear_target with storage space_editor:runtime transformState
scoreboard players set #state_ok se.v 1
execute if data storage space_editor:runtime transformState{kind:"stairs"} store success score #state_ok se.v run function space_editor:transform/apply_stairs with storage space_editor:runtime transformState
execute if data storage space_editor:runtime transformState{kind:"slab"} store success score #state_ok se.v run function space_editor:transform/apply_slab with storage space_editor:runtime transformState
execute if data storage space_editor:runtime transformState{kind:"connections"} store success score #state_ok se.v run function space_editor:transform/apply_connections with storage space_editor:runtime transformState
execute if data storage space_editor:runtime transformState{kind:"wall"} store success score #state_ok se.v run function space_editor:transform/apply_wall with storage space_editor:runtime transformState
execute if data storage space_editor:runtime transformState{kind:"axis"} store success score #state_ok se.v run function space_editor:transform/apply_axis with storage space_editor:runtime transformState
execute if data storage space_editor:runtime transformState{kind:"axis_waterlogged"} store success score #state_ok se.v run function space_editor:transform/apply_axis_waterlogged with storage space_editor:runtime transformState
execute unless score #state_ok se.v matches 1 run return run function space_editor:transform/fail_state_apply
execute store result score #done se.v run data get storage space_editor:document job.completedBlocks 1
scoreboard players add #done se.v 1
execute store result storage space_editor:document job.completedBlocks int 1 run scoreboard players get #done se.v
