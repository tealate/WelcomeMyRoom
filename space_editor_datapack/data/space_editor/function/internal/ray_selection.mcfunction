execute unless block ~ ~ ~ #space_editor:ray_pass run return run execute align xyz run function space_editor:selection/hover_capture
execute if score #selection_ray se.v matches 30 run return run execute align xyz run function space_editor:selection/hover_capture
scoreboard players add #selection_ray se.v 1
execute positioned ^ ^ ^0.1 run return run function space_editor:internal/ray_selection
