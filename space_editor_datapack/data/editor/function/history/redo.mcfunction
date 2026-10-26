execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
execute unless data storage editor:data history.future[-1] run return run tellraw @s {text:"対象の履歴がありません。",color:"yellow"}
data modify storage editor:data history.past append value {}
data modify storage editor:data history.past[-1].objects set from storage editor:data document.objects
data modify storage editor:data document.objects set from storage editor:data history.future[-1].objects
data remove storage editor:data history.future[-1]
function editor:internal/revision
function editor:build
