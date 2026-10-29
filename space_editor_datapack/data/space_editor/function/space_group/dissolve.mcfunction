function space_editor:space_group/remove_group with storage space_editor:runtime sg.group
data remove storage space_editor:runtime sg.after[0].spaceLinkGroupId
data remove storage space_editor:runtime sg.after[0].kind
data remove storage space_editor:runtime sg.after[0].legacyPairId
data modify storage space_editor:runtime sg.queue set from storage space_editor:runtime sg.after
function space_editor:space_group/store_scan
data remove storage space_editor:runtime sg.group
