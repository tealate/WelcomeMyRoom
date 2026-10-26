data modify storage editor:data prefs.ox set value 0
data modify storage editor:data prefs.oy set value 0
data modify storage editor:data prefs.oz set value 0
data modify storage editor:data prefs.ex set value 0
data modify storage editor:data prefs.ey set value 0
data modify storage editor:data prefs.ez set value 0
tellraw @s {"text": "[Space Editor] 生成補正を0に戻しました。", "color": "aqua"}
