$execute in $(dimension) as @e[tag=space_editor.region,scores={se.id=$(id)}] run data merge entity @s {block_state:{Name:"minecraft:magenta_glazed_terracotta"}}
$function space_editor:preview/type_color {id:$(id),dimension:"$(dimension)"}
