$execute in $(dimension) positioned 0.0 0.0 0.0 positioned ~$(cx) ~$(cy) ~$(cz) run summon minecraft:text_display ~ ~0.5 ~ {Tags:["space_editor.preview","space_editor.label","space_editor.new"],text:{text:"ProxyExistence #$(id)",color:"yellow"},billboard:"center",see_through:1b}
$execute in $(dimension) run scoreboard players set @e[tag=space_editor.new] se.id $(id)
$execute in $(dimension) run tag @e[tag=space_editor.new] remove space_editor.new
