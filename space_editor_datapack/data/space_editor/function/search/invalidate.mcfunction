scoreboard players add #revision pr.v 1
data modify storage space_editor:search index set value []
data remove storage space_editor:search building
data modify storage space_editor:search existence set value []
data modify storage space_editor:search areas set value []
data modify storage space_editor:search existence append from storage space_editor:search snapshot[{kind:"proxy_existence"}]
data modify storage space_editor:search areas append from storage space_editor:search snapshot[{kind:"search_area"}]
data modify storage space_editor:search buildAreas set from storage space_editor:search areas
