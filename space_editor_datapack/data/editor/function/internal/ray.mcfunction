execute unless block ~ ~ ~ #editor:ray_pass run return run execute align xyz run function editor:internal/capture
scoreboard players add #ray se 1
execute if score #ray se matches ..128 positioned ^ ^ ^0.1 run return run function editor:internal/ray
tellraw @s {"text": "[Space Editor] 12.8ブロック以内に対象がありません。足元指定や座標指定も使えます。", "color": "yellow"}
