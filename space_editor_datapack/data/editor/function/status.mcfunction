execute if data storage editor:runtime job store result storage editor:runtime remaining int 1 run data get storage editor:runtime job.queue
tellraw @s [{"text": "状態: ", "color": "gold"}, {"nbt": "build_state", "storage": "editor:data"}, {"text": " / revision="}, {"nbt": "revision", "storage": "editor:data"}]
execute if data storage editor:runtime job run tellraw @s [{"text": "残り処理数: ", "color": "yellow"}, {"nbt": "remaining", "storage": "editor:runtime"}, {"text": " / "}, {"nbt": "work.dim", "storage": "editor:runtime"}, {"text": " / "}, {"nbt": "job.phase", "storage": "editor:runtime"}]
tellraw @s [{"text": "Selection: ", "color": "aqua"}, {"nbt": "selection", "storage": "editor:data"}]
tellraw @s [{"text": "設定: ", "color": "gray"}, {"nbt": "prefs", "storage": "editor:data"}]
tellraw @s [{"text": " [停止後に再開] ", "color": "yellow", "click_event": {"action": "run_command", "command": "/function editor:build/resume"}, "hover_event": {"action": "show_text", "value": "クリックして実行"}}, {"text": " [メニュー] ", "color": "aqua", "click_event": {"action": "run_command", "command": "/function editor:menu"}, "hover_event": {"action": "show_text", "value": "クリックして実行"}}]
