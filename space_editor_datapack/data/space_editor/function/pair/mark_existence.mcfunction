execute if data storage space_editor:runtime hit.pairId run return 0
data modify storage space_editor:runtime hit.kind set value "proxy_existence"
data modify storage space_editor:runtime frame set from storage space_editor:runtime hit
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] Proxy存在範囲の各辺は0.1〜128ブロックにしてください。", "color": "red"}
execute unless data storage space_editor:runtime hit.roomId run data modify storage space_editor:runtime hit.roomId set value ""
function space_editor:region/store_hit with storage space_editor:runtime hit
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] 単独のProxy存在範囲として登録しました。", "color": "green"}
