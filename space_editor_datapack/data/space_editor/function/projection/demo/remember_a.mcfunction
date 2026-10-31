$execute if data storage space_editor:document regions[{id:$(a)}] run data modify storage space_editor:projection demo.ids append value {id:$(a)}
data modify storage space_editor:document projection.demo set from storage space_editor:projection demo
