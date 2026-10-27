scoreboard players operation #special_id se.v = @s se.sid
execute store result storage space_editor:runtime specialDelete.id int 1 run scoreboard players get #special_id se.v
function space_editor:special/remove_record with storage space_editor:runtime specialDelete
kill @s
