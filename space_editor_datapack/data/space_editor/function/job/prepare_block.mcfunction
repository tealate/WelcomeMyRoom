execute store result score #sx se.v run data get storage space_editor:document job.sx 1
execute store result score #sy se.v run data get storage space_editor:document job.sy 1
execute store result score #sz se.v run data get storage space_editor:document job.sz 1
scoreboard players operation #rx se.v = #cursor se.v
scoreboard players operation #rx se.v %= #sx se.v
scoreboard players operation #work se.v = #cursor se.v
scoreboard players operation #work se.v /= #sx se.v
scoreboard players operation #rz se.v = #work se.v
scoreboard players operation #rz se.v %= #sz se.v
scoreboard players operation #ry se.v = #work se.v
scoreboard players operation #ry se.v /= #sz se.v
execute store result score #srcx se.v run data get storage space_editor:document job.sourceX 1
execute store result score #srcy se.v run data get storage space_editor:document job.sourceY 1
execute store result score #srcz se.v run data get storage space_editor:document job.sourceZ 1
execute store result score #dstx se.v run data get storage space_editor:document job.targetX 1
execute store result score #dsty se.v run data get storage space_editor:document job.targetY 1
execute store result score #dstz se.v run data get storage space_editor:document job.targetZ 1
scoreboard players operation #srcx se.v += #rx se.v
scoreboard players operation #srcy se.v += #ry se.v
scoreboard players operation #srcz se.v += #rz se.v
scoreboard players operation #tx se.v = #rx se.v
scoreboard players operation #ty se.v = #ry se.v
scoreboard players operation #tz se.v = #rz se.v
execute store result score #rotation se.v run data get storage space_editor:document job.rotation 1
execute store result score #flip se.v run data get storage space_editor:document job.flipY 1
execute if score #rotation se.v matches 90 run function space_editor:transform/coord_90
execute if score #rotation se.v matches 180 run function space_editor:transform/coord_180
execute if score #rotation se.v matches 270 run function space_editor:transform/coord_270
execute if score #flip se.v matches 1 run function space_editor:transform/coord_flip_y
scoreboard players operation #dstx se.v += #tx se.v
scoreboard players operation #dsty se.v += #ty se.v
scoreboard players operation #dstz se.v += #tz se.v
execute store result storage space_editor:document job.blockSourceX int 1 run scoreboard players get #srcx se.v
execute store result storage space_editor:document job.blockSourceY int 1 run scoreboard players get #srcy se.v
execute store result storage space_editor:document job.blockSourceZ int 1 run scoreboard players get #srcz se.v
execute store result storage space_editor:document job.blockTargetX int 1 run scoreboard players get #dstx se.v
execute store result storage space_editor:document job.blockTargetY int 1 run scoreboard players get #dsty se.v
execute store result storage space_editor:document job.blockTargetZ int 1 run scoreboard players get #dstz se.v
