scoreboard objectives add se.v dummy
scoreboard objectives add se.use minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add se.cd dummy
scoreboard objectives add se.id dummy
scoreboard objectives add se.dim dummy
scoreboard players set #minus_one se.v -1
scoreboard players set #50 se.v 50
scoreboard players set #100 se.v 100
scoreboard players set #1000 se.v 1000
scoreboard players set #two se.v 2
scoreboard players set #ray_limit se.v 128
execute unless data storage space_editor:document schemaVersion run function space_editor:internal/init
execute unless data storage space_editor:document {schemaVersion:1} run return run tellraw @a {"text": "[Space Editor] 未対応の保存形式です。データは変更していません。", "color": "red"}
execute unless data storage space_editor:document settings.stepMilli run function space_editor:internal/migrate_step
execute unless data storage space_editor:document settings{boundsVersion:3} run function space_editor:internal/migrate_bounds
execute in minecraft:overworld run kill @e[tag=space_editor.preview]
execute in minecraft:the_nether run kill @e[tag=space_editor.preview]
execute in minecraft:the_end run kill @e[tag=space_editor.preview]
execute in minecraft:overworld run kill @e[tag=space_editor.selection_capture]
execute in minecraft:the_nether run kill @e[tag=space_editor.selection_capture]
execute in minecraft:the_end run kill @e[tag=space_editor.selection_capture]
execute if entity @a[tag=space_editor.editing] run function space_editor:preview/resync
execute unless data storage space_editor:document templates run data modify storage space_editor:document templates set value []
execute unless data storage space_editor:document nextTemplateId run data modify storage space_editor:document nextTemplateId set value 1
execute unless data storage space_editor:document nextActionId run data modify storage space_editor:document nextActionId set value 1
execute unless data storage space_editor:document archive run data modify storage space_editor:document archive set value {dimension:"minecraft:overworld",baseX:20000000,baseY:-63,baseZ:20000000,stride:64}
execute if data storage space_editor:document job{state:"running"} run tellraw @a {"text": "[Space Editor] 保存中のCopy/Paste Jobを再開します。", "color": "yellow"}
tellraw @a {"text": "[Space Editor] 第1段階を読み込みました。/function space_editor:start", "color": "aqua"}
tellraw @a {"text": "[Space Editor] 第2段階: Fill / Copy / Pasteを読み込みました。", "color": "aqua"}
