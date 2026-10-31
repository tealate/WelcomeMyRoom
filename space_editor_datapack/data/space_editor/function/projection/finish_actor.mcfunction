$execute unless entity @a[scores={pr.owner=$(id)},nbt={UUID:$(uuid),DeathTime:0s},gamemode=!spectator] run function space_editor:projection/remove_owner with storage space_editor:projection actorQueue[0]
$execute unless entity @a[scores={pr.owner=$(id)},nbt={UUID:$(uuid),DeathTime:0s},gamemode=!spectator] run data remove storage space_editor:projection active[{owner:$(id)}]
$execute unless entity @a[scores={pr.owner=$(id)},nbt={UUID:$(uuid),DeathTime:0s},gamemode=!spectator] run return run data remove storage space_editor:projection players[{id:$(id)}]
$data modify storage space_editor:projection players[{id:$(id)}].previous set from storage space_editor:projection players[{id:$(id)}].next
