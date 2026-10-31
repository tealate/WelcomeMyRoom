$data modify storage space_editor:proxy_spike input set value $(fy)
execute store result score @s sp.fy run data get storage space_editor:proxy_spike input 1000
execute if score @s sp.fy matches ..-16001 run scoreboard players set @s sp.fy -16000
execute if score @s sp.fy matches 16001.. run scoreboard players set @s sp.fy 16000
function space_editor:proxy_spike/select
function space_editor:proxy_spike/update_labels
