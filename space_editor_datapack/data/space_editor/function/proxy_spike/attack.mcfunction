advancement revoke @s only space_editor:proxy_spike/attack
execute if entity @s[tag=sp.active,scores={sp.follow=1}] at @s run function space_editor:proxy_spike/swing_main
