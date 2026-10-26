data modify storage space_editor:document job.state set value "error"
data modify storage space_editor:document job.error set value "block_state_apply_failed"
tellraw @a {"text": "[Space Editor] BlockState補正に失敗しました。Jobを停止しました。", "color": "red"}
