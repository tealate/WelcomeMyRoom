execute if data storage space_editor:document job{state:"running"} run data modify storage space_editor:document job.state set value "paused"
tellraw @s {"text": "[Space Editor] Jobを一時停止しました。", "color": "yellow"}
