scoreboard players set @s se.cd 5
data modify storage space_editor:runtime activeTool set value "fill"
data remove storage space_editor:runtime hit
execute unless data storage space_editor:runtime hover.pos run return run tellraw @s {"text": "[Space Editor] 選択予定位置を取得できません。", "color": "red"}
function space_editor:region/from_hover
