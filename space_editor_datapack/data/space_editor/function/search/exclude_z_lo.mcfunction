execute store result score #cert_bound pr.v run data get storage space_editor:projection route.searchCert.zlo
scoreboard players operation #cert_bound pr.v > #bound pr.v
execute store result storage space_editor:projection route.searchCert.zlo int 1 run scoreboard players get #cert_bound pr.v
