execute store result storage editor:runtime ticket.x int 1 run scoreboard players get #cx se
execute store result storage editor:runtime ticket.z int 1 run scoreboard players get #cz se
data modify storage editor:runtime ticket.dim set from storage editor:runtime work.dim
function editor:internal/job/ticket with storage editor:runtime ticket
scoreboard players add #cz se 16
execute if score #cz se <= #cz2 se run function editor:internal/job/chunk_z
