$function space_editor:space_group/set_room {id:$(a),roomId:"stage6_demo_$(a)_a"}
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(ea)}]
function space_editor:pair/mark_existence
$function space_editor:proxy_existence/set_room {id:$(ea),roomId:"stage6_demo_$(a)_a"}
$function space_editor:space_group/set_room {id:$(b),roomId:"stage6_demo_$(a)_b"}
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(eb)}]
function space_editor:pair/mark_existence
$function space_editor:proxy_existence/set_room {id:$(eb),roomId:"stage6_demo_$(a)_b"}
$function space_editor:space_group/set_room {id:$(c),roomId:"stage6_demo_$(a)_c"}
$data modify storage space_editor:runtime hit set from storage space_editor:document regions[{id:$(ec)}]
function space_editor:pair/mark_existence
$function space_editor:proxy_existence/set_room {id:$(ec),roomId:"stage6_demo_$(a)_c"}
$function space_editor:projection/debug/map {target:$(b),region:$(db)}
$function space_editor:projection/debug/map {target:$(c),region:$(dc)}
