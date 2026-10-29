data modify storage space_editor:runtime snapshot set value {uuid:[I;0,0,0,0],point:[0d,0d,0d],rotation:[0f,0f],instanceId:0}
data modify storage space_editor:runtime snapshot.uuid set from entity @s UUID
data modify storage space_editor:runtime snapshot.vector set from entity @s Motion
data modify storage space_editor:runtime snapshot.point set from entity @s Pos
data modify storage space_editor:runtime snapshot.rotation set from entity @s Rotation
execute store result storage space_editor:runtime snapshot.instanceId int 1 run scoreboard players get @s se.instance
data modify storage space_editor:runtime snapshot.dimension set from entity @s Dimension
execute if dimension minecraft:overworld run data modify storage space_editor:runtime snapshot.dimension set value "minecraft:overworld"
execute if dimension minecraft:the_nether run data modify storage space_editor:runtime snapshot.dimension set value "minecraft:the_nether"
execute if dimension minecraft:the_end run data modify storage space_editor:runtime snapshot.dimension set value "minecraft:the_end"
data modify storage space_editor:runtime playerSnapshots append from storage space_editor:runtime snapshot
