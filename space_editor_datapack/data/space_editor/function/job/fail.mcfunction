data modify storage space_editor:document job.state set value "error"
data modify storage space_editor:document job.error set value "clone_failed_or_chunk_unloaded"
tellraw @a {"text": "[Space Editor] Clone区画に失敗したためJobを停止しました。/function space_editor:job/retry", "color": "red"}
