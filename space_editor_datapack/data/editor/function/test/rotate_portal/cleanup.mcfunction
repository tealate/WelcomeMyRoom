data modify storage editor:spacewarp_test running set value 0b
schedule clear editor:test/rotate_portal/tick
execute in minecraft:overworld run kill @e[type=minecraft:marker,tag=swp_test_marker]
execute in minecraft:the_nether run kill @e[type=minecraft:marker,tag=swp_test_marker]
execute in minecraft:the_end run kill @e[type=minecraft:marker,tag=swp_test_marker]
tag @a remove swp_test_locked
tag @a remove swp_test_outside
data remove storage editor:spacewarp_test setup
data remove storage editor:spacewarp_test running
data remove storage editor:spacewarp_test tp
scoreboard objectives remove swp.test
tellraw @s {"text":"[90度ポータル] マーカーと一時データを削除しました。","color":"gray"}
