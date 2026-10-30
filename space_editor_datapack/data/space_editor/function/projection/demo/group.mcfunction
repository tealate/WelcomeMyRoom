data modify storage space_editor:projection demo.b set from storage space_editor:document nextId
$data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:$(a)}]
data remove storage space_editor:runtime pairCandidate.spaceLinkGroupId
data remove storage space_editor:runtime pairCandidate.kind
data modify storage space_editor:runtime pairCandidate.rotationY set value 90
data modify storage space_editor:runtime pairCandidate.flipY set value 1b
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 12
execute store result storage space_editor:runtime pairCandidate.x1m int 1000 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 16
execute store result storage space_editor:runtime pairCandidate.x2m int 1000 run scoreboard players get #demo_tmp pr.v
$function space_editor:space_group/add {source:$(a)}
function space_editor:projection/demo/remember_b with storage space_editor:projection demo
data modify storage space_editor:projection demo.c set from storage space_editor:document nextId
$data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:$(a)}]
data remove storage space_editor:runtime pairCandidate.spaceLinkGroupId
data remove storage space_editor:runtime pairCandidate.kind
data modify storage space_editor:runtime pairCandidate.rotationY set value 180
data modify storage space_editor:runtime pairCandidate.flipY set value 1b
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 24
execute store result storage space_editor:runtime pairCandidate.x1m int 1000 run scoreboard players get #demo_tmp pr.v
scoreboard players operation #demo_tmp pr.v = #demo_x pr.v
scoreboard players add #demo_tmp pr.v 28
execute store result storage space_editor:runtime pairCandidate.x2m int 1000 run scoreboard players get #demo_tmp pr.v
$function space_editor:space_group/add {source:$(a)}
function space_editor:projection/demo/remember_c with storage space_editor:projection demo
