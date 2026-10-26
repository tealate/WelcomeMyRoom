data modify storage editor:runtime volume_item set from storage editor:runtime volumes[0]
execute if data storage editor:runtime volume_item{type:"teleport_volume"} if data storage editor:runtime volume_item.target run function editor:internal/teleport/check with storage editor:runtime volumes[0]
data remove storage editor:runtime volumes[0]
execute if data storage editor:runtime volumes[0] run function editor:internal/teleport/next
