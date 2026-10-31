# Space Editor — Stage06 代理プレイヤー投影

Minecraft Java Edition 26.1 用のライブ編集データパックです。現行 runtime の namespace は
`space_editor:`、保存先は `storage space_editor:document` です。旧 `editor:` runtime と
`storage editor:data` は使用しません。

現在ロードされる実装は01〜06です。複数RegionのSpaceLinkGroupから、経路別にMannequinを投影します。
正式ランタイム・1人用配置・検証結果は [Stage06操作・設計](docs/stage06-projection.md) を参照してください。
初期状態は無効です。`/reload` 後に `/function space_editor:projection/demo/setup`、
`/function space_editor:play` の順で、地形を変更せず足元基準の3部屋テストを開始できます。
06-1のMannequin単体技術検証は [操作・検証レポート](docs/stage06-1-mannequin.md) を参照してください。
Maskは従来どおり独立Objectとして動作します。

06-1は `/reload` 後に `/function space_editor:proxy_spike/start` で通常／反転の2体比較、
`help` で操作一覧、`stop` で自分の検証Entityを削除できます。正式投影とは別管理です。
06-1の実現可能性は確認済みとのユーザー報告を引き継いでいます。今回の正式投影の描画品質は実機確認が必要です。

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

generator の依存順は `stage5 -> stage4 -> stage3 -> stage2 -> stage1 -> resources` です。
Stage05生成の末尾で06-1と正式Stage06も生成します。最新の全体を生成する場合は次を実行します。

```powershell
python tools/build_space_editor_stage6.py
```

各段階を単独で生成する入口も残しています。

- 01 Region: `tools/build_space_editor_stage1.py`
- 02 Fill / Copy / Paste: `tools/build_space_editor_stage2.py`
- 03 Paste transform: `tools/build_space_editor_stage3.py`
- 04 Mask: `tools/build_space_editor_stage4.py`
- 05 共通ペア編集 / TP: `tools/build_space_editor_stage5.py`
- 06-1 Mannequin単体検証: `tools/build_space_editor_stage6_1.py`（05を含む）
- 06 正式投影: `tools/build_space_editor_stage6.py`（05・06-1を含む）
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

「透過ペースト棒」はコピー元のAir 3種を無視して配置先を保持します。通常ペースト棒と同じ
Template紙・プレビュー・回転・FlipY操作を使い、水・溶岩の状態も複製します。
取得方法、strictによる液体更新抑制、検証内容は [透過ペーストの仕様](docs/masked-paste.md) を参照してください。

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

Mask 本体の初期割り当ては `waxed_oxidized_cut_copper` です。専用テクスチャを使うため、通常は
ほぼ不可視の translucent Display になります。割り当ては `displayBlocks.maskBody` で変更できます。

Mask 本体の手編集元は、Minecraft が直接読む
`assets/editor/textures/block/mask_body.png` です。LibreSprite ではこのファイルを編集し、保存後に
`F3+T` してください。生成器はこの PNG を上書きせず、`space_editor_resources/` 側へ同じ内容を
ミラーします。補助側の同名 PNG を編集しても、それだけでは Minecraft の表示へ反映されません。

実体と範囲をテクスチャに依存せず確認する場合は、次の一時デバッグ表示を使えます。

```mcfunction
/function space_editor:mask/debug/show
/function space_editor:mask/debug/status
/function space_editor:mask/debug/hide
```

`debug/show` は既存の Mask 本体を発光輪郭にして `view_range` を 16 へ広げるだけで、Mask方式や
テクスチャは変更しません。PNGそのものを不透明色で確認する場合も、上記ライブPNGだけを編集します。

`space_editor:document` の `masks`、`nextMaskId` を含む既存フィールドやワールドデータを、
生成や旧実装の整理で削除・初期化しないでください。

### 05: ペアRegionとTP

1. `F3+T`、`/reload`、`/function space_editor:start`。
2. 範囲選択棒で元Regionを作り、TP接続棒で右クリックする。
3. 相手側のプレビューを視線で移動する。Shift+右クリックは、棒を持ち始めた向きを
   基準として左／右を見れば90度回転、上／下を見ればFlipYを切り替える。
4. 通常の右クリックで配置を確定する。削除棒または持ち替えで未確定配置を取り消す。
5. 配置後は同じ接続棒でA／Bそれぞれを選び、Shift操作で回転・反転できる。
   移動棒は選択側だけを移動する。面伸縮棒は双方の対応ローカル面だけを動かす。
6. `/function space_editor:play` で編集表示を隠し、TPを有効にする。

緑の3D矢印がローカル前（+Z）、黄色がローカル上（+Y）です。ラベルに種類、pairId、
A/B、回転、反転を表示します。SpaceLink接続棒も同じ操作ですが、本人をTPしません。
Proxy存在範囲棒は既存Regionを単独の存在範囲として登録します。
接続棒の選択では別種別を除外し、同距離は既存Regionの保存順で決定します。

回転は中心固定です。3×4など奇数・偶数混合の範囲では境界が半ブロック座標になります。
面伸縮は選択面だけを移動し、相手も対応するローカル面だけを移動します。どちらかが
高さ・サイズ制限に違反すれば両方とも保存しません。全体拡縮は各面を同量ずつ増減します。
ペアの削除は両Regionと付属Maskをまとめて1操作として記録し、他のペアや存在範囲を残します。

