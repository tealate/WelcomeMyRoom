$give @s minecraft:paper[minecraft:custom_data={space_editor:{kind:"template",templateId:$(id),version:$(version)}},minecraft:custom_name={text:"Template #$(id)",color:"green",italic:false},minecraft:lore=[{text:"参照アイテム / ブロック本体はTool Archive",color:"gray",italic:false}]]
tellraw @s {"text": "[Space Editor] Templateアイテムを発行しました。", "color": "green"}
data modify storage space_editor:document job.state set value "done"
