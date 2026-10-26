scoreboard players set #direction se.v 1
execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run scoreboard players set #direction se.v -1
execute store result score #x se.v run data get storage space_editor:runtime pastePending.x 1
execute store result score #y se.v run data get storage space_editor:runtime pastePending.y 1
execute store result score #z se.v run data get storage space_editor:runtime pastePending.z 1
execute if data storage space_editor:runtime {hitFace:0} run scoreboard players remove #x se.v 1
execute if data storage space_editor:runtime {hitFace:0} if score #direction se.v matches -1 run scoreboard players add #x se.v 2
execute if data storage space_editor:runtime {hitFace:1} run scoreboard players add #x se.v 1
execute if data storage space_editor:runtime {hitFace:1} if score #direction se.v matches -1 run scoreboard players remove #x se.v 2
execute if data storage space_editor:runtime {hitFace:2} run scoreboard players remove #y se.v 1
execute if data storage space_editor:runtime {hitFace:2} if score #direction se.v matches -1 run scoreboard players add #y se.v 2
execute if data storage space_editor:runtime {hitFace:3} run scoreboard players add #y se.v 1
execute if data storage space_editor:runtime {hitFace:3} if score #direction se.v matches -1 run scoreboard players remove #y se.v 2
execute if data storage space_editor:runtime {hitFace:4} run scoreboard players remove #z se.v 1
execute if data storage space_editor:runtime {hitFace:4} if score #direction se.v matches -1 run scoreboard players add #z se.v 2
execute if data storage space_editor:runtime {hitFace:5} run scoreboard players add #z se.v 1
execute if data storage space_editor:runtime {hitFace:5} if score #direction se.v matches -1 run scoreboard players remove #z se.v 2
execute store result score #y2 se.v run data get storage space_editor:runtime pastePending.sy 1
scoreboard players operation #y2 se.v += #y se.v
execute if data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y se.v matches -64..319 run return run tellraw @s {"text": "[Space Editor] Overworldの高さ範囲を超えています。", "color": "red"}
execute if data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y2 se.v matches -63..320 run return run tellraw @s {"text": "[Space Editor] Overworldの高さ範囲を超えています。", "color": "red"}
execute unless data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y se.v matches 0..255 run return run tellraw @s {"text": "[Space Editor] Nether/Endの高さ範囲を超えています。", "color": "red"}
execute unless data storage space_editor:runtime pastePending{targetDimension:"minecraft:overworld"} unless score #y2 se.v matches 1..256 run return run tellraw @s {"text": "[Space Editor] Nether/Endの高さ範囲を超えています。", "color": "red"}
execute store result storage space_editor:runtime pastePending.x int 1 run scoreboard players get #x se.v
execute store result storage space_editor:runtime pastePending.y int 1 run scoreboard players get #y se.v
execute store result storage space_editor:runtime pastePending.z int 1 run scoreboard players get #z se.v
data remove storage space_editor:runtime hit
function space_editor:preview/resync
tellraw @s {"text": "[Space Editor] Pasteプレビューを1ブロック移動しました。", "color": "green"}
