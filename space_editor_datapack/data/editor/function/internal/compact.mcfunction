data modify storage editor:runtime compact_item set from storage editor:runtime compact[0]
execute if data storage editor:runtime compact_item{type:"block_fill"} run data modify storage editor:data footprints append from storage editor:runtime compact_item
execute unless data storage editor:runtime compact_item{type:"block_fill"} run data modify storage editor:data display_footprints append from storage editor:runtime compact_item
data remove storage editor:runtime compact[0]
execute if data storage editor:runtime compact[0] run function editor:internal/compact
