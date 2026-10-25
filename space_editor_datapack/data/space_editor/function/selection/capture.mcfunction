data remove storage space_editor:runtime clickDimension
execute if dimension minecraft:overworld run data modify storage space_editor:runtime clickDimension set value "minecraft:overworld"
execute if dimension minecraft:the_nether run data modify storage space_editor:runtime clickDimension set value "minecraft:the_nether"
execute if dimension minecraft:the_end run data modify storage space_editor:runtime clickDimension set value "minecraft:the_end"
execute unless data storage space_editor:runtime clickDimension run return run tellraw @s {"text": "[Space Editor] この段階は通常3ディメンションのみ対応です。", "color": "red"}
summon minecraft:marker ~ ~ ~ {Tags:["space_editor.capture"]}
data modify storage space_editor:runtime clickPos set from entity @e[type=minecraft:marker,tag=space_editor.capture,limit=1,sort=nearest] Pos
kill @e[type=minecraft:marker,tag=space_editor.capture]
execute unless data storage space_editor:runtime selection.a run return run function space_editor:selection/set_a
function space_editor:selection/set_b
