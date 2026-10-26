$execute as @a[tag=!editor.editing,scores={se.cd=0}] at @s if dimension $(dim) run function editor:internal/teleport/player with storage editor:runtime volumes[0]
