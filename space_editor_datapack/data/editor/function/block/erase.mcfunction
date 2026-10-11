execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
execute unless data storage editor:data selection.valid run return run tellraw @s {"text":"先にA/Bの2点を選択してください。","color":"red"}
function editor:internal/object/base
data merge storage editor:runtime {object:{type:"block_fill",mode:"fill",palette:"air",variant:"normal"}}
function editor:internal/object/commit
