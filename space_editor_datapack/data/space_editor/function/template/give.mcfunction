$give @s minecraft:paper[minecraft:custom_data={space_editor:{kind:"template",templateId:$(id),version:$(version)}},minecraft:custom_name={text:"Template #$(id)",color:"green",italic:false},minecraft:lore=[{text:"再発行された参照アイテム",color:"gray",italic:false}]]
tellraw @s {"text": "[Space Editor] Templateアイテムを再発行しました。", "color": "green"}
