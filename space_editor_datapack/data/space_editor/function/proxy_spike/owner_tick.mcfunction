execute unless score @s sp.epoch = #epoch sp.epoch run return run function space_editor:proxy_spike/stop
execute unless score @s sp.seen = @s sp.leave run return run function space_editor:proxy_spike/stop
function space_editor:proxy_spike/mark_online
execute if score @s sp.follow matches 1 run function space_editor:proxy_spike/update_selected
