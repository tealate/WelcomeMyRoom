scoreboard players add @a se.cd 0
scoreboard players remove @a[scores={se.cd=1..}] se.cd 1
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"region"}}] run function space_editor:input/region
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"resize_all"}}] run function space_editor:input/resize_all
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"resize_face"}}] run function space_editor:input/resize_face
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"delete"}}] run function space_editor:input/delete
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"copy"}}] run function space_editor:input/copy
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste"}}] run function space_editor:input/paste
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"fill"}}] run function space_editor:input/fill
execute if data storage space_editor:document job{state:"running"} run function space_editor:job/tick
execute if data storage space_editor:document job{state:"awaiting_item"} run function space_editor:copy/try_issue
execute if data storage space_editor:document job{state:"complete"} run function space_editor:job/notify_complete
scoreboard players set @a[scores={se.use=1..}] se.use 0
execute as @a[tag=space_editor.editing] at @s run function space_editor:internal/dimension_tick
