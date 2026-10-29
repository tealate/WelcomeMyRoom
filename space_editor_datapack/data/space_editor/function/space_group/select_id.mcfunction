execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {"text": "[Space Editor] 別プレイヤーが編集中です。終了後に開始してください。", "color": "red"}
execute unless entity @s[tag=space_editor.editing] run return 0
$execute unless data storage space_editor:document regions[{id:$(id)}] run return 0
$execute if data storage space_editor:document regions[{id:$(id)}].kind unless data storage space_editor:document regions[{id:$(id),kind:"space_link"}] run return 0
function space_editor:pair/cancel
function space_editor:pair/held_space_link
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(id)}]
function space_editor:space_group/select
