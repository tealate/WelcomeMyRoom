$execute unless entity @a[scores={pr.owner=$(owner)},gamemode=!spectator,nbt={DeathTime:0s}] run return run kill @s
$execute unless data storage space_editor:projection active[{id:$(id),owner:$(owner)}] run kill @s
