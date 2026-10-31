scoreboard players set #fill_axis se.v 0
execute if data storage space_editor:runtime {fillBlock:"minecraft:oak_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:oak_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_oak_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_oak_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:spruce_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:spruce_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_spruce_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_spruce_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:birch_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:birch_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_birch_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_birch_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:jungle_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:jungle_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_jungle_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_jungle_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:acacia_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:acacia_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_acacia_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_acacia_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:dark_oak_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:dark_oak_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_dark_oak_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_dark_oak_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:mangrove_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:mangrove_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_mangrove_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_mangrove_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:cherry_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:cherry_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_cherry_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_cherry_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:pale_oak_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:pale_oak_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_pale_oak_log"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_pale_oak_wood"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:crimson_stem"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:crimson_hyphae"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_crimson_stem"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_crimson_hyphae"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:warped_stem"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:warped_hyphae"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_warped_stem"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_warped_hyphae"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:bamboo_block"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:stripped_bamboo_block"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:hay_block"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:bone_block"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:quartz_pillar"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:purpur_pillar"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:basalt"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:polished_basalt"} run scoreboard players set #fill_axis se.v 1
execute if data storage space_editor:runtime {fillBlock:"minecraft:deepslate"} run scoreboard players set #fill_axis se.v 1
execute unless score #fill_axis se.v matches 1 run return 0
execute if entity @s[type=minecraft:player] anchored eyes positioned ^ ^ ^ run function space_editor:fill/face_from_ray
execute if data storage space_editor:runtime {hitFace:0} run data modify storage space_editor:runtime fill.axis set value "x"
execute if data storage space_editor:runtime {hitFace:1} run data modify storage space_editor:runtime fill.axis set value "x"
execute if data storage space_editor:runtime {hitFace:2} run data modify storage space_editor:runtime fill.axis set value "y"
execute if data storage space_editor:runtime {hitFace:3} run data modify storage space_editor:runtime fill.axis set value "y"
execute if data storage space_editor:runtime {hitFace:4} run data modify storage space_editor:runtime fill.axis set value "z"
execute if data storage space_editor:runtime {hitFace:5} run data modify storage space_editor:runtime fill.axis set value "z"
function space_editor:fill/orient_axis with storage space_editor:runtime fill
