scoreboard players set #exists pr.v 0
scoreboard players set #pending pr.v 0
scoreboard players set #cache_revision pr.v -1
execute store result score #cache_revision pr.v run data get storage space_editor:projection route.searchRevision
execute unless score #cache_revision pr.v = #revision pr.v run function space_editor:search/reset_route
execute if data storage space_editor:projection route.existenceCache run function space_editor:search/cache
execute if score #exists pr.v matches 1 run return 1
scoreboard players set #cert_ok pr.v 0
execute if data storage space_editor:projection route.searchCert run function space_editor:search/cert_check with storage space_editor:projection route.searchCert
execute unless score #cert_ok pr.v matches 1 run data remove storage space_editor:projection route.searchQueue
execute unless data storage space_editor:projection route.searchQueue run function space_editor:search/begin with storage space_editor:projection route
function space_editor:search/scan
execute unless score #exists pr.v matches 1 if data storage space_editor:projection route.searchQueue[0] run scoreboard players set #pending pr.v 1
