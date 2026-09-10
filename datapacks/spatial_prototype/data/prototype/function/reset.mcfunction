function prototype:load
scoreboard players set #boot proto.state 0
function prototype:hub/setup
execute in prototype:lab as @a[distance=0..] run tag @s add prototype.to_hub
execute in prototype:lab positioned 128 64 0 run forceload add ~-16 ~-16 ~31 ~63
scoreboard players set #p01.built proto.state 0
scoreboard players set #p01 proto.state -1
execute in prototype:lab positioned 256 64 0 run forceload add ~-16 ~-16 ~31 ~63
scoreboard players set #p02.built proto.state 0
scoreboard players set #p02 proto.state -1
execute in prototype:lab positioned 384 64 0 run forceload add ~-16 ~-16 ~31 ~63
scoreboard players set #p03.built proto.state 0
scoreboard players set #p03 proto.state -1
execute in prototype:lab positioned 512 64 0 run forceload add ~-16 ~-16 ~31 ~63
scoreboard players set #p04.built proto.state 0
scoreboard players set #p04 proto.state -1
execute in prototype:lab positioned 640 64 0 run forceload add ~-16 ~-16 ~31 ~63
scoreboard players set #p05.built proto.state 0
scoreboard players set #p05 proto.state -1
tellraw @s {"text":"[prototype] Removing experiments after chunks load. Safety hub is retained.","color":"yellow"}
