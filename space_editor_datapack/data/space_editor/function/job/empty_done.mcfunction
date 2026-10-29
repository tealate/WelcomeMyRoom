data remove storage space_editor:document job.emptyCheck
execute store result score #cursor se.v run data get storage space_editor:document job.cursorX 1
execute store result score #sx se.v run data get storage space_editor:document job.sx 1
scoreboard players operation #width se.v = #empty_width se.v
function space_editor:job/advance_chunk
