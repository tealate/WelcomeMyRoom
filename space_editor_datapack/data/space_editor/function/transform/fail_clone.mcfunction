data modify storage space_editor:document job.state set value "error"
data modify storage space_editor:document job.error set value "single_block_clone_failed"
tellraw @a {"text": "[Space Editor] 1ブロックCloneに失敗しました。Jobを停止しました。", "color": "red"}
