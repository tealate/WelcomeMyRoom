$data modify storage space_editor:runtime editA.pairId set value $(id)
$data modify storage space_editor:runtime editB.pairId set value $(id)
$data modify storage space_editor:runtime editA.kind set value "$(kind)"
$data modify storage space_editor:runtime editB.kind set value "$(kind)"
$data modify storage space_editor:runtime editA.partnerId set value $(b)
$data modify storage space_editor:runtime editB.partnerId set value $(a)
data modify storage space_editor:runtime editA.side set value "A"
data modify storage space_editor:runtime editB.side set value "B"
$data modify storage space_editor:runtime editB.idText set value "region_$(b)"
execute unless data storage space_editor:runtime editA.roomId run data modify storage space_editor:runtime editA.roomId set value ""
execute unless data storage space_editor:runtime editB.roomId run data modify storage space_editor:runtime editB.roomId set value ""
