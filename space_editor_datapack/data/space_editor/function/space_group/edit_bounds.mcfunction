scoreboard players set #pair_ok se.v 0
function space_editor:space_group/load with storage space_editor:runtime hit
execute unless score #sg_ok se.v matches 1 run return 0
function space_editor:space_group/read_old with storage space_editor:runtime hit
data modify storage space_editor:runtime frame set from storage space_editor:runtime hit
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run return 0
data modify storage space_editor:runtime hit set from storage space_editor:runtime frame
data modify storage space_editor:runtime sg.group.localSize set from storage space_editor:runtime hit.localSize
data modify storage space_editor:runtime sg.operation set from storage space_editor:runtime activeTool
data modify storage space_editor:runtime sg.queue set from storage space_editor:runtime sg.before.regions
function space_editor:space_group/edit_scan
execute unless score #sg_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] メンバーの制限によりグループ全体の変更を取り消しました。", "color": "red"}
function space_editor:space_group/commit
