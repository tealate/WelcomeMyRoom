data remove storage editor:runtime dim
execute if dimension minecraft:overworld run data modify storage editor:runtime dim set value "minecraft:overworld"
execute if dimension minecraft:the_nether run data modify storage editor:runtime dim set value "minecraft:the_nether"
execute if dimension minecraft:the_end run data modify storage editor:runtime dim set value "minecraft:the_end"
execute unless data storage editor:runtime dim run return run tellraw @s {text:"この版は通常の3ディメンションに対応しています。",color:"red"}
data modify storage editor:runtime old_dim set from storage editor:data selection.dim
execute store success score #changed se run data modify storage editor:runtime old_dim set from storage editor:runtime dim
execute if score #changed se matches 1 run data remove storage editor:data selection
data modify storage editor:data selection.dim set from storage editor:runtime dim
kill @e[type=minecraft:marker,tag=editor.capture]
summon minecraft:marker ~ ~ ~ {Tags:["editor.capture"]}
data modify storage editor:runtime pos set from entity @e[type=minecraft:marker,tag=editor.capture,limit=1] Pos
kill @e[type=minecraft:marker,tag=editor.capture]
function editor:internal/capture_point with storage editor:runtime
function editor:internal/selection/normalize
