scoreboard players remove #bound pr.v 1
execute store result score #cert_bound pr.v run data get storage space_editor:projection route.searchCert.zhi
scoreboard players operation #cert_bound pr.v < #bound pr.v
execute store result storage space_editor:projection route.searchCert.zhi int 1 run scoreboard players get #cert_bound pr.v
