data modify storage editor:data history.past append value {}
data modify storage editor:data history.past[-1].objects set from storage editor:data document.objects
execute if data storage editor:data history.past[20] run data remove storage editor:data history.past[0]
data modify storage editor:data history.future set value []
