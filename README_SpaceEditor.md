# Space Editor — 第3段階（回転・上下反転）

現在ロードされる実装は、01のRegion編集基盤と02のブロック操作に、Notion
「03｜回転・上下反転・ブロック変換エンジン」を追加した版です。旧版のBlock / Mask / TP機能と
保存データは削除していませんが、この段階ではロードも実行もしません。

## まず試す

1. Minecraftで `/reload`。今回は見た目の追加がないため、通常は`F3+T`不要です。
2. `/function space_editor:start`（旧コマンド `/function editor:start` も可）。
3. **範囲選択棒**を持つと、視線上3ブロック以内のブロック、またはブロックがない場合は
   3ブロック先の空中座標へオレンジ色の1ブロック仮枠が追従します。右クリック1回目でA、
   2回目でBを確定します。A/Bともブロックと空中を混ぜて指定できます。
4. 水色の枠＋斜線が出たら、別の2点をクリックしてRegionを追加できます。
5. **全体サイズ変更棒**で枠を右クリックすると全方向へ拡大、Shift＋右クリックで縮小。
6. **面伸縮棒**は見ている1面だけを動かします。Shiftで逆方向です。
7. **Region削除棒**で見ているRegionを削除します。
8. 枠中央の文字でID・現在位置・サイズを確認できます。
9. `/function space_editor:play` で補助枠を非表示、`/function space_editor:start` で復帰。

## Fill / Copy / Paste

- **Fill**：Fill棒をメインハンド、素材ブロックをオフハンドに持ちます。範囲選択棒と同じく、視線上
  3ブロック以内のブロック、またはブロックがなければ3ブロック先の空中セルへ1ブロック仮枠が追従します。
  右クリックすると、そのセルの中心を含むRegionをFillします。成功時だけ、そのFill専用Regionと
  プレビューを削除します。従来のコマンド操作も残しています。
- **Copy**：コピー棒でRegionを見て右クリック。完了すると`Template #ID`アイテムを受け取ります。
- **Paste**：ペースト棒をメインハンド、Templateアイテムをオフハンドに持ちます。Fill棒と同じ
  1ブロック仮枠を始点候補として表示し、ブロックがなくても3ブロック先の空中セルを選べます。
  1回目の右クリックで候補座標を始点とするPaste範囲を表示し、2回目で確定します。airも含めて貼り付けます。
- ペースト棒へ持ち替えた瞬間の向きを基準に、**Shift＋右クリック**で変換を選びます。
  左を見ると左90度、右を見ると右90度、上下を見るとFlipYを切り替えます。現在の`Rot` / `FlipY`と
  入力候補はアクションバーに表示され、1回目のクリック後も仮枠へ即時反映されます。
  通常の向きへ戻して右クリックすると貼り付け確定です。棒を持ち替えると`Rot 0° / FlipY OFF`へ戻ります。
- プレビューのキャンセルは `/function space_editor:paste/cancel` です。Shiftは変換操作専用です。
- Templateアイテムは参照キーだけを保持します。紛失時は
  `/function space_editor:template/reissue {id:1}`で再発行できます。
- 無変換Pasteは02と同じ高速な分割`clone`を使います。回転またはFlipYありのPasteは、全ブロックを
  先に検査してから1tick最大64ブロックずつ座標・状態を変換します。進捗カーソルは
  `storage space_editor:document job`へ保存され、`/reload`後も途中から継続します。
- 変換対応は通常の完全立方体、階段、ハーフブロック、柵・板ガラス、塀、柱系（`axis`）です。
  未対応の向き・形状・BlockEntityは、その配置先を変更せずスキップして残りを続行します。
  事前走査時と完了時にスキップ数を警告し、Actionにも`skippedBlocks`を保存します。
  柵・板ガラス・塀のFlipYも、衝突形状を正しく反転できないためスキップ対象です。
- Job操作：`/function space_editor:job/pause`、`resume`、`retry`、`cancel`。

ブロック操作は整数のブロック境界に揃ったRegionだけ受け付けます。01の0.1刻み伸縮で境界が小数に
なったRegionは、誤った丸めを避けるためFill/Copyを拒否します。Template実体は再起動不要の方式として、
Overworldの予約領域（基点`20000000 -63 20000000`、64ブロック間隔）へ保存します。

増減量は `/function space_editor:set_step {amount:0.1}`（0.1〜16、0.1単位）、一時的なA選択の解除は
`/function space_editor:selection/clear`、保存Regionからの表示復帰は
`/function space_editor:resume`、状態確認は `/function space_editor:status` です。

