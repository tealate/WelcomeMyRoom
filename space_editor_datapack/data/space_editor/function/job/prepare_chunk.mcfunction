execute store result score #srcx se.v run data get storage space_editor:document job.sourceX 1
execute store result score #srcy se.v run data get storage space_editor:document job.sourceY 1
execute store result score #srcz se.v run data get storage space_editor:document job.sourceZ 1
execute store result score #dstx se.v run data get storage space_editor:document job.targetX 1
execute store result score #dsty se.v run data get storage space_editor:document job.targetY 1
execute store result score #dstz se.v run data get storage space_editor:document job.targetZ 1
scoreboard players operation #srcx se.v += #cursor se.v
scoreboard players operation #dstx se.v += #cursor se.v
scoreboard players operation #srcx2 se.v = #srcx se.v
scoreboard players operation #srcx2 se.v += #width se.v
scoreboard players remove #srcx2 se.v 1
scoreboard players operation #srcy2 se.v = #srcy se.v
scoreboard players operation #srcy2 se.v += #sy se.v
scoreboard players remove #srcy2 se.v 1
scoreboard players operation #srcz2 se.v = #srcz se.v
scoreboard players operation #srcz2 se.v += #sz se.v
scoreboard players remove #srcz2 se.v 1
execute store result storage space_editor:document job.chunkSourceX1 int 1 run scoreboard players get #srcx se.v
execute store result storage space_editor:document job.chunkSourceY1 int 1 run scoreboard players get #srcy se.v
execute store result storage space_editor:document job.chunkSourceZ1 int 1 run scoreboard players get #srcz se.v
execute store result storage space_editor:document job.chunkSourceX2 int 1 run scoreboard players get #srcx2 se.v
execute store result storage space_editor:document job.chunkSourceY2 int 1 run scoreboard players get #srcy2 se.v
execute store result storage space_editor:document job.chunkSourceZ2 int 1 run scoreboard players get #srcz2 se.v
execute store result storage space_editor:document job.chunkTargetX int 1 run scoreboard players get #dstx se.v
execute store result storage space_editor:document job.chunkTargetY int 1 run scoreboard players get #dsty se.v
execute store result storage space_editor:document job.chunkTargetZ int 1 run scoreboard players get #dstz se.v
