data remove storage space_editor:runtime pairPending
data remove storage space_editor:runtime pairSession
data remove storage space_editor:runtime pairCandidate
scoreboard players set @a se.pheld 0
execute in minecraft:overworld run kill @e[tag=space_editor.pair_pending]
execute in minecraft:the_nether run kill @e[tag=space_editor.pair_pending]
execute in minecraft:the_end run kill @e[tag=space_editor.pair_pending]
