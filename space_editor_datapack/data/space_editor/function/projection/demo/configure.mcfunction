$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(ea)}]
function space_editor:pair/mark_existence
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(eb)}]
function space_editor:pair/mark_existence
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(ec)}]
function space_editor:pair/mark_existence
$function space_editor:projection/debug/map {target:$(b),region:$(db)}
$function space_editor:projection/debug/map {target:$(c),region:$(dc)}
