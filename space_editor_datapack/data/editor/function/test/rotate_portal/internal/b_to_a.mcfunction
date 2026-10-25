# Read the player's precise position at milliblock resolution, relative to B.
execute store result score #x swp.test run data get entity @s Pos[0] 1000
execute store result score #y swp.test run data get entity @s Pos[1] 1000
execute store result score #z swp.test run data get entity @s Pos[2] 1000
scoreboard players operation #x swp.test -= #bx swp.test
scoreboard players operation #y swp.test -= #by swp.test
scoreboard players operation #z swp.test -= #bz swp.test

# -90 degrees around Y: (dx, dz) -> (dz, -dx).
scoreboard players operation #old_x swp.test = #x swp.test
scoreboard players operation #x swp.test = #z swp.test
scoreboard players operation #z swp.test = #old_x swp.test
scoreboard players operation #z swp.test *= #-1 swp.test
scoreboard players operation #x swp.test += #ax swp.test
scoreboard players operation #y swp.test += #ay swp.test
scoreboard players operation #z swp.test += #az swp.test

execute store result storage editor:spacewarp_test tp.x double 0.001 run scoreboard players get #x swp.test
execute store result storage editor:spacewarp_test tp.y double 0.001 run scoreboard players get #y swp.test
execute store result storage editor:spacewarp_test tp.z double 0.001 run scoreboard players get #z swp.test
tag @s add swp_test_locked
function editor:test/rotate_portal/internal/tp_minus_90 with storage editor:spacewarp_test tp
