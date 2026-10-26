execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
execute unless data storage editor:data selection.valid run return run tellraw @s {"text":"先にA/Bの2点を選択してください。","color":"red"}
function editor:internal/object/base
data modify storage editor:runtime object.type set value "block_fill"
data modify storage editor:runtime object.mode set value "fill"
data modify storage editor:runtime object.palette set from storage editor:data prefs.palette
data modify storage editor:runtime object.variant set from storage editor:data prefs.variant
function editor:internal/object/commit
