scoreboard players set @s pr.gc 40
execute unless score @s pr.epoch = #epoch pr.epoch run return run kill @s
execute unless data storage space_editor:document projection{enabled:1b} run return run kill @s
execute store result storage space_editor:projection gc.id int 1 run scoreboard players get @s pr.id
execute store result storage space_editor:projection gc.owner int 1 run scoreboard players get @s pr.owner
function space_editor:projection/gc_check with storage space_editor:projection gc
