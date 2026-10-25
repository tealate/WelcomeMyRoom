$execute as @a[nbt={UUID:[I;$(owner0),$(owner1),$(owner2),$(owner3)]}] run tellraw @s {"text": "[Space Editor] Paste完了。", "color": "green"}
data modify storage space_editor:document job.state set value "done"
