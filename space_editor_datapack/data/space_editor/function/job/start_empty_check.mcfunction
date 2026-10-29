execute if score #area se.v > #limit se.v run return run function space_editor:job/fail
data modify storage space_editor:document job.emptyCheck set value 1b
data modify storage space_editor:document job.emptyCursor set value 0
execute store result storage space_editor:document job.emptyWidth int 1 run scoreboard players get #width se.v
function space_editor:job/empty_tick
