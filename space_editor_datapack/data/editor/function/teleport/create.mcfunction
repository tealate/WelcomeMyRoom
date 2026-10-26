execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
execute unless data storage editor:data selection.valid run return run tellraw @s {"text":"先にA/Bの2点を選択してください。","color":"red"}
function editor:internal/object/base
data modify storage editor:runtime object.type set value "teleport_volume"
function editor:internal/object/transform
execute unless score #transform_ok se matches 1 run return 0
function editor:internal/object/commit
