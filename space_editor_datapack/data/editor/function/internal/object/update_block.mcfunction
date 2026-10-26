data modify storage editor:runtime object.mode set value "fill"
execute if data storage editor:runtime previous.mode run data modify storage editor:runtime object.mode set from storage editor:runtime previous.mode
data modify storage editor:runtime object.palette set from storage editor:data prefs.palette
data modify storage editor:runtime object.variant set from storage editor:data prefs.variant
