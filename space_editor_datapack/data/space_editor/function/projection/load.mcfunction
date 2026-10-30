scoreboard objectives add pr.owner dummy
scoreboard objectives add pr.id dummy
scoreboard objectives add pr.epoch dummy
scoreboard objectives add pr.debug dummy
scoreboard objectives add pr.gc dummy
scoreboard objectives add pr.v dummy
scoreboard objectives add pr.leave minecraft.custom:minecraft.leave_game
scoreboard players add #owner pr.owner 0
scoreboard players add #epoch pr.epoch 1
team add pr_hidden
team modify pr_hidden nametagVisibility never
team modify pr_hidden collisionRule never
execute unless data storage space_editor:document projection run data modify storage space_editor:document projection set value {enabled:0b,debugMaps:[],visual:{standing:1900,crouching:1600,swimming:700,fall_flying:700,sleeping:300},labelGap:300}
execute unless data storage space_editor:projection active run data modify storage space_editor:projection active set value []
execute unless data storage space_editor:projection players run data modify storage space_editor:projection players set value []
execute unless data storage space_editor:projection nextId run data modify storage space_editor:projection nextId set value 1
data modify storage space_editor:projection schema set value 1
execute in minecraft:overworld run kill @e[type=minecraft:mannequin,tag=space_editor.proxy]
execute in minecraft:overworld run kill @e[type=minecraft:text_display,tag=space_editor.proxy]
execute in minecraft:the_nether run kill @e[type=minecraft:mannequin,tag=space_editor.proxy]
execute in minecraft:the_nether run kill @e[type=minecraft:text_display,tag=space_editor.proxy]
execute in minecraft:the_end run kill @e[type=minecraft:mannequin,tag=space_editor.proxy]
execute in minecraft:the_end run kill @e[type=minecraft:text_display,tag=space_editor.proxy]
