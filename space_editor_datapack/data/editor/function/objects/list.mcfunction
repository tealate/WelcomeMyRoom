data modify storage editor:runtime list set from storage editor:data document.objects
execute unless data storage editor:runtime list[0] run return run tellraw @s {text:"登録はまだありません。",color:"gray"}
function editor:internal/list/next
