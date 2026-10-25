execute unless block ~ ~ ~ #space_editor:ray_pass run return run execute align xyz run function space_editor:selection/capture
scoreboard players add #ray se.v 1
execute if score #ray se.v matches ..128 positioned ^ ^ ^0.1 run return run function space_editor:internal/ray_block
tellraw @s {"text": "[Space Editor] 12.8ブロック以内に対象ブロックがありません。", "color": "red"}
