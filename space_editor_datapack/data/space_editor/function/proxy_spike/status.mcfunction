function space_editor:proxy_spike/ensure_owner
scoreboard players add @s sp.follow 0
scoreboard players add @s sp.flip 0
scoreboard players add @s sp.name 0
function space_editor:proxy_spike/select
tellraw @s [{text:"[06-1] owned mannequins: "},{selector:"@e[tag=sp.selected,type=minecraft:mannequin]"},{text:" | follow="},{score:{name:"@s",objective:"sp.follow"}},{text:" flip="},{score:{name:"@s",objective:"sp.flip"}},{text:" name mode="},{score:{name:"@s",objective:"sp.name"}}]
