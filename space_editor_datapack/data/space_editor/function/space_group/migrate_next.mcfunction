data modify storage space_editor:runtime sgLegacy set from storage space_editor:runtime sgMigrateQueue[0]
execute if data storage space_editor:runtime sgLegacy{kind:"space_link"} unless data storage space_editor:runtime sgLegacy.spaceLinkGroupId run function space_editor:space_group/migrate_pair with storage space_editor:runtime sgLegacy
data remove storage space_editor:runtime sgMigrateQueue[0]
