$data modify storage space_editor:runtime input set value {amount:$(amount)}
execute store result score #step se.v run data get storage space_editor:runtime input.amount 1000
execute unless score #step se.v matches 100..16000 run return run tellraw @s {"text": "[Space Editor] 増減量は0.1〜16です。", "color": "red"}
scoreboard players operation #remainder se.v = #step se.v
scoreboard players operation #remainder se.v %= #100 se.v
execute unless score #remainder se.v matches 0 run return run tellraw @s {"text": "[Space Editor] 増減量は0.1単位で指定してください。", "color": "red"}
execute store result storage space_editor:document settings.step double 0.001 run scoreboard players get #step se.v
execute store result storage space_editor:document settings.stepMilli int 1 run scoreboard players get #step se.v
tellraw @s {"text": "[Space Editor] 増減量を更新しました（0.1単位）。", "color": "aqua"}
