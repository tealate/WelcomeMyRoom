scoreboard players add #revision pr.v 0
scoreboard players set #changed pr.v 0
execute if data storage space_editor:document regions store success score #changed pr.v run data modify storage space_editor:search snapshot set from storage space_editor:document regions
execute unless data storage space_editor:document regions store success score #changed pr.v run data modify storage space_editor:search snapshot set value []
execute if score #changed pr.v matches 1 run function space_editor:search/invalidate
scoreboard players set #search_budget pr.v 64
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
execute if data storage space_editor:search buildAreas[0] run function space_editor:search/build_step
