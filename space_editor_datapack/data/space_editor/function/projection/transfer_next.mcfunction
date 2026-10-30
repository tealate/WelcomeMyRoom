data modify storage space_editor:projection transfer set from storage space_editor:projection transfers[0]
data remove storage space_editor:projection transfers[0]
data modify storage space_editor:projection rebases set value []
data modify storage space_editor:projection rebaseQueue set from storage space_editor:projection active
function space_editor:projection/rebase_scan
