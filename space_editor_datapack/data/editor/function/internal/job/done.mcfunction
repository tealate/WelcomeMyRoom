data remove storage editor:runtime job
data modify storage editor:data build_state set value "clean"
data modify storage editor:data footprints set value []
data modify storage editor:data display_footprints set value []
data modify storage editor:runtime compact set from storage editor:data document.objects
execute if data storage editor:runtime compact[0] run function editor:internal/compact
function editor:internal/selection/preview
tellraw @a[tag=editor.editing] {"text": "[Space Editor] ワールドへの反映が完了しました。", "color": "green"}
