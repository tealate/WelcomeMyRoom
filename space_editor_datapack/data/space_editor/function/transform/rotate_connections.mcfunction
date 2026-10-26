data modify storage space_editor:runtime connectionSource set from storage space_editor:runtime transformState
execute if score #rotation se.v matches 90 run function space_editor:transform/connections_90
execute if score #rotation se.v matches 180 run function space_editor:transform/connections_180
execute if score #rotation se.v matches 270 run function space_editor:transform/connections_270