Regionの正本は `storage space_editor:document` にあり、`schemaVersion:1`、一意な
`id` / `idText`、`dimension`、整数配列 `min` / `maxExclusive`、`role`、表示状態を保存します。
クリック途中のSelectionは `storage space_editor:runtime selection` に分離しています。

この段階ではMask本体、TP、Portal、Undo/Redo、JSON書き出しは実装対象外です。
以下は保存してある旧版の資料です。

---

# Space Editor — 旧版資料

Minecraft Java Edition **26.1** 用、1人編集の空間制作ツールです。
選択棒で2点を選び、チャットのボタンから建材・マスク・テレポート範囲を配置します。
操作をデータとして保存し、Undo／Redo、編集、再構築、Codex向けJSON書き出しができます。

## この作業環境での反映

**ZIPの導入は不要です。現在有効な`testpack`をそのまま使ってください。**

- 見た目：この作業フォルダの`assets/`をMinecraftが直接読み込みます。
- 処理：`saves/新規ワールド (2)/datapacks/space_editor`から、この作業フォルダの
  `space_editor_datapack/`をディレクトリジャンクションで直接参照します。
- `build_space_editor.py`で生成した見た目も、有効な`assets/`へ自動反映します。

### 表示・マスク用ブロックの割り当て

`space_editor_blocks.json`を、Space Editorが専用表示に借りるブロックの正本として使います。
`displayBlocks`では範囲枠・補助枠・1ブロック候補・マスク本体を、
`maskablePalettes`では通常ブロック・マスク表示用の代理ブロック・元テクスチャを変更できます。

設定変更後は、次を順番に実行してください。

```powershell
python tools/build_space_editor.py
python tools/build_space_editor_stage3.py
```

生成時に、未知のキー、不正または26.1に存在しないブロックID、重複したブロック割り当て、
存在しない元テクスチャ、別用途ですでに上書き済みのblockstateを検出すると、
変更内容が分かるエラーで、生成物を書き換える前に停止します。
以前の割り当ては`space_editor_generated_manifest.json`で管理します。新しく借りるblockstateに
既存の定義があれば元のバイト列を退避し、割り当て解除時に完全復元します。
生成後に手作業で変更された管理ファイルは上書き・解除せず、ハッシュ不一致エラーで停止します。
生成が完了したら処理側を`/reload`、見た目を`F3+T`で再読み込みしてください。

1. `/reload`を実行します。
2. `F3+T`で見た目を再読み込みします。
3. `/function editor:start`で**専用の選択棒**を受け取ります。
4. その棒を持って操作し、`/function editor:menu`で配置メニューを開きます。

クリエイティブ一覧から取り出した通常のニンジン付きの棒は、選択棒にはなりません。
リソースパックだけでは右クリックを処理できないため、上記のデータパック参照も必要です。

既存の`dist/`のZIPは保存していますが、今回の直接反映の修正では更新していません。
別のワールドへ移すときは、そのワールドの`datapacks/`にも処理側を配置する必要があります。

## 最初の操作

1. **選択棒（ニンジン付きの棒）をメインハンドに持つ。**
2. ブロックに向けて **右クリックでA**、別のブロックへ **しゃがみ＋右クリックでB**。
3. 水色の枠と斜線が出たら `/function editor:menu`。
4. **素材** → `stone` など → **通常** または **Mask対象**。
5. **埋める**で範囲を埋めます。**空洞の箱**なら床・壁・天井だけを作り、内部を空気にします。

範囲は両端のブロックを含みます。同じブロックをA/Bに指定すると1ブロック、
同じYなら床・天井、同じXまたはZなら壁になります。選択は配置後も残ります。
選択棒は12.8ブロック先まで届き、水・空気などを通過します。

空中を指定したいときはメニューの **A:足元／B:足元** を使います。
座標で指定する場合も、同じ選択・プレビュー・保存機構を使います。

```mcfunction
/function editor:selection/set {ax:0,ay:80,az:0,bx:8,by:84,bz:8,dimension:"minecraft:overworld"}
```

## メニューでできること

