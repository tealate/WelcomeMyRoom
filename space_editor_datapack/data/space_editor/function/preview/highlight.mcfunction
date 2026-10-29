$execute in $(dimension) as @e[tag=space_editor.region,scores={se.id=$(id)}] run data merge entity @s {block_state:{Name:"minecraft:lime_glazed_terracotta"}}
$data modify storage space_editor:runtime highlightedRegion set value {id:$(id),dimension:"$(dimension)"}
