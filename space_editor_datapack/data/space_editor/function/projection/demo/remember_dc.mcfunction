$execute if data storage space_editor:document regions[{id:$(dc)}] run data modify storage space_editor:projection demo.ids append value {id:$(dc)}
data modify storage space_editor:document projection.demo set from storage space_editor:projection demo
