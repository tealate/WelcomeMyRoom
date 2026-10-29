execute unless data storage space_editor:runtime frame.x1m run return run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame.x1m run return run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame.x2m run return run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame.y1m run return run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame.y2m run return run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame.z1m run return run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame.z2m run return run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame{dimension:"minecraft:overworld"} unless data storage space_editor:runtime frame{dimension:"minecraft:the_nether"} unless data storage space_editor:runtime frame{dimension:"minecraft:the_end"} run return run scoreboard players set #sg_ok se.v 0
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame{rotationY:0} unless data storage space_editor:runtime frame{rotationY:90} unless data storage space_editor:runtime frame{rotationY:180} unless data storage space_editor:runtime frame{rotationY:270} run scoreboard players set #sg_ok se.v 0
execute unless data storage space_editor:runtime frame{flipY:0b} unless data storage space_editor:runtime frame{flipY:1b} run scoreboard players set #sg_ok se.v 0
data modify storage space_editor:runtime sgSize set from storage space_editor:runtime frame.localSize
execute store success score #sg_diff se.v run data modify storage space_editor:runtime sgSize set from storage space_editor:runtime sg.group.localSize
execute if score #sg_diff se.v matches 1 run scoreboard players set #sg_ok se.v 0
