execute unless entity @s[type=minecraft:player] run return 0
function space_editor:proxy_spike/delete_selected
scoreboard players set @s sp.follow 0
scoreboard players set @s sp.owner 0
tag @s remove sp.active
