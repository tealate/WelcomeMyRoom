execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {"text": "[Space Editor] 別プレイヤーが編集中です。終了後に開始してください。", "color": "red"}
execute if data storage space_editor:runtime pairPending{kind:"space_link"} run return run function space_editor:space_group/confirm
execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {"text": "[Space Editor] 別プレイヤーが編集中です。終了後に開始してください。", "color": "red"}
function space_editor:pair/create with storage space_editor:runtime pairPending
