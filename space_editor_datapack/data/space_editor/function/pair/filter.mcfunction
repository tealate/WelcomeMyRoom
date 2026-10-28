scoreboard players set #pair_filter se.v 0
execute if data storage space_editor:runtime pairSession{kind:"teleport"} if data storage space_editor:runtime candidate{kind:"teleport"} run scoreboard players set #pair_filter se.v 1
execute if data storage space_editor:runtime pairSession{kind:"space_link"} if data storage space_editor:runtime candidate{kind:"space_link"} run scoreboard players set #pair_filter se.v 1
execute if data storage space_editor:runtime pairSession{kind:"proxy_existence"} if data storage space_editor:runtime candidate{kind:"proxy_existence"} run scoreboard players set #pair_filter se.v 1
