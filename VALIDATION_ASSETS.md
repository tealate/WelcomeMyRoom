# Space Editor アセット検証

- Parsed 21 JSON/mcmeta files
- 5 maskable textures: exact RGB/pixel checks and no-op dry-run passed
- Mask body alpha={1}; selection and guide alpha={0,255}
- All custom model/texture references resolved
- All references among 102 functions resolved

## PNG（すべて独立した配布用リソースパック内）

- `space_editor_resources/assets/editor/textures/block/stone_maskable.png` — 既存の複製元に部分αがあるため、追加のピクセル変更はスキップ
- `space_editor_resources/assets/editor/textures/block/dirt_maskable.png` — 1ピクセルだけα255→254、RGBおよび他のαは保持
- `space_editor_resources/assets/editor/textures/block/oak_maskable.png` — 1ピクセルだけα255→254、RGBおよび他のαは保持
- `space_editor_resources/assets/editor/textures/block/bricks_maskable.png` — 1ピクセルだけα255→254、RGBおよび他のαは保持
- `space_editor_resources/assets/editor/textures/block/quartz_maskable.png` — 1ピクセルだけα255→254、RGBおよび他のαは保持
- `space_editor_resources/assets/editor/textures/block/mask_body.png` — 新規の描画用画像。全画素α1
- `space_editor_resources/assets/editor/textures/block/selection.png` — 新規の線表示画像。α0/255のみ
- `space_editor_resources/assets/editor/textures/block/guide.png` — 新規の線表示画像。α0/255のみ

## JSON / pack.mcmeta

- `space_editor_datapack/data/editor/tags/block/ray_pass.json`
- `space_editor_datapack/data/minecraft/tags/function/load.json`
- `space_editor_datapack/data/minecraft/tags/function/tick.json`
- `space_editor_datapack/pack.mcmeta`
- `space_editor_resources/assets/editor/models/block/bricks_maskable.json`
- `space_editor_resources/assets/editor/models/block/dirt_maskable.json`
- `space_editor_resources/assets/editor/models/block/guide.json`
- `space_editor_resources/assets/editor/models/block/mask_body.json`
- `space_editor_resources/assets/editor/models/block/oak_maskable.json`
- `space_editor_resources/assets/editor/models/block/quartz_maskable.json`
- `space_editor_resources/assets/editor/models/block/selection.json`
- `space_editor_resources/assets/editor/models/block/stone_maskable.json`
- `space_editor_resources/assets/minecraft/blockstates/blue_terracotta.json`
- `space_editor_resources/assets/minecraft/blockstates/brown_terracotta.json`
- `space_editor_resources/assets/minecraft/blockstates/lime_glazed_terracotta.json`
- `space_editor_resources/assets/minecraft/blockstates/magenta_glazed_terracotta.json`
- `space_editor_resources/assets/minecraft/blockstates/orange_terracotta.json`
- `space_editor_resources/assets/minecraft/blockstates/red_terracotta.json`
- `space_editor_resources/assets/minecraft/blockstates/waxed_oxidized_cut_copper.json`
- `space_editor_resources/assets/minecraft/blockstates/white_terracotta.json`
- `space_editor_resources/pack.mcmeta`

上記は初回生成時の一覧です。2026-09-11に以下の有効パックへの反映を追加しました。

## 2026-09-11 有効なtestpackへの反映

Space Editorをゲームが読み込めるよう、以下24ファイルをルートassets/へ反映しました。
JSON16ファイルは解析済み、PNG8ファイルは検証済み生成元とバイト一致。
Mask対象PNG5ファイルのdry-runは全てalready-translucentで、追加の画像変更はありません。
元のバニラテクスチャ・シェーダー・pack.mcmetaは変更していません。ZIPは更新していません。

- `assets/editor/models/block/bricks_maskable.json`
- `assets/editor/models/block/dirt_maskable.json`
- `assets/editor/models/block/guide.json`
- `assets/editor/models/block/mask_body.json`
- `assets/editor/models/block/oak_maskable.json`
- `assets/editor/models/block/quartz_maskable.json`
- `assets/editor/models/block/selection.json`
- `assets/editor/models/block/stone_maskable.json`
- `assets/editor/textures/block/bricks_maskable.png`
- `assets/editor/textures/block/dirt_maskable.png`
- `assets/editor/textures/block/guide.png`
- `assets/editor/textures/block/mask_body.png`
- `assets/editor/textures/block/oak_maskable.png`
- `assets/editor/textures/block/quartz_maskable.png`
- `assets/editor/textures/block/selection.png`
- `assets/editor/textures/block/stone_maskable.png`
- `assets/minecraft/blockstates/blue_terracotta.json`
- `assets/minecraft/blockstates/brown_terracotta.json`
- `assets/minecraft/blockstates/lime_glazed_terracotta.json`
- `assets/minecraft/blockstates/magenta_glazed_terracotta.json`
- `assets/minecraft/blockstates/orange_terracotta.json`
- `assets/minecraft/blockstates/red_terracotta.json`
- `assets/minecraft/blockstates/waxed_oxidized_cut_copper.json`
- `assets/minecraft/blockstates/white_terracotta.json`
