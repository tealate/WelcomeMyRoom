execute unless data storage space_editor:runtime hit.id run return run tellraw @s {"text": "[Space Editor] 先にRegionを選択してください。", "color": "red"}
execute unless data storage space_editor:runtime fillBlock run return run tellraw @s {"text": "[Space Editor] Fill棒ではオフハンドに素材ブロックを持ってください。", "color": "red"}
execute store result score #aligned se.v run function space_editor:operation/check_aligned
execute unless score #aligned se.v matches 1 run return run tellraw @s {"text": "[Space Editor] Fillはブロック境界に揃ったRegionだけ使用できます。", "color": "red"}
data modify storage space_editor:runtime fill set from storage space_editor:runtime hit
data modify storage space_editor:runtime fill.block set from storage space_editor:runtime fillBlock
execute store result storage space_editor:runtime fill.x1 int 1 run scoreboard players get #x1 se.v
execute store result storage space_editor:runtime fill.y1 int 1 run scoreboard players get #y1 se.v
execute store result storage space_editor:runtime fill.z1 int 1 run scoreboard players get #z1 se.v
scoreboard players remove #x2 se.v 1
scoreboard players remove #y2 se.v 1
scoreboard players remove #z2 se.v 1
execute store result storage space_editor:runtime fill.x2 int 1 run scoreboard players get #x2 se.v
execute store result storage space_editor:runtime fill.y2 int 1 run scoreboard players get #y2 se.v
execute store result storage space_editor:runtime fill.z2 int 1 run scoreboard players get #z2 se.v
execute store success score #op_ok se.v run function space_editor:fill/run with storage space_editor:runtime fill
execute unless score #op_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] Fillに失敗しました。手持ちが設置可能なブロックか、範囲が読み込まれているか確認してください。", "color": "red"}
data modify storage space_editor:runtime hit.role set value "fill"
function space_editor:region/delete_hit with storage space_editor:runtime hit
data modify storage space_editor:document selectedId set value ""
data remove storage space_editor:runtime hit
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] Fill完了。Fill専用RegionをDocumentと表示から削除しました。", "color": "green"}
