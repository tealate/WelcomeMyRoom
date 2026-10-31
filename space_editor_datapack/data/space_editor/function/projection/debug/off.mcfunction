scoreboard players set @s pr.debug 0
execute store result storage space_editor:projection actor.id int 1 run scoreboard players get @s pr.owner
function space_editor:projection/debug/clear_owner with storage space_editor:projection actor
