execute store result score #contact_id se.v run data get storage space_editor:runtime contactMembers[0]
execute store result score #contact_source se.v run data get storage space_editor:runtime contactSource.id
execute if score #contact_id se.v = #contact_source se.v run scoreboard players set #source_member se.v 1
data remove storage space_editor:runtime contactMembers[0]
