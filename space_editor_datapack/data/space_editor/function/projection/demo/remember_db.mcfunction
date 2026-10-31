$execute if data storage space_editor:document regions[{id:$(db)}] run data modify storage space_editor:projection demo.ids append value {id:$(db)}
data modify storage space_editor:document projection.demo set from storage space_editor:projection demo
