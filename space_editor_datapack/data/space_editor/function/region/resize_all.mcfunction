scoreboard players set #region_max se.v 128000
execute if data storage space_editor:runtime hit{kind:"space_link"} run scoreboard players set #region_max se.v 128000
execute if data storage space_editor:runtime hit{kind:"proxy_existence"} run scoreboard players set #region_max se.v 128000
execute if data storage space_editor:runtime hit{kind:"search_area"} run scoreboard players set #region_max se.v 1024000
function space_editor:region/load_scores
scoreboard players operation #x1 se.v -= #delta se.v
scoreboard players operation #x2 se.v += #delta se.v
scoreboard players operation #sizex se.v = #x2 se.v
scoreboard players operation #sizex se.v -= #x1 se.v
execute unless score #sizex se.v matches 100.. run return run tellraw @s {"text": "[Space Editor] 変更後の各辺は0.1〜128ブロックである必要があります。", "color": "red"}
execute if score #sizex se.v > #region_max se.v run return run tellraw @s {"text": "[Space Editor] 変更後の各辺は通常0.1〜128、SpaceLink0.1〜128、Proxy存在範囲0.1〜128、検索エリア0.1〜1024ブロックである必要があります。", "color": "red"}
scoreboard players operation #y1 se.v -= #delta se.v
scoreboard players operation #y2 se.v += #delta se.v
scoreboard players operation #sizey se.v = #y2 se.v
scoreboard players operation #sizey se.v -= #y1 se.v
execute unless score #sizey se.v matches 100.. run return run tellraw @s {"text": "[Space Editor] 変更後の各辺は0.1〜128ブロックである必要があります。", "color": "red"}
execute if score #sizey se.v > #region_max se.v run return run tellraw @s {"text": "[Space Editor] 変更後の各辺は通常0.1〜128、SpaceLink0.1〜128、Proxy存在範囲0.1〜128、検索エリア0.1〜1024ブロックである必要があります。", "color": "red"}
scoreboard players operation #z1 se.v -= #delta se.v
scoreboard players operation #z2 se.v += #delta se.v
scoreboard players operation #sizez se.v = #z2 se.v
scoreboard players operation #sizez se.v -= #z1 se.v
execute unless score #sizez se.v matches 100.. run return run tellraw @s {"text": "[Space Editor] 変更後の各辺は0.1〜128ブロックである必要があります。", "color": "red"}
execute if score #sizez se.v > #region_max se.v run return run tellraw @s {"text": "[Space Editor] 変更後の各辺は通常0.1〜128、SpaceLink0.1〜128、Proxy存在範囲0.1〜128、検索エリア0.1〜1024ブロックである必要があります。", "color": "red"}
function space_editor:region/save_resize
