$data modify storage space_editor:projection resolved set value {groupId:$(groupId),oldSource:$(sourceId)}
data remove storage space_editor:projection oldFrame
$data modify storage space_editor:projection oldFrame set from storage space_editor:document regions[{id:$(sourceId)}]
function space_editor:projection/rebase_basis with storage space_editor:projection transfer
data modify storage space_editor:projection candidates set value []
$data modify storage space_editor:projection candidates append from storage space_editor:document regions[{kind:"space_link",spaceLinkGroupId:$(groupId)}]
function space_editor:projection/candidate_scan
data modify storage space_editor:projection rebases append from storage space_editor:projection resolved
