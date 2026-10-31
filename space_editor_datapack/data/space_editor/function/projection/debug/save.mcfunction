$data remove storage space_editor:document projection.debugMaps[{uuid:$(uuid),targetId:$(targetId)}]
data modify storage space_editor:document projection.debugMaps append from storage space_editor:projection config
