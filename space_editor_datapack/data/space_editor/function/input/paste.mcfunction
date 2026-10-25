scoreboard players set @s se.cd 5
execute if data storage space_editor:runtime pastePending if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run return run function space_editor:paste/cancel
execute if data storage space_editor:runtime pastePending run return run function space_editor:paste/confirm
execute if data storage space_editor:document job{state:"running"} run return run tellraw @s {"text": "[Space Editor] 別のCopy/Paste Jobが実行中です。", "color": "red"}
data remove storage space_editor:runtime pasteItem
data modify storage space_editor:runtime pasteItem set from entity @s equipment.offhand
execute unless data storage space_editor:runtime pasteItem.components."minecraft:custom_data".space_editor{kind:"template"} run return run tellraw @s {"text": "[Space Editor] オフハンドにTemplateアイテムを持ってください。", "color": "red"}
data modify storage space_editor:runtime lookup set value {id:0}
execute store result storage space_editor:runtime lookup.id int 1 run data get storage space_editor:runtime pasteItem.components."minecraft:custom_data".space_editor.templateId 1
execute store result storage space_editor:runtime lookup.owner0 int 1 run data get entity @s UUID[0] 1
execute store result storage space_editor:runtime lookup.owner1 int 1 run data get entity @s UUID[1] 1
execute store result storage space_editor:runtime lookup.owner2 int 1 run data get entity @s UUID[2] 1
execute store result storage space_editor:runtime lookup.owner3 int 1 run data get entity @s UUID[3] 1
data remove storage space_editor:runtime targetDimension
execute if dimension minecraft:overworld run data modify storage space_editor:runtime targetDimension set value "minecraft:overworld"
execute if dimension minecraft:the_nether run data modify storage space_editor:runtime targetDimension set value "minecraft:the_nether"
execute if dimension minecraft:the_end run data modify storage space_editor:runtime targetDimension set value "minecraft:the_end"
execute unless data storage space_editor:runtime targetDimension run return run tellraw @s {"text": "[Space Editor] このDimensionにはPasteできません。", "color": "red"}
scoreboard players set #paste_ray se.v 0
execute anchored eyes positioned ^ ^ ^ run function space_editor:paste/ray
