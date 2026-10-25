summon minecraft:marker ~ ~ ~ {Tags:["space_editor.paste_anchor"]}
data modify storage space_editor:runtime targetPos set from entity @e[type=minecraft:marker,tag=space_editor.paste_anchor,limit=1,sort=nearest] Pos
kill @e[type=minecraft:marker,tag=space_editor.paste_anchor]
function space_editor:paste/preview with storage space_editor:runtime lookup
