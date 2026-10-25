scoreboard players add @a se.cd 0
scoreboard players remove @a[scores={se.cd=1..}] se.cd 1
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"region"}}] run function space_editor:input/region
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"resize_all"}}] run function space_editor:input/resize_all
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"resize_face"}}] run function space_editor:input/resize_face
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"delete"}}] run function space_editor:input/delete
scoreboard players set @a[scores={se.use=1..}] se.use 0
execute as @a[tag=space_editor.editing] at @s run function space_editor:internal/dimension_tick
