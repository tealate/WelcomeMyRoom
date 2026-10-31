data modify storage space_editor:projection demo.tb set from storage space_editor:document nextId
$data modify storage space_editor:runtime pairCandidate set from storage space_editor:document regions[{id:$(b)}]
data remove storage space_editor:runtime pairCandidate.spaceLinkGroupId
data remove storage space_editor:runtime pairCandidate.kind
$function space_editor:pair/create {source:$(ta),kind:"teleport"}
function space_editor:projection/demo/remember_tb with storage space_editor:projection demo
$data modify storage space_editor:projection tpConfig set from storage space_editor:document regions[{id:$(ta)}]
$data modify storage space_editor:projection tpConfig.roomA set value "stage6_demo_$(a)_a"
$data modify storage space_editor:projection tpConfig.roomB set value "stage6_demo_$(a)_b"
function space_editor:projection/demo/tp_configure with storage space_editor:projection tpConfig
