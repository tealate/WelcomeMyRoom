execute unless data storage space_editor:document projection{enabled:1b} run return 0
scoreboard players set #spawn pr.v 8
scoreboard players set #blocked pr.v 0
execute as @a[gamemode=!spectator,nbt={DeathTime:0s}] at @s run function space_editor:projection/register
data modify storage space_editor:projection contacts set from storage space_editor:runtime spaceLinkContacts
scoreboard players set #updates pr.v 24
execute store result score #contacts pr.v run data get storage space_editor:projection contacts
execute if score #contacts pr.v matches 64.. run scoreboard players set #updates pr.v 8
execute if score #contacts pr.v matches 64.. if entity @a[scores={pr.debug=1}] run scoreboard players set #updates pr.v 4
function space_editor:projection/contact_scan
data modify storage space_editor:projection actorQueue set from storage space_editor:projection players
function space_editor:projection/finish_players
data modify storage space_editor:projection work set from storage space_editor:projection active
data modify storage space_editor:projection done set value []
execute if score #updates pr.v matches 1.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 2.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 3.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 4.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 5.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 6.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 7.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 8.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 9.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 10.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 11.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 12.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 13.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 14.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 15.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 16.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 17.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 18.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 19.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 20.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 21.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 22.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 23.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
execute if score #updates pr.v matches 24.. if data storage space_editor:projection work[0] run function space_editor:projection/route_step
data modify storage space_editor:projection active set from storage space_editor:projection work
data modify storage space_editor:projection active append from storage space_editor:projection done[]
