execute unless data storage space_editor:document spaceLinkGroups run data modify storage space_editor:document spaceLinkGroups set value []
execute unless data storage space_editor:document nextSpaceLinkGroupId run data modify storage space_editor:document nextSpaceLinkGroupId set value 1
data modify storage space_editor:runtime spaceLinkWarnings set value []
data modify storage space_editor:runtime sgMigrateQueue set from storage space_editor:document regionPairs
function space_editor:space_group/migrate_scan
execute if data storage space_editor:runtime sgMigrateQueue[0] run data modify storage space_editor:runtime spaceLinkWarnings append value {reason:"migration_scan_limit_4096"}
execute if data storage space_editor:runtime spaceLinkWarnings[0] run tellraw @a {"text": "[Space Editor] SpaceLink移行警告: /data get storage space_editor:runtime spaceLinkWarnings", "color": "yellow"}
