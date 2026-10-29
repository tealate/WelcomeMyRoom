scoreboard players operation #cursor se.v += #width se.v
execute store result storage space_editor:document job.cursorX int 1 run scoreboard players get #cursor se.v
execute store result score #chunks se.v run data get storage space_editor:document job.completedChunks 1
scoreboard players add #chunks se.v 1
execute store result storage space_editor:document job.completedChunks int 1 run scoreboard players get #chunks se.v
execute if score #cursor se.v >= #sx se.v run function space_editor:job/finish
