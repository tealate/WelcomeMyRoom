function editor:internal/job/release
data modify storage editor:runtime job.phase set value "error"
data modify storage editor:data build_state set value "error"
tellraw @a[tag=editor.editing] {"text": "[Space Editor] チャンク読み込み待ちがタイムアウト。データは保存済みです。status→再開で再構築します。", "color": "red"}
