$execute unless entity @a[scores={pr.owner=$(owner)},gamemode=!spectator,nbt={DeathTime:0s}] run return run function space_editor:projection/delete/self
$execute unless data storage space_editor:projection active[{id:$(id),owner:$(owner)}] run function space_editor:projection/delete/self
