$execute unless data storage space_editor:document regions[{id:$(id),kind:"proxy_existence"}] run return 0
$data modify storage space_editor:document regions[{id:$(id)}].roomId set value "$(roomId)"
