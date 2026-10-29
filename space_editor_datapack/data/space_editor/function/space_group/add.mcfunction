scoreboard players set #pair_ok se.v 0
data remove storage space_editor:runtime sgSource
$data modify storage space_editor:runtime sgSource set from storage space_editor:document regions[{id:$(source)}]
execute unless data storage space_editor:runtime sgSource.id run return 0
execute if data storage space_editor:runtime sgSource.pairId run return run tellraw @s {"text": "[Space Editor] 旧ペアを先に/reloadで移行してください。", "color": "red"}
execute if data storage space_editor:runtime sgSource.kind unless data storage space_editor:runtime sgSource{kind:"space_link"} run return 0
execute if data storage space_editor:runtime sgSource.spaceLinkGroupId run function space_editor:space_group/load with storage space_editor:runtime sgSource
execute unless data storage space_editor:runtime sgSource.spaceLinkGroupId run function space_editor:space_group/new
execute unless score #sg_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] グループの参照・サイズ・Dimensionが不正なため変更しません。", "color": "red"}
execute if score #sg_count se.v matches 4096.. run return run tellraw @s {"text": "[Space Editor] SpaceLinkの安全走査上限4096 Regionを超えています。", "color": "red"}
data modify storage space_editor:runtime frame set from storage space_editor:runtime pairCandidate
execute if data storage space_editor:runtime frame.spaceLinkGroupId run return run tellraw @s {"text": "[Space Editor] 既存グループのRegionは取り込めません。グループ結合は行いません。", "color": "red"}
execute if data storage space_editor:runtime frame.pairId run return 0
function space_editor:space_group/validate_frame
execute unless score #sg_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] 追加候補のサイズ・位置・姿勢が不正です。", "color": "red"}
execute store result storage space_editor:runtime frame.id int 1 run data get storage space_editor:document nextId 1
function space_editor:space_group/new_id with storage space_editor:runtime frame
execute unless score #sg_ok se.v matches 1 run return 0
data modify storage space_editor:runtime sg.after set from storage space_editor:runtime sg.before.regions
data modify storage space_editor:runtime sg.after append from storage space_editor:runtime frame
data modify storage space_editor:runtime sg.group.members append from storage space_editor:runtime frame.id
data modify storage space_editor:runtime sg.operation set value "add"
function space_editor:space_group/identify_all
function space_editor:space_group/store
function space_editor:space_group/action
execute store result score #sg_next se.v run data get storage space_editor:document nextId 1
scoreboard players add #sg_next se.v 1
execute store result storage space_editor:document nextId int 1 run scoreboard players get #sg_next se.v
function space_editor:preview/resync
scoreboard players set #pair_ok se.v 1
