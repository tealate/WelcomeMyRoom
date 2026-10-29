# 透過ペーストと液体（Minecraft Java 26.1）

`/reload` 後、`/function space_editor:start` で「透過ペースト棒」を取得する。
`custom_data.space_editor.tool` は `paste_masked`。既存の `editor:tool_paste` モデルを共有するため、
この変更に `F3+T` は不要。オフハンドには従来の Template 紙を使用し、右クリックでプレビュー、
通常右クリックで確定、Shift＋右クリックで従来の回転・FlipY操作を行う。
削除棒または `/function space_editor:paste/cancel` でキャンセルできる。

## 実装

- `pastePending.masked` → `pasteTransform.masked` → 永続 `document.job.masked` にモードを保存する。
  プレビュー作成時の棒でモードが決まり、別の棒で確定しても変わらない。
  旧テンプレートと Template 紙の識別データは変更しない。フラグのない旧Jobは通常ペーストとして動く。
- 両ペースト棒で hover・入力・プレビュー・変換セッションを共有する。
  プレビュー中に他の道具へ持ち替えた場合も、再装備時にプレビューの回転・FlipYを復元する。
- 高速経路の透過時は `clone ... strict masked force`、通常時とCopyは従来の `strict replace force`。
  全Air区画では26.1のCloneが失敗するため、失敗を一律に成功へ置き換えない。
  その区画の各セルについて、コピー元がAir 3種であることと、両座標のロード・高さ条件を確認する。
  全セルが有効な場合だけ共通の区画進行処理へ進む。
  この確認は256セル/tick、カーソルをJobへ保存し、再読み込みや再開にも対応する。
  非Airや未ロード・無効座標、区画の最小幅でもブロック変更上限を超える場合は従来のJobエラーにする。
- 変換経路は既存の64セル/tickを維持する。`transform/skip_check` でAir 3種を早期スキップし、
  Clone、BlockState補正、特殊Display削除に入らない。未対応数にも含めず、通常のカーソル進行を使う。
- `transform_allowed` に `minecraft:water` と `minecraft:lava` を追加する。
  向きの補正をせず既存の1ブロックstrict Cloneで `level` をそのまま複製する。
  Waterloggedは既存の階段・ハーフ・フェンス・壁・接続・軸系の状態変換を共有する。

## strictと液体の制限

[公式のstrict構文・更新抑制仕様](https://www.minecraft.net/en-us/article/minecraft-snapshot-25w02a)に加え、
ローカルの26.1サーバー実装とGameTestで確認した。
strict Clone直後は水源・溶岩源・流水の状態を保存するが、配置だけでは液体の流動を開始しない。
水・溶岩とも、周囲に通常のブロック更新を与えるとMinecraft標準の流動を始める。
その後の重力・流動・混合反応などで状態が変化することは通常のMinecraftの挙動となる。
既存ペーストの状態保持を維持するため、一括の更新通知や流動開始処理は追加していない。

全Airの高速区画は確認処理のため追加tickを要する（最大32³セルで128回の確認バッチ）。
既存の変換未対応ブロックは従来どおりスキップする。Waterlogged全ブロック種への対応拡張は含まない。

## 検証

生成: `python -B tools/build_space_editor_stage5.py`

- `tools/test_space_editor_paste.ps1`: 26.1 dispatcherによるValidateMinecraftと専用GameTest。
  通常/透過 × 4方向 × FlipY有無 × 混在/全Airの32ケース。
  Air 3種、水・溶岩の全16レベル、Waterlogged階段/ハーフ/チェーンの状態一致。
  実際のCopyからの保存、Air位置のチェスト/樽の内容・特殊Display UUID/保存レコード保持。
  棒の取得、プレビューから確定までの持ち替え、空区画から液体区画への進行。
  256セルの空区画確認、分割Job、実際のリソース再読み込み、変換配置中のloadと継続。
  未ロード元・高さ範囲外・非Air・ブロック変更上限によるClone失敗、strict後の液体更新を検証する。
  既定65,536コマンド上限で実行し、各Job tickのコマンド使用数も計測する。
- `tools/test_space_editor_stage3.ps1`: 既存の座標変換8状態、全階段形状4方向、FlipY特殊Display、削除、移動、再開。
- `tools/test_space_editor_stage5.ps1`: 現行Stage 05の既存回帰テスト。

上記は隔離したGameTestワールドでのサーバー実行確認。プレイヤーのライブワールドでの
アイテム表示、視線操作、プレビューの見た目と体感速度は未検証。

## 変更ファイル

- 生成元: `tools/build_space_editor_stage3.py`
- 検証追加: `tools/SpaceEditorPasteGameTest.java`、`tools/test_space_editor_paste.ps1`
- ドキュメント: 本ファイル、`README_SpaceEditor.md`
- 生成関数（以下は `space_editor_datapack/data/space_editor/function/` 配下）:
  `start.mcfunction`、`tick.mcfunction`、`menu.mcfunction`、
  `paste/preview.mcfunction`、`paste/confirm.mcfunction`、`paste/start.mcfunction`、
  `paste_mode/begin.mcfunction`、`transform/skip_check.mcfunction`、
  `job/clone_chunk.mcfunction`、`job/fast_tick.mcfunction`、`job/advance_chunk.mcfunction`、
  `job/clone_masked_chunk.mcfunction`、`job/start_empty_check.mcfunction`、`job/empty_tick.mcfunction`、
  `job/empty_loop.mcfunction`、`job/check_empty_block.mcfunction`、`job/empty_done.mcfunction`
- JSON: `space_editor_datapack/data/space_editor/tags/block/transform_allowed.json`、
  `space_editor_datapack/data/space_editor/tags/block/paste_air.json`

PNGおよびリソースJSONの変更はなし。作業開始前からのFill関連変更は保持している。
