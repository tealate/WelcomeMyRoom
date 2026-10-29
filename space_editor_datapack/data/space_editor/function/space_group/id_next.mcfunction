execute store result score #sg_existing se.v run data get storage space_editor:runtime sgIds[0].id 1
execute if score #sg_existing se.v >= #sg_id se.v run scoreboard players operation #sg_id se.v = #sg_existing se.v
execute if score #sg_existing se.v = #sg_id se.v run scoreboard players add #sg_id se.v 1
data remove storage space_editor:runtime sgIds[0]
