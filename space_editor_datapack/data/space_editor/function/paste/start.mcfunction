$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]
execute unless data storage space_editor:runtime template.id run return run tellraw @s {"text": "[Space Editor] TemplateIDがDocumentにありません。", "color": "red"}
execute unless data storage space_editor:runtime pasteTransform run data modify storage space_editor:runtime pasteTransform set value {rotation:0,flipY:0b}
data modify storage space_editor:document job set value {type:"paste",state:"running",mode:"fast",phase:"place",id:0,version:1,sourceDimension:"",targetDimension:"",sourceX:0,sourceY:0,sourceZ:0,targetX:0,targetY:0,targetZ:0,targetX2:0,targetZ2:0,scratchX:0,scratchY:0,scratchZ:0,sx:0,sy:0,sz:0,outSx:0,outSy:0,outSz:0,cursorX:0,cursor:0,totalBlocks:0,completedChunks:0,completedBlocks:0,unsupportedBlocks:0,skippedBlocks:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}
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
data modify storage space_editor:document job.outSx set from storage space_editor:runtime template.size[0]
data modify storage space_editor:document job.outSy set from storage space_editor:runtime template.size[1]
data modify storage space_editor:document job.outSz set from storage space_editor:runtime template.size[2]
data modify storage space_editor:document job.rotation set from storage space_editor:runtime pasteTransform.rotation
data modify storage space_editor:document job.flipY set from storage space_editor:runtime pasteTransform.flipY
data modify storage space_editor:document job.masked set value 0b
data modify storage space_editor:document job.masked set from storage space_editor:runtime pasteTransform.masked
data modify storage space_editor:document job.owner0 set from storage space_editor:runtime lookup.owner0
data modify storage space_editor:document job.owner1 set from storage space_editor:runtime lookup.owner1
data modify storage space_editor:document job.owner2 set from storage space_editor:runtime lookup.owner2
data modify storage space_editor:document job.owner3 set from storage space_editor:runtime lookup.owner3
execute store result score #rotation se.v run data get storage space_editor:document job.rotation 1
execute if score #rotation se.v matches 90 run function space_editor:paste/swap_job_xz
execute if score #rotation se.v matches 270 run function space_editor:paste/swap_job_xz
execute store result score #sx se.v run data get storage space_editor:document job.sx 1
execute store result score #sy se.v run data get storage space_editor:document job.sy 1
execute store result score #sz se.v run data get storage space_editor:document job.sz 1
execute store result score #outSx se.v run data get storage space_editor:document job.outSx 1
execute store result score #outSz se.v run data get storage space_editor:document job.outSz 1
scoreboard players operation #total se.v = #sx se.v
scoreboard players operation #total se.v *= #sy se.v
scoreboard players operation #total se.v *= #sz se.v
execute store result storage space_editor:document job.totalBlocks int 1 run scoreboard players get #total se.v
execute store result score #target_x2 se.v run data get storage space_editor:document job.targetX 1
scoreboard players operation #target_x2 se.v += #outSx se.v
scoreboard players remove #target_x2 se.v 1
execute store result score #target_z2 se.v run data get storage space_editor:document job.targetZ 1
scoreboard players operation #target_z2 se.v += #outSz se.v
scoreboard players remove #target_z2 se.v 1
execute store result storage space_editor:document job.targetX2 int 1 run scoreboard players get #target_x2 se.v
execute store result storage space_editor:document job.targetZ2 int 1 run scoreboard players get #target_z2 se.v
data modify storage space_editor:document job.archiveDimension set from storage space_editor:runtime template.archive.dimension
data modify storage space_editor:document job.archiveX1 set from storage space_editor:runtime template.archive.x
data modify storage space_editor:document job.archiveZ1 set from storage space_editor:runtime template.archive.z
execute store result score #archive_x2 se.v run data get storage space_editor:runtime template.archive.x 1
execute store result score #archive_z2 se.v run data get storage space_editor:runtime template.archive.z 1
scoreboard players operation #archive_x2 se.v += #sx se.v
scoreboard players remove #archive_x2 se.v 1
scoreboard players operation #archive_z2 se.v += #sz se.v
scoreboard players remove #archive_z2 se.v 1
execute store result storage space_editor:document job.archiveX2 int 1 run scoreboard players get #archive_x2 se.v
execute store result storage space_editor:document job.archiveZ2 int 1 run scoreboard players get #archive_z2 se.v
data modify storage space_editor:document job.scratchX set from storage space_editor:document job.sourceX
data modify storage space_editor:document job.scratchZ set from storage space_editor:document job.sourceZ
execute store result score #scratch_y se.v run data get storage space_editor:document job.sourceY 1
scoreboard players add #scratch_y se.v 48
execute store result storage space_editor:document job.scratchY int 1 run scoreboard players get #scratch_y se.v
execute store result score #flip se.v run data get storage space_editor:document job.flipY 1
execute unless score #rotation se.v matches 0 run data modify storage space_editor:document job.mode set value "transformed"
execute unless score #rotation se.v matches 0 run data modify storage space_editor:document job.phase set value "preflight"
execute if score #flip se.v matches 1 run data modify storage space_editor:document job.mode set value "transformed"
execute if score #flip se.v matches 1 run data modify storage space_editor:document job.phase set value "preflight"
function space_editor:job/forceload_archive with storage space_editor:document job
function space_editor:job/forceload_target with storage space_editor:document job
tellraw @s {"text": "[Space Editor] Paste Jobを開始しました。変換ありは事前走査後、1ブロックずつ配置します。", "color": "green"}
