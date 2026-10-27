# Space Editor

Minecraft Java Edition 26.1 用のライブ編集データパックです。現行 runtime の namespace は
`space_editor:`、保存先は `storage space_editor:document` です。旧 `editor:` runtime と
`storage editor:data` は使用しません。

## ライブ環境

- リソースパック: このリポジトリ直下の `assets/`
- データパック: `space_editor_datapack/`
- ワールド側: `新規ワールド (2)/datapacks/space_editor` から上記データパックへのジャンクション
- データパック変更後: `/reload`
- モデル・テクスチャ変更後: `F3+T`
- 両方を生成した場合: `/reload` と `F3+T`

開始は `/function space_editor:start`、補助表示を隠す場合は
`/function space_editor:play` を使います。ワールド内の既存
`storage space_editor:document` はビルドや `/reload` で削除されません。

## 実装段階

### 01: Region

Region の作成、選択、移動、全体／面ごとの伸縮、削除を扱います。座標とサイズの正本は
0.001 ブロック単位の整数値です。

```powershell
python tools/build_space_editor_stage1.py
```

### 02: Fill / Copy / Paste

01 の上に Fill、Template Copy/Paste、永続 Job、archive 領域を追加します。

```powershell
python tools/build_space_editor_stage2.py
powershell -ExecutionPolicy Bypass -File tools/test_space_editor_stage2.ps1
```

### 03: Paste transform

02 の上に回転、FlipY、block state 変換、特殊な fence/wall 表示を追加します。

```powershell
python tools/build_space_editor_stage3.py
powershell -ExecutionPolicy Bypass -File tools/test_space_editor_stage3.ps1
```

### 04: 開発中

04 は 03 の生成結果へ Mask の永続レコードと表示を追加する構成です。generator の依存順は
`stage4 -> stage3 -> stage2 -> stage1` とし、`space_editor:document` の `masks`、
`nextMaskId` を含む既存フィールドやワールドデータを、旧実装の削除目的で変更・消去しないでください。

## 主な操作

`/function space_editor:start` で現行ツール一式を受け取ります。

- 範囲選択棒: 1回目の右クリックで A、2回目で B
- 全体サイズ変更棒: 右クリックで拡大、Shift+右クリックで縮小
- 面伸縮棒: 見ている面を移動、Shift で逆方向
- 範囲移動棒: 見ている面方向へ移動、Shift で逆方向
- 削除棒: Paste preview、特殊ブロック、Region の順に対象を削除
- Copy / Paste / Fill 棒: Stage 02 以降で使用

状態確認は `/function space_editor:status`、一時 Selection の解除は
`/function space_editor:selection/clear`、保存 Region からの表示復帰は
`/function space_editor:resume` です。

Paste preview のキャンセルは `/function space_editor:paste/cancel`、Job 操作は
`/function space_editor:job/pause`、`resume`、`retry`、`cancel` を使います。

## 生成とアセット

現行 generator の依存関係は `stage3 -> stage2 -> stage1` です。Stage 01 の生成時に
`tools/build_space_editor_resources.py` が共有描画アセットを再生成し、次の2か所を同期します。

- 生成元: `space_editor_resources/assets/`
- Minecraft が読むライブ先: ルート `assets/`

`assets/editor/` というリソース namespace 名は互換性のため維持しています。これは
`space_editor:` の block display が参照する現役アセットであり、旧 function namespace ではありません。
blockstate の割り当ては `space_editor_blocks.json`、安全な上書き／復元情報は
`space_editor_generated_manifest.json` で管理します。

アセットだけを明示的に再生成する場合:

```powershell
python tools/build_space_editor_resources.py
```

## 検証

最新の影響段階を生成してから、公式 26.1 dispatcher を使う command validation と
該当 Stage の GameTest を実行します。

- Stage 01: `tools/SpaceEditorStage1GameTest.java`
- Stage 02: `tools/SpaceEditorStage2GameTest.java` / `tools/test_space_editor_stage2.ps1`
- Stage 03: `tools/SpaceEditorStage3GameTest.java` / `tools/test_space_editor_stage3.ps1`
- Stage 04: 開発中の `SpaceEditorStage4GameTest.java` と runner があるブランチで検証

JSON／mcmeta はすべて parse し、現行 function 参照が `space_editor:` 内で解決することも確認します。
GameTest 成功はクライアント描画や実マウス操作の確認を代替しません。

## 開発上の注意

- generator を変更し、出力を再生成してから検証する。
- `space_editor:document` を正本とし、生成物からワールドデータを初期化しない。
- 旧 `editor:` の function、storage、import/export 形式へ依存しない。
- `assets/editor/` は現行表示に必要なため namespace 名だけで削除しない。
- 配布 ZIP や別フォルダへのコピーは、配布を明示的に行う場合だけ作る。
