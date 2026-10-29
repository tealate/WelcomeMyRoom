$execute unless data storage space_editor:document regions[{id:$(id)}] run data modify storage space_editor:document regions append from storage space_editor:runtime sg.queue[0]
$data modify storage space_editor:document regions[{id:$(id)}] set from storage space_editor:runtime sg.queue[0]
