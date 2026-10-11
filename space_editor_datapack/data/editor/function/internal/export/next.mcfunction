tellraw @s [{text:"SE_OBJECT "},{nbt:"export[0]",storage:"editor:runtime"}]
data remove storage editor:runtime export[0]
execute if data storage editor:runtime export[0] run function editor:internal/export/next
