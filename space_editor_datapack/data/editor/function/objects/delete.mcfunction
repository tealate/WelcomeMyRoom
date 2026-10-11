execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
$execute unless data storage editor:data document.objects[{id:$(id)}] run return run tellraw @s {text:"IDが見つかりません。",color:"red"}
function editor:internal/history/save
$data remove storage editor:data document.objects[{id:$(id)}]
function editor:internal/revision
function editor:build
