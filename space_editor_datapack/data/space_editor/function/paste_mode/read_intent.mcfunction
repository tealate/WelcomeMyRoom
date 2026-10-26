scoreboard players set @s se.intent 0
execute store result score @s se.pitch run data get entity @s Rotation[1] 1
scoreboard players operation #pitch_abs se.v = @s se.pitch
execute if score #pitch_abs se.v matches ..-1 run scoreboard players operation #pitch_abs se.v *= #minus_one se.v
execute if score #pitch_abs se.v matches 45.. run scoreboard players set @s se.intent 3
execute if score @s se.intent matches 3 run return 0
execute store result score #view_yaw se.v run data get entity @s Rotation[0] 1
scoreboard players operation #yaw_delta se.v = #view_yaw se.v
scoreboard players operation #yaw_delta se.v -= @s se.pyaw
execute if score #yaw_delta se.v matches ..-181 run scoreboard players add #yaw_delta se.v 360
execute if score #yaw_delta se.v matches 180.. run scoreboard players remove #yaw_delta se.v 360
execute if score #yaw_delta se.v matches -135..-45 run scoreboard players set @s se.intent 1
execute if score #yaw_delta se.v matches 45..135 run scoreboard players set @s se.intent 2
