data modify storage space_editor:runtime selection set value {a:[I;0,0,0],ax:0,ay:0,az:0}
data modify storage space_editor:runtime selection.dimension set from storage space_editor:runtime clickDimension
execute store result storage space_editor:runtime selection.a[0] int 1 run data get storage space_editor:runtime clickPos[0] 1
execute store result storage space_editor:runtime selection.a[1] int 1 run data get storage space_editor:runtime clickPos[1] 1
execute store result storage space_editor:runtime selection.a[2] int 1 run data get storage space_editor:runtime clickPos[2] 1
execute store result storage space_editor:runtime selection.ax int 1 run data get storage space_editor:runtime clickPos[0] 1
execute store result storage space_editor:runtime selection.ay int 1 run data get storage space_editor:runtime clickPos[1] 1
execute store result storage space_editor:runtime selection.az int 1 run data get storage space_editor:runtime clickPos[2] 1
function space_editor:preview/point
tellraw @s {"text": "[Space Editor] Aを設定しました。次の右クリックでBを設定します。", "color": "aqua"}
