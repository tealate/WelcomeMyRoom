function editor:internal/selection/kill
execute unless data storage editor:data selection.valid run return 0
execute if data storage editor:data {guides:0b} run return 0
function editor:internal/selection/spawn with storage editor:data selection
