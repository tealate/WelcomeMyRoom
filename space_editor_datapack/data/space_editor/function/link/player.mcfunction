execute unless entity @s[nbt={DeathTime:0s}] run return 0
function space_editor:teleport/read_snapshot
execute unless data storage space_editor:runtime tpPlayer.point run return 0
data modify storage space_editor:runtime linkQueue set from storage space_editor:document regions
function space_editor:link/scan
execute if data storage space_editor:runtime linkQueue[0] run data modify storage space_editor:runtime spaceLinkRuntimeWarnings append value {reason:"source_scan_limit_4096"}
