function space_editor:selection/track
data modify storage space_editor:runtime frame set from storage space_editor:runtime pairPending.frame
data modify storage space_editor:runtime frame.dimension set from storage space_editor:runtime hover.dimension
execute store result storage space_editor:runtime frame.rotationY int 1 run scoreboard players get @s se.prot
execute store result storage space_editor:runtime frame.flipY byte 1 run scoreboard players get @s se.pflip
execute if data storage space_editor:runtime frame{rotationY:0} store result score #psx se.v run data get storage space_editor:runtime frame.localSize[0] 1
execute if data storage space_editor:runtime frame{rotationY:0} store result score #psy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:0} store result score #psz se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:90} store result score #psx se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:90} store result score #psy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:90} store result score #psz se.v run data get storage space_editor:runtime frame.localSize[0] 1
execute if data storage space_editor:runtime frame{rotationY:180} store result score #psx se.v run data get storage space_editor:runtime frame.localSize[0] 1
execute if data storage space_editor:runtime frame{rotationY:180} store result score #psy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:180} store result score #psz se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:270} store result score #psx se.v run data get storage space_editor:runtime frame.localSize[2] 1
execute if data storage space_editor:runtime frame{rotationY:270} store result score #psy se.v run data get storage space_editor:runtime frame.localSize[1] 1
execute if data storage space_editor:runtime frame{rotationY:270} store result score #psz se.v run data get storage space_editor:runtime frame.localSize[0] 1
execute store result score #pp se.v run data get storage space_editor:runtime hover.pos[0] 1000
execute store result storage space_editor:runtime frame.x1m int 1 run scoreboard players get #pp se.v
scoreboard players operation #pp se.v += #psx se.v
execute store result storage space_editor:runtime frame.x2m int 1 run scoreboard players get #pp se.v
execute store result score #pp se.v run data get storage space_editor:runtime hover.pos[1] 1000
execute store result storage space_editor:runtime frame.y1m int 1 run scoreboard players get #pp se.v
scoreboard players operation #pp se.v += #psy se.v
execute store result storage space_editor:runtime frame.y2m int 1 run scoreboard players get #pp se.v
execute store result score #pp se.v run data get storage space_editor:runtime hover.pos[2] 1000
execute store result storage space_editor:runtime frame.z1m int 1 run scoreboard players get #pp se.v
scoreboard players operation #pp se.v += #psz se.v
execute store result storage space_editor:runtime frame.z2m int 1 run scoreboard players get #pp se.v
function space_editor:pair/frame
data modify storage space_editor:runtime pairCandidate set from storage space_editor:runtime frame
data modify storage space_editor:runtime pairCandidate.kind set from storage space_editor:runtime pairPending.kind
data modify storage space_editor:runtime pairCandidate.side set value "B preview"
data modify storage space_editor:runtime pairCandidate.pairId set value 0
function space_editor:pair/preview_pending with storage space_editor:runtime pairCandidate
