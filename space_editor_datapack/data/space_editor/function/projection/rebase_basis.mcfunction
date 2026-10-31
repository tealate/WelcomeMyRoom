$data modify storage space_editor:projection tpSource set from storage space_editor:document regions[{id:$(sourceRegionId)}]
$data modify storage space_editor:projection tpTarget set from storage space_editor:document regions[{id:$(targetRegionId)}]
execute store result score #desiredRot pr.v run data get storage space_editor:projection oldFrame.rotationY
execute store result score #basis pr.v run data get storage space_editor:projection tpSource.rotationY
scoreboard players operation #desiredRot pr.v -= #basis pr.v
execute store result score #basis pr.v run data get storage space_editor:projection tpTarget.rotationY
scoreboard players operation #desiredRot pr.v += #basis pr.v
scoreboard players set #circle pr.v 360
scoreboard players operation #desiredRot pr.v %= #circle pr.v
execute store result score #desiredFlip pr.v run data get storage space_editor:projection oldFrame.flipY
execute store result score #basis pr.v run data get storage space_editor:projection tpSource.flipY
scoreboard players operation #desiredFlip pr.v += #basis pr.v
execute store result score #basis pr.v run data get storage space_editor:projection tpTarget.flipY
scoreboard players operation #desiredFlip pr.v += #basis pr.v
scoreboard players set #two pr.v 2
scoreboard players operation #desiredFlip pr.v %= #two pr.v
