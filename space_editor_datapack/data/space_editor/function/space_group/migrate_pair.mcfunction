data modify storage space_editor:runtime sg set value {group:{members:[]},before:{},after:[]}
scoreboard players set #sg_unique se.v 1
data modify storage space_editor:runtime sgUnique set value []
$data modify storage space_editor:runtime sgUnique append from storage space_editor:document regionPairs[{id:$(id)}]
execute store result score #sg_n se.v run data get storage space_editor:runtime sgUnique
execute unless score #sg_n se.v matches 1 run scoreboard players set #sg_unique se.v 0
data modify storage space_editor:runtime sgUnique set value []
$data modify storage space_editor:runtime sgUnique append from storage space_editor:document regions[{id:$(a)}]
execute store result score #sg_n se.v run data get storage space_editor:runtime sgUnique
execute unless score #sg_n se.v matches 1 run scoreboard players set #sg_unique se.v 0
data modify storage space_editor:runtime sgUnique set value []
$data modify storage space_editor:runtime sgUnique append from storage space_editor:document regions[{id:$(b)}]
execute store result score #sg_n se.v run data get storage space_editor:runtime sgUnique
execute unless score #sg_n se.v matches 1 run scoreboard players set #sg_unique se.v 0
execute unless score #sg_unique se.v matches 1 run return run function space_editor:space_group/migration_warning
data remove storage space_editor:runtime sgA
data remove storage space_editor:runtime sgB
$data modify storage space_editor:runtime sgA set from storage space_editor:document regions[{id:$(a),kind:"space_link",pairId:$(id),partnerId:$(b)}]
$data modify storage space_editor:runtime sgB set from storage space_editor:document regions[{id:$(b),kind:"space_link",pairId:$(id),partnerId:$(a)}]
execute unless data storage space_editor:runtime sgA.id run return run function space_editor:space_group/migration_warning
execute unless data storage space_editor:runtime sgB.id run return run function space_editor:space_group/migration_warning
execute if data storage space_editor:runtime sgA.spaceLinkGroupId run return run function space_editor:space_group/migration_warning
execute if data storage space_editor:runtime sgB.spaceLinkGroupId run return run function space_editor:space_group/migration_warning
$execute if data storage space_editor:runtime sgA{id:$(b)} run return run function space_editor:space_group/migration_warning
data modify storage space_editor:runtime frame set from storage space_editor:runtime sgA
function space_editor:pair/frame
execute unless score #frame_ok se.v matches 1 run return run function space_editor:space_group/migration_warning
data modify storage space_editor:runtime sg.group.localSize set from storage space_editor:runtime frame.localSize
scoreboard players set #sg_ok se.v 1
function space_editor:space_group/validate_frame
data modify storage space_editor:runtime frame set from storage space_editor:runtime sgB
function space_editor:space_group/validate_frame
execute unless score #sg_ok se.v matches 1 run return run function space_editor:space_group/migration_warning
data modify storage space_editor:runtime sg.before.legacyPair set from storage space_editor:runtime sgLegacy
data modify storage space_editor:runtime sg.before.regions set value []
data modify storage space_editor:runtime sg.before.regions append from storage space_editor:runtime sgA
data modify storage space_editor:runtime sg.before.regions append from storage space_editor:runtime sgB
function space_editor:space_group/allocate
execute unless score #sg_ok se.v matches 1 run return run function space_editor:space_group/migration_warning
$data modify storage space_editor:runtime sg.group.members set value [$(a),$(b)]
data modify storage space_editor:runtime sg.after set from storage space_editor:runtime sg.before.regions
data modify storage space_editor:runtime sg.operation set value "migrate"
function space_editor:space_group/identify_all
function space_editor:space_group/store
$data modify storage space_editor:document regionPairs[{id:$(id)}].spaceLinkGroupId set from storage space_editor:runtime sg.group.id
function space_editor:space_group/action