TPは足元点をmin以上・maxExclusive未満で判定し、両方向に対応します。編集モード中は停止します。
到着したペア内に留まる間は再転送せず、退出・再侵入とクールダウン満了後に再転送できます。
未ロードの出口や、幅0.6×高さ1.8の到着範囲に通行対象外ブロックがある場合は転送を待ちます。
地形の変更や自動チャンクロードは行いません。FlipYは座標とpitchの変換で、本人の重力・身体・
カメラのロールを反転するものではありません。速度の適用は今回のTP対象外です。

Room／Groupの関連付けと片方向指定は補助APIで設定できます。IDはラベルと`status`で確認します。

```mcfunction
/function space_editor:pair/configure {id:1,groupId:1,roomA:"room_a",roomB:"room_b",direction:"both",cooldownTicks:20}
/function space_editor:proxy_existence/set_room {id:5,roomId:"room_a"}
/function space_editor:pair/set_pose {id:1,rotationY:90,flipY:1}
/function space_editor:link/status
```

`direction`は`both`または`one_way`（A→B）。Groupを共有するTPとSpaceLinkの変換・包含関係が
一致しなければ警告し、相手ペアの位置は変更しません。Group未指定のペアは独立して使えます。
ペアRegionの各辺は0.1〜32ブロック、座標は各軸±500,000ブロック以内です。
追加APIと06への接続契約は[paired-regions.md](docs/paired-regions.md)を参照してください。

## 主な操作

- 範囲選択棒: 右クリック1回目で A、2回目で B
- 全体サイズ変更棒: 右クリックで拡大、Shift+右クリックで縮小
- 面伸縮棒: 見ている面を移動、Shift で逆方向
- 範囲移動棒: 見ている面方向へ移動、Shift で逆方向
- 範囲表示切替棒: 右クリックで全Region枠・ラベル・Maskガイドを表示／非表示（Mask本体は維持）
- 削除棒: Paste preview、特殊ブロック、Mask、Region の順に対象を削除
- Copy / Paste / Fill 棒: Stage 02 以降で使用
- Mask 棒: Stage 04 で Region から Mask を生成

状態確認は `/function space_editor:status`、一時 Selection の解除は
`/function space_editor:selection/clear`、保存 Region からの表示復帰は
`/function space_editor:resume` です。

## アセット

Stage 01 の生成時に `tools/build_space_editor_resources.py` が共有描画アセットを再生成し、
次の2か所を同期します。ただし手編集対象の `mask_body.png` だけはライブ先を正本とします。

- 通常の生成元: `space_editor_resources/assets/`
- Minecraft が読むライブ先: ルート `assets/`
- `mask_body.png` の正本: ルート `assets/editor/textures/block/mask_body.png`

`assets/editor/` という resource namespace は現行 block display が使用しています。旧 function
namespace ではないため削除しません。blockstate の割り当ては `space_editor_blocks.json`、
安全な上書き／復元情報は `space_editor_generated_manifest.json` で管理します。

選択カーソルの手編集元は
`assets/editor/textures/block/selection_candidate.png` です。32×32の透明面＋不透明な外枠・対角線を
持つ専用テクスチャで、生成器は内容を上書きせず補助ツリーへミラーします。モデルは外向きの面に加え、
内側からも線を確認できる薄い内向き面を持ちます。編集後は `F3+T` で反映してください。

## 検証

最新の影響段階を生成してから、公式 26.1 dispatcher を使う command validation と該当 Stage の
GameTest を実行します。

```powershell
pwsh -File tools/test_space_editor_stage6.ps1
pwsh -File tools/test_space_editor_stage5.ps1
```

- Stage 01: `tools/SpaceEditorStage1GameTest.java` / `tools/test_space_editor_stage1.ps1`
- Stage 02: `tools/SpaceEditorStage2GameTest.java` / `tools/test_space_editor_stage2.ps1`
- Stage 03: `tools/SpaceEditorStage3GameTest.java` / `tools/test_space_editor_stage3.ps1`
- Stage 04: `tools/SpaceEditorStage4GameTest.java` / `tools/test_space_editor_stage4.ps1`
- Stage 05: `tools/SpaceEditorStage5GameTest.java` / `tools/test_space_editor_stage5.ps1`
- Stage 06-1: `tools/SpaceEditorStage6_1GameTest.java` / `tools/test_space_editor_stage6_1.ps1`
- Stage 06: `tools/SpaceEditorStage6GameTest.java` / `tools/test_space_editor_stage6.ps1`

JSON／mcmeta はすべて parse し、現行 function 参照が `space_editor:` 内で解決することも確認します。
GameTest 成功はクライアント描画や実マウス操作の確認を代替しません。

## 開発上の注意

- generator を変更し、出力を再生成してから検証する。
- `space_editor:document` を正本とし、生成物からワールドデータを初期化しない。
- 旧 `editor:` の function、storage、import/export 形式へ依存しない。
- `assets/editor/` は現行表示に必要なため namespace 名だけで削除しない。
- 配布 ZIP や別フォルダへのコピーは、配布を明示的に行う場合だけ作る。
