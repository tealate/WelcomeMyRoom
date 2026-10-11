execute unless entity @a[tag=!editor.editing,scores={se.cd=0}] run return 0
data modify storage editor:runtime volumes set from storage editor:data document.objects
execute if data storage editor:runtime volumes[0] run function editor:internal/teleport/next
