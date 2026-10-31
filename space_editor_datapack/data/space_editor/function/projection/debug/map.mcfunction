$execute unless data storage space_editor:document regions[{id:$(target),kind:"space_link"}] run return 0
$execute unless data storage space_editor:document regions[{id:$(region)}] run return 0
$data modify storage space_editor:projection config set value {targetId:$(target),regionId:$(region)}
data modify storage space_editor:projection config.uuid set from entity @s UUID
function space_editor:projection/debug/save with storage space_editor:projection config
