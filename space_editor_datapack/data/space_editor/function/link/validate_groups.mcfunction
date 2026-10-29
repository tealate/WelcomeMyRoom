function space_editor:space_group/migrate
data modify storage space_editor:runtime linkWarnings set value []
data modify storage space_editor:runtime validationPairs set from storage space_editor:document regionPairs
execute if data storage space_editor:runtime validationPairs[0] run function space_editor:link/validate_next
execute if data storage space_editor:runtime linkWarnings[0] run tellraw @s {"text": "[Space Editor] TP / SpaceLinkの範囲または変換に不整合があります。/function space_editor:link/status で確認してください。", "color": "yellow"}
