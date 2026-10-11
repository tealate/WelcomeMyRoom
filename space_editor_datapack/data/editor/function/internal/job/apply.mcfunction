execute if data storage editor:runtime work{type:"clear"} run function editor:internal/render/clear with storage editor:runtime work
execute if data storage editor:runtime work{type:"block_fill"} run function editor:internal/render/block with storage editor:runtime work
execute if data storage editor:runtime work{type:"mask"} run function editor:internal/render/mask with storage editor:runtime work
execute if data storage editor:runtime work{type:"teleport_volume"} run function editor:internal/render/teleport with storage editor:runtime work
execute if data storage editor:runtime work{type:"sweep"} run function editor:internal/render/sweep with storage editor:runtime work
function editor:internal/job/release
data remove storage editor:runtime job.queue[0]
data modify storage editor:runtime job.phase set value "next"
