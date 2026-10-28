data modify storage space_editor:runtime peerPair set from storage space_editor:runtime comparePeers[0]
$execute if data storage space_editor:runtime peerPair{groupId:$(groupId),kind:"space_link"} run function space_editor:link/compare
data remove storage space_editor:runtime comparePeers[0]
execute if data storage space_editor:runtime comparePeers[0] run function space_editor:link/compare_next with storage space_editor:runtime validationPair
