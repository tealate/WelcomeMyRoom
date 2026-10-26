execute if data storage space_editor:document job{state:"running"} run function space_editor:job/unforceload_archive with storage space_editor:document job
execute if data storage space_editor:document job{state:"paused"} run function space_editor:job/unforceload_archive with storage space_editor:document job
execute if data storage space_editor:document job{state:"error"} run function space_editor:job/unforceload_archive with storage space_editor:document job
execute if data storage space_editor:document job{type:"paste",state:"running"} run function space_editor:job/unforceload_target with storage space_editor:document job
execute if data storage space_editor:document job{type:"paste",state:"paused"} run function space_editor:job/unforceload_target with storage space_editor:document job
execute if data storage space_editor:document job{type:"paste",state:"error"} run function space_editor:job/unforceload_target with storage space_editor:document job
$execute if data storage space_editor:document job{type:"paste"} in $(sourceDimension) run setblock $(scratchX) $(scratchY) $(scratchZ) minecraft:air
execute if data storage space_editor:document job{state:"running"} run data modify storage space_editor:document job.state set value "cancelled"
execute if data storage space_editor:document job{state:"paused"} run data modify storage space_editor:document job.state set value "cancelled"
execute if data storage space_editor:document job{state:"error"} run data modify storage space_editor:document job.state set value "cancelled"
tellraw @s {"text": "[Space Editor] Jobを中断しました。コピー元と既存Templateは変更していません。", "color": "yellow"}
