$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]
execute unless data storage space_editor:runtime template.id run return run tellraw @s {"text": "[Space Editor] TemplateIDがDocumentにありません。", "color": "red"}
data modify storage space_editor:runtime pastePending set value {id:0,version:1,targetDimension:"",x:0,y:0,z:0,w:0,h:0,d:0,sx:0,sy:0,sz:0,rotation:0,flipY:0b,owner0:0,owner1:0,owner2:0,owner3:0}
data modify storage space_editor:runtime pastePending.masked set value 0b
execute if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste_masked"}}] run data modify storage space_editor:runtime pastePending.masked set value 1b
data modify storage space_editor:runtime pastePending.id set from storage space_editor:runtime template.id
data modify storage space_editor:runtime pastePending.version set from storage space_editor:runtime template.version
data modify storage space_editor:runtime pastePending.targetDimension set from storage space_editor:runtime targetDimension
execute store result storage space_editor:runtime pastePending.x int 1 run data get storage space_editor:runtime targetPos[0] 1
execute store result storage space_editor:runtime pastePending.y int 1 run data get storage space_editor:runtime targetPos[1] 1
execute store result storage space_editor:runtime pastePending.z int 1 run data get storage space_editor:runtime targetPos[2] 1
data modify storage space_editor:runtime pastePending.w set from storage space_editor:runtime template.size[0]
data modify storage space_editor:runtime pastePending.h set from storage space_editor:runtime template.size[1]
data modify storage space_editor:runtime pastePending.d set from storage space_editor:runtime template.size[2]
data modify storage space_editor:runtime pastePending.owner0 set from storage space_editor:runtime lookup.owner0
data modify storage space_editor:runtime pastePending.owner1 set from storage space_editor:runtime lookup.owner1
data modify storage space_editor:runtime pastePending.owner2 set from storage space_editor:runtime lookup.owner2
data modify storage space_editor:runtime pastePending.owner3 set from storage space_editor:runtime lookup.owner3
function space_editor:paste/update_pending_transform
tellraw @s {"text": "[Space Editor] Paste範囲を表示しました。通常右クリックで確定、Shift＋右クリックで変換。", "color": "yellow"}
