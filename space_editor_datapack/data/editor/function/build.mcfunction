execute unless score #enabled se = #one se run return 0
execute if data storage editor:runtime job run return run tellraw @s {"text":"処理中です。/function editor:status で確認できます。","color":"yellow"}
scoreboard players add #epoch se.gen 1
data modify storage editor:runtime job set value {queue:[],tickets:[],wait:0,phase:"next"}
data modify storage editor:runtime clear_list set from storage editor:data footprints
execute if data storage editor:runtime clear_list[0] run function editor:internal/build/clear_list
data modify storage editor:runtime sweep_list set from storage editor:data display_footprints
execute if data storage editor:runtime sweep_list[0] run function editor:internal/build/sweep_list
data modify storage editor:runtime job.queue append from storage editor:data document.objects[]
execute in minecraft:overworld run kill @e[tag=editor.object]
execute in minecraft:the_nether run kill @e[tag=editor.object]
execute in minecraft:the_end run kill @e[tag=editor.object]
data modify storage editor:data build_state set value "pending"
tellraw @s {"text": "[Space Editor] 再構築を開始しました。配置跡を消去してデータを順番に再生します。", "color": "aqua"}
