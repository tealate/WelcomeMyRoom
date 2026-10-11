tellraw @s {"text": "[Space Editor] SE_EXPORT_BEGIN", "color": "gray"}
tellraw @s [{text:"SE_META "},{nbt:"document.schema",storage:"editor:data"},{text:" "},{nbt:"revision",storage:"editor:data"}]
data modify storage editor:runtime export set from storage editor:data document.objects
execute if data storage editor:runtime export[0] run function editor:internal/export/next
tellraw @s {"text": "[Space Editor] SE_EXPORT_END", "color": "gray"}
tellraw @s {"text": "[Space Editor] 完全なJSON出力: ワールドを保存して閉じ、付属 editor_data.py export <ワールドフォルダ> を実行してください。", "color": "aqua"}
