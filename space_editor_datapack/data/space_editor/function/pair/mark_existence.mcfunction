execute if data storage space_editor:runtime hit.pairId run return 0
data modify storage space_editor:runtime hit.kind set value "proxy_existence"
execute unless data storage space_editor:runtime hit.roomId run data modify storage space_editor:runtime hit.roomId set value ""
function space_editor:region/store_hit with storage space_editor:runtime hit
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] 単独のProxy存在範囲として登録しました。", "color": "green"}
