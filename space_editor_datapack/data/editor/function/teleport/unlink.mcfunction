execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
function editor:internal/history/save
$data remove storage editor:data document.objects[{id:$(id)}].target
function editor:internal/revision
