execute unless block ~ ~ ~ #space_editor:ray_pass run return run execute align xyz run function space_editor:paste/capture
scoreboard players add #paste_ray se.v 1
execute if score #paste_ray se.v matches ..128 positioned ^ ^ ^0.1 run return run function space_editor:paste/ray
tellraw @s {"text": "[Space Editor] 12.8ブロック以内にPaste始点となるブロックがありません。", "color": "red"}
