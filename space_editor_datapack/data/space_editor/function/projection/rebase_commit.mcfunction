$data remove storage space_editor:projection active[{id:$(id)}].suspended
$data modify storage space_editor:projection active[{id:$(id)}].sourceId set from storage space_editor:projection resolved.sourceId
data modify storage space_editor:projection arrived.groupId set from storage space_editor:projection resolved.groupId
data modify storage space_editor:projection arrived.sourceId set from storage space_editor:projection resolved.sourceId
$data modify storage space_editor:projection players[{id:$(owner)}].previous append from storage space_editor:projection arrived
