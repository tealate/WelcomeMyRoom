scoreboard players set #skip se.v 1
execute store result score #skipped se.v run data get storage space_editor:document job.skippedBlocks 1
scoreboard players add #skipped se.v 1
execute store result storage space_editor:document job.skippedBlocks int 1 run scoreboard players get #skipped se.v
