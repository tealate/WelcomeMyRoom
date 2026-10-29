data modify storage space_editor:runtime contactRef.id set from storage space_editor:runtime contactMembers[0]
data modify storage space_editor:runtime contactRef.groupId set from storage space_editor:runtime contactGroup.id
data modify storage space_editor:runtime contactRef.sourceId set from storage space_editor:runtime contactSource.id
function space_editor:link/target with storage space_editor:runtime contactRef
data remove storage space_editor:runtime contactMembers[0]
