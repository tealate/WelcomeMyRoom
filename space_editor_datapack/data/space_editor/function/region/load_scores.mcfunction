execute store result score #id se.v run data get storage space_editor:runtime hit.id 1
execute store result score #step se.v run data get storage space_editor:document settings.stepMilli 1
scoreboard players set #direction se.v 1
execute if predicate {condition:"minecraft:entity_properties",entity:"this",predicate:{flags:{is_sneaking:true}}} run scoreboard players set #direction se.v -1
scoreboard players operation #delta se.v = #step se.v
scoreboard players operation #delta se.v *= #direction se.v
execute store result score #x1 se.v run data get storage space_editor:runtime hit.x1m 1
execute store result score #x2 se.v run data get storage space_editor:runtime hit.x2m 1
execute store result score #y1 se.v run data get storage space_editor:runtime hit.y1m 1
execute store result score #y2 se.v run data get storage space_editor:runtime hit.y2m 1
execute store result score #z1 se.v run data get storage space_editor:runtime hit.z1m 1
execute store result score #z2 se.v run data get storage space_editor:runtime hit.z2m 1
