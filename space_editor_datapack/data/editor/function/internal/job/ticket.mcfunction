$execute in $(dim) store success score #exists se run forceload query $(x) $(z)
execute if score #exists se matches 1 run return 0
$execute in $(dim) store success score #added se run forceload add $(x) $(z)
execute if score #added se matches 1 run data modify storage editor:runtime job.tickets append from storage editor:runtime ticket
