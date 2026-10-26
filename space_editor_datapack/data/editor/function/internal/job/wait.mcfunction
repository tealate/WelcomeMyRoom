scoreboard players set #loaded se 0
function editor:internal/job/loaded with storage editor:runtime work
execute if score #loaded se matches 1 run return run function editor:internal/job/apply
execute store result score #wait se run data get storage editor:runtime job.wait
scoreboard players add #wait se 1
execute store result storage editor:runtime job.wait int 1 run scoreboard players get #wait se
execute if score #wait se matches 1200.. run function editor:internal/job/error
