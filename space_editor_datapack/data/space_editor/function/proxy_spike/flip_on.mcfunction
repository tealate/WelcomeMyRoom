scoreboard players set @s sp.flip 1
function space_editor:proxy_spike/select
data modify entity @e[type=minecraft:mannequin,tag=sp.selected,tag=sp.main,limit=1] CustomName set value {text:"Dinnerbone"}
function space_editor:proxy_spike/apply_name
function space_editor:proxy_spike/update_labels
