scoreboard objectives add sp.owner dummy
scoreboard objectives add sp.follow dummy
scoreboard objectives add sp.flip dummy
scoreboard objectives add sp.name dummy
scoreboard players add #next sp.owner 0
team add sp_hidden
team modify sp_hidden nametagVisibility never
team modify sp_hidden collisionRule never
team add sp_body
team modify sp_body collisionRule never
execute in minecraft:overworld run kill @e[tag=space_editor.proxy_spike]
execute in minecraft:the_nether run kill @e[tag=space_editor.proxy_spike]
execute in minecraft:the_end run kill @e[tag=space_editor.proxy_spike]
scoreboard players set @a sp.follow 0
