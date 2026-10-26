execute store result score #px se run data get entity @s Pos[0] 1000
execute store result score #py se run data get entity @s Pos[1] 1000
execute store result score #pz se run data get entity @s Pos[2] 1000
$execute unless score #px se matches $(lox).. run return 0
$execute unless score #py se matches $(loy).. run return 0
$execute unless score #pz se matches $(loz).. run return 0
$execute if score #px se matches $(hix).. run return 0
$execute if score #py se matches $(hiy).. run return 0
$execute if score #pz se matches $(hiz).. run return 0
scoreboard players set @s se.cd 20
data modify storage editor:runtime target set from storage editor:runtime volumes[0].target
execute store result storage editor:runtime target.x double 0.001 run data get storage editor:runtime target.pos[0] 1000
execute store result storage editor:runtime target.y double 0.001 run data get storage editor:runtime target.pos[1] 1000
execute store result storage editor:runtime target.z double 0.001 run data get storage editor:runtime target.pos[2] 1000
execute store result storage editor:runtime target.yaw float 0.001 run data get storage editor:runtime target.rotation[0] 1000
execute store result storage editor:runtime target.pitch float 0.001 run data get storage editor:runtime target.rotation[1] 1000
function editor:internal/teleport/go with storage editor:runtime target
