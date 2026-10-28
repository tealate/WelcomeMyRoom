function space_editor:pair/read_intent
execute if score @s se.intent matches 1 run scoreboard players remove @s se.prot 90
execute if score @s se.intent matches 2 run scoreboard players add @s se.prot 90
execute if score @s se.prot matches ..-1 run scoreboard players set @s se.prot 270
execute if score @s se.prot matches 360.. run scoreboard players set @s se.prot 0
execute if score @s se.intent matches 3 run function space_editor:pair/toggle_flip
execute if data storage space_editor:runtime pairPending run return run function space_editor:pair/track
data modify storage space_editor:runtime pairPose set value {}
data modify storage space_editor:runtime pairPose.id set from storage space_editor:runtime pairSession.selected
execute store result storage space_editor:runtime pairPose.rotationY int 1 run scoreboard players get @s se.prot
execute store result storage space_editor:runtime pairPose.flipY int 1 run scoreboard players get @s se.pflip
function space_editor:pair/set_pose with storage space_editor:runtime pairPose
