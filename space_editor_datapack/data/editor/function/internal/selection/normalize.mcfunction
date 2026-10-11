data remove storage editor:data selection.valid
function editor:internal/selection/kill
execute unless data storage editor:data selection.ax run return 0
execute store result score #ax se run data get storage editor:data selection.ax 1
execute store result storage editor:data selection.ax int 1 run scoreboard players get #ax se
execute unless data storage editor:data selection.ay run return 0
execute store result score #ay se run data get storage editor:data selection.ay 1
execute store result storage editor:data selection.ay int 1 run scoreboard players get #ay se
execute unless data storage editor:data selection.az run return 0
execute store result score #az se run data get storage editor:data selection.az 1
execute store result storage editor:data selection.az int 1 run scoreboard players get #az se
execute unless data storage editor:data selection.bx run return 0
execute store result score #bx se run data get storage editor:data selection.bx 1
execute store result storage editor:data selection.bx int 1 run scoreboard players get #bx se
execute unless data storage editor:data selection.by run return 0
execute store result score #by se run data get storage editor:data selection.by 1
execute store result storage editor:data selection.by int 1 run scoreboard players get #by se
execute unless data storage editor:data selection.bz run return 0
execute store result score #bz se run data get storage editor:data selection.bz 1
execute store result storage editor:data selection.bz int 1 run scoreboard players get #bz se
scoreboard players set #dim_ok se 0
execute if data storage editor:data selection{dim:"minecraft:overworld"} run scoreboard players set #dim_ok se 1
execute if data storage editor:data selection{dim:"minecraft:the_nether"} run scoreboard players set #dim_ok se 1
execute if data storage editor:data selection{dim:"minecraft:the_end"} run scoreboard players set #dim_ok se 1
execute unless score #dim_ok se matches 1 run return run tellraw @s {text:"未対応ディメンションです。",color:"red"}
scoreboard players set #volume se 1
scoreboard players operation #x1 se = #ax se
scoreboard players operation #x1 se < #bx se
scoreboard players operation #x2 se = #ax se
scoreboard players operation #x2 se > #bx se
execute unless score #x1 se matches -1000000..1000000 run return run tellraw @s {text:"座標は±1000000以内にしてください。",color:"red"}
execute unless score #x2 se matches -1000000..1000000 run return run tellraw @s {text:"座標は±1000000以内にしてください。",color:"red"}
scoreboard players operation #sx se = #x2 se
scoreboard players operation #sx se -= #x1 se
scoreboard players add #sx se 1
execute unless score #sx se matches 1..32 run return run tellraw @s {text:"1回の選択は各辺1〜32ブロックです。",color:"red"}
execute store result storage editor:data selection.x1 int 1 run scoreboard players get #x1 se
execute store result storage editor:data selection.x2 int 1 run scoreboard players get #x2 se
execute store result storage editor:data selection.sx int 1 run scoreboard players get #sx se
scoreboard players operation #y1 se = #ay se
scoreboard players operation #y1 se < #by se
scoreboard players operation #y2 se = #ay se
scoreboard players operation #y2 se > #by se
execute unless score #y1 se matches -1000000..1000000 run return run tellraw @s {text:"座標は±1000000以内にしてください。",color:"red"}
execute unless score #y2 se matches -1000000..1000000 run return run tellraw @s {text:"座標は±1000000以内にしてください。",color:"red"}
scoreboard players operation #sy se = #y2 se
scoreboard players operation #sy se -= #y1 se
scoreboard players add #sy se 1
execute unless score #sy se matches 1..32 run return run tellraw @s {text:"1回の選択は各辺1〜32ブロックです。",color:"red"}
execute store result storage editor:data selection.y1 int 1 run scoreboard players get #y1 se
execute store result storage editor:data selection.y2 int 1 run scoreboard players get #y2 se
execute store result storage editor:data selection.sy int 1 run scoreboard players get #sy se
scoreboard players operation #z1 se = #az se
scoreboard players operation #z1 se < #bz se
scoreboard players operation #z2 se = #az se
scoreboard players operation #z2 se > #bz se
execute unless score #z1 se matches -1000000..1000000 run return run tellraw @s {text:"座標は±1000000以内にしてください。",color:"red"}
execute unless score #z2 se matches -1000000..1000000 run return run tellraw @s {text:"座標は±1000000以内にしてください。",color:"red"}
scoreboard players operation #sz se = #z2 se
scoreboard players operation #sz se -= #z1 se
scoreboard players add #sz se 1
execute unless score #sz se matches 1..32 run return run tellraw @s {text:"1回の選択は各辺1〜32ブロックです。",color:"red"}
execute store result storage editor:data selection.z1 int 1 run scoreboard players get #z1 se
execute store result storage editor:data selection.z2 int 1 run scoreboard players get #z2 se
execute store result storage editor:data selection.sz int 1 run scoreboard players get #sz se
execute unless score #y1 se matches -64..319 run return run tellraw @s {text:"高さが範囲外です。",color:"red"}
execute unless score #y2 se matches -64..319 run return run tellraw @s {text:"高さが範囲外です。",color:"red"}
execute unless data storage editor:data selection{dim:"minecraft:overworld"} unless score #y1 se matches 0..255 run return run tellraw @s {text:"ネザー/エンドの高さは0〜255です。",color:"red"}
execute unless data storage editor:data selection{dim:"minecraft:overworld"} unless score #y2 se matches 0..255 run return run tellraw @s {text:"ネザー/エンドの高さは0〜255です。",color:"red"}
data modify storage editor:data selection.valid set value 1b
function editor:internal/selection/preview
tellraw @s {"text": "[Space Editor] Selectionを更新しました。/function editor:menu から配置できます。", "color": "aqua"}
