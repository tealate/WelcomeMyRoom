data modify storage space_editor:runtime template set value {id:0,version:1,archive:{dimension:"",x:0,y:0,z:0},size:[I;0,0,0],source:{},rotation:0,flipY:0b}
data modify storage space_editor:runtime template.id set from storage space_editor:document job.id
data modify storage space_editor:runtime template.version set from storage space_editor:document job.version
data modify storage space_editor:runtime template.archive set value {dimension:"",x:0,y:0,z:0}
data modify storage space_editor:runtime template.archive.dimension set from storage space_editor:document job.targetDimension
data modify storage space_editor:runtime template.archive.x set from storage space_editor:document job.targetX
data modify storage space_editor:runtime template.archive.y set from storage space_editor:document job.targetY
data modify storage space_editor:runtime template.archive.z set from storage space_editor:document job.targetZ
data modify storage space_editor:runtime template.size set value [I;0,0,0]
data modify storage space_editor:runtime template.size[0] set from storage space_editor:document job.sx
data modify storage space_editor:runtime template.size[1] set from storage space_editor:document job.sy
data modify storage space_editor:runtime template.size[2] set from storage space_editor:document job.sz
data modify storage space_editor:runtime template.source set from storage space_editor:document job.sourceRegion
data modify storage space_editor:document templates append from storage space_editor:runtime template
data modify storage space_editor:document job.state set value "awaiting_item"
function space_editor:copy/try_issue
