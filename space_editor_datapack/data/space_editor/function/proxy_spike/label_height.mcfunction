$data modify storage space_editor:proxy_spike input set value $(normal)
execute store result score @s sp.normal run data get storage space_editor:proxy_spike input 1000
execute if score @s sp.normal matches ..-16001 run scoreboard players set @s sp.normal -16000
execute if score @s sp.normal matches 16001.. run scoreboard players set @s sp.normal 16000
$data modify storage space_editor:proxy_spike input set value $(inverted)
execute store result score @s sp.inverted run data get storage space_editor:proxy_spike input 1000
execute if score @s sp.inverted matches ..-16001 run scoreboard players set @s sp.inverted -16000
execute if score @s sp.inverted matches 16001.. run scoreboard players set @s sp.inverted 16000
function space_editor:proxy_spike/select
function space_editor:proxy_spike/update_labels
