data modify storage space_editor:runtime spatialRegion set from storage space_editor:runtime tpQueue[0]
execute if data storage space_editor:runtime spatialRegion{kind:"teleport"} run function space_editor:teleport/check
data remove storage space_editor:runtime tpQueue[0]
execute if data storage space_editor:runtime tpQueue[0] run function space_editor:teleport/scan
