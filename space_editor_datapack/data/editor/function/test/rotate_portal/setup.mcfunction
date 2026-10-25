# Reset only this isolated test before creating a fresh pair.
schedule clear editor:test/rotate_portal/tick
data modify storage editor:spacewarp_test running set value 0b
execute in minecraft:overworld run kill @e[type=minecraft:marker,tag=swp_test_marker]
execute in minecraft:the_nether run kill @e[type=minecraft:marker,tag=swp_test_marker]
execute in minecraft:the_end run kill @e[type=minecraft:marker,tag=swp_test_marker]
tag @a remove swp_test_locked
tag @a remove swp_test_outside

# Keep 0.001-block precision while doing the 90-degree coordinate transform.
scoreboard objectives add swp.test dummy
scoreboard players set #-1 swp.test -1
scoreboard players set #clock swp.test 0

# A is four blocks ahead. B is twelve blocks to the player's right.
# The centers are 1.5 blocks above the setup position, so each volume spans a
# walkable 3x3x3 region from setup-foot-level upward.
execute rotated ~ 0 positioned ^ ^1.5 ^4 run summon minecraft:marker ~ ~ ~ {Tags:["swp_test_marker","swp_test_a"]}
execute rotated ~ 0 positioned ^-12 ^1.5 ^ run summon minecraft:marker ~ ~ ~ {Tags:["swp_test_marker","swp_test_b"]}

execute as @e[type=minecraft:marker,tag=swp_test_a,limit=1,sort=nearest] store result score #ax swp.test run data get entity @s Pos[0] 1000
execute as @e[type=minecraft:marker,tag=swp_test_a,limit=1,sort=nearest] store result score #ay swp.test run data get entity @s Pos[1] 1000
execute as @e[type=minecraft:marker,tag=swp_test_a,limit=1,sort=nearest] store result score #az swp.test run data get entity @s Pos[2] 1000
execute as @e[type=minecraft:marker,tag=swp_test_b,limit=1,sort=nearest] store result score #bx swp.test run data get entity @s Pos[0] 1000
execute as @e[type=minecraft:marker,tag=swp_test_b,limit=1,sort=nearest] store result score #by swp.test run data get entity @s Pos[1] 1000
execute as @e[type=minecraft:marker,tag=swp_test_b,limit=1,sort=nearest] store result score #bz swp.test run data get entity @s Pos[2] 1000

data modify storage editor:spacewarp_test setup set value 1b
function editor:test/rotate_portal/internal/visualize_all
tellraw @s [{"text":"[90度ポータル] ","color":"gold"},{"text":"セットアップ完了。橙=A、青=B。","color":"yellow"},{"text":" /function editor:test/rotate_portal/start","color":"aqua"}]
