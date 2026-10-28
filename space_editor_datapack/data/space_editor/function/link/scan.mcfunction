data modify storage space_editor:runtime spatialRegion set from storage space_editor:runtime linkQueue[0]
execute if data storage space_editor:runtime spatialRegion{kind:"space_link"} run function space_editor:link/check
data remove storage space_editor:runtime linkQueue[0]
execute if data storage space_editor:runtime linkQueue[0] run function space_editor:link/scan
