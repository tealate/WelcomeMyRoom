execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
$execute unless data storage editor:data document.objects[{id:$(id)}] run return 0
$data modify storage editor:runtime selected_object set from storage editor:data document.objects[{id:$(id)}]
data modify storage editor:data selection set value {}
data modify storage editor:data selection.dim set from storage editor:runtime selected_object.dim
data modify storage editor:data selection.ax set from storage editor:runtime selected_object.ax
data modify storage editor:data selection.ay set from storage editor:runtime selected_object.ay
data modify storage editor:data selection.az set from storage editor:runtime selected_object.az
data modify storage editor:data selection.bx set from storage editor:runtime selected_object.bx
data modify storage editor:data selection.by set from storage editor:runtime selected_object.by
data modify storage editor:data selection.bz set from storage editor:runtime selected_object.bz
function editor:settings/zero
execute if data storage editor:runtime selected_object.palette run data modify storage editor:data prefs.palette set from storage editor:runtime selected_object.palette
execute if data storage editor:runtime selected_object.variant run data modify storage editor:data prefs.variant set from storage editor:runtime selected_object.variant
execute if data storage editor:runtime selected_object.ox run data modify storage editor:data prefs.ox set from storage editor:runtime selected_object.ox
execute if data storage editor:runtime selected_object.oy run data modify storage editor:data prefs.oy set from storage editor:runtime selected_object.oy
execute if data storage editor:runtime selected_object.oz run data modify storage editor:data prefs.oz set from storage editor:runtime selected_object.oz
execute if data storage editor:runtime selected_object.ex run data modify storage editor:data prefs.ex set from storage editor:runtime selected_object.ex
execute if data storage editor:runtime selected_object.ey run data modify storage editor:data prefs.ey set from storage editor:runtime selected_object.ey
execute if data storage editor:runtime selected_object.ez run data modify storage editor:data prefs.ez set from storage editor:runtime selected_object.ez
function editor:internal/selection/normalize
