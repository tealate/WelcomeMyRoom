execute store result score #fcx se.v run data get storage space_editor:runtime frame.x1m 1
execute store result score #ft se.v run data get storage space_editor:runtime frame.x2m 1
scoreboard players operation #fcx se.v += #ft se.v
execute store result score #fcy se.v run data get storage space_editor:runtime frame.y1m 1
execute store result score #ft se.v run data get storage space_editor:runtime frame.y2m 1
scoreboard players operation #fcy se.v += #ft se.v
execute store result score #fcz se.v run data get storage space_editor:runtime frame.z1m 1
execute store result score #ft se.v run data get storage space_editor:runtime frame.z2m 1
scoreboard players operation #fcz se.v += #ft se.v
execute if data storage space_editor:runtime frame{rotationY:0} store result score #fsx se.v run data get storage space_editor:runtime frame.localSize[0] 1
execute if data storage space_editor:runtime frame{rotationY:0} store result score #fsy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:0} store result score #fsz se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:90} store result score #fsx se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:90} store result score #fsy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:90} store result score #fsz se.v run data get storage space_editor:runtime frame.localSize[0] 1
execute if data storage space_editor:runtime frame{rotationY:180} store result score #fsx se.v run data get storage space_editor:runtime frame.localSize[0] 1
execute if data storage space_editor:runtime frame{rotationY:180} store result score #fsy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:180} store result score #fsz se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:270} store result score #fsx se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:270} store result score #fsy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:270} store result score #fsz se.v run data get storage space_editor:runtime frame.localSize[0] 1
scoreboard players set #pose_ok se.v 1
scoreboard players operation #fx1 se.v = #fcx se.v
scoreboard players operation #fx1 se.v -= #fsx se.v
scoreboard players operation #ft se.v = #fx1 se.v
scoreboard players operation #ft se.v %= #two se.v
execute unless score #ft se.v matches 0 run scoreboard players set #pose_ok se.v 0
scoreboard players operation #fx1 se.v /= #two se.v
scoreboard players operation #fx2 se.v = #fx1 se.v
scoreboard players operation #fx2 se.v += #fsx se.v
execute store result storage space_editor:runtime frame.x1m int 1 run scoreboard players get #fx1 se.v
execute store result storage space_editor:runtime frame.x2m int 1 run scoreboard players get #fx2 se.v
scoreboard players operation #fy1 se.v = #fcy se.v
scoreboard players operation #fy1 se.v -= #fsy se.v
scoreboard players operation #ft se.v = #fy1 se.v
scoreboard players operation #ft se.v %= #two se.v
execute unless score #ft se.v matches 0 run scoreboard players set #pose_ok se.v 0
scoreboard players operation #fy1 se.v /= #two se.v
scoreboard players operation #fy2 se.v = #fy1 se.v
scoreboard players operation #fy2 se.v += #fsy se.v
execute store result storage space_editor:runtime frame.y1m int 1 run scoreboard players get #fy1 se.v
execute store result storage space_editor:runtime frame.y2m int 1 run scoreboard players get #fy2 se.v
scoreboard players operation #fz1 se.v = #fcz se.v
scoreboard players operation #fz1 se.v -= #fsz se.v
scoreboard players operation #ft se.v = #fz1 se.v
scoreboard players operation #ft se.v %= #two se.v
execute unless score #ft se.v matches 0 run scoreboard players set #pose_ok se.v 0
scoreboard players operation #fz1 se.v /= #two se.v
scoreboard players operation #fz2 se.v = #fz1 se.v
scoreboard players operation #fz2 se.v += #fsz se.v
execute store result storage space_editor:runtime frame.z1m int 1 run scoreboard players get #fz1 se.v
execute store result storage space_editor:runtime frame.z2m int 1 run scoreboard players get #fz2 se.v
function space_editor:pair/frame
execute unless score #pose_ok se.v matches 1 run scoreboard players set #frame_ok se.v 0
