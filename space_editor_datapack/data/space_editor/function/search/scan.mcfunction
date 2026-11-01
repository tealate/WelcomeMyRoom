execute unless data storage space_editor:projection route.searchQueue[0] run return 0
execute if score #search_budget pr.v matches ..0 run return 0
scoreboard players remove #search_budget pr.v 1
data modify storage space_editor:runtime spatialRegion set from storage space_editor:projection route.searchQueue[0]
function space_editor:search/check with storage space_editor:projection route
execute if score #inside se.v matches 1 run return run function space_editor:search/hit
function space_editor:search/exclude
data remove storage space_editor:projection route.searchQueue[0]
function space_editor:search/scan
