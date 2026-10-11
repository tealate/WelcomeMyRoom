execute unless data storage editor:runtime job.queue[0] run return run function editor:internal/job/done
data modify storage editor:runtime work set from storage editor:runtime job.queue[0]
execute if data storage editor:runtime work.px run function editor:internal/job/display_bounds
data modify storage editor:runtime job.tickets set value []
data modify storage editor:runtime job.wait set value 0
function editor:internal/job/chunks
data modify storage editor:runtime job.phase set value "wait"