| 操作 | 動作 |
|---|---|
| 埋める | Selection全体を選んだ建材で埋める |
| 空洞の箱 | 外殻を建材にし、内部を空気にする |
| 外殻のみ | 外殻だけ配置し、内部はその時点の状態を保つ |
| 空気で消去 | 範囲を空気にする。消去自体も記録する |
| Mask生成 | 選択範囲に低αのマスクDisplayを生成する |
| TP範囲登録 | 足元の侵入判定用Volumeを登録する。接続前はワープしない |
| Undo／Redo | 直近20手の配置・更新・削除・名前変更・TP接続を戻す／やり直す |
| 選択移動 | 選択範囲を東西南北・上下へ1ブロック移動する |
| 登録一覧 | ID・種類・名前を表示し、選択・更新・削除・TP接続へ進む |
| ガイド切替 | 選択枠とMask/TPの補助表示を表示／非表示にする |
| 再構築 | 記録された配置跡を消して、保存データを順番に再生する |
| プレイ | 補助表示を隠し、自分をTP判定の対象に戻す |
| 状態 | 処理状態・現在の選択・補正値を確認する |

削除や更新のボタンはコマンドを入力欄に入れます。対象IDを見てEnterで実行します。
編集モードの対象は1人です。`start`を別プレイヤーが実行すると編集者が交代します。

## 置いたものを修正する

1. **登録一覧 → 選択**で、対象の元の範囲と生成補正を呼び戻します。
2. 選択移動、A/Bの変更、素材変更、補正変更を行います。
3. 同じIDの **更新**を実行すると、そのIDと配置順を保って置き換えます。

```mcfunction
/function editor:objects/select {id:4}
/function editor:settings/offset {x:0,y:0,z:-0.01}
/function editor:objects/update {id:4}
/function editor:objects/rename {id:4,label:"entrance_mask"}
```

「選択」はオブジェクトを動かす操作ではありません。更新して初めてワールドへ反映されます。
MaskやTPの更新時は現在の補正を使います。Blockの更新時は現在の素材と以前の配置方式を使います。
名前にはダブルクォートや改行を含めず、短い説明を付けてください。

## マスクを調整する

**Mask対象**の建材は通常の建材と見た目がほぼ同じですが、別の実ブロックIDです。
その手前などへ、**マスク本体**をDisplayとして配置します。
マスク本体はほぼ不可視なので、編集時には黄色のガイドも表示します。
実際の見え方を確認するときは **プレイ** または **ガイド切替**で補助表示を消してください。

生成補正はMask/TPだけに適用され、SelectionやBlock配置は整数範囲のままです。
値は0.001ブロック単位、各軸±16までです。以下は選択をZ方向に0.01ずらして生成する例です。

```mcfunction
/function editor:settings/offset {x:0,y:0,z:-0.01}
/function editor:mask/create
```

`expand`は**各軸の両側それぞれ**を広げる量です。負数で縮めます。
例えば`x:-0.1`なら左側と右側を各0.1縮め、幅は合計0.2小さくなります。

```mcfunction
/function editor:settings/expand {x:-0.1,y:-0.1,z:-0.1}
/function editor:teleport/create
/function editor:settings/zero
```

補正は次の生成にも残ります。通常の大きさに戻すときは**補正リセット**を使います。
状態表示の`ox/oy/oz/ex/ey/ez`は1/1000単位の整数です（例：`-10` = `-0.01`）。

## テレポートを接続する

1. A/Bを選んで **TP範囲登録**。
2. プレイヤーを行き先へ移動し、向きも合わせます。
3. **登録一覧 → 現在地をTP先に設定** を選んでEnter。
4. **プレイ**に切り替えて、登録した範囲へ入ります。

```mcfunction
/function editor:teleport/link {id:5}
/function editor:teleport/unlink {id:5}
```

判定対象はプレイヤーの**足元の点**です。下端を含み上端を含まない直方体判定で、
接続後20tick（通常1秒）は再転送しません。重なる範囲は先に登録した接続を優先します。
ワープ先は登録時の足元座標と向きです。未接続の範囲や編集者は転送しません。
通常3ディメンション間を接続できます。Room間の相対位置保持や反転接続は今回の機能外です。

## 保存・再構築の考え方

**通常のワールド保存で、編集データも一緒に保存されます。** `/reload`で初期化しません。
`editor:data`の`document`が正本で、配置は順番付きの操作として残ります。
後から置いたものが前のものを上書きします。画面で手置きしたブロックは自動記録しません。

管理領域を手で決める必要はありません。ツールが各操作の配置跡を覚えます。
ただし、配置跡の下に元々あった**天然地形やツール外の建築を保存・復元する機能ではありません**。
Undoや再構築はその配置跡を空気にしてからデータを再生します。
今回の「制作をすべてツール経由で行う」運用を前提にしています。

