execute if score @s se.intent matches 1 run function space_editor:paste_mode/rotate_left
execute if score @s se.intent matches 2 run function space_editor:paste_mode/rotate_right
execute if score @s se.intent matches 3 run function space_editor:paste_mode/toggle_flip
execute if data storage space_editor:runtime pastePending run function space_editor:paste/update_pending_transform
function space_editor:paste_mode/actionbar
