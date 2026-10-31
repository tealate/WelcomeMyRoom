execute unless data storage space_editor:projection candidates[0] run return 0
execute if data storage space_editor:projection resolved.sourceId run return 0
function space_editor:projection/candidate with storage space_editor:projection candidates[0]
data remove storage space_editor:projection candidates[0]
execute if data storage space_editor:projection candidates[0] run function space_editor:projection/candidate_scan
