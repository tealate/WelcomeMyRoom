function space_editor:pair/cancel
execute store result score @s se.pbase run data get entity @s Rotation[0] 1
scoreboard players set @s se.pheld 1
scoreboard players set @s se.prot 0
scoreboard players set @s se.pflip 0
data modify storage space_editor:runtime pairSession set value {}
data modify storage space_editor:runtime pairSession.owner set from entity @s UUID
