data modify storage space_editor:runtime migrateQueue set from storage space_editor:document regions
execute if data storage space_editor:runtime migrateQueue[0] run function space_editor:internal/migrate_bounds_next
data modify storage space_editor:document settings.fixedBounds set value 1b
data modify storage space_editor:document settings.boundsVersion set value 3
