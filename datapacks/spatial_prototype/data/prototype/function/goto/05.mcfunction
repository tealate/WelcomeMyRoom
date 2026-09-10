execute unless score #p05.built proto.state matches 1 run tellraw @s {"text":"Run /function prototype:p05/setup and wait for ready.","color":"yellow"}
execute if score #p05.built proto.state matches 1 run scoreboard players set @s proto.cd 20
execute if score #p05.built proto.state matches 1 in prototype:lab run tp @s 645.5 65 -6.5 0 0
