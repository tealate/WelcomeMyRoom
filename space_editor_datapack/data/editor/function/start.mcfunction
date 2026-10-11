execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
execute unless entity @s[type=minecraft:player] run return 0
tag @a remove editor.editing
tag @s add editor.editing
execute unless items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{editor_wand:1b}] run give @s minecraft:carrot_on_a_stick[minecraft:custom_data={editor_wand:1b},minecraft:custom_name={text:"Space Editor — 選択棒",color:"aqua",italic:false},minecraft:lore=[{text:"右クリック: A / しゃがみ+右クリック: B",italic:false},{text:"/function editor:menu で配置メニュー",italic:false}]]
function editor:preview/show
tellraw @s {"text": "[Space Editor] 右クリック=A、しゃがみ+右クリック=B。選択後は /function editor:menu。編集者はTP判定から除外されます。", "color": "aqua"}
