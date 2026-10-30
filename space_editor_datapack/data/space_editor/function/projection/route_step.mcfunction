data modify storage space_editor:projection route set from storage space_editor:projection work[0]
data remove storage space_editor:projection work[0]
scoreboard players set #valid pr.v 0
function space_editor:projection/route_actor with storage space_editor:projection route
execute if score #valid pr.v matches 1 run data modify storage space_editor:projection done append from storage space_editor:projection route
execute unless score #valid pr.v matches 1 run function space_editor:projection/remove_render with storage space_editor:projection route
