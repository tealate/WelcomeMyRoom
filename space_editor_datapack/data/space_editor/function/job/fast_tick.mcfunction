execute if data storage space_editor:document job{emptyCheck:1b} run return run function space_editor:job/empty_tick
execute store result score #cursor se.v run data get storage space_editor:document job.cursorX 1
execute store result score #sx se.v run data get storage space_editor:document job.sx 1
execute store result score #sy se.v run data get storage space_editor:document job.sy 1
execute store result score #sz se.v run data get storage space_editor:document job.sz 1
scoreboard players operation #remaining se.v = #sx se.v
scoreboard players operation #remaining se.v -= #cursor se.v
execute if score #remaining se.v matches ..0 run return run function space_editor:job/finish
execute store result score #limit se.v run gamerule minecraft:max_block_modifications
scoreboard players operation #area se.v = #sy se.v
scoreboard players operation #area se.v *= #sz se.v
scoreboard players operation #width se.v = #limit se.v
scoreboard players operation #width se.v /= #area se.v
execute if score #width se.v matches ..0 run scoreboard players set #width se.v 1
scoreboard players operation #width se.v < #remaining se.v
function space_editor:job/prepare_chunk
execute store success score #clone_ok se.v run function space_editor:job/clone_chunk with storage space_editor:document job
execute unless score #clone_ok se.v matches 1 if data storage space_editor:document job{type:"paste",masked:1b} run return run function space_editor:job/start_empty_check
execute unless score #clone_ok se.v matches 1 run return run function space_editor:job/fail
function space_editor:job/advance_chunk
