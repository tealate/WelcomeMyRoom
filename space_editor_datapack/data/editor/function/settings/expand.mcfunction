$data modify storage editor:runtime input set value {x:$(x),y:$(y),z:$(z)}
execute store result score #ix se run data get storage editor:runtime input.x 1000
execute store result score #iy se run data get storage editor:runtime input.y 1000
execute store result score #iz se run data get storage editor:runtime input.z 1000
execute unless score #ix se matches -16000..16000 run return run tellraw @s {text:"補正値は±16以内です。",color:"red"}
execute unless score #iy se matches -16000..16000 run return run tellraw @s {text:"補正値は±16以内です。",color:"red"}
execute unless score #iz se matches -16000..16000 run return run tellraw @s {text:"補正値は±16以内です。",color:"red"}
execute store result storage editor:data prefs.ex int 1 run scoreboard players get #ix se
execute store result storage editor:data prefs.ey int 1 run scoreboard players get #iy se
execute store result storage editor:data prefs.ez int 1 run scoreboard players get #iz se
tellraw @s {"text": "[Space Editor] expandを設定しました（1/1000ブロック精度）。", "color": "aqua"}
