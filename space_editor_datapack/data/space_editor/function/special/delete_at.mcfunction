scoreboard players set #special_water se.v 0
execute if block ~ ~ ~ minecraft:cherry_fence[waterlogged=true] run scoreboard players set #special_water se.v 1
execute if block ~ ~ ~ minecraft:sandstone_wall[waterlogged=true] run scoreboard players set #special_water se.v 1
execute as @e[type=minecraft:block_display,tag=space_editor.special,distance=..0.1] run function space_editor:special/remove_entity
execute if score #special_water se.v matches 1 run setblock ~ ~ ~ minecraft:water
execute unless score #special_water se.v matches 1 run setblock ~ ~ ~ minecraft:air
function space_editor:special/sync_neighbors
tellraw @s {"text": "[Space Editor] 反転特殊ブロックを表示と当たり判定ごと削除しました。", "color": "yellow"}
return 1
