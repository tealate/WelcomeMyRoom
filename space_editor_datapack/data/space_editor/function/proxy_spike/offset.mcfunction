$data modify storage space_editor:proxy_spike input set value $(x)
execute store result score @s sp.x run data get storage space_editor:proxy_spike input 1000
execute if score @s sp.x matches ..-16001 run scoreboard players set @s sp.x -16000
execute if score @s sp.x matches 16001.. run scoreboard players set @s sp.x 16000
$data modify storage space_editor:proxy_spike input set value $(y)
execute store result score @s sp.y run data get storage space_editor:proxy_spike input 1000
execute if score @s sp.y matches ..-16001 run scoreboard players set @s sp.y -16000
execute if score @s sp.y matches 16001.. run scoreboard players set @s sp.y 16000
$data modify storage space_editor:proxy_spike input set value $(z)
execute store result score @s sp.z run data get storage space_editor:proxy_spike input 1000
execute if score @s sp.z matches ..-16001 run scoreboard players set @s sp.z -16000
execute if score @s sp.z matches 16001.. run scoreboard players set @s sp.z 16000
function space_editor:proxy_spike/select
function space_editor:proxy_spike/update_labels
