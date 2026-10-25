execute unless data storage editor:spacewarp_test {running:1b} run return 0

# A player is unlocked only after leaving both 3x3x3 volumes.
tag @a[tag=swp_test_locked] add swp_test_outside
execute in minecraft:overworld at @e[type=minecraft:marker,tag=swp_test_a,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=swp_test_outside,dx=3,dy=3,dz=3] run tag @s remove swp_test_outside
execute in minecraft:overworld at @e[type=minecraft:marker,tag=swp_test_b,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=swp_test_outside,dx=3,dy=3,dz=3] run tag @s remove swp_test_outside
execute in minecraft:the_nether at @e[type=minecraft:marker,tag=swp_test_a,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=swp_test_outside,dx=3,dy=3,dz=3] run tag @s remove swp_test_outside
execute in minecraft:the_nether at @e[type=minecraft:marker,tag=swp_test_b,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=swp_test_outside,dx=3,dy=3,dz=3] run tag @s remove swp_test_outside
execute in minecraft:the_end at @e[type=minecraft:marker,tag=swp_test_a,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=swp_test_outside,dx=3,dy=3,dz=3] run tag @s remove swp_test_outside
execute in minecraft:the_end at @e[type=minecraft:marker,tag=swp_test_b,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=swp_test_outside,dx=3,dy=3,dz=3] run tag @s remove swp_test_outside
tag @a[tag=swp_test_locked,tag=swp_test_outside] remove swp_test_locked
tag @a remove swp_test_outside

# Check A first. The destination lock prevents the B check from returning the
# same player during this tick or while the player remains inside either volume.
execute in minecraft:overworld at @e[type=minecraft:marker,tag=swp_test_a,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=!swp_test_locked,dx=3,dy=3,dz=3] run function editor:test/rotate_portal/internal/a_to_b
execute in minecraft:overworld at @e[type=minecraft:marker,tag=swp_test_b,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=!swp_test_locked,dx=3,dy=3,dz=3] run function editor:test/rotate_portal/internal/b_to_a
execute in minecraft:the_nether at @e[type=minecraft:marker,tag=swp_test_a,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=!swp_test_locked,dx=3,dy=3,dz=3] run function editor:test/rotate_portal/internal/a_to_b
execute in minecraft:the_nether at @e[type=minecraft:marker,tag=swp_test_b,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=!swp_test_locked,dx=3,dy=3,dz=3] run function editor:test/rotate_portal/internal/b_to_a
execute in minecraft:the_end at @e[type=minecraft:marker,tag=swp_test_a,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=!swp_test_locked,dx=3,dy=3,dz=3] run function editor:test/rotate_portal/internal/a_to_b
execute in minecraft:the_end at @e[type=minecraft:marker,tag=swp_test_b,limit=1] positioned ~-1.5 ~-1.5 ~-1.5 as @a[tag=!swp_test_locked,dx=3,dy=3,dz=3] run function editor:test/rotate_portal/internal/b_to_a

scoreboard players add #clock swp.test 1
execute if score #clock swp.test matches 1 run function editor:test/rotate_portal/internal/visualize_all
execute if score #clock swp.test matches 4.. run scoreboard players set #clock swp.test 0
schedule function editor:test/rotate_portal/tick 1t replace
