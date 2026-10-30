data remove storage space_editor:projection resolved
$data modify storage space_editor:projection resolved set from storage space_editor:projection rebases[{groupId:$(groupId),oldSource:$(sourceId)}]
execute unless data storage space_editor:projection resolved run function space_editor:projection/rebase_find with storage space_editor:projection rebase
execute if data storage space_editor:projection resolved.sourceId run function space_editor:projection/rebase_commit with storage space_editor:projection rebase
execute unless data storage space_editor:projection resolved.sourceId run data modify storage space_editor:projection warning set value "unresolved_transfer_source: retained path suspended until valid source is known"
$execute unless data storage space_editor:projection resolved.sourceId run data modify storage space_editor:projection active[{id:$(id)}].suspended set value 1b
