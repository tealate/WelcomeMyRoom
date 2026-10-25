data modify storage space_editor:runtime migrateRegion set from storage space_editor:runtime migrateQueue[0]
function space_editor:internal/migrate_bounds_one
data remove storage space_editor:runtime migrateQueue[0]
execute if data storage space_editor:runtime migrateQueue[0] run function space_editor:internal/migrate_bounds_next
