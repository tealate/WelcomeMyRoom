tellraw @s {"text": "Stage06: /function space_editor:projection/enable → space_editor:play → SpaceLinkへ外から侵入", "color": "aqua"}
tellraw @s {"text": "各SpaceLinkにspace_group/set_room、存在範囲にproxy_existence/set_roomで同じroomIdを設定", "color": "aqua"}
tellraw @s {"text": "projection/debug/map {target:3,region:7} → projection/debug/on / off", "color": "aqua"}
tellraw @s {"text": "projection/status / clear（経路と侵入履歴を初期化、内部でも再生成） / disable", "color": "aqua"}
tellraw @s {"text": "projection/visual {pose:\"standing\",pivot:1.9} は反転ピボット補正。詳細 docs/stage06-projection.md", "color": "aqua"}
tellraw @s {"text": "projection/demo/setup: 地形変更なしの3部屋検証配置 / demo/teleport: TP追加 / demo/cleanup: この配置だけ削除", "color": "aqua"}
