function space_editor:region/load_scores
scoreboard players operation #delta se.v = #1000 se.v
scoreboard players operation #delta se.v *= #direction se.v
execute if data storage space_editor:runtime {hitFace:0} run scoreboard players operation #x1 se.v -= #delta se.v
execute if data storage space_editor:runtime {hitFace:0} run scoreboard players operation #x2 se.v -= #delta se.v
execute if data storage space_editor:runtime {hitFace:1} run scoreboard players operation #x1 se.v += #delta se.v
execute if data storage space_editor:runtime {hitFace:1} run scoreboard players operation #x2 se.v += #delta se.v
execute if data storage space_editor:runtime {hitFace:2} run scoreboard players operation #y1 se.v -= #delta se.v
execute if data storage space_editor:runtime {hitFace:2} run scoreboard players operation #y2 se.v -= #delta se.v
execute if data storage space_editor:runtime {hitFace:3} run scoreboard players operation #y1 se.v += #delta se.v
execute if data storage space_editor:runtime {hitFace:3} run scoreboard players operation #y2 se.v += #delta se.v
execute if data storage space_editor:runtime {hitFace:4} run scoreboard players operation #z1 se.v -= #delta se.v
execute if data storage space_editor:runtime {hitFace:4} run scoreboard players operation #z2 se.v -= #delta se.v
execute if data storage space_editor:runtime {hitFace:5} run scoreboard players operation #z1 se.v += #delta se.v
execute if data storage space_editor:runtime {hitFace:5} run scoreboard players operation #z2 se.v += #delta se.v
scoreboard players operation #sizex se.v = #x2 se.v
scoreboard players operation #sizex se.v -= #x1 se.v
scoreboard players operation #sizey se.v = #y2 se.v
scoreboard players operation #sizey se.v -= #y1 se.v
scoreboard players operation #sizez se.v = #z2 se.v
scoreboard players operation #sizez se.v -= #z1 se.v
function space_editor:region/save_resize
