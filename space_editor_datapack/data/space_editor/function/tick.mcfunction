function space_editor:space_group/session_tick
scoreboard players add @a se.cd 0
scoreboard players remove @a[scores={se.cd=1..}] se.cd 1
execute as @a[scores={se.pheld=1}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"teleport"}}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"space_link"}}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"proxy_existence"}}] run function space_editor:pair/cancel
scoreboard players set #selection_cursor_active se.v 0
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"region"}}] run function space_editor:selection/track
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"region"}}] run function space_editor:input/region
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"resize_all"}}] run function space_editor:input/resize_all
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"resize_face"}}] run function space_editor:input/resize_face
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"move"}}] run function space_editor:input/move
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"delete"}}] run function space_editor:input/delete
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"region_visibility"}}] run function space_editor:input/region_visibility
scoreboard players add @a se.ph 0
scoreboard players add @a se.rot 0
scoreboard players add @a se.flip 0
scoreboard players add @a se.intent 0
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste"}}] run function space_editor:paste_mode/held_tick
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste_masked"}}] run function space_editor:paste_mode/held_tick
execute as @a[scores={se.ph=1..}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste"}}] unless items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste_masked"}}] run scoreboard players set @s se.ph 0
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste"}}] unless data storage space_editor:runtime pastePending run function space_editor:selection/track
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste_masked"}}] unless data storage space_editor:runtime pastePending run function space_editor:selection/track
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"fill"}}] run function space_editor:selection/track
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"copy"}}] run function space_editor:input/copy
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste"}}] run function space_editor:input/paste
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"paste_masked"}}] run function space_editor:input/paste
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"fill"}}] run function space_editor:input/fill
execute if data storage space_editor:document job{state:"running"} run function space_editor:job/tick
execute if data storage space_editor:document job{state:"awaiting_item"} run function space_editor:copy/try_issue
execute if data storage space_editor:document job{state:"complete"} run function space_editor:job/notify_complete
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"mask"}}] run function space_editor:input/mask
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"teleport"}}] run function space_editor:pair/held_teleport
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"teleport"}}] run function space_editor:pair/click
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"space_link"}}] run function space_editor:pair/held_space_link
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"space_link"}}] run function space_editor:pair/click
execute as @a[tag=space_editor.editing] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"proxy_existence"}}] run function space_editor:pair/held_proxy_existence
execute as @a[tag=space_editor.editing,scores={se.use=1..,se.cd=0}] at @s if items entity @s weapon.mainhand minecraft:carrot_on_a_stick[minecraft:custom_data~{space_editor:{tool:"proxy_existence"}}] run function space_editor:pair/click
scoreboard players set @a[scores={se.use=1..}] se.use 0
execute unless score #selection_cursor_active se.v matches 1 run function space_editor:preview/remove_selection_candidate
execute as @a[tag=space_editor.editing] at @s run function space_editor:internal/dimension_tick
function space_editor:teleport/tick
function space_editor:proxy_spike/tick
