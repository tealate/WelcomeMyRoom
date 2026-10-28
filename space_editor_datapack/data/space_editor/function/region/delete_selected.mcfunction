execute if data storage space_editor:runtime hit.pairId run return run function space_editor:pair/delete with storage space_editor:runtime hit
execute unless data storage space_editor:runtime hit.id run return run tellraw @s {"text": "[Space Editor] 先にサイズ変更棒でRegionを選択してください。", "color": "red"}
function space_editor:region/delete_hit with storage space_editor:runtime hit
data modify storage space_editor:document selectedId set value ""
data remove storage space_editor:runtime hit
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] 選択Regionを削除しました。", "color": "yellow"}
