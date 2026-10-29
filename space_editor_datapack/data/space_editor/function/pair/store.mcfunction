$data modify storage space_editor:document regions[{id:$(a)}] set from storage space_editor:runtime editA
$execute if data storage space_editor:document regions[{id:$(b)}] run data modify storage space_editor:document regions[{id:$(b)}] set from storage space_editor:runtime editB
$execute unless data storage space_editor:document regions[{id:$(b)}] run data modify storage space_editor:document regions append from storage space_editor:runtime editB
$execute if data storage space_editor:document regionPairs[{id:$(id)}] run data modify storage space_editor:document regionPairs[{id:$(id)}] set from storage space_editor:runtime pair
