data modify storage space_editor:projection route.existenceCache set value {}
function space_editor:search/cache_bounds
data remove storage space_editor:projection route.searchQueue
data remove storage space_editor:projection route.searchPoint
data remove storage space_editor:projection route.searchCert
scoreboard players set #exists pr.v 1
