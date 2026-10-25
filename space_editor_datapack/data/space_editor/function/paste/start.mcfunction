$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]
execute unless data storage space_editor:runtime template.id run return run tellraw @s {"text": "[Space Editor] TemplateIDがDocumentにありません。", "color": "red"}
data modify storage space_editor:document job set value {type:"paste",state:"running",id:0,version:1,sourceDimension:"",targetDimension:"",sourceX:0,sourceY:0,sourceZ:0,targetX:0,targetY:0,targetZ:0,sx:0,sy:0,sz:0,cursorX:0,completedChunks:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}
data modify storage space_editor:document job.id set from storage space_editor:runtime template.id
data modify storage space_editor:document job.version set from storage space_editor:runtime template.version
data modify storage space_editor:document job.sourceDimension set from storage space_editor:runtime template.archive.dimension
data modify storage space_editor:document job.sourceX set from storage space_editor:runtime template.archive.x
data modify storage space_editor:document job.sourceY set from storage space_editor:runtime template.archive.y
data modify storage space_editor:document job.sourceZ set from storage space_editor:runtime template.archive.z
data modify storage space_editor:document job.targetDimension set from storage space_editor:runtime targetDimension
execute store result storage space_editor:document job.targetX int 1 run data get storage space_editor:runtime targetPos[0] 1
execute store result storage space_editor:document job.targetY int 1 run data get storage space_editor:runtime targetPos[1] 1
execute store result storage space_editor:document job.targetZ int 1 run data get storage space_editor:runtime targetPos[2] 1
data modify storage space_editor:document job.sx set from storage space_editor:runtime template.size[0]
data modify storage space_editor:document job.sy set from storage space_editor:runtime template.size[1]
data modify storage space_editor:document job.sz set from storage space_editor:runtime template.size[2]
data modify storage space_editor:document job.owner0 set from storage space_editor:runtime lookup.owner0
data modify storage space_editor:document job.owner1 set from storage space_editor:runtime lookup.owner1
data modify storage space_editor:document job.owner2 set from storage space_editor:runtime lookup.owner2
data modify storage space_editor:document job.owner3 set from storage space_editor:runtime lookup.owner3
data modify storage space_editor:document job.archiveDimension set from storage space_editor:runtime template.archive.dimension
data modify storage space_editor:document job.archiveX1 set from storage space_editor:runtime template.archive.x
data modify storage space_editor:document job.archiveZ1 set from storage space_editor:runtime template.archive.z
execute store result score #archive_x2 se.v run data get storage space_editor:runtime template.archive.x 1
execute store result score #archive_z2 se.v run data get storage space_editor:runtime template.archive.z 1
execute store result score #sx se.v run data get storage space_editor:runtime template.size[0] 1
execute store result score #sz se.v run data get storage space_editor:runtime template.size[2] 1
scoreboard players operation #archive_x2 se.v += #sx se.v
scoreboard players remove #archive_x2 se.v 1
scoreboard players operation #archive_z2 se.v += #sz se.v
scoreboard players remove #archive_z2 se.v 1
execute store result storage space_editor:document job.archiveX2 int 1 run scoreboard players get #archive_x2 se.v
execute store result storage space_editor:document job.archiveZ2 int 1 run scoreboard players get #archive_z2 se.v
function space_editor:job/forceload_archive with storage space_editor:document job
tellraw @s {"text": "[Space Editor] Paste Jobを開始しました（0度・反転なし・airを含む・クリックしたブロック原点）。", "color": "green"}
