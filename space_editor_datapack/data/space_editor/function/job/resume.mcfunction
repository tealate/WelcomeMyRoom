execute if data storage space_editor:document job{state:"paused"} run data modify storage space_editor:document job.state set value "running"
tellraw @s {"text": "[Space Editor] Jobを再開しました。", "color": "green"}
