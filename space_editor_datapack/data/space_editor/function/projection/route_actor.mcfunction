$execute as @a[scores={pr.owner=$(owner)},nbt={UUID:$(uuid),DeathTime:0s},gamemode=!spectator,limit=1] at @s run function space_editor:projection/update with storage space_editor:projection route
