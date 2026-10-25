data modify storage space_editor:runtime hover set value {dimension:"",pos:[I;0,0,0],x:0,y:0,z:0}
execute if dimension minecraft:overworld run data modify storage space_editor:runtime hover.dimension set value "minecraft:overworld"
execute if dimension minecraft:the_nether run data modify storage space_editor:runtime hover.dimension set value "minecraft:the_nether"
execute if dimension minecraft:the_end run data modify storage space_editor:runtime hover.dimension set value "minecraft:the_end"
execute if data storage space_editor:runtime hover{dimension:""} run return run data remove storage space_editor:runtime hover
kill @e[type=minecraft:marker,tag=space_editor.selection_capture]
summon minecraft:marker ~ ~ ~ {Tags:["space_editor.selection_capture"]}
execute store result storage space_editor:runtime hover.pos[0] int 1 run data get entity @e[type=minecraft:marker,tag=space_editor.selection_capture,limit=1,sort=nearest] Pos[0] 1
execute store result storage space_editor:runtime hover.pos[1] int 1 run data get entity @e[type=minecraft:marker,tag=space_editor.selection_capture,limit=1,sort=nearest] Pos[1] 1
execute store result storage space_editor:runtime hover.pos[2] int 1 run data get entity @e[type=minecraft:marker,tag=space_editor.selection_capture,limit=1,sort=nearest] Pos[2] 1
execute store result storage space_editor:runtime hover.x int 1 run data get storage space_editor:runtime hover.pos[0] 1
execute store result storage space_editor:runtime hover.y int 1 run data get storage space_editor:runtime hover.pos[1] 1
execute store result storage space_editor:runtime hover.z int 1 run data get storage space_editor:runtime hover.pos[2] 1
kill @e[type=minecraft:marker,tag=space_editor.selection_capture]
function space_editor:preview/selection_candidate with storage space_editor:runtime hover
