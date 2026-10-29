data modify storage space_editor:runtime sg set value {group:{members:[]},before:{regions:[]}}
data modify storage space_editor:runtime frame set from storage space_editor:runtime sgSource
function space_editor:pair/frame
data modify storage space_editor:runtime sg.group.localSize set from storage space_editor:runtime frame.localSize
scoreboard players set #sg_ok se.v 1
function space_editor:space_group/validate_frame
data modify storage space_editor:runtime sg.before.regions append from storage space_editor:runtime sgSource
data modify storage space_editor:runtime sg.group.members append from storage space_editor:runtime sgSource.id
function space_editor:space_group/allocate
scoreboard players set #sg_count se.v 1
