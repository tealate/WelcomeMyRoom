scoreboard players set @s se.cd 5
execute unless data storage space_editor:runtime hover.pos run return run tellraw @s {"text": "[Space Editor] 選択予定位置を取得できません。", "color": "red"}
function space_editor:selection/capture
