$execute unless data storage space_editor:projection players[{id:$(id),uuid:$(uuid),leave:$(leave)}] run function space_editor:projection/remove_owner with storage space_editor:projection actor
$execute unless data storage space_editor:projection players[{id:$(id),uuid:$(uuid),leave:$(leave)}] run data remove storage space_editor:projection active[{owner:$(id)}]
$execute unless data storage space_editor:projection players[{id:$(id),uuid:$(uuid),leave:$(leave)}] run data remove storage space_editor:projection players[{id:$(id)}]
$execute unless data storage space_editor:projection players[{id:$(id)}] run data modify storage space_editor:projection players append value {id:$(id),uuid:$(uuid),leave:$(leave),previous:[],next:[]}
$data modify storage space_editor:projection players[{id:$(id)}].next set value []
