execute if data storage space_editor:runtime pairSession unless data storage space_editor:runtime pairSession{kind:"teleport"} run function space_editor:pair/cancel
execute unless score @s se.pheld matches 1 run function space_editor:pair/begin_session
data modify storage space_editor:runtime pairSession.kind set value "teleport"
function space_editor:pair/read_intent
execute if data storage space_editor:runtime pairPending run function space_editor:pair/track
execute if data storage space_editor:runtime pairSession.selected run title @s actionbar [{text:"Pair編集: ",color:"aqua"},{nbt:"pairSession.kind",storage:"space_editor:runtime"},{text:" Region #"},{nbt:"pairSession.selected",storage:"space_editor:runtime"},{text:" Rot="},{score:{name:"@s",objective:"se.prot"}},{text:" FlipY="},{score:{name:"@s",objective:"se.pflip"}}]
