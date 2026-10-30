execute if entity @a[tag=space_editor.editing] unless entity @s[tag=space_editor.editing] run return run tellraw @s {text:"別プレイヤーの編集終了後に実行してください",color:"red"}
execute unless data storage space_editor:document projection.demo run return 0
data modify storage space_editor:projection demoDelete set from storage space_editor:document projection.demo.ids
function space_editor:projection/demo/delete_scan
data remove storage space_editor:document projection.demo
function space_editor:projection/maintenance
