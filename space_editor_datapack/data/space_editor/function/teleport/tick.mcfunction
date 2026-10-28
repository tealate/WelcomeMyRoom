scoreboard players add @a se.tp_lock 0
scoreboard players add @a se.tp_cd 0
scoreboard players add @a se.instance 0
scoreboard players remove @a[scores={se.tp_cd=1..}] se.tp_cd 1
data modify storage space_editor:runtime playerSnapshots set value []
data modify storage space_editor:runtime spaceLinkContacts set value []
data modify storage space_editor:runtime transfers set value []
execute as @a at @s run function space_editor:teleport/snapshot
execute if data storage space_editor:document {editMode:1b} run return 0
execute as @a[gamemode=!spectator] at @s run function space_editor:link/player
function #space_editor:before_teleport
execute as @a[gamemode=!spectator] at @s run function space_editor:teleport/player
function #space_editor:after_teleport
