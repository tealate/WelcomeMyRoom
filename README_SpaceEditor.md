# Space Editor — 第4段階（Mask生成・編集・可視化）

Minecraft Java Edition 26.1 用のライブ編集データパックです。現行 runtime の namespace は
`space_editor:`、保存先は `storage space_editor:document` です。旧 `editor:` runtime と
`storage editor:data` は使用しません。

現在ロードされる実装は、01 の Region 編集、02 の Fill / Copy / Paste、03 の回転・上下反転に、
04 の Mask 生成・編集・可視化を追加した版です。Mask は Region を参照する独立 Object として保存し、
編集用ガイドと実ゲーム用の低α Display を分離しています。

## ライブ環境

- リソースパック: このリポジトリ直下の `assets/`
- データパック: `space_editor_datapack/`
- ワールド側: `新規ワールド (2)/datapacks/space_editor` から上記データパックへのジャンクション
- データパック変更後: `/reload`
- モデル・テクスチャ変更後: `F3+T`
- 両方を生成した場合: `F3+T` と `/reload`

開始は `/function space_editor:start`、補助表示を隠す場合は
`/function space_editor:play` を使います。ワールド内の既存
`storage space_editor:document` はビルドや `/reload` で削除されません。

## まず試す

1. `F3+T`、続けて `/reload`。
2. `/function space_editor:start` で現行ツール一式を受け取る。
3. 範囲選択棒を持ち、右クリック1回目で A、2回目で B を確定する。
4. Region が表示されたら Mask 棒で Region を右クリックする。
5. `/function space_editor:play` で Region 枠と編集ガイドを隠し、Mask 本体を確認する。

クリエイティブ一覧から取り出した通常のニンジン付きの棒では操作できません。
`space_editor:start` が発行する custom data 付きの棒を使用してください。

## 実装段階と生成

generator の依存順は `stage4 -> stage3 -> stage2 -> stage1 -> resources` です。
最新の04を生成する場合は次を実行します。

```powershell
python tools/build_space_editor_stage4.py
```

各段階を単独で生成する入口も残しています。

- 01 Region: `tools/build_space_editor_stage1.py`
- 02 Fill / Copy / Paste: `tools/build_space_editor_stage2.py`
- 03 Paste transform: `tools/build_space_editor_stage3.py`
- 04 Mask: `tools/build_space_editor_stage4.py`
- 共有描画アセットのみ: `tools/build_space_editor_resources.py`

### 01: Region

Region の作成、選択、移動、全体／面ごとの伸縮、削除を扱います。座標とサイズの正本は
0.001 ブロック単位の整数値です。

### 02: Fill / Copy / Paste

Fill、Template Copy/Paste、永続 Job、archive 領域を追加します。Fill 棒は素材をオフハンドに持ち、
視線上の候補セルを含む Region に適用します。Copy 完了時は `Template #ID` アイテムを発行します。

Template の再発行は `/function space_editor:template/reissue {id:1}`、Paste preview のキャンセルは
`/function space_editor:paste/cancel` です。Job 操作は `/function space_editor:job/pause`、
`resume`、`retry`、`cancel` を使います。

### 03: Paste transform

Paste の4方向回転、FlipY、block state 変換、特殊な fence/wall 表示を追加します。未対応ブロックは
配置先を変更せずスキップし、`skippedBlocks` として記録します。

### 04: Mask

- Mask 棒で Region を右クリックすると、その Region を参照する Mask を生成します。
- 編集中はガイドを表示し、`space_editor:play` ではガイドと Region 枠だけを隠します。
  低αの Mask 本体はプレイ中も残ります。
- Region を移動・伸縮すると、関連する Mask の位置とサイズも追従します。
- 削除棒で Mask 付き Region をクリックすると、1回目は Mask を削除して Region を残します。
  もう一度クリックすると Region を削除します。
- offset と expand は 1/1000 ブロック単位で保存します。expand の結果が0以下になる変更は拒否します。

```mcfunction
/function space_editor:mask/set_offset {id:1,x:0,y:0,z:-0.01}
/function space_editor:mask/set_expand {id:1,x:0.1,y:0,z:0}
/function space_editor:mask/rename {id:1,name:"entrance"}
/function space_editor:mask/delete {id:1}
/function space_editor:mask/help
```

Mask 対象素材は `/function space_editor:mask/give_target_stone` などで受け取り、Fill 棒の
オフハンドに持って使います。`stone`、`dirt`、`oak`、`bricks`、`quartz` を用意しています。
論理素材名と代理ブロックは `space_editor_blocks.json` で管理します。

Mask 本体の初期割り当ては `waxed_oxidized_cut_copper` です。全画素α1の専用テクスチャを使うため、
ほぼ不可視の translucent Display になります。割り当ては `displayBlocks.maskBody` で変更できます。

`space_editor:document` の `masks`、`nextMaskId` を含む既存フィールドやワールドデータを、
生成や旧実装の整理で削除・初期化しないでください。

## 主な操作

- 範囲選択棒: 右クリック1回目で A、2回目で B
- 全体サイズ変更棒: 右クリックで拡大、Shift+右クリックで縮小
- 面伸縮棒: 見ている面を移動、Shift で逆方向
- 範囲移動棒: 見ている面方向へ移動、Shift で逆方向
- 削除棒: Paste preview、特殊ブロック、Mask、Region の順に対象を削除
- Copy / Paste / Fill 棒: Stage 02 以降で使用
- Mask 棒: Stage 04 で Region から Mask を生成

状態確認は `/function space_editor:status`、一時 Selection の解除は
`/function space_editor:selection/clear`、保存 Region からの表示復帰は
`/function space_editor:resume` です。

## アセット

Stage 01 の生成時に `tools/build_space_editor_resources.py` が共有描画アセットを再生成し、
次の2か所を同期します。

- 生成元: `space_editor_resources/assets/`
- Minecraft が読むライブ先: ルート `assets/`

`assets/editor/` という resource namespace は現行 block display が使用しています。旧 function
namespace ではないため削除しません。blockstate の割り当ては `space_editor_blocks.json`、
安全な上書き／復元情報は `space_editor_generated_manifest.json` で管理します。

## 検証

最新の影響段階を生成してから、公式 26.1 dispatcher を使う command validation と該当 Stage の
GameTest を実行します。

```powershell
powershell -ExecutionPolicy Bypass -File tools/test_space_editor_stage4.ps1
```

- Stage 01: `tools/SpaceEditorStage1GameTest.java`
- Stage 02: `tools/SpaceEditorStage2GameTest.java` / `tools/test_space_editor_stage2.ps1`
- Stage 03: `tools/SpaceEditorStage3GameTest.java` / `tools/test_space_editor_stage3.ps1`
- Stage 04: `tools/SpaceEditorStage4GameTest.java` / `tools/test_space_editor_stage4.ps1`

JSON／mcmeta はすべて parse し、現行 function 参照が `space_editor:` 内で解決することも確認します。
GameTest 成功はクライアント描画や実マウス操作の確認を代替しません。

## 開発上の注意

- generator を変更し、出力を再生成してから検証する。
- `space_editor:document` を正本とし、生成物からワールドデータを初期化しない。
- 旧 `editor:` の function、storage、import/export 形式へ依存しない。
- `assets/editor/` は現行表示に必要なため namespace 名だけで削除しない。
- 配布 ZIP や別フォルダへのコピーは、配布を明示的に行う場合だけ作る。
