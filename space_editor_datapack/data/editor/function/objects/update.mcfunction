execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
execute unless data storage editor:data selection.valid run return run tellraw @s {"text":"先にA/Bの2点を選択してください。","color":"red"}
$execute unless data storage editor:data document.objects[{id:$(id)}] run return 0
$data modify storage editor:runtime previous set from storage editor:data document.objects[{id:$(id)}]
function editor:internal/object/base
data modify storage editor:runtime object.id set from storage editor:runtime previous.id
data modify storage editor:runtime object.type set from storage editor:runtime previous.type
data modify storage editor:runtime object.label set from storage editor:runtime previous.label
execute if data storage editor:runtime previous.target run data modify storage editor:runtime object.target set from storage editor:runtime previous.target
execute if data storage editor:runtime previous{type:"block_fill"} run function editor:internal/object/update_block
execute unless data storage editor:runtime previous{type:"block_fill"} run function editor:internal/object/transform
execute unless data storage editor:runtime previous{type:"block_fill"} unless score #transform_ok se matches 1 run return 0
execute if data storage editor:runtime previous{type:"mask"} run data modify storage editor:runtime object.material set value "mask_default"
function editor:internal/history/save
$data modify storage editor:data document.objects[{id:$(id)}] set from storage editor:runtime object
function editor:internal/revision
function editor:build
