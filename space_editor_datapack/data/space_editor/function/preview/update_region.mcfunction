$execute in minecraft:overworld run kill @e[tag=space_editor.region,scores={se.id=$(id)}]
$execute in minecraft:overworld run kill @e[tag=space_editor.label,scores={se.id=$(id)}]
$execute in minecraft:the_nether run kill @e[tag=space_editor.region,scores={se.id=$(id)}]
$execute in minecraft:the_nether run kill @e[tag=space_editor.label,scores={se.id=$(id)}]
$execute in minecraft:the_end run kill @e[tag=space_editor.region,scores={se.id=$(id)}]
$execute in minecraft:the_end run kill @e[tag=space_editor.label,scores={se.id=$(id)}]
data remove storage space_editor:runtime renderRegion
$data modify storage space_editor:runtime renderRegion set from storage space_editor:document regions[{id:$(id)}]
execute if data storage space_editor:runtime renderRegion.id if data storage space_editor:document {editMode:1b} if data storage space_editor:document settings{regionsVisible:1b} run function space_editor:preview/prepare
execute if data storage space_editor:runtime renderRegion.id if data storage space_editor:document {editMode:1b} if data storage space_editor:document settings{regionsVisible:1b} run function space_editor:preview/spawn with storage space_editor:runtime renderRegion
data remove storage space_editor:runtime currentMask
$data modify storage space_editor:runtime currentMask set from storage space_editor:document masks[{regionId:$(id)}]
execute if data storage space_editor:runtime currentMask.id run function space_editor:mask/update_region with storage space_editor:runtime currentMask
