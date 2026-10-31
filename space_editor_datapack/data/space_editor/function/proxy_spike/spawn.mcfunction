execute unless entity @s[type=minecraft:player] run return 0
execute at @s unless loaded ~ ~ ~3 run return run tellraw @s {text:'[06-1] 生成先チャンクが未ロードです',color:'yellow'}
function space_editor:proxy_spike/stop
scoreboard players add #next sp.owner 1
scoreboard players operation @s sp.owner = #next sp.owner
scoreboard players add @s sp.leave 0
scoreboard players operation @s sp.seen = @s sp.leave
scoreboard players operation @s sp.epoch = #epoch sp.epoch
tag @s add sp.active
scoreboard players set @s sp.flip 0
scoreboard players set @s sp.name 3
scoreboard players set @s sp.follow 1
scoreboard players set @s sp.x 0
scoreboard players set @s sp.y 0
scoreboard players set @s sp.z 3000
scoreboard players set @s sp.fy 0
scoreboard players set @s sp.normal 2100
scoreboard players set @s sp.inverted -300
scoreboard players set @s sp.demo 0
execute at @s run function space_editor:proxy_spike/spawn_main
execute at @s run function space_editor:proxy_spike/player_tick
