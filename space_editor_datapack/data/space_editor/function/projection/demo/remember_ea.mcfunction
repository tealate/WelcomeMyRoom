$execute if data storage space_editor:document regions[{id:$(ea)}] run data modify storage space_editor:projection demo.ids append value {id:$(ea)}
data modify storage space_editor:document projection.demo set from storage space_editor:projection demo
