data modify storage space_editor:document job.state set value "error"
data modify storage space_editor:document job.error set value "state_block_item_unavailable"
tellraw @a {"text": "[Space Editor] BlockState変換用のブロックID取得に失敗しました。Jobを停止しました。", "color": "red"}
