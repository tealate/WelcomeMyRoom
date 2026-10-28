data remove storage space_editor:runtime pair
data remove storage space_editor:runtime editA
data remove storage space_editor:runtime editB
$data modify storage space_editor:runtime pair set from storage space_editor:document regionPairs[{id:$(pairId)}]
execute if data storage space_editor:runtime pair.id run function space_editor:pair/load_members with storage space_editor:runtime pair
