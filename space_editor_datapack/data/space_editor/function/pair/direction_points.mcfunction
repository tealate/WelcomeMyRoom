execute if data storage space_editor:runtime frame{rotationY:0} run data modify storage space_editor:runtime frame.frontRotation set value [0f,0f,0f,1f]
execute if data storage space_editor:runtime frame{rotationY:90} run data modify storage space_editor:runtime frame.frontRotation set value [0f,0.70710677f,0f,0.70710677f]
execute if data storage space_editor:runtime frame{rotationY:180} run data modify storage space_editor:runtime frame.frontRotation set value [0f,1f,0f,0f]
execute if data storage space_editor:runtime frame{rotationY:270} run data modify storage space_editor:runtime frame.frontRotation set value [0f,-0.70710677f,0f,0.70710677f]
execute if data storage space_editor:runtime frame{flipY:0b} run data modify storage space_editor:runtime frame.upRotation set value [-0.70710677f,0f,0f,0.70710677f]
execute if data storage space_editor:runtime frame{flipY:1b} run data modify storage space_editor:runtime frame.upRotation set value [0.70710677f,0f,0f,0.70710677f]
scoreboard players operation #arrow_front_x se.v = #fcx se.v
scoreboard players operation #arrow_front_y se.v = #fcy se.v
scoreboard players operation #arrow_front_z se.v = #fcz se.v
scoreboard players operation #arrow_up_x se.v = #fcx se.v
scoreboard players operation #arrow_up_y se.v = #fcy se.v
scoreboard players operation #arrow_up_z se.v = #fcz se.v
execute if data storage space_editor:runtime frame{rotationY:0} run scoreboard players add #arrow_front_z se.v 1600
execute if data storage space_editor:runtime frame{rotationY:90} run scoreboard players remove #arrow_front_x se.v 1600
execute if data storage space_editor:runtime frame{rotationY:180} run scoreboard players remove #arrow_front_z se.v 1600
execute if data storage space_editor:runtime frame{rotationY:270} run scoreboard players add #arrow_front_x se.v 1600
execute if data storage space_editor:runtime frame{flipY:0b} run scoreboard players add #arrow_up_y se.v 1600
execute if data storage space_editor:runtime frame{flipY:1b} run scoreboard players remove #arrow_up_y se.v 1600
execute store result storage space_editor:runtime frame.frontx double 0.0005 run scoreboard players get #arrow_front_x se.v
execute store result storage space_editor:runtime frame.fronty double 0.0005 run scoreboard players get #arrow_front_y se.v
execute store result storage space_editor:runtime frame.frontz double 0.0005 run scoreboard players get #arrow_front_z se.v
execute store result storage space_editor:runtime frame.upx double 0.0005 run scoreboard players get #arrow_up_x se.v
execute store result storage space_editor:runtime frame.upy double 0.0005 run scoreboard players get #arrow_up_y se.v
execute store result storage space_editor:runtime frame.upz double 0.0005 run scoreboard players get #arrow_up_z se.v
