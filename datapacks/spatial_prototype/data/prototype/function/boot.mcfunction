function prototype:load
scoreboard players set #boot proto.state 1
function prototype:hub/setup
function prototype:p01/setup
function prototype:p02/setup
function prototype:p03/setup
function prototype:p04/setup
function prototype:p05/setup
execute in prototype:lab as @a[distance=0..] run tag @s add prototype.to_hub
tellraw @s {"text":"[prototype] Building in prototype:lab. Wait for ALL READY, then /function prototype:goto/hub","color":"yellow"}
