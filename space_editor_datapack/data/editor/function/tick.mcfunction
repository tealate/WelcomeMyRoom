execute unless score #enabled se matches 1 run return 0
execute in minecraft:overworld as @e[tag=editor.object] unless score @s se.gen = #epoch se.gen run kill @s
execute in minecraft:the_nether as @e[tag=editor.object] unless score @s se.gen = #epoch se.gen run kill @s
execute in minecraft:the_end as @e[tag=editor.object] unless score @s se.gen = #epoch se.gen run kill @s
execute if data storage editor:runtime job run function editor:internal/job/tick
scoreboard players add #clock se 1
execute if score #clock se matches 20.. run function editor:internal/preview_sync
scoreboard players add @a se.cd 0
scoreboard players remove @a[scores={se.cd=1..}] se.cd 1
execute as @a[scores={se.use=1..},tag=editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{editor_wand:1b}] run function editor:internal/wand
scoreboard players set @a[scores={se.use=1..}] se.use 0
execute unless data storage editor:runtime job unless data storage editor:data {build_state:"error"} run function editor:internal/teleport/tick
