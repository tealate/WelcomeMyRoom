$execute positioned ^ ^ ^$(rayDistance) run tp @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] ~ ~ ~
data modify storage space_editor:runtime rayPos set from entity @e[type=minecraft:marker,tag=space_editor.ray_probe,limit=1] Pos
execute store result score #px se.v run data get storage space_editor:runtime rayPos[0] 1000
execute store result score #py se.v run data get storage space_editor:runtime rayPos[1] 1000
execute store result score #pz se.v run data get storage space_editor:runtime rayPos[2] 1000
