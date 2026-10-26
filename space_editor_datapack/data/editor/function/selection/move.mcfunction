execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
execute unless data storage editor:data selection.valid run return run tellraw @s {"text":"先にA/Bの2点を選択してください。","color":"red"}
$data modify storage editor:runtime delta set value {x:$(x),y:$(y),z:$(z)}
execute store result score #dx se run data get storage editor:runtime delta.x 1
execute store result score #dy se run data get storage editor:runtime delta.y 1
execute store result score #dz se run data get storage editor:runtime delta.z 1
execute unless score #dx se matches -32..32 run return 0
execute unless score #dy se matches -32..32 run return 0
execute unless score #dz se matches -32..32 run return 0
execute store result score #coord se run data get storage editor:data selection.ax
scoreboard players operation #coord se += #dx se
execute store result storage editor:data selection.ax int 1 run scoreboard players get #coord se
execute store result score #coord se run data get storage editor:data selection.ay
scoreboard players operation #coord se += #dy se
execute store result storage editor:data selection.ay int 1 run scoreboard players get #coord se
execute store result score #coord se run data get storage editor:data selection.az
scoreboard players operation #coord se += #dz se
execute store result storage editor:data selection.az int 1 run scoreboard players get #coord se
execute store result score #coord se run data get storage editor:data selection.bx
scoreboard players operation #coord se += #dx se
execute store result storage editor:data selection.bx int 1 run scoreboard players get #coord se
execute store result score #coord se run data get storage editor:data selection.by
scoreboard players operation #coord se += #dy se
execute store result storage editor:data selection.by int 1 run scoreboard players get #coord se
execute store result score #coord se run data get storage editor:data selection.bz
scoreboard players operation #coord se += #dz se
execute store result storage editor:data selection.bz int 1 run scoreboard players get #coord se
function editor:internal/selection/normalize
