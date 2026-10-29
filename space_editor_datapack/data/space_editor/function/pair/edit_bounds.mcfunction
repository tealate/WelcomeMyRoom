function space_editor:pair/load with storage space_editor:runtime hit
execute unless data storage space_editor:runtime editA.id run return 0
execute unless data storage space_editor:runtime editB.id run return 0
function space_editor:pair/snapshot
data modify storage space_editor:runtime pairOperation set from storage space_editor:runtime activeTool
data modify storage space_editor:runtime old set from storage space_editor:runtime editA
data modify storage space_editor:runtime partner set from storage space_editor:runtime editB
execute if data storage space_editor:runtime hit{side:"B"} run data modify storage space_editor:runtime old set from storage space_editor:runtime editB
execute if data storage space_editor:runtime hit{side:"B"} run data modify storage space_editor:runtime partner set from storage space_editor:runtime editA
execute unless data storage space_editor:runtime {activeTool:"move"} run function space_editor:pair/sync_bounds
data modify storage space_editor:runtime frame set from storage space_editor:runtime partner
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] 相手側の制限により、両方の変更を取り消しました。", "color": "red"}
data modify storage space_editor:runtime partner set from storage space_editor:runtime frame
data modify storage space_editor:runtime frame set from storage space_editor:runtime hit
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run return 0
data modify storage space_editor:runtime hit set from storage space_editor:runtime frame
data modify storage space_editor:runtime pair.localSize set from storage space_editor:runtime frame.localSize
data modify storage space_editor:runtime editA set from storage space_editor:runtime hit
data modify storage space_editor:runtime editB set from storage space_editor:runtime partner
execute if data storage space_editor:runtime hit{side:"B"} run data modify storage space_editor:runtime editB set from storage space_editor:runtime hit
execute if data storage space_editor:runtime hit{side:"B"} run data modify storage space_editor:runtime editA set from storage space_editor:runtime partner
function space_editor:pair/commit
