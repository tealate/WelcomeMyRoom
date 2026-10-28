function space_editor:link/load_tp with storage space_editor:runtime validationPair
function space_editor:link/load_sl with storage space_editor:runtime peerPair
scoreboard players set #link_mismatch se.v 0
data modify storage space_editor:runtime map set value {point:[0d,0d,0d],vector:[1d,2d,3d]}
data modify storage space_editor:runtime map.source set from storage space_editor:runtime tpA
data modify storage space_editor:runtime map.target set from storage space_editor:runtime tpB
function space_editor:mapping/position
data modify storage space_editor:runtime expectedMapping set from storage space_editor:runtime map.result
data modify storage space_editor:runtime map set value {point:[0d,0d,0d],vector:[1d,2d,3d]}
data modify storage space_editor:runtime map.source set from storage space_editor:runtime slA
data modify storage space_editor:runtime map.target set from storage space_editor:runtime slB
function space_editor:mapping/position
execute store success score #link_mismatch se.v run data modify storage space_editor:runtime expectedMapping set from storage space_editor:runtime map.result
data modify storage space_editor:runtime compareDimension set from storage space_editor:runtime tpA.dimension
execute store success score #dimension_diff se.v run data modify storage space_editor:runtime compareDimension set from storage space_editor:runtime slA.dimension
execute if score #dimension_diff se.v matches 1 run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpA.x1m 1
execute store result score #outer se.v run data get storage space_editor:runtime slA.x1m 1
execute if score #inner se.v < #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpA.x2m 1
execute store result score #outer se.v run data get storage space_editor:runtime slA.x2m 1
execute if score #inner se.v > #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpA.y1m 1
execute store result score #outer se.v run data get storage space_editor:runtime slA.y1m 1
execute if score #inner se.v < #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpA.y2m 1
execute store result score #outer se.v run data get storage space_editor:runtime slA.y2m 1
execute if score #inner se.v > #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpA.z1m 1
execute store result score #outer se.v run data get storage space_editor:runtime slA.z1m 1
execute if score #inner se.v < #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpA.z2m 1
execute store result score #outer se.v run data get storage space_editor:runtime slA.z2m 1
execute if score #inner se.v > #outer se.v run scoreboard players set #link_mismatch se.v 1
data modify storage space_editor:runtime compareDimension set from storage space_editor:runtime tpB.dimension
execute store success score #dimension_diff se.v run data modify storage space_editor:runtime compareDimension set from storage space_editor:runtime slB.dimension
execute if score #dimension_diff se.v matches 1 run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpB.x1m 1
execute store result score #outer se.v run data get storage space_editor:runtime slB.x1m 1
execute if score #inner se.v < #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpB.x2m 1
execute store result score #outer se.v run data get storage space_editor:runtime slB.x2m 1
execute if score #inner se.v > #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpB.y1m 1
execute store result score #outer se.v run data get storage space_editor:runtime slB.y1m 1
execute if score #inner se.v < #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpB.y2m 1
execute store result score #outer se.v run data get storage space_editor:runtime slB.y2m 1
execute if score #inner se.v > #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpB.z1m 1
execute store result score #outer se.v run data get storage space_editor:runtime slB.z1m 1
execute if score #inner se.v < #outer se.v run scoreboard players set #link_mismatch se.v 1
execute store result score #inner se.v run data get storage space_editor:runtime tpB.z2m 1
execute store result score #outer se.v run data get storage space_editor:runtime slB.z2m 1
execute if score #inner se.v > #outer se.v run scoreboard players set #link_mismatch se.v 1
data modify storage space_editor:runtime linkWarning set value {reason:"transform_or_containment_mismatch"}
data modify storage space_editor:runtime linkWarning.teleportPairId set from storage space_editor:runtime validationPair.id
data modify storage space_editor:runtime linkWarning.spaceLinkPairId set from storage space_editor:runtime peerPair.id
execute if score #link_mismatch se.v matches 1 run data modify storage space_editor:runtime linkWarnings append from storage space_editor:runtime linkWarning
