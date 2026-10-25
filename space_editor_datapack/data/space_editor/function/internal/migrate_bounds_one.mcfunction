execute store result score #x1 se.v run data get storage space_editor:runtime migrateRegion.x1 1000
scoreboard players set #negative se.v 0
execute if score #x1 se.v matches ..-1 run scoreboard players set #negative se.v 1
scoreboard players operation #rounded se.v = #x1 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #rounded se.v += #50 se.v
scoreboard players operation #rounded se.v /= #100 se.v
scoreboard players operation #rounded se.v *= #100 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #x1 se.v = #rounded se.v
execute store result score #x2 se.v run data get storage space_editor:runtime migrateRegion.x2 1000
scoreboard players set #negative se.v 0
execute if score #x2 se.v matches ..-1 run scoreboard players set #negative se.v 1
scoreboard players operation #rounded se.v = #x2 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #rounded se.v += #50 se.v
scoreboard players operation #rounded se.v /= #100 se.v
scoreboard players operation #rounded se.v *= #100 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #x2 se.v = #rounded se.v
scoreboard players operation #sizex se.v = #x2 se.v
scoreboard players operation #sizex se.v -= #x1 se.v
execute store result storage space_editor:runtime migrateRegion.x1m int 1 run scoreboard players get #x1 se.v
execute store result storage space_editor:runtime migrateRegion.x2m int 1 run scoreboard players get #x2 se.v
execute store result storage space_editor:runtime migrateRegion.sxm int 1 run scoreboard players get #sizex se.v
execute store result storage space_editor:runtime migrateRegion.x1 double 0.001 run scoreboard players get #x1 se.v
execute store result storage space_editor:runtime migrateRegion.x2 double 0.001 run scoreboard players get #x2 se.v
execute store result storage space_editor:runtime migrateRegion.sx double 0.001 run scoreboard players get #sizex se.v
execute store result storage space_editor:runtime migrateRegion.min[0] double 0.001 run scoreboard players get #x1 se.v
execute store result storage space_editor:runtime migrateRegion.maxExclusive[0] double 0.001 run scoreboard players get #x2 se.v
execute store result score #y1 se.v run data get storage space_editor:runtime migrateRegion.y1 1000
scoreboard players set #negative se.v 0
execute if score #y1 se.v matches ..-1 run scoreboard players set #negative se.v 1
scoreboard players operation #rounded se.v = #y1 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #rounded se.v += #50 se.v
scoreboard players operation #rounded se.v /= #100 se.v
scoreboard players operation #rounded se.v *= #100 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #y1 se.v = #rounded se.v
execute store result score #y2 se.v run data get storage space_editor:runtime migrateRegion.y2 1000
scoreboard players set #negative se.v 0
execute if score #y2 se.v matches ..-1 run scoreboard players set #negative se.v 1
scoreboard players operation #rounded se.v = #y2 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #rounded se.v += #50 se.v
scoreboard players operation #rounded se.v /= #100 se.v
scoreboard players operation #rounded se.v *= #100 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #y2 se.v = #rounded se.v
scoreboard players operation #sizey se.v = #y2 se.v
scoreboard players operation #sizey se.v -= #y1 se.v
execute store result storage space_editor:runtime migrateRegion.y1m int 1 run scoreboard players get #y1 se.v
execute store result storage space_editor:runtime migrateRegion.y2m int 1 run scoreboard players get #y2 se.v
execute store result storage space_editor:runtime migrateRegion.sym int 1 run scoreboard players get #sizey se.v
execute store result storage space_editor:runtime migrateRegion.y1 double 0.001 run scoreboard players get #y1 se.v
execute store result storage space_editor:runtime migrateRegion.y2 double 0.001 run scoreboard players get #y2 se.v
execute store result storage space_editor:runtime migrateRegion.sy double 0.001 run scoreboard players get #sizey se.v
execute store result storage space_editor:runtime migrateRegion.min[1] double 0.001 run scoreboard players get #y1 se.v
execute store result storage space_editor:runtime migrateRegion.maxExclusive[1] double 0.001 run scoreboard players get #y2 se.v
execute store result score #z1 se.v run data get storage space_editor:runtime migrateRegion.z1 1000
scoreboard players set #negative se.v 0
execute if score #z1 se.v matches ..-1 run scoreboard players set #negative se.v 1
scoreboard players operation #rounded se.v = #z1 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #rounded se.v += #50 se.v
scoreboard players operation #rounded se.v /= #100 se.v
scoreboard players operation #rounded se.v *= #100 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #z1 se.v = #rounded se.v
execute store result score #z2 se.v run data get storage space_editor:runtime migrateRegion.z2 1000
scoreboard players set #negative se.v 0
execute if score #z2 se.v matches ..-1 run scoreboard players set #negative se.v 1
scoreboard players operation #rounded se.v = #z2 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #rounded se.v += #50 se.v
scoreboard players operation #rounded se.v /= #100 se.v
scoreboard players operation #rounded se.v *= #100 se.v
execute if score #negative se.v matches 1 run scoreboard players operation #rounded se.v *= #minus_one se.v
scoreboard players operation #z2 se.v = #rounded se.v
scoreboard players operation #sizez se.v = #z2 se.v
scoreboard players operation #sizez se.v -= #z1 se.v
execute store result storage space_editor:runtime migrateRegion.z1m int 1 run scoreboard players get #z1 se.v
execute store result storage space_editor:runtime migrateRegion.z2m int 1 run scoreboard players get #z2 se.v
execute store result storage space_editor:runtime migrateRegion.szm int 1 run scoreboard players get #sizez se.v
execute store result storage space_editor:runtime migrateRegion.z1 double 0.001 run scoreboard players get #z1 se.v
execute store result storage space_editor:runtime migrateRegion.z2 double 0.001 run scoreboard players get #z2 se.v
execute store result storage space_editor:runtime migrateRegion.sz double 0.001 run scoreboard players get #sizez se.v
execute store result storage space_editor:runtime migrateRegion.min[2] double 0.001 run scoreboard players get #z1 se.v
execute store result storage space_editor:runtime migrateRegion.maxExclusive[2] double 0.001 run scoreboard players get #z2 se.v
function space_editor:internal/store_migrated with storage space_editor:runtime migrateRegion
