execute store result storage space_editor:projection route.searchCert.xlo int 1 run data get storage space_editor:search chosen.x1m 2
execute store result score #bound pr.v run data get storage space_editor:search chosen.x2m 2
scoreboard players remove #bound pr.v 1
execute store result storage space_editor:projection route.searchCert.xhi int 1 run scoreboard players get #bound pr.v
execute store result storage space_editor:projection route.searchCert.ylo int 1 run data get storage space_editor:search chosen.y1m 2
execute store result score #bound pr.v run data get storage space_editor:search chosen.y2m 2
scoreboard players remove #bound pr.v 1
execute store result storage space_editor:projection route.searchCert.yhi int 1 run scoreboard players get #bound pr.v
execute store result storage space_editor:projection route.searchCert.zlo int 1 run data get storage space_editor:search chosen.z1m 2
execute store result score #bound pr.v run data get storage space_editor:search chosen.z2m 2
scoreboard players remove #bound pr.v 1
execute store result storage space_editor:projection route.searchCert.zhi int 1 run scoreboard players get #bound pr.v
