execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
data remove storage editor:data selection
function editor:internal/selection/kill
tellraw @s {"text": "[Space Editor] Selectionを解除しました。", "color": "aqua"}
