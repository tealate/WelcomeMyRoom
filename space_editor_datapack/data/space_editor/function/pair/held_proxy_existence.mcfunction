function space_editor:space_group/check_owner
execute if data storage space_editor:runtime pairSession.owner unless score #session_owner se.v matches 1 run return 0
execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {"text": "[Space Editor] 別プレイヤーが編集中です。終了後に開始してください。", "color": "red"}
execute if data storage space_editor:runtime pairSession unless data storage space_editor:runtime pairSession{kind:"proxy_existence"} run function space_editor:pair/cancel
execute unless score @s se.pheld matches 1 run function space_editor:pair/begin_session
data modify storage space_editor:runtime pairSession.kind set value "proxy_existence"
function space_editor:pair/read_intent
execute if data storage space_editor:runtime pairPending run function space_editor:pair/track
execute if data storage space_editor:runtime pairSession.selected run title @s actionbar [{text:"Pair編集: ",color:"aqua"},{nbt:"pairSession.kind",storage:"space_editor:runtime"},{text:" Region #"},{nbt:"pairSession.selected",storage:"space_editor:runtime"},{text:" Rot="},{score:{name:"@s",objective:"se.prot"}},{text:" FlipY="},{score:{name:"@s",objective:"se.pflip"}}]
