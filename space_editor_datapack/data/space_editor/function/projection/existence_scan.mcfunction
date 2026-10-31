execute unless data storage space_editor:projection exists[0] run return 0
execute if score #exists pr.v matches 1 run return 0
data modify storage space_editor:runtime spatialRegion set from storage space_editor:projection exists[0]
function space_editor:projection/existence_check with storage space_editor:projection exists[0]
data remove storage space_editor:projection exists[0]
execute if data storage space_editor:projection exists[0] run function space_editor:projection/existence_scan
