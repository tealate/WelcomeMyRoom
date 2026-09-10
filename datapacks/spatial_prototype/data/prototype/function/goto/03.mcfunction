execute unless score #p03.built proto.state matches 1 run tellraw @s {"text":"Run /function prototype:p03/setup and wait for ready.","color":"yellow"}
execute if score #p03.built proto.state matches 1 run scoreboard players set @s proto.cd 20
execute if score #p03.built proto.state matches 1 in prototype:lab run tp @s 389.5 65 -6.5 0 0
