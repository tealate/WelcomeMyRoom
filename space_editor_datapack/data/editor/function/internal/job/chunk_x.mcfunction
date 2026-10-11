scoreboard players operation #cz se = #cz1 se
function editor:internal/job/chunk_z
scoreboard players add #cx se 16
execute if score #cx se <= #cx2 se run function editor:internal/job/chunk_x
