function space_editor:proxy_spike/spawn
execute unless entity @s[tag=sp.active] run return 0
execute at @s if loaded ~2 ~ ~3 run function space_editor:proxy_spike/spawn_reference
function space_editor:proxy_spike/flip_on
execute at @s run function space_editor:proxy_spike/player_tick
