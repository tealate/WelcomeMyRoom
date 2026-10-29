function space_editor:proxy_spike/select
execute if entity @e[tag=sp.selected,tag=sp.main] run scoreboard players set @s sp.follow 1
execute if entity @e[tag=sp.selected,tag=sp.main] run function space_editor:proxy_spike/player_tick
execute unless entity @e[tag=sp.selected,tag=sp.main] run tellraw @s {text:"[06-1] /function space_editor:proxy_spike/spawn を先に実行してください",color:"yellow"}
