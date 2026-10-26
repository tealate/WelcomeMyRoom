execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
$execute unless data storage editor:data document.objects[{id:$(id),type:"teleport_volume"}] run return run tellraw @s {text:"TP範囲のIDではありません。",color:"red"}
execute unless entity @s[type=minecraft:player] run return 0
scoreboard players set #dim_ok se 0
execute if dimension minecraft:overworld run scoreboard players set #dim_ok se 1
execute if dimension minecraft:the_nether run scoreboard players set #dim_ok se 1
execute if dimension minecraft:the_end run scoreboard players set #dim_ok se 1
execute unless score #dim_ok se matches 1 run return run tellraw @s {text:"TP先は通常3ディメンション内にしてください。",color:"red"}
execute store result score #target_coord se run data get entity @s Pos[0] 1
execute unless score #target_coord se matches -1000000..1000000 run return run tellraw @s {text:"TP先は±1000000以内にしてください。",color:"red"}
execute store result score #target_coord se run data get entity @s Pos[1] 1
execute unless score #target_coord se matches -1000000..1000000 run return run tellraw @s {text:"TP先は±1000000以内にしてください。",color:"red"}
execute store result score #target_coord se run data get entity @s Pos[2] 1
execute unless score #target_coord se matches -1000000..1000000 run return run tellraw @s {text:"TP先は±1000000以内にしてください。",color:"red"}
function editor:internal/history/save
$data modify storage editor:data document.objects[{id:$(id)}].target set value {}
$data modify storage editor:data document.objects[{id:$(id)}].target.pos set from entity @s Pos
$data modify storage editor:data document.objects[{id:$(id)}].target.rotation set from entity @s Rotation
$execute if dimension minecraft:overworld run data modify storage editor:data document.objects[{id:$(id)}].target.dim set value "minecraft:overworld"
$execute if dimension minecraft:the_nether run data modify storage editor:data document.objects[{id:$(id)}].target.dim set value "minecraft:the_nether"
$execute if dimension minecraft:the_end run data modify storage editor:data document.objects[{id:$(id)}].target.dim set value "minecraft:the_end"
function editor:internal/revision
tellraw @s {"text": "[Space Editor] 現在の足元・向きをTP先として保存しました。playで動作確認できます。", "color": "aqua"}
