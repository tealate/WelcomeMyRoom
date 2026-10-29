scoreboard players set #frame_ok se.v 1
execute unless data storage space_editor:runtime frame.rotationY run data modify storage space_editor:runtime frame.rotationY set value 0
execute unless data storage space_editor:runtime frame.flipY run data modify storage space_editor:runtime frame.flipY set value 0b
data modify storage space_editor:runtime frame.localSize set value [I;0,0,0]
data modify storage space_editor:runtime frame.min set value [0d,0d,0d]
data modify storage space_editor:runtime frame.maxExclusive set value [0d,0d,0d]
execute store result score #fx1 se.v run data get storage space_editor:runtime frame.x1m 1
execute store result score #fx2 se.v run data get storage space_editor:runtime frame.x2m 1
scoreboard players operation #fsx se.v = #fx2 se.v
scoreboard players operation #fsx se.v -= #fx1 se.v
execute unless score #fsx se.v matches 100..32000 run scoreboard players set #frame_ok se.v 0
execute unless score #fx1 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0
execute unless score #fx2 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0
execute store result storage space_editor:runtime frame.x1 double 0.001 run scoreboard players get #fx1 se.v
execute store result storage space_editor:runtime frame.x2 double 0.001 run scoreboard players get #fx2 se.v
execute store result storage space_editor:runtime frame.min[0] double 0.001 run scoreboard players get #fx1 se.v
execute store result storage space_editor:runtime frame.maxExclusive[0] double 0.001 run scoreboard players get #fx2 se.v
execute store result storage space_editor:runtime frame.sx double 0.001 run scoreboard players get #fsx se.v
execute store result storage space_editor:runtime frame.sxm int 1 run scoreboard players get #fsx se.v
scoreboard players operation #fcx se.v = #fx1 se.v
scoreboard players operation #fcx se.v += #fx2 se.v
execute store result storage space_editor:runtime frame.cx double 0.0005 run scoreboard players get #fcx se.v
execute store result score #fy1 se.v run data get storage space_editor:runtime frame.y1m 1
execute store result score #fy2 se.v run data get storage space_editor:runtime frame.y2m 1
scoreboard players operation #fsy se.v = #fy2 se.v
scoreboard players operation #fsy se.v -= #fy1 se.v
execute unless score #fsy se.v matches 100..32000 run scoreboard players set #frame_ok se.v 0
execute unless score #fy1 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0
execute unless score #fy2 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0
execute store result storage space_editor:runtime frame.y1 double 0.001 run scoreboard players get #fy1 se.v
execute store result storage space_editor:runtime frame.y2 double 0.001 run scoreboard players get #fy2 se.v
execute store result storage space_editor:runtime frame.min[1] double 0.001 run scoreboard players get #fy1 se.v
execute store result storage space_editor:runtime frame.maxExclusive[1] double 0.001 run scoreboard players get #fy2 se.v
execute store result storage space_editor:runtime frame.sy double 0.001 run scoreboard players get #fsy se.v
execute store result storage space_editor:runtime frame.sym int 1 run scoreboard players get #fsy se.v
scoreboard players operation #fcy se.v = #fy1 se.v
scoreboard players operation #fcy se.v += #fy2 se.v
execute store result storage space_editor:runtime frame.cy double 0.0005 run scoreboard players get #fcy se.v
execute store result score #fz1 se.v run data get storage space_editor:runtime frame.z1m 1
execute store result score #fz2 se.v run data get storage space_editor:runtime frame.z2m 1
scoreboard players operation #fsz se.v = #fz2 se.v
scoreboard players operation #fsz se.v -= #fz1 se.v
execute unless score #fsz se.v matches 100..32000 run scoreboard players set #frame_ok se.v 0
execute unless score #fz1 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0
execute unless score #fz2 se.v matches -500000000..500000000 run scoreboard players set #frame_ok se.v 0
execute store result storage space_editor:runtime frame.z1 double 0.001 run scoreboard players get #fz1 se.v
execute store result storage space_editor:runtime frame.z2 double 0.001 run scoreboard players get #fz2 se.v
execute store result storage space_editor:runtime frame.min[2] double 0.001 run scoreboard players get #fz1 se.v
execute store result storage space_editor:runtime frame.maxExclusive[2] double 0.001 run scoreboard players get #fz2 se.v
execute store result storage space_editor:runtime frame.sz double 0.001 run scoreboard players get #fsz se.v
execute store result storage space_editor:runtime frame.szm int 1 run scoreboard players get #fsz se.v
scoreboard players operation #fcz se.v = #fz1 se.v
scoreboard players operation #fcz se.v += #fz2 se.v
execute store result storage space_editor:runtime frame.cz double 0.0005 run scoreboard players get #fcz se.v
execute if data storage space_editor:runtime frame{dimension:"minecraft:overworld"} unless score #fy1 se.v matches -64000..319900 run scoreboard players set #frame_ok se.v 0
execute if data storage space_editor:runtime frame{dimension:"minecraft:overworld"} unless score #fy2 se.v matches -63900..320000 run scoreboard players set #frame_ok se.v 0
execute unless data storage space_editor:runtime frame{dimension:"minecraft:overworld"} unless score #fy1 se.v matches 0..255900 run scoreboard players set #frame_ok se.v 0
execute unless data storage space_editor:runtime frame{dimension:"minecraft:overworld"} unless score #fy2 se.v matches 100..256000 run scoreboard players set #frame_ok se.v 0
execute if data storage space_editor:runtime frame{rotationY:0} store result storage space_editor:runtime frame.localSize[0] int 1 run scoreboard players get #fsx se.v
execute if data storage space_editor:runtime frame{rotationY:0} store result storage space_editor:runtime frame.localSize[1] int 1 run scoreboard players get #fsy se.v
execute if data storage space_editor:runtime frame{rotationY:0} store result storage space_editor:runtime frame.localSize[2] int 1 run scoreboard players get #fsz se.v
execute if data storage space_editor:runtime frame{rotationY:90} store result storage space_editor:runtime frame.localSize[2] int 1 run scoreboard players get #fsx se.v
execute if data storage space_editor:runtime frame{rotationY:90} store result storage space_editor:runtime frame.localSize[1] int 1 run scoreboard players get #fsy se.v
execute if data storage space_editor:runtime frame{rotationY:90} store result storage space_editor:runtime frame.localSize[0] int 1 run scoreboard players get #fsz se.v
execute if data storage space_editor:runtime frame{rotationY:180} store result storage space_editor:runtime frame.localSize[0] int 1 run scoreboard players get #fsx se.v
execute if data storage space_editor:runtime frame{rotationY:180} store result storage space_editor:runtime frame.localSize[1] int 1 run scoreboard players get #fsy se.v
execute if data storage space_editor:runtime frame{rotationY:180} store result storage space_editor:runtime frame.localSize[2] int 1 run scoreboard players get #fsz se.v
execute if data storage space_editor:runtime frame{rotationY:270} store result storage space_editor:runtime frame.localSize[2] int 1 run scoreboard players get #fsx se.v
execute if data storage space_editor:runtime frame{rotationY:270} store result storage space_editor:runtime frame.localSize[1] int 1 run scoreboard players get #fsy se.v
execute if data storage space_editor:runtime frame{rotationY:270} store result storage space_editor:runtime frame.localSize[0] int 1 run scoreboard players get #fsz se.v
