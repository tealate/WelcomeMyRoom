data modify storage space_editor:document job.phase set value "place"
data modify storage space_editor:document job.cursor set value 0
execute store result score #unsupported se.v run data get storage space_editor:document job.unsupportedBlocks 1
execute if score #unsupported se.v matches 1.. run tellraw @a [{"text":"[Space Editor] 警告: 未対応ブロック ","color":"yellow"},{"score":{"name":"#unsupported","objective":"se.v"}},{"text":" 個は変更せずスキップします。残りの配置を続行します。"}]
tellraw @a {"text": "[Space Editor] 変換Pasteの事前走査が完了しました。配置を開始します。", "color": "green"}
