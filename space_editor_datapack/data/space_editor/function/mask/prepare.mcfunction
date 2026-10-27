scoreboard players set #mask_valid se.v 1
scoreboard players set #mask_region_found se.v 0
data remove storage space_editor:runtime maskRegion
function space_editor:mask/load_region with storage space_editor:runtime currentMask
execute if data storage space_editor:runtime maskRegion.id run scoreboard players set #mask_region_found se.v 1
execute unless score #mask_region_found se.v matches 1 run return run scoreboard players set #mask_valid se.v 0
data modify storage space_editor:runtime maskRender set from storage space_editor:runtime currentMask
data modify storage space_editor:runtime maskRender.dimension set from storage space_editor:runtime maskRegion.dimension
data modify storage space_editor:runtime maskRender.dim set from storage space_editor:runtime maskRegion.dimension
data modify storage space_editor:runtime maskRender.pos set value [0.0d,0.0d,0.0d]
data modify storage space_editor:runtime maskRender.scale set value [1.0f,1.0f,1.0f]
data modify storage space_editor:runtime maskRender.x1 set from storage space_editor:runtime maskRegion.x1
execute store result score #mask_pos se.v run data get storage space_editor:runtime maskRegion.x1m 1
execute store result score #mask_size se.v run data get storage space_editor:runtime maskRegion.sxm 1
execute store result score #mask_offset se.v run data get storage space_editor:runtime currentMask.offset[0] 1
execute store result score #mask_expand se.v run data get storage space_editor:runtime currentMask.expand[0] 1
scoreboard players operation #mask_pos se.v += #mask_offset se.v
scoreboard players operation #mask_pos se.v -= #mask_expand se.v
scoreboard players operation #mask_size se.v += #mask_expand se.v
scoreboard players operation #mask_size se.v += #mask_expand se.v
execute unless score #mask_size se.v matches 1..128000 run scoreboard players set #mask_valid se.v 0
execute store result storage space_editor:runtime maskRender.px double 0.001 run scoreboard players get #mask_pos se.v
execute store result storage space_editor:runtime maskRender.sx double 0.001 run scoreboard players get #mask_size se.v
execute store result storage space_editor:runtime maskRender.pos[0] double 0.001 run scoreboard players get #mask_pos se.v
execute store result storage space_editor:runtime maskRender.scale[0] float 0.001 run scoreboard players get #mask_size se.v
data modify storage space_editor:runtime maskRender.y1 set from storage space_editor:runtime maskRegion.y1
execute store result score #mask_pos se.v run data get storage space_editor:runtime maskRegion.y1m 1
execute store result score #mask_size se.v run data get storage space_editor:runtime maskRegion.sym 1
execute store result score #mask_offset se.v run data get storage space_editor:runtime currentMask.offset[1] 1
execute store result score #mask_expand se.v run data get storage space_editor:runtime currentMask.expand[1] 1
scoreboard players operation #mask_pos se.v += #mask_offset se.v
scoreboard players operation #mask_pos se.v -= #mask_expand se.v
scoreboard players operation #mask_size se.v += #mask_expand se.v
scoreboard players operation #mask_size se.v += #mask_expand se.v
execute unless score #mask_size se.v matches 1..128000 run scoreboard players set #mask_valid se.v 0
execute store result storage space_editor:runtime maskRender.py double 0.001 run scoreboard players get #mask_pos se.v
execute store result storage space_editor:runtime maskRender.sy double 0.001 run scoreboard players get #mask_size se.v
execute store result storage space_editor:runtime maskRender.pos[1] double 0.001 run scoreboard players get #mask_pos se.v
execute store result storage space_editor:runtime maskRender.scale[1] float 0.001 run scoreboard players get #mask_size se.v
data modify storage space_editor:runtime maskRender.z1 set from storage space_editor:runtime maskRegion.z1
execute store result score #mask_pos se.v run data get storage space_editor:runtime maskRegion.z1m 1
execute store result score #mask_size se.v run data get storage space_editor:runtime maskRegion.szm 1
execute store result score #mask_offset se.v run data get storage space_editor:runtime currentMask.offset[2] 1
execute store result score #mask_expand se.v run data get storage space_editor:runtime currentMask.expand[2] 1
scoreboard players operation #mask_pos se.v += #mask_offset se.v
scoreboard players operation #mask_pos se.v -= #mask_expand se.v
scoreboard players operation #mask_size se.v += #mask_expand se.v
scoreboard players operation #mask_size se.v += #mask_expand se.v
execute unless score #mask_size se.v matches 1..128000 run scoreboard players set #mask_valid se.v 0
execute store result storage space_editor:runtime maskRender.pz double 0.001 run scoreboard players get #mask_pos se.v
execute store result storage space_editor:runtime maskRender.sz double 0.001 run scoreboard players get #mask_size se.v
execute store result storage space_editor:runtime maskRender.pos[2] double 0.001 run scoreboard players get #mask_pos se.v
execute store result storage space_editor:runtime maskRender.scale[2] float 0.001 run scoreboard players get #mask_size se.v
