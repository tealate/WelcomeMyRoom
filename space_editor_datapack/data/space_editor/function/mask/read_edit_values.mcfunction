scoreboard players set #mask_input_valid se.v 1
execute store result score #mask_input_x se.v run data get storage space_editor:runtime maskEdit.values[0] 1000
execute unless score #mask_input_x se.v matches -16000..16000 run scoreboard players set #mask_input_valid se.v 0
execute store result storage space_editor:runtime maskEdit.fixed[0] int 1 run scoreboard players get #mask_input_x se.v
execute store result score #mask_input_y se.v run data get storage space_editor:runtime maskEdit.values[1] 1000
execute unless score #mask_input_y se.v matches -16000..16000 run scoreboard players set #mask_input_valid se.v 0
execute store result storage space_editor:runtime maskEdit.fixed[1] int 1 run scoreboard players get #mask_input_y se.v
execute store result score #mask_input_z se.v run data get storage space_editor:runtime maskEdit.values[2] 1000
execute unless score #mask_input_z se.v matches -16000..16000 run scoreboard players set #mask_input_valid se.v 0
execute store result storage space_editor:runtime maskEdit.fixed[2] int 1 run scoreboard players get #mask_input_z se.v
