execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
$data modify storage editor:data selection set value {ax:$(ax),ay:$(ay),az:$(az),bx:$(bx),by:$(by),bz:$(bz),dim:"$(dimension)"}
function editor:internal/selection/normalize
