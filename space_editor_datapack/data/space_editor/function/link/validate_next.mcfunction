data modify storage space_editor:runtime validationPair set from storage space_editor:runtime validationPairs[0]
execute if data storage space_editor:runtime validationPair{kind:"teleport"} unless data storage space_editor:runtime validationPair{groupId:0} run function space_editor:link/validate_pair with storage space_editor:runtime validationPair
data remove storage space_editor:runtime validationPairs[0]
execute if data storage space_editor:runtime validationPairs[0] run function space_editor:link/validate_next
