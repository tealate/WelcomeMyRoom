execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {"text": "[Space Editor] 別プレイヤーが編集中です。終了後に開始してください。", "color": "red"}
execute if data storage space_editor:runtime pairSession{kind:"space_link"} run return run function space_editor:space_group/select
execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {"text": "[Space Editor] 別プレイヤーが編集中です。終了後に開始してください。", "color": "red"}
data modify storage space_editor:document selectedId set from storage space_editor:runtime hit.idText
execute if data storage space_editor:runtime pairSession{kind:"proxy_existence"} run return run function space_editor:pair/mark_existence
data modify storage space_editor:runtime pairSession.selected set from storage space_editor:runtime hit.id
data modify storage space_editor:runtime frame set from storage space_editor:runtime hit
function space_editor:pair/frame
execute store result score @s se.prot run data get storage space_editor:runtime frame.rotationY 1
execute store result score @s se.pflip run data get storage space_editor:runtime frame.flipY 1
execute if data storage space_editor:runtime hit.pairId run return run tellraw @s {"text": "[Space Editor] 選択しました。Shift+右クリックで回転・反転できます。", "color": "aqua"}
data modify storage space_editor:runtime pairPending set value {}
data modify storage space_editor:runtime pairPending.source set from storage space_editor:runtime hit.id
data modify storage space_editor:runtime pairPending.kind set from storage space_editor:runtime pairSession.kind
data modify storage space_editor:runtime pairPending.frame set from storage space_editor:runtime frame
function space_editor:pair/track
