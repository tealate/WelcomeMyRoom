scoreboard players set #pair_ok se.v 0
data remove storage space_editor:runtime hit
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(id)}]
execute unless data storage space_editor:runtime hit.pairId run return 0
function space_editor:pair/load with storage space_editor:runtime hit
function space_editor:pair/snapshot
execute unless data storage space_editor:runtime editA.id run return 0
execute unless data storage space_editor:runtime editB.id run return 0
data modify storage space_editor:runtime frame set from storage space_editor:runtime hit
$data modify storage space_editor:runtime frame.rotationY set value $(rotationY)
$data modify storage space_editor:runtime frame.flipY set value $(flipY)b
execute unless data storage space_editor:runtime frame{rotationY:0} unless data storage space_editor:runtime frame{rotationY:90} unless data storage space_editor:runtime frame{rotationY:180} unless data storage space_editor:runtime frame{rotationY:270} run return 0
execute unless data storage space_editor:runtime frame{flipY:0b} unless data storage space_editor:runtime frame{flipY:1b} run return 0
function space_editor:pair/pose_bounds
execute unless score #frame_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] 中心を保った回転を保存できる範囲ではありません。", "color": "red"}
execute if data storage space_editor:runtime frame{side:"A"} run data modify storage space_editor:runtime editA set from storage space_editor:runtime frame
execute if data storage space_editor:runtime frame{side:"B"} run data modify storage space_editor:runtime editB set from storage space_editor:runtime frame
data modify storage space_editor:runtime pairOperation set value "pose"
function space_editor:pair/commit
