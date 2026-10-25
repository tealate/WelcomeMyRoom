execute if data storage space_editor:document job{state:"running"} run return run tellraw @s {"text": "[Space Editor] 別のCopy/Paste Jobが実行中です。", "color": "red"}
execute store result score #aligned se.v run function space_editor:operation/check_aligned
execute unless score #aligned se.v matches 1 run return run tellraw @s {"text": "[Space Editor] Copyはブロック境界に揃ったRegionだけ使用できます。", "color": "red"}
execute store result score #template se.v run data get storage space_editor:document nextTemplateId 1
scoreboard players operation #archive_x se.v = #template se.v
scoreboard players set #stride se.v 64
scoreboard players operation #archive_x se.v *= #stride se.v
scoreboard players add #archive_x se.v 20000000
data modify storage space_editor:document job set value {type:"copy",state:"running",id:0,version:1,sourceDimension:"",targetDimension:"minecraft:overworld",sourceX:0,sourceY:0,sourceZ:0,targetX:0,targetY:-63,targetZ:20000000,sx:0,sy:0,sz:0,cursorX:0,completedChunks:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}
execute store result storage space_editor:document job.id int 1 run scoreboard players get #template se.v
data modify storage space_editor:document job.sourceDimension set from storage space_editor:runtime hit.dimension
execute store result storage space_editor:document job.sourceX int 1 run scoreboard players get #x1 se.v
execute store result storage space_editor:document job.sourceY int 1 run scoreboard players get #y1 se.v
execute store result storage space_editor:document job.sourceZ int 1 run scoreboard players get #z1 se.v
execute store result storage space_editor:document job.targetX int 1 run scoreboard players get #archive_x se.v
execute store result storage space_editor:document job.sx int 1 run scoreboard players get #sx se.v
execute store result storage space_editor:document job.sy int 1 run scoreboard players get #sy se.v
execute store result storage space_editor:document job.sz int 1 run scoreboard players get #sz se.v
scoreboard players operation #archive_x2 se.v = #archive_x se.v
scoreboard players operation #archive_x2 se.v += #sx se.v
scoreboard players remove #archive_x2 se.v 1
scoreboard players set #archive_z2 se.v 20000000
scoreboard players operation #archive_z2 se.v += #sz se.v
scoreboard players remove #archive_z2 se.v 1
data modify storage space_editor:document job.archiveDimension set value "minecraft:overworld"
execute store result storage space_editor:document job.archiveX1 int 1 run scoreboard players get #archive_x se.v
data modify storage space_editor:document job.archiveZ1 set value 20000000
execute store result storage space_editor:document job.archiveX2 int 1 run scoreboard players get #archive_x2 se.v
execute store result storage space_editor:document job.archiveZ2 int 1 run scoreboard players get #archive_z2 se.v
execute store result storage space_editor:document job.owner0 int 1 run data get entity @s UUID[0] 1
execute store result storage space_editor:document job.owner1 int 1 run data get entity @s UUID[1] 1
execute store result storage space_editor:document job.owner2 int 1 run data get entity @s UUID[2] 1
execute store result storage space_editor:document job.owner3 int 1 run data get entity @s UUID[3] 1
data modify storage space_editor:document job.sourceRegion set from storage space_editor:runtime hit
function space_editor:job/forceload_archive with storage space_editor:document job
scoreboard players add #template se.v 1
execute store result storage space_editor:document nextTemplateId int 1 run scoreboard players get #template se.v
tellraw @s {"text": "[Space Editor] Copy Jobを開始しました。進捗はDocumentへ保存されます。", "color": "green"}
