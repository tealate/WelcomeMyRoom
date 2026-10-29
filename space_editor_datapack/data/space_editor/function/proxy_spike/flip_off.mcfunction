scoreboard players set @s sp.flip 0
function space_editor:proxy_spike/select
data remove entity @e[tag=sp.selected,tag=sp.main,limit=1] CustomName
function space_editor:proxy_spike/apply_name
