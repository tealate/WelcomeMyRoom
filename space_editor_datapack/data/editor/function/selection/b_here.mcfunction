execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
data modify storage editor:runtime point set value "b"
execute align xyz run function editor:internal/capture
