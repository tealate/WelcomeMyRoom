data modify storage space_editor:runtime comparePeers set from storage space_editor:document regionPairs
execute if data storage space_editor:runtime comparePeers[0] run function space_editor:link/compare_next with storage space_editor:runtime validationPair
