scoreboard objectives add sp.owner dummy
scoreboard objectives add sp.follow dummy
scoreboard objectives add sp.flip dummy
scoreboard objectives add sp.name dummy
scoreboard objectives add sp.epoch dummy
scoreboard objectives add sp.seen dummy
scoreboard objectives add sp.x dummy
scoreboard objectives add sp.y dummy
scoreboard objectives add sp.z dummy
scoreboard objectives add sp.fy dummy
scoreboard objectives add sp.normal dummy
scoreboard objectives add sp.inverted dummy
scoreboard objectives add sp.demo dummy
scoreboard objectives add sp.v dummy
scoreboard objectives add sp.leave minecraft.custom:minecraft.leave_game
scoreboard players add #next sp.owner 0
scoreboard players add #epoch sp.epoch 1
team add sp_hidden
team modify sp_hidden nametagVisibility never
team modify sp_hidden collisionRule never
team add sp_body
team modify sp_body nametagVisibility always
team modify sp_body collisionRule never
function space_editor:proxy_spike/clear_all
data modify storage space_editor:proxy_spike note set value "Transient Stage06-1 scratch; document untouched"
