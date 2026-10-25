tellraw @s {"text": "[Space Editor] 開始: /function space_editor:start  プレイ: /function space_editor:play", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 増減量: /function space_editor:set_step {amount:0.1}", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 一時選択解除: /function space_editor:selection/clear  再同期: /function space_editor:resume", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Fill: Region選択→ブロックをメインハンド→/function space_editor:fill", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Fill: Fill棒＋オフハンド素材 / Copy: コピー棒 / Paste: ペースト棒＋オフハンドTemplate", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Pasteは1回目で範囲表示、2回目で確定。Shift＋右クリックでキャンセル。", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Job: /function space_editor:job/pause | resume | retry | cancel", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 再発行: /function space_editor:template/reissue {id:1}", "color": "aqua"}
