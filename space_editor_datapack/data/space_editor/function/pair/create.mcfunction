$data modify storage space_editor:runtime requestedPairKind set value "$(kind)"
$execute if data storage space_editor:runtime {requestedPairKind:"space_link"} run return run function space_editor:space_group/add {source:$(source)}
$execute if data storage space_editor:document regions[{id:$(source)}].spaceLinkGroupId run return 0
scoreboard players set #pair_ok se.v 0
data remove storage space_editor:runtime editA
$data modify storage space_editor:runtime editA set from storage space_editor:document regions[{id:$(source)}]
execute unless data storage space_editor:runtime editA.id run return 0
execute if data storage space_editor:runtime editA.pairId run return run tellraw @s {"text": "[Space Editor] このRegionは既にペアに属しています。", "color": "red"}
execute if data storage space_editor:runtime editA{kind:"proxy_existence"} run return 0
$data modify storage space_editor:runtime pair set value {id:0,a:$(source),b:0,kind:"$(kind)",localSize:[I;0,0,0],groupId:0,roomA:"",roomB:"",direction:"both",cooldownTicks:20}
execute unless data storage space_editor:runtime pair{kind:"teleport"} unless data storage space_editor:runtime pair{kind:"space_link"} run return 0
data modify storage space_editor:runtime frame set from storage space_editor:runtime editA
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run return 0
data modify storage space_editor:runtime editA set from storage space_editor:runtime frame
data modify storage space_editor:runtime pair.localSize set from storage space_editor:runtime frame.localSize
data modify storage space_editor:runtime frame set from storage space_editor:runtime pairCandidate
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run return run tellraw @s {"text": "[Space Editor] 配置先がRegionの範囲制限を超えています。", "color": "red"}
scoreboard players set #different_size se.v 0
execute store success score #different_size se.v run data modify storage space_editor:runtime frame.localSize set from storage space_editor:runtime pair.localSize
execute if score #different_size se.v matches 1 run return run tellraw @s {"text": "[Space Editor] ローカルサイズが一致しません。", "color": "red"}
data modify storage space_editor:runtime editB set from storage space_editor:runtime frame
execute store result storage space_editor:runtime pair.id int 1 run data get storage space_editor:document nextPairId 1
execute store result storage space_editor:runtime pair.b int 1 run data get storage space_editor:document nextId 1
data modify storage space_editor:runtime editB.id set from storage space_editor:runtime pair.b
function space_editor:pair/identify with storage space_editor:runtime pair
data modify storage space_editor:runtime pairBefore set value {}
data modify storage space_editor:runtime pairOperation set value "create"
function space_editor:pair/store with storage space_editor:runtime pair
data modify storage space_editor:document regionPairs append from storage space_editor:runtime pair
execute store result score #pair_next se.v run data get storage space_editor:document nextPairId 1
scoreboard players add #pair_next se.v 1
execute store result storage space_editor:document nextPairId int 1 run scoreboard players get #pair_next se.v
execute store result score #pair_next se.v run data get storage space_editor:document nextId 1
scoreboard players add #pair_next se.v 1
execute store result storage space_editor:document nextId int 1 run scoreboard players get #pair_next se.v
function space_editor:pair/action
function space_editor:pair/cancel
function space_editor:preview/resync
scoreboard players set #pair_ok se.v 1
