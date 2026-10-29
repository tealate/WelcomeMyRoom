execute store result score @s se.pyaw run data get entity @s Rotation[0] 1
scoreboard players set @s se.rot 0
scoreboard players set @s se.flip 0
execute if data storage space_editor:runtime pastePending.rotation store result score @s se.rot run data get storage space_editor:runtime pastePending.rotation 1
execute if data storage space_editor:runtime pastePending.flipY store result score @s se.flip run data get storage space_editor:runtime pastePending.flipY 1
scoreboard players set @s se.ph 1
