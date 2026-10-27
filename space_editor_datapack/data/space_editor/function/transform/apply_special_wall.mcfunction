$execute in $(targetDimension) run setblock $(x) $(y) $(z) minecraft:sandstone_wall[north=$(north),east=$(east),south=$(south),west=$(west),up=$(up),waterlogged=$(waterlogged)] strict
data modify storage space_editor:runtime transformState.displayEast set from storage space_editor:runtime transformState.west
data modify storage space_editor:runtime transformState.displayWest set from storage space_editor:runtime transformState.east
function space_editor:special/spawn_wall with storage space_editor:runtime transformState
function space_editor:special/register with storage space_editor:runtime transformState
return 1
