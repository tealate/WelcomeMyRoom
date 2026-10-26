$execute unless dimension $(targetDimension) run return 0
execute store result score #x1m se.v run data get storage space_editor:runtime pastePending.x 1000
execute store result score #sxm se.v run data get storage space_editor:runtime pastePending.sx 1000
scoreboard players operation #x2m se.v = #x1m se.v
scoreboard players operation #x2m se.v += #sxm se.v
execute if score #px se.v < #x1m se.v run return 0
execute if score #px se.v >= #x2m se.v run return 0
execute store result score #y1m se.v run data get storage space_editor:runtime pastePending.y 1000
execute store result score #sym se.v run data get storage space_editor:runtime pastePending.sy 1000
scoreboard players operation #y2m se.v = #y1m se.v
scoreboard players operation #y2m se.v += #sym se.v
execute if score #py se.v < #y1m se.v run return 0
execute if score #py se.v >= #y2m se.v run return 0
execute store result score #z1m se.v run data get storage space_editor:runtime pastePending.z 1000
execute store result score #szm se.v run data get storage space_editor:runtime pastePending.sz 1000
scoreboard players operation #z2m se.v = #z1m se.v
scoreboard players operation #z2m se.v += #szm se.v
execute if score #pz se.v < #z1m se.v run return 0
execute if score #pz se.v >= #z2m se.v run return 0
data modify storage space_editor:runtime hit set value {kind:"paste_preview",x1m:0,x2m:0,y1m:0,y2m:0,z1m:0,z2m:0}
execute store result storage space_editor:runtime hit.x1m int 1 run scoreboard players get #x1m se.v
execute store result storage space_editor:runtime hit.x2m int 1 run scoreboard players get #x2m se.v
execute store result storage space_editor:runtime hit.y1m int 1 run scoreboard players get #y1m se.v
execute store result storage space_editor:runtime hit.y2m int 1 run scoreboard players get #y2m se.v
execute store result storage space_editor:runtime hit.z1m int 1 run scoreboard players get #z1m se.v
execute store result storage space_editor:runtime hit.z2m int 1 run scoreboard players get #z2m se.v
function space_editor:region/face
return 1
