data modify storage space_editor:runtime pairBefore.masks set value []
$data modify storage space_editor:runtime pairBefore.masks append from storage space_editor:document masks[{regionId:$(a)}]
$data modify storage space_editor:runtime pairBefore.masks append from storage space_editor:document masks[{regionId:$(b)}]
$data modify storage space_editor:runtime pairBefore.group set from storage space_editor:document linkGroups[{id:$(groupId)}]
