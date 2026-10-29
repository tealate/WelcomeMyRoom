function space_editor:space_group/check_owner
execute unless score #session_owner se.v matches 1 run return 0
scoreboard players set #session_live se.v 1
