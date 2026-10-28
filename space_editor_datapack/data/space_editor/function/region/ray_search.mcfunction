scoreboard players operation #ray_mid se.v = #ray_low se.v
scoreboard players operation #ray_mid se.v += #ray_high se.v
scoreboard players operation #ray_mid se.v /= #two se.v
execute store result storage space_editor:runtime rayDistance double 0.025 run scoreboard players get #ray_mid se.v
function space_editor:region/ray_probe with storage space_editor:runtime
scoreboard players set #ray_before se.v 0
scoreboard players set #ray_after se.v 0
execute if score #px se.v < #ray_lo_x se.v if score #ray_sign_x se.v matches 1 run scoreboard players set #ray_before se.v 1
execute if score #px se.v >= #ray_hi_x se.v if score #ray_sign_x se.v matches -1 run scoreboard players set #ray_before se.v 1
execute if score #px se.v < #ray_lo_x se.v if score #ray_sign_x se.v matches -1 run scoreboard players set #ray_after se.v 1
execute if score #px se.v >= #ray_hi_x se.v if score #ray_sign_x se.v matches 1 run scoreboard players set #ray_after se.v 1
execute if score #py se.v < #ray_lo_y se.v if score #ray_sign_y se.v matches 1 run scoreboard players set #ray_before se.v 1
execute if score #py se.v >= #ray_hi_y se.v if score #ray_sign_y se.v matches -1 run scoreboard players set #ray_before se.v 1
execute if score #py se.v < #ray_lo_y se.v if score #ray_sign_y se.v matches -1 run scoreboard players set #ray_after se.v 1
execute if score #py se.v >= #ray_hi_y se.v if score #ray_sign_y se.v matches 1 run scoreboard players set #ray_after se.v 1
execute if score #pz se.v < #ray_lo_z se.v if score #ray_sign_z se.v matches 1 run scoreboard players set #ray_before se.v 1
execute if score #pz se.v >= #ray_hi_z se.v if score #ray_sign_z se.v matches -1 run scoreboard players set #ray_before se.v 1
execute if score #pz se.v < #ray_lo_z se.v if score #ray_sign_z se.v matches -1 run scoreboard players set #ray_after se.v 1
execute if score #pz se.v >= #ray_hi_z se.v if score #ray_sign_z se.v matches 1 run scoreboard players set #ray_after se.v 1
execute if score #ray_before se.v matches 1 if score #ray_after se.v matches 1 run return 0
execute if score #ray_before se.v matches 0 if score #ray_after se.v matches 0 run scoreboard players operation #ray_found se.v = #ray_mid se.v
execute if score #ray_before se.v matches 1 run scoreboard players operation #ray_low se.v = #ray_mid se.v
execute if score #ray_before se.v matches 1 run scoreboard players add #ray_low se.v 1
execute if score #ray_before se.v matches 0 run scoreboard players operation #ray_high se.v = #ray_mid se.v
execute if score #ray_before se.v matches 0 run scoreboard players remove #ray_high se.v 1
execute if score #ray_low se.v <= #ray_high se.v run function space_editor:region/ray_search
