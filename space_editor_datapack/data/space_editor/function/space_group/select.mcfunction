execute if data storage space_editor:runtime hit.pairId run return run tellraw @s {"text": "[Space Editor] 旧ペアを先に/reloadで移行してください。", "color": "red"}
data modify storage space_editor:document selectedId set from storage space_editor:runtime hit.idText
data modify storage space_editor:runtime pairSession.selected set from storage space_editor:runtime hit.id
data modify storage space_editor:runtime pairSession.mode set value "add"
data modify storage space_editor:runtime pairSession.groupId set value 0
execute if data storage space_editor:runtime hit.spaceLinkGroupId run data modify storage space_editor:runtime pairSession.groupId set from storage space_editor:runtime hit.spaceLinkGroupId
data modify storage space_editor:runtime frame set from storage space_editor:runtime hit
function space_editor:pair/frame
execute store result score @s se.prot run data get storage space_editor:runtime frame.rotationY
execute store result score @s se.pflip run data get storage space_editor:runtime frame.flipY
execute if data storage space_editor:runtime hit.spaceLinkGroupId if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run return run function space_editor:space_group/select_pose
function space_editor:space_group/start_add
