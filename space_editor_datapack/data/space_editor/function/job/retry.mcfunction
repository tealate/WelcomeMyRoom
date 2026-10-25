execute if data storage space_editor:document job{state:"error"} run data modify storage space_editor:document job.state set value "running"
data remove storage space_editor:document job.error
tellraw @s {"text": "[Space Editor] 失敗した区画からJobを再試行します。", "color": "yellow"}
