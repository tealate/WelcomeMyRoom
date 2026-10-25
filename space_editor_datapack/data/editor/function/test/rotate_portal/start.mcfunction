execute unless data storage editor:spacewarp_test {setup:1b} run return run tellraw @s {"text":"[90度ポータル] 先に setup を実行してください。","color":"red"}
data modify storage editor:spacewarp_test running set value 1b
scoreboard players set #clock swp.test 0
schedule function editor:test/rotate_portal/tick 1t replace
tellraw @s {"text":"[90度ポータル] テストを開始しました。","color":"green"}
