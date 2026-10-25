$data modify storage space_editor:runtime template set from storage space_editor:document templates[{id:$(id)}]
execute unless data storage space_editor:runtime template.id run return run tellraw @s {"text": "[Space Editor] TemplateIDが見つかりません。", "color": "red"}
function space_editor:template/give with storage space_editor:runtime template
