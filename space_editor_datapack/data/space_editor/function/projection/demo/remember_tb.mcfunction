$execute if data storage space_editor:document regions[{id:$(tb)}] run data modify storage space_editor:projection demo.ids append value {id:$(tb)}
data modify storage space_editor:document projection.demo set from storage space_editor:projection demo
