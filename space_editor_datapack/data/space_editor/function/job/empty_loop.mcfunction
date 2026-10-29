scoreboard players operation #ex se.v = #empty_cursor se.v
scoreboard players operation #ex se.v %= #empty_width se.v
scoreboard players operation #ez se.v = #empty_cursor se.v
scoreboard players operation #ez se.v /= #empty_width se.v
scoreboard players operation #ey se.v = #ez se.v
scoreboard players operation #ey se.v /= #sz se.v
scoreboard players operation #ez se.v %= #sz se.v
execute store result score #empty_pos se.v run data get storage space_editor:document job.chunkSourceX1 1
scoreboard players operation #empty_pos se.v += #ex se.v
execute store result storage space_editor:document job.blockSourceX int 1 run scoreboard players get #empty_pos se.v
execute store result score #empty_pos se.v run data get storage space_editor:document job.chunkSourceY1 1
scoreboard players operation #empty_pos se.v += #ey se.v
execute store result storage space_editor:document job.blockSourceY int 1 run scoreboard players get #empty_pos se.v
execute store result score #empty_pos se.v run data get storage space_editor:document job.chunkSourceZ1 1
scoreboard players operation #empty_pos se.v += #ez se.v
execute store result storage space_editor:document job.blockSourceZ int 1 run scoreboard players get #empty_pos se.v
execute store result score #empty_pos se.v run data get storage space_editor:document job.chunkTargetX 1
scoreboard players operation #empty_pos se.v += #ex se.v
execute store result storage space_editor:document job.blockTargetX int 1 run scoreboard players get #empty_pos se.v
execute store result score #empty_pos se.v run data get storage space_editor:document job.chunkTargetY 1
scoreboard players operation #empty_pos se.v += #ey se.v
execute store result storage space_editor:document job.blockTargetY int 1 run scoreboard players get #empty_pos se.v
execute store result score #empty_pos se.v run data get storage space_editor:document job.chunkTargetZ 1
scoreboard players operation #empty_pos se.v += #ez se.v
execute store result storage space_editor:document job.blockTargetZ int 1 run scoreboard players get #empty_pos se.v
execute store success score #empty_valid se.v run function space_editor:job/check_empty_block with storage space_editor:document job
execute unless score #empty_valid se.v matches 1 run data remove storage space_editor:document job.emptyCheck
execute unless score #empty_valid se.v matches 1 run return run function space_editor:job/fail
scoreboard players add #empty_cursor se.v 1
execute store result storage space_editor:document job.emptyCursor int 1 run scoreboard players get #empty_cursor se.v
execute if score #empty_cursor se.v >= #empty_total se.v run return run function space_editor:job/empty_done
scoreboard players remove #empty_budget se.v 1
execute if score #empty_budget se.v matches 1.. run function space_editor:job/empty_loop
