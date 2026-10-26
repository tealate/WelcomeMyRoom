execute if score #cursor se.v >= #total se.v run return run function space_editor:job/transformed_phase_done
function space_editor:job/prepare_block
execute if data storage space_editor:document job{phase:"preflight"} run function space_editor:transform/preflight
execute if data storage space_editor:document job{phase:"place"} run function space_editor:transform/clone_one
execute unless data storage space_editor:document job{state:"running"} run return 0
scoreboard players add #cursor se.v 1
execute store result storage space_editor:document job.cursor int 1 run scoreboard players get #cursor se.v
scoreboard players remove #budget se.v 1
execute if score #budget se.v matches 1.. run function space_editor:job/transformed_loop
