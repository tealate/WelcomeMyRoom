execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
$execute unless data storage editor:data document.objects[{id:$(id)}] run return 0
function editor:internal/history/save
$data modify storage editor:data document.objects[{id:$(id)}].label set value "$(label)"
function editor:internal/revision
tellraw @s {"text": "[Space Editor] 名前を変更しました。", "color": "aqua"}
