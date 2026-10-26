execute store result score #cx1 se run data get storage editor:runtime work.x1
scoreboard players operation #cx1 se /= #16 se
scoreboard players operation #cx1 se *= #16 se
execute store result score #cx2 se run data get storage editor:runtime work.x2
scoreboard players operation #cx2 se /= #16 se
scoreboard players operation #cx2 se *= #16 se
execute store result score #cz1 se run data get storage editor:runtime work.z1
scoreboard players operation #cz1 se /= #16 se
scoreboard players operation #cz1 se *= #16 se
execute store result score #cz2 se run data get storage editor:runtime work.z2
scoreboard players operation #cz2 se /= #16 se
scoreboard players operation #cz2 se *= #16 se
scoreboard players operation #cx se = #cx1 se
function editor:internal/job/chunk_x
