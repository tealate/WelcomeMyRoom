tellraw @s {"text": "[Space Editor] 開始: /function space_editor:start  プレイ: /function space_editor:play", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 増減量: /function space_editor:set_step {amount:0.1}", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 一時選択解除: /function space_editor:selection/clear  再同期: /function space_editor:resume", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 範囲移動棒: 見ている面方向へ1ブロック移動。Shiftで反対方向。", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Fill: Region選択→ブロックをメインハンド→/function space_editor:fill", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Fill: Fill棒＋オフハンド素材 / Copy: コピー棒 / Paste: ペースト棒＋オフハンドTemplate", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Fill/Paste棒は範囲棒と同じ3ブロック候補を使用。ブロックがなければ空中セルを選択します。", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Pasteは1回目で範囲表示、2回目で確定。キャンセル: /function space_editor:paste/cancel", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Job: /function space_editor:job/pause | resume | retry | cancel", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 再発行: /function space_editor:template/reissue {id:1}", "color": "aqua"}
tellraw @s {"text": "[Space Editor] Paste変換: 棒を持った時の正面を基準にShift＋左/右で90度回転、Shift＋上/下でFlipY。", "color": "aqua"}
tellraw @s {"text": "[Space Editor] 変換設定は棒を持ち替えると0度 / FlipY OFFへ戻ります。キャンセル: /function space_editor:paste/cancel", "color": "aqua"}
