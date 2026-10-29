scoreboard players set #session_live se.v 0
execute as @a[tag=space_editor.editing] if data storage space_editor:runtime pairSession.owner run function space_editor:space_group/session_player
execute if data storage space_editor:runtime pairSession.owner unless score #session_live se.v matches 1 run function space_editor:pair/cancel
