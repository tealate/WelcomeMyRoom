scoreboard players set @s se.cd 5
execute if data storage space_editor:document settings{regionsVisible:1b} run return run function space_editor:region/display/hide
function space_editor:region/display/show
