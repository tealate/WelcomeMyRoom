execute unless data storage space_editor:runtime selection{kind:"search_area"} run data remove storage space_editor:runtime selection
data modify storage space_editor:runtime selectionKind set value "search_area"
scoreboard players set @s se.cd 5
execute unless data storage space_editor:runtime hover.pos run return run tellraw @s {"text": "[Space Editor] 選択予定位置を取得できません。", "color": "red"}
function space_editor:selection/capture
