data remove storage space_editor:runtime pairPending
data modify storage space_editor:runtime pairSession.mode set value "pose"
tellraw @s {"text": "[Space Editor] 既存Regionの姿勢編集。Shift+右クリック: 回転/FlipY。通常クリック: 連続追加へ。", "color": "green"}
