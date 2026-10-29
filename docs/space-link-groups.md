# SpaceLinkGroup — Stage05 / 2026-10-29

`codex/teleport-regions` の `7322faf` と、着手時のPaste/Fill未コミット変更を
維持して実装。コミット・Pushは行っていない。Stage06のMannequin、
ActiveProjection、Stage07のInstance生成は含まない。

正本として確認したNotion（2026-10-29節を優先）:

- [05 テレポート範囲・接続・相対座標](https://app.notion.com/p/4041fd1a615181159d48dea3d575a76e)
- [06 代理プレイヤー同期・反転ポータル](https://app.notion.com/p/4041fd1a61518139a7f6ed7939cc5889)
- [メイン仕様・ロードマップ](https://app.notion.com/p/3f61fd1a615181d285d1d5b5445fe75f)

## 保存形式と移行

`storage space_editor:document` のschemaVersionと既存Region構造は保持。
次のフィールドを追加する。整数リストの順番は配置順であり、RoomIDは一意キーではない。

```snbt
spaceLinkGroups:[{id:1,localSize:[I;3000,4000,5000],members:[101,102,103]}],
nextSpaceLinkGroupId:2
```

Regionは既存のmilliblock境界・Dimension・RoomIDなどに加えて
`kind:"space_link",spaceLinkGroupId:1,rotationY:90,flipY:1b,localSize:[I;3000,4000,5000]`
を持つ。`pairId`/`partnerId`は新しいSpaceLinkの所属判定には使わない。
`groupId`/`linkGroups`は従来のTP・Room対応用のままで、ID空間を共有しない。

`load`から呼ばれる`link/validate_groups`が`space_group/migrate`を呼ぶ。
旧`regionPairs[{kind:"space_link"}]`の相互参照、ID一意性、位置・姿勢・サイズを
検証し、2 Regionのグループへ変換する。既存RegionID、RoomID、Dimension、
固定境界、姿勢、未知フィールドを保持する。TP、通常Region、ProxyExistenceは対象外。

- 移行済みの旧ペア行には`spaceLinkGroupId`を付け、互換参照として残す。
  Regionの旧`pairId`は`legacyPairId`へ保存する。
- 旧ペア行は全メンバーを表すものではなく、旧TP/Room整合性検査の2端点参照。
  その`a`/`b`は現在のRegionを読むので、移動・姿勢変更後も整合性警告が機能する。
- 新GroupIDは既存の最大IDと`nextSpaceLinkGroupId`の双方を考慮して割り当てる。
  移行を再実行してもグループ・Actionを重複作成しない。
- **新形式の所属を優先**する。新所属のあるRegionを旧ペアが参照しても、旧形式で
  上書き・結合しない。壊れた旧参照や重複IDはそのまま残して
  `runtime.spaceLinkWarnings`へ警告する。未移行の旧ペアから接触は生成しない。
- 過去のActionは編集せず、移行前の2 Regionと旧ペア、移行後のGroupを含む
  `type:"space_link_group_edit",operation:"migrate"`のActionを追加する。
- 個別削除で無効になった互換ペアは`retiredSpaceLinkPairs`へ退避する。
  過去Actionと`legacyPairId`の参照元を失わず、現役の`regionPairs`とRoom整合性検査からは外す。
  TPのペア削除規則は変わらない。

警告確認: `/data get storage space_editor:runtime spaceLinkWarnings`

## 接続棒の操作

1. `/function space_editor:start`で編集開始し、範囲選択棒で元Regionを作る。
2. SpaceLink接続棒の**通常右クリック**で元Regionを選ぶ。既存GroupのRegionなら
   そのGroupを選ぶ。未接続Regionなら最初の配置確定時に2個のGroupを保存する。
   1個だけの不完全Groupは保存しない。
3. 視線の既存hoverセルへ新規候補を表示。Shift＋右クリックの左右で90度回転、
   上下方向でFlipY。基準Yawは棒を持って操作を始めた時の方向。
4. 通常右クリックで配置。そのまま次の候補へ進み、3個目、4個目以降も連続追加。
5. 持ち替えまたは削除棒によるキャンセルで候補を破棄。確定済みRegionは残る。

**既存Regionの姿勢編集**: 棒を持ち直し、Group内のRegionを最初に
**Shift＋右クリック**で選ぶ。以降のShift操作はその既存Regionの姿勢だけを編集する。
通常右クリックで、そのRegionを元にした連続追加へ切り替える。

Actionbarの`add`は新規候補、`pose`は既存Region。GroupID、元RegionID、回転、Flipを表示。
確定RegionのラベルもGroupIDとRegionIDを表示し、前・上の矢印を再利用する。
通常プレイでは編集枠を表示しない。

重なりは既存の近いヒット・リスト順の選択規則を保持する。完全に重なる別Regionを
IDで指定したい場合は、編集状態で次を使える（現在の追加候補を破棄して再選択）。

```mcfunction
function space_editor:space_group/select_id {id:103}
```

別Groupの既存Regionを取り込むAPIはない。既存所属を持つ候補は理由を表示して拒否する。
通常クリックによる配置は常に新しいRegionIDを割り当てる。

編集は引き続き**1人のみ**。他プレイヤーの`start`/`play`と接続セッションへの割り込みを
拒否する。セッションは所有者UUIDを持ち、所有者不在、持ち替え、`load`で破棄する。
`/reload`や再ログイン後は追加を選び直す。完全な複数人同時編集は実装していない。

## 編集・削除のトランザクション

- 移動と中心固定回転・FlipYは選択したRegionだけを変更する。
- 面伸縮・全体サイズ変更は、既存`pair/sync_bounds`の符号付き軸変換を使用し、
  同じローカル面の差分を全メンバーに適用する。反対面は固定される。
- 全メンバーの候補をRuntimeに作り、参照、同一localSize、0.1〜32ブロックの各辺、
  既存の座標限界、Dimensionの高さ、姿勢を検証してから保存する。
  どれかが失敗したらDocument・Action・IDカウンターを変更しない。
- Actionは操作前後のGroupとメンバーの完全な記録を持つ。MaskはRegionID参照を
  保ち、各Regionの表示更新時に追従する。Maskの設定自体は変更しない。
- 削除は選択RegionとそのMaskのみ。残り2個以上ならGroupを維持。
  残り1個ならGroupを削除し、残存Regionから接続種別・所属を外す。
  残存RegionとMaskは通常の未接続Regionとして再利用可能。
- 削除対象を含む接触サンプルと旧互換ペアを整理し、表示を再構築する。
  別Group、TPペア、ProxyExistenceを巻き込まない。

## Stage06 API

既存`mapping/position`は変更していない。
`worldA -> inverse(poseA) -> common local -> poseB -> worldB`を現在のRegionから導出する。
全組合せの変換表は保存しない。位置・ベクトルは0.0005ブロックの内部格子、
Region境界は0.001ブロック、yaw/pitchは0.001度。負座標と小数を保持する。

Group所属も検証する入口:

```mcfunction
data modify storage space_editor:runtime map set value {point:[0.5d,80.5d,1.5d],vector:[0.1d,0d,0.2d],yaw:15f,pitch:25f}
function space_editor:space_group/map {groupId:1,source:101,target:103}
```

結果は`runtime.map.result`、成否は`#map_ok se.v`。
source/targetを逆にすると逆変換。B→Cも同じAPIで求められる。
足元がリンク外へ出た後のマッピングにも利用できる。

各tickの`spaceLinkContacts`要素:

```snbt
{
  uuid:[I;1,2,3,4],instanceId:7,
  dimension:"minecraft:overworld",point:[0.5d,80.5d,1.5d],
  rotation:[15f,25f],vector:[0.1d,0d,0.2d],
  spaceLinkGroupId:1,sourceRegionId:101,targetRegionId:103,
  sourceRoomId:"room_1",targetRoomId:"room_3",
  destination:{dimension:"minecraft:the_nether",point:[40.5d,80.5d,1.5d],
               x:40.5d,y:80.5d,z:1.5d,vector:[0.1d,0d,0.2d],yaw:15f,pitch:25f},
  projectionPathId:{uuid:[I;1,2,3,4],instanceId:7,
                    spaceLinkGroupId:1,sourceRegionId:101,targetRegionId:103}
}
```

`projectionPathId`は文字列ではなく構造化キー。RoomIDが同じでもRegion経路を区別する。
これは現在tickの接触サンプルであり、ActiveProjectionの永続IDではない。
本人TP後にsourceRegionIdが変わる場合の継続経路の管理は06が担当する。
Instance生成は行わず、元Instanceは従来の`se.instance`から取得する。

処理順: 全員の`playerSnapshots`（Motionも取得）→全接触→
`#space_editor:before_teleport`→本人TPと`transfers`→`#space_editor:after_teleport`。
自己リンクを除外。欠落メンバーはスキップし、`spaceLinkRuntimeWarnings`に記録する。
最初に存在Regionを特定し、そのGroupの宛先だけを処理。元Regionの検証は接触元ごとに1回。

その他の入口:

- `space_group/add {source:101}`: `runtime.pairCandidate`に新規候補のRegionを用意して呼ぶ。
  候補の`spaceLinkGroupId`/`pairId`は不可。`#pair_ok se.v = 1`が成功。
  `pair/create {source:101,kind:"space_link"}`もこの処理へ委譲する。
- `pair/set_pose {id:103,rotationY:90,flipY:1}`: 新Group/旧TP共通の入口。
- `space_group/delete {id:103}`: 個別削除。旧`pair/delete`で移行済みSpaceLinkを削除する呼出しは拒否。
- `space_group/set_room {id:103,roomId:"room_3"}`: 個別RoomID変更とAction記録。
- 旧`pair/configure`は移行済みの旧2端点のRoom対応を変更可能。
  新Group自体をTP用`linkGroups`に転用・結合しない。

## 検証結果と限界

2026-10-29〜30にMinecraft 26.1の隔離GameTestワールドで実行。
ライブのユーザーワールドは操作していない。

- `ValidateMinecraft`: **4,146コマンド、0エラー**。
- 静的な`space_editor:`関数参照1,116件に欠落なし。JSONパース、
  `git diff --check`、再生成前後の本改修ファイルのバイト一致を確認。
- Stage05既存TP・Region編集回帰、追加SpaceLinkGroup GameTest: PASS。
- Stage02/03/04既存GameTest: PASS。各required test passとプロセス終了コード0を確認。
- 新旧混在、再移行、壊れた旧参照、2/3/4個の作成と連続配置、別Group候補拒否、
  重複位置の経路識別とID選択、持ち替え、別編集者拒否、所有者不在、loadの候補破棄。
- 4メンバーで384通りのローカル面編集、個別移動・姿勢、全体伸縮の逆操作、
  後半メンバーの高さ違反時の全体取り消し、無効な候補、Mask追従・個別削除と解体。
- 既存64 pose pair/往復精度に加え512 pose tripleでA→B→CとA→Cの位置・ベクトル・視線が一致。
- 3部屋・2人の同tick接触/TP、フックの実行時点、A→BのTP後のCへの投影座標の連続性、
  異Dimension、欠落メンバーの安全なスキップ。
- 65個目まで追加確認。標準65,536コマンド上限での実測（ゲームのtick時間ではなく実行コマンド数）:

| メンバー | 1人の接触処理 |
| --- | ---: |
| 4 | 1,587 |
| 8 | 3,175 |
| 16 | 6,351 |
| 32 | 12,757 |
| 64 | 25,569 |

64メンバー・2人の全TP tickは51,921、64メンバー面編集は27,779コマンド。
大規模化ではサーバー側のコマンド上限を調整可能だが、本改修は設定値を変更しない。
64個で制限しない。深い再帰を避ける走査は最大4096要素・固定3段のバッチ関数で構成。
4096を超えるGroup編集は拒否し、元Region走査の超過は警告する。
4096メンバーでの実行や大人数・多数重複Regionの性能は未検証。
人数・実際に存在する元Region数・そのGroupの接続先数に応じて処理量が増える。

新Groupの保存・編集のDimension検証はVanillaのOverworld/Nether/Endに限定する。
未知のDimensionは高さを推測せず拒否する。カスタムDimension・Instanceの実解決は07向けの残課題。
通常の`mapping/position`自体はDimension名を結果へ引き継ぐ純粋な変換として利用できる。

クライアントでの実際のマウス操作、見え方、再接続、実ワールドでの`/reload`は未検証。
GameTestのload再実行とセッション消失検証は、その実機確認を代替しない。
隔離サーバー終了時のWindows保存ファイルrename警告は従来同様発生するが、
上記実行時アサーション・required test・終了コードは成功。

## 変更ファイルと反映

手書きソース:

- `tools/build_space_link_groups.py` — 保存、移行、グループ編集、接触、UIの生成。
- `tools/build_space_editor_stage5.py` — 既存生成チェーンの最後に追加モジュールを接続。
- `tools/SpaceEditorStage5GameTest.java` — 新仕様テストと旧ペア移行fixture。
- `tools/test_space_editor_stage5.ps1` — 隔離テスト専用の前後フックとPASS出力。
- `docs/paired-regions.md`、この文書、[変更ファイル一覧](space-link-groups-files.txt)。

生成先は既存`space_editor_datapack/data/space_editor/function/`内。
`space_group/*`、`link/*`と既存pair/Region/preview/起動・tickの接続箇所を更新。
全生成ファイルの一覧は上記一覧を参照。Stage05→04→03→02→01→resourcesの生成順を維持。

着手前のPaste/Fill変更・Stage05内Fill回帰テストは保持。
今回の変更によるJSON・PNG・アイコン変更はない。生成時に再出力されるPNGは、
実行直前のバイト列を保持して復元し、手描きアセットを変更していない。

リソースルートはこのcheckoutの`assets/`。ワールド
`新規ワールド (2)/datapacks/space_editor`のjunction先が
このcheckoutの`space_editor_datapack/`であることを確認済み。
**Minecraft側は`/reload`で反映・移行。今回F3+Tは不要。**
移行は初期化を行わず、未確定の追加セッションだけ破棄する。
