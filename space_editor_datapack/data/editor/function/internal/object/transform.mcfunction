scoreboard players set #transform_ok se 0
execute store result score #pos se run data get storage editor:runtime object.x1 1000
execute store result score #size se run data get storage editor:runtime object.sx 1000
execute store result score #offset se run data get storage editor:data prefs.ox
execute store result score #expand se run data get storage editor:data prefs.ex
scoreboard players operation #pos se += #offset se
scoreboard players operation #pos se -= #expand se
scoreboard players operation #size se += #expand se
scoreboard players operation #size se += #expand se
execute unless score #size se matches 1..64000 run return run tellraw @s {text:"補正後のサイズは0.001〜64ブロックにしてください。",color:"red"}
execute store result storage editor:runtime object.px double 0.001 run scoreboard players get #pos se
execute store result storage editor:runtime object.sx double 0.001 run scoreboard players get #size se
execute store result storage editor:runtime object.lox int 1 run scoreboard players get #pos se
scoreboard players operation #pos se += #size se
execute store result storage editor:runtime object.hix int 1 run scoreboard players get #pos se
data modify storage editor:runtime object.ox set from storage editor:data prefs.ox
data modify storage editor:runtime object.ex set from storage editor:data prefs.ex
execute store result score #pos se run data get storage editor:runtime object.y1 1000
execute store result score #size se run data get storage editor:runtime object.sy 1000
execute store result score #offset se run data get storage editor:data prefs.oy
execute store result score #expand se run data get storage editor:data prefs.ey
scoreboard players operation #pos se += #offset se
scoreboard players operation #pos se -= #expand se
scoreboard players operation #size se += #expand se
scoreboard players operation #size se += #expand se
execute unless score #size se matches 1..64000 run return run tellraw @s {text:"補正後のサイズは0.001〜64ブロックにしてください。",color:"red"}
execute store result storage editor:runtime object.py double 0.001 run scoreboard players get #pos se
execute store result storage editor:runtime object.sy double 0.001 run scoreboard players get #size se
execute store result storage editor:runtime object.loy int 1 run scoreboard players get #pos se
scoreboard players operation #pos se += #size se
execute store result storage editor:runtime object.hiy int 1 run scoreboard players get #pos se
data modify storage editor:runtime object.oy set from storage editor:data prefs.oy
data modify storage editor:runtime object.ey set from storage editor:data prefs.ey
execute store result score #pos se run data get storage editor:runtime object.z1 1000
execute store result score #size se run data get storage editor:runtime object.sz 1000
execute store result score #offset se run data get storage editor:data prefs.oz
execute store result score #expand se run data get storage editor:data prefs.ez
scoreboard players operation #pos se += #offset se
scoreboard players operation #pos se -= #expand se
scoreboard players operation #size se += #expand se
scoreboard players operation #size se += #expand se
execute unless score #size se matches 1..64000 run return run tellraw @s {text:"補正後のサイズは0.001〜64ブロックにしてください。",color:"red"}
execute store result storage editor:runtime object.pz double 0.001 run scoreboard players get #pos se
execute store result storage editor:runtime object.sz double 0.001 run scoreboard players get #size se
execute store result storage editor:runtime object.loz int 1 run scoreboard players get #pos se
scoreboard players operation #pos se += #size se
execute store result storage editor:runtime object.hiz int 1 run scoreboard players get #pos se
data modify storage editor:runtime object.oz set from storage editor:data prefs.oz
data modify storage editor:runtime object.ez set from storage editor:data prefs.ez
scoreboard players set #transform_ok se 1
