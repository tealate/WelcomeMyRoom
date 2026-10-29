$execute if data storage space_editor:document regionPairs[{id:$(pairId)}].spaceLinkGroupId run return run tellraw @s {"text": "[Space Editor] 移行済みSpaceLinkはRegionIDを指定してspace_group/deleteを使用してください。", "color": "red"}
$function space_editor:pair/load {pairId:$(pairId)}
execute unless data storage space_editor:runtime pair.id run return 0
function space_editor:pair/snapshot
function space_editor:pair/capture_attached with storage space_editor:runtime pair
data modify storage space_editor:runtime pairOperation set value "delete"
function space_editor:pair/action
function space_editor:pair/remove with storage space_editor:runtime pair
data remove storage space_editor:runtime hit
data modify storage space_editor:document selectedId set value ""
function space_editor:pair/cancel
function space_editor:preview/resync
function space_editor:link/clean_groups
function space_editor:link/validate_groups