再構築中は編集をロックし、チャンクを一時的に読み込みます。
処理途中でも保存されたデータから再開でき、元々あった強制読み込み指定は解除しません。
状態が`error`で止まった場合は `/function editor:build/resume`。
再開は途中の続きだけを推測せず、正本から再構築し直します。

## Codexへ渡す・別ワールドへ持っていく

### 完全なJSONを取り出す（おすすめ）

1. ワールドを**保存して閉じます**。
2. 配布セットの `tools/Export-Level.cmd` をダブルクリックし、ワールドのフォルダを選びます。
   ワールドのフォルダをCMDへドラッグ＆ドロップしても構いません。
3. `tools/exports/level-日時.json`ができます。このJSONをCodexへ渡してください。

Python 3.10以上が必要です。このPCではCodex同梱Pythonを自動検出します。
書き出しは保存ファイルを読むだけで、元ワールドには書き込みません。
別PCやターミナルでは、追加ライブラリなしで次のコマンドが使えます。

```text
python editor_data.py export "ワールドのフォルダ" --out level.json
python editor_data.py inspect level.json
python editor_data.py pack level.json --out SpaceEditor-Level.zip
```

生成した`SpaceEditor-Level.zip`を、移動先のSpace Editor導入済みワールドの`datapacks/`へ追加します。
`/reload` → `/function editor_import:load`で**現在の編集データを置き換え**て再構築します。
位置は絶対座標のままです。取り込みはUndoで戻せます。自動では取り込みません。

### ゲーム内で確認する

`/function editor:export`で1件ずつSNBTをチャットに出力します。
大量のデータではチャット履歴・ログ側で欠ける場合があるため、完全な受け渡しは上のJSON書き出しを使います。

## 使用する建材ID

| 用途 | 通常版 | Mask対象版／専用ID |
|---|---|---|
| stone | stone | blue_terracotta |
| dirt | dirt | brown_terracotta |
| oak | oak_planks | orange_terracotta |
| bricks | bricks | red_terracotta |
| quartz | quartz_block | white_terracotta |
| マスク本体 | — | waxed_oxidized_cut_copper |
| 選択枠 | — | magenta_glazed_terracotta |
| Mask/TPガイド | — | lime_glazed_terracotta |

この8つのIDはリソースパック有効中、通常の見た目としては使えません。
マスク対象版の隣接面は元の不透明ブロック同様にカリングされます。

## 現在の範囲と確認事項

- 対応：Java 26.1、チート／OP権限、通常3ディメンション、1人編集。
- 1回の選択：各辺1〜32、最大32,768ブロック。大きい部屋は壁・床ごとに分けて作れます。
- 座標：各軸±1,000,000以内。ブロック配置は各ディメンションの建築可能高度内。
- 登録：最大512操作。Undo／Redoは20手。基礎建材5種類＋空気。
- 未対応：Room・相対座標・反転複製、自由な手置きの自動検出、任意の建材／BlockEntity NBT。
- 反転やPortalらしい連続移動の演出は、保存したレベルデータを使って今後作る対象です。
- ツールの配置・履歴・TP・再構築は26.1のGameTestで確認しています。
- **クライアント画面でのマスク効果、線の見え方、実際のマウス操作の手触りは未確認**です。最初に小さな壁で確認してください。

仕組みのバージョン根拠：[Minecraft Java 26.1公式変更点](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1)。
データパック形式101.1、リソースパック形式84を指定しています。

## 開発用

- `tools/build_space_editor.py`：読みやすいmcfunctionと最小リソースパックを生成。
- `tools/mark_textures_translucent.py`：元からある1ピクセルα変更スクリプトを再利用。
- `tools/editor_data.py`：保存NBTの読み出し、JSON検証、取り込みパックの生成。
- `tools/test_space_editor.ps1`：公式Java 25＋26.1サーバーライブラリを使う隔離GameTest。
- `tools/package_space_editor.py`：アセット検証、配布ZIP、変更ファイル一覧を生成。

現在はルート`assets/`に専用モデル・専用テクスチャ・8種類のblockstateを反映しています。
既存の元テクスチャ、シェーダー、ルート`pack.mcmeta`は変更していません。
`space_editor_resources/`は生成元の補助フォルダで、そこだけを変更してもF3+Tでは反映されません。
見た目の生成は`build_space_editor.py`、functionの直接編集は`space_editor_datapack/`で行います。
