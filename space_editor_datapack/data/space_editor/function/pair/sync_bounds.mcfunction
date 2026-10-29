execute store result score #dwx1 se.v run data get storage space_editor:runtime hit.x1m 1
execute store result score #dt se.v run data get storage space_editor:runtime old.x1m 1
scoreboard players operation #dwx1 se.v -= #dt se.v
execute store result score #dwx2 se.v run data get storage space_editor:runtime hit.x2m 1
execute store result score #dt se.v run data get storage space_editor:runtime old.x2m 1
scoreboard players operation #dwx2 se.v -= #dt se.v
execute store result score #dwy1 se.v run data get storage space_editor:runtime hit.y1m 1
execute store result score #dt se.v run data get storage space_editor:runtime old.y1m 1
scoreboard players operation #dwy1 se.v -= #dt se.v
execute store result score #dwy2 se.v run data get storage space_editor:runtime hit.y2m 1
execute store result score #dt se.v run data get storage space_editor:runtime old.y2m 1
scoreboard players operation #dwy2 se.v -= #dt se.v
execute store result score #dwz1 se.v run data get storage space_editor:runtime hit.z1m 1
execute store result score #dt se.v run data get storage space_editor:runtime old.z1m 1
scoreboard players operation #dwz1 se.v -= #dt se.v
execute store result score #dwz2 se.v run data get storage space_editor:runtime hit.z2m 1
execute store result score #dt se.v run data get storage space_editor:runtime old.z2m 1
scoreboard players operation #dwz2 se.v -= #dt se.v
execute if data storage space_editor:runtime old{rotationY:0,flipY:0b} run function space_editor:pair/delta_inverse_0_0
execute if data storage space_editor:runtime old{rotationY:0,flipY:1b} run function space_editor:pair/delta_inverse_0_1
execute if data storage space_editor:runtime old{rotationY:90,flipY:0b} run function space_editor:pair/delta_inverse_90_0
execute if data storage space_editor:runtime old{rotationY:90,flipY:1b} run function space_editor:pair/delta_inverse_90_1
execute if data storage space_editor:runtime old{rotationY:180,flipY:0b} run function space_editor:pair/delta_inverse_180_0
execute if data storage space_editor:runtime old{rotationY:180,flipY:1b} run function space_editor:pair/delta_inverse_180_1
execute if data storage space_editor:runtime old{rotationY:270,flipY:0b} run function space_editor:pair/delta_inverse_270_0
execute if data storage space_editor:runtime old{rotationY:270,flipY:1b} run function space_editor:pair/delta_inverse_270_1
execute if data storage space_editor:runtime partner{rotationY:0,flipY:0b} run function space_editor:pair/delta_forward_0_0
execute if data storage space_editor:runtime partner{rotationY:0,flipY:1b} run function space_editor:pair/delta_forward_0_1
execute if data storage space_editor:runtime partner{rotationY:90,flipY:0b} run function space_editor:pair/delta_forward_90_0
execute if data storage space_editor:runtime partner{rotationY:90,flipY:1b} run function space_editor:pair/delta_forward_90_1
execute if data storage space_editor:runtime partner{rotationY:180,flipY:0b} run function space_editor:pair/delta_forward_180_0
execute if data storage space_editor:runtime partner{rotationY:180,flipY:1b} run function space_editor:pair/delta_forward_180_1
execute if data storage space_editor:runtime partner{rotationY:270,flipY:0b} run function space_editor:pair/delta_forward_270_0
execute if data storage space_editor:runtime partner{rotationY:270,flipY:1b} run function space_editor:pair/delta_forward_270_1
execute store result score #dt se.v run data get storage space_editor:runtime partner.x1m 1
scoreboard players operation #dt se.v += #dox1 se.v
execute store result storage space_editor:runtime partner.x1m int 1 run scoreboard players get #dt se.v
execute store result score #dt se.v run data get storage space_editor:runtime partner.x2m 1
scoreboard players operation #dt se.v += #dox2 se.v
execute store result storage space_editor:runtime partner.x2m int 1 run scoreboard players get #dt se.v
execute store result score #dt se.v run data get storage space_editor:runtime partner.y1m 1
scoreboard players operation #dt se.v += #doy1 se.v
execute store result storage space_editor:runtime partner.y1m int 1 run scoreboard players get #dt se.v
execute store result score #dt se.v run data get storage space_editor:runtime partner.y2m 1
scoreboard players operation #dt se.v += #doy2 se.v
execute store result storage space_editor:runtime partner.y2m int 1 run scoreboard players get #dt se.v
execute store result score #dt se.v run data get storage space_editor:runtime partner.z1m 1
scoreboard players operation #dt se.v += #doz1 se.v
execute store result storage space_editor:runtime partner.z1m int 1 run scoreboard players get #dt se.v
execute store result score #dt se.v run data get storage space_editor:runtime partner.z2m 1
scoreboard players operation #dt se.v += #doz2 se.v
execute store result storage space_editor:runtime partner.z2m int 1 run scoreboard players get #dt se.v
