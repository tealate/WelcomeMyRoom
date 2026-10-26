scoreboard objectives add se dummy
scoreboard objectives add se.use minecraft.used:minecraft.carrot_on_a_stick
scoreboard objectives add se.cd dummy
scoreboard objectives add se.id dummy
scoreboard objectives add se.gen dummy
scoreboard players add #epoch se.gen 0
scoreboard players set #one se 1
scoreboard players set #16 se 16
scoreboard players set #1000 se 1000
scoreboard players add #preview_version se 0
scoreboard players set #clock se 0
scoreboard players set #enabled se 0
execute unless data storage editor:data document run function editor:internal/init
execute if data storage editor:data document{schema:1} run scoreboard players set #enabled se 1
execute unless score #enabled se matches 1 run return run tellraw @a {text:"Space Editor: 未対応の保存形式です。データは変更していません。",color:"red"}
execute unless data storage editor:data prefs run function editor:settings/reset
execute if data storage editor:runtime job run data modify storage editor:runtime job.wait set value 0
tellraw @a {"text": "[Space Editor] 準備完了。/function editor:menu で開始", "color": "aqua"}
