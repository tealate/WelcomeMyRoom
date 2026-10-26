execute store result score #cursor se.v run data get storage space_editor:document job.cursor 1
execute store result score #total se.v run data get storage space_editor:document job.totalBlocks 1
execute if score #cursor se.v >= #total se.v run return run function space_editor:job/transformed_phase_done
scoreboard players set #budget se.v 64
function space_editor:job/transformed_loop
