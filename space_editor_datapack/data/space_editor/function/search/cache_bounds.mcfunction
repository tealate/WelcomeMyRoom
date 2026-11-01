execute store result storage space_editor:projection route.existenceCache.xlo int 1 run data get storage space_editor:runtime spatialRegion.x1m 2
execute store result score #cache_hi pr.v run data get storage space_editor:runtime spatialRegion.x2m 2
scoreboard players remove #cache_hi pr.v 1
execute store result storage space_editor:projection route.existenceCache.xhi int 1 run scoreboard players get #cache_hi pr.v
execute store result storage space_editor:projection route.existenceCache.ylo int 1 run data get storage space_editor:runtime spatialRegion.y1m 2
execute store result score #cache_hi pr.v run data get storage space_editor:runtime spatialRegion.y2m 2
scoreboard players remove #cache_hi pr.v 1
execute store result storage space_editor:projection route.existenceCache.yhi int 1 run scoreboard players get #cache_hi pr.v
execute store result storage space_editor:projection route.existenceCache.zlo int 1 run data get storage space_editor:runtime spatialRegion.z1m 2
execute store result score #cache_hi pr.v run data get storage space_editor:runtime spatialRegion.z2m 2
scoreboard players remove #cache_hi pr.v 1
execute store result storage space_editor:projection route.existenceCache.zhi int 1 run scoreboard players get #cache_hi pr.v
