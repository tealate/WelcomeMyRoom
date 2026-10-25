scoreboard players set #valid se.v 1
execute store result score #ax se.v run data get storage space_editor:runtime selection.a[0] 1
execute store result score #bx se.v run data get storage space_editor:runtime selection.b[0] 1
scoreboard players operation #minx se.v = #ax se.v
scoreboard players operation #minx se.v < #bx se.v
scoreboard players operation #maxx se.v = #ax se.v
scoreboard players operation #maxx se.v > #bx se.v
scoreboard players add #maxx se.v 1
scoreboard players operation #sizex se.v = #maxx se.v
scoreboard players operation #sizex se.v -= #minx se.v
execute unless score #sizex se.v matches 1..32 run scoreboard players set #valid se.v 0
execute store result score #ay se.v run data get storage space_editor:runtime selection.a[1] 1
execute store result score #by se.v run data get storage space_editor:runtime selection.b[1] 1
scoreboard players operation #miny se.v = #ay se.v
scoreboard players operation #miny se.v < #by se.v
scoreboard players operation #maxy se.v = #ay se.v
scoreboard players operation #maxy se.v > #by se.v
scoreboard players add #maxy se.v 1
scoreboard players operation #sizey se.v = #maxy se.v
scoreboard players operation #sizey se.v -= #miny se.v
execute unless score #sizey se.v matches 1..32 run scoreboard players set #valid se.v 0
execute store result score #az se.v run data get storage space_editor:runtime selection.a[2] 1
execute store result score #bz se.v run data get storage space_editor:runtime selection.b[2] 1
scoreboard players operation #minz se.v = #az se.v
scoreboard players operation #minz se.v < #bz se.v
scoreboard players operation #maxz se.v = #az se.v
scoreboard players operation #maxz se.v > #bz se.v
scoreboard players add #maxz se.v 1
scoreboard players operation #sizez se.v = #maxz se.v
scoreboard players operation #sizez se.v -= #minz se.v
execute unless score #sizez se.v matches 1..32 run scoreboard players set #valid se.v 0
execute unless score #valid se.v matches 1 run return run tellraw @s {"text": "[Space Editor] 各辺は1〜32ブロックにしてください。", "color": "red"}
execute store result score #next se.v run data get storage space_editor:document nextId 1
data modify storage space_editor:runtime region set value {id:0,idText:"",dimension:"",min:[I;0,0,0],maxExclusive:[I;0,0,0],role:"generic",state:"committed",visible:1b}
execute store result storage space_editor:runtime region.id int 1 run scoreboard players get #next se.v
function space_editor:internal/set_region_id_text with storage space_editor:runtime region
data modify storage space_editor:runtime region.dimension set from storage space_editor:runtime selection.dimension
execute store result storage space_editor:runtime region.min[0] int 1 run scoreboard players get #minx se.v
execute store result storage space_editor:runtime region.maxExclusive[0] int 1 run scoreboard players get #maxx se.v
execute store result storage space_editor:runtime region.x1 int 1 run scoreboard players get #minx se.v
execute store result storage space_editor:runtime region.x2 int 1 run scoreboard players get #maxx se.v
execute store result storage space_editor:runtime region.sx int 1 run scoreboard players get #sizex se.v
scoreboard players operation #x1m se.v = #minx se.v
scoreboard players operation #x1m se.v *= #1000 se.v
scoreboard players operation #x2m se.v = #maxx se.v
scoreboard players operation #x2m se.v *= #1000 se.v
scoreboard players operation #sxm se.v = #sizex se.v
scoreboard players operation #sxm se.v *= #1000 se.v
execute store result storage space_editor:runtime region.x1m int 1 run scoreboard players get #x1m se.v
execute store result storage space_editor:runtime region.x2m int 1 run scoreboard players get #x2m se.v
execute store result storage space_editor:runtime region.sxm int 1 run scoreboard players get #sxm se.v
execute store result storage space_editor:runtime region.min[1] int 1 run scoreboard players get #miny se.v
execute store result storage space_editor:runtime region.maxExclusive[1] int 1 run scoreboard players get #maxy se.v
execute store result storage space_editor:runtime region.y1 int 1 run scoreboard players get #miny se.v
execute store result storage space_editor:runtime region.y2 int 1 run scoreboard players get #maxy se.v
execute store result storage space_editor:runtime region.sy int 1 run scoreboard players get #sizey se.v
scoreboard players operation #y1m se.v = #miny se.v
scoreboard players operation #y1m se.v *= #1000 se.v
scoreboard players operation #y2m se.v = #maxy se.v
scoreboard players operation #y2m se.v *= #1000 se.v
scoreboard players operation #sym se.v = #sizey se.v
scoreboard players operation #sym se.v *= #1000 se.v
execute store result storage space_editor:runtime region.y1m int 1 run scoreboard players get #y1m se.v
execute store result storage space_editor:runtime region.y2m int 1 run scoreboard players get #y2m se.v
execute store result storage space_editor:runtime region.sym int 1 run scoreboard players get #sym se.v
execute store result storage space_editor:runtime region.min[2] int 1 run scoreboard players get #minz se.v
execute store result storage space_editor:runtime region.maxExclusive[2] int 1 run scoreboard players get #maxz se.v
execute store result storage space_editor:runtime region.z1 int 1 run scoreboard players get #minz se.v
execute store result storage space_editor:runtime region.z2 int 1 run scoreboard players get #maxz se.v
execute store result storage space_editor:runtime region.sz int 1 run scoreboard players get #sizez se.v
scoreboard players operation #z1m se.v = #minz se.v
scoreboard players operation #z1m se.v *= #1000 se.v
scoreboard players operation #z2m se.v = #maxz se.v
scoreboard players operation #z2m se.v *= #1000 se.v
scoreboard players operation #szm se.v = #sizez se.v
scoreboard players operation #szm se.v *= #1000 se.v
execute store result storage space_editor:runtime region.z1m int 1 run scoreboard players get #z1m se.v
execute store result storage space_editor:runtime region.z2m int 1 run scoreboard players get #z2m se.v
execute store result storage space_editor:runtime region.szm int 1 run scoreboard players get #szm se.v
data modify storage space_editor:document regions append from storage space_editor:runtime region
scoreboard players add #next se.v 1
execute store result storage space_editor:document nextId int 1 run scoreboard players get #next se.v
data remove storage space_editor:runtime selection
execute in minecraft:overworld run kill @e[tag=space_editor.point]
execute in minecraft:the_nether run kill @e[tag=space_editor.point]
execute in minecraft:the_end run kill @e[tag=space_editor.point]
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] Regionを保存しました。続けて範囲棒で次のRegionを作れます。", "color": "green"}
