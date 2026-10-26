scoreboard players add @s se.rot 0
scoreboard players add @s se.flip 0
execute store result storage space_editor:runtime pastePending.rotation int 1 run scoreboard players get @s se.rot
execute store result storage space_editor:runtime pastePending.flipY byte 1 run scoreboard players get @s se.flip
data modify storage space_editor:runtime pastePending.sx set from storage space_editor:runtime pastePending.w
data modify storage space_editor:runtime pastePending.sy set from storage space_editor:runtime pastePending.h
data modify storage space_editor:runtime pastePending.sz set from storage space_editor:runtime pastePending.d
execute if score @s se.rot matches 90 if data storage space_editor:runtime pastePending run function space_editor:paste/swap_preview_xz
execute if score @s se.rot matches 270 if data storage space_editor:runtime pastePending run function space_editor:paste/swap_preview_xz
function space_editor:preview/resync
