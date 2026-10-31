$execute store result score #height pr.v run data get storage space_editor:document projection.visual.$(pose)
execute store result score #y pr.v run data get storage space_editor:projection render.y 2000
scoreboard players operation #offset pr.v = #height pr.v
scoreboard players operation #offset pr.v += #height pr.v
execute if score #flip pr.v matches 1 run scoreboard players operation #y pr.v -= #offset pr.v
execute store result storage space_editor:projection render.y double 0.0005 run scoreboard players get #y pr.v
scoreboard players operation #nameY pr.v = #y pr.v
execute store result score #gap pr.v run data get storage space_editor:document projection.labelGap 2
execute if score #flip pr.v matches 0 run scoreboard players operation #nameY pr.v += #offset pr.v
execute if score #flip pr.v matches 0 run scoreboard players remove #nameY pr.v 200
execute if score #flip pr.v matches 0 run scoreboard players operation #nameY pr.v += #gap pr.v
execute if score #flip pr.v matches 1 run scoreboard players operation #nameY pr.v -= #gap pr.v
execute if score #flip pr.v matches 1 run scoreboard players add #nameY pr.v 200
execute store result storage space_editor:projection render.nameY double 0.0005 run scoreboard players get #nameY pr.v
