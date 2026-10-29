scoreboard players set #session_owner se.v 0
data modify storage space_editor:runtime ownerLookup.uuid set from entity @s UUID
function space_editor:space_group/owner_match with storage space_editor:runtime ownerLookup
