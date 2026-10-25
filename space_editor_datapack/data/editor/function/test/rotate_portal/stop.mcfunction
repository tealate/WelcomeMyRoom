data modify storage editor:spacewarp_test running set value 0b
schedule clear editor:test/rotate_portal/tick
tag @a remove swp_test_locked
tag @a remove swp_test_outside
tellraw @s {"text":"[90度ポータル] テストを停止しました。マーカーは cleanup まで保持します。","color":"yellow"}
