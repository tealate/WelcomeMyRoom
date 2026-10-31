function space_editor:proxy_spike/select
$data modify storage space_editor:proxy_spike input set value $(scale)
execute store result score #scale sp.v run data get storage space_editor:proxy_spike input 1000
execute if score #scale sp.v matches ..99 run return 0
execute if score #scale sp.v matches 3001.. run return 0
$execute as @e[type=minecraft:text_display,tag=sp.selected] run data merge entity @s {background:$(background),transformation:{scale:[$(scale)f,$(scale)f,$(scale)f]}}
