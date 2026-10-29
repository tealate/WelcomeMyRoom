data modify storage space_editor:runtime sgRef.id set from storage space_editor:runtime sg.queue[0]
data modify storage space_editor:runtime sgRef.groupId set from storage space_editor:runtime sg.group.id
function space_editor:space_group/load_member with storage space_editor:runtime sgRef
data remove storage space_editor:runtime sg.queue[0]
