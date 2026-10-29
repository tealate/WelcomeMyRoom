execute store result score #empty_cursor se.v run data get storage space_editor:document job.emptyCursor 1
execute store result score #empty_width se.v run data get storage space_editor:document job.emptyWidth 1
execute store result score #sy se.v run data get storage space_editor:document job.sy 1
execute store result score #sz se.v run data get storage space_editor:document job.sz 1
scoreboard players operation #empty_total se.v = #empty_width se.v
scoreboard players operation #empty_total se.v *= #sy se.v
scoreboard players operation #empty_total se.v *= #sz se.v
scoreboard players set #empty_budget se.v 256
function space_editor:job/empty_loop
