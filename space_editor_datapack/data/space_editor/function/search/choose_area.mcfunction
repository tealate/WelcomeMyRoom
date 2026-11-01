execute unless data storage space_editor:search queryAreas[0] run return 0
execute if score #search_budget pr.v matches ..0 run return 0
scoreboard players remove #search_budget pr.v 1
data modify storage space_editor:runtime spatialRegion set from storage space_editor:search queryAreas[0]
function space_editor:search/check with storage space_editor:projection route
execute if score #inside se.v matches 1 run return run data modify storage space_editor:search chosen set from storage space_editor:search queryAreas[0]
data remove storage space_editor:search queryAreas[0]
function space_editor:search/choose_area
