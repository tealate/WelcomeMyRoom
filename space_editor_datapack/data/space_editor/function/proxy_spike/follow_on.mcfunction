function space_editor:proxy_spike/select
execute unless entity @e[type=minecraft:mannequin,tag=sp.selected] run return run tellraw @s {text:'[06-1] spawn / pair で生成してください',color:'yellow'}
scoreboard players set @s sp.follow 1
execute at @s run function space_editor:proxy_spike/player_tick
