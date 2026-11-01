data modify storage space_editor:search queryAreas set value []
$data modify storage space_editor:search queryAreas append from storage space_editor:search index[{dimension:"$(dimension)",complete:1b}]
data remove storage space_editor:search chosen
function space_editor:search/choose_area
data modify storage space_editor:projection route.searchQueue set value []
execute if data storage space_editor:search chosen run data modify storage space_editor:projection route.searchQueue set from storage space_editor:search chosen.candidates
$execute unless data storage space_editor:search chosen run data modify storage space_editor:projection route.searchQueue append from storage space_editor:search existence[{dimension:"$(dimension)"}]
data modify storage space_editor:projection route.searchCert set value {xlo:-2147483648,xhi:2147483647,ylo:-2147483648,yhi:2147483647,zlo:-2147483648,zhi:2147483647}
execute if data storage space_editor:search chosen run function space_editor:search/cert_area
