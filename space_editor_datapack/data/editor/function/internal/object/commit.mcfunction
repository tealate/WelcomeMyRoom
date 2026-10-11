execute if data storage editor:data document.objects[511] run return run tellraw @s {text:"この版の登録上限は512件です。",color:"red"}
function editor:internal/history/save
data modify storage editor:data document.objects append from storage editor:runtime object
execute if data storage editor:runtime object{type:"block_fill"} run data modify storage editor:data footprints append from storage editor:runtime object
execute store result score #next se run data get storage editor:data next_id
scoreboard players add #next se 1
execute store result storage editor:data next_id int 1 run scoreboard players get #next se
execute unless data storage editor:runtime object{type:"block_fill"} run data modify storage editor:data display_footprints append from storage editor:runtime object
function editor:internal/revision
data modify storage editor:runtime job set value {queue:[],tickets:[],wait:0,phase:"next"}
data modify storage editor:runtime job.queue append from storage editor:runtime object
data modify storage editor:data build_state set value "pending"
tellraw @s {"text": "[Space Editor] 配置を記録しました。チャンクを読み込み、ワールドに反映します。", "color": "aqua"}
