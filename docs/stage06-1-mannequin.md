# Stage06-1｜Mannequin単体技術検証

2026-10-30。単体検証環境を実装し、公式26.1サーバーで検証しました。
**クライアント描画の受入確認は未完了**です。SpaceLinkGroup、ActiveProjection、独自Dimensionには接続しません。
`space_editor:document` は変更しません。通常体とDinnerbone体を並べ、本人の名前を独立Displayで表示します。

## ゲーム内で使う

ライブの `space_editor_datapack/` に反映済み。**`/reload` のみ必要**です。画像・モデル変更はなく、`F3+T` は不要です。
本人のチャットから実行してください（OP権限が必要）。

```mcfunction
/reload
/function space_editor:proxy_spike/help
/function space_editor:proxy_spike/start
```

`start` は `pair` の別名です。本人の**ワールド座標Z+3**に反転体、X+2/Z+3に通常体を出します。
南（+Z）を向けば前に見えます。視線を回すだけでは本人の周囲を回りません。
F5、または `follow_off` で止めて周囲から観察してください。

以下の操作には `/function space_editor:proxy_spike/` を付けます。

| 操作 | 関数名・引数 |
| --- | --- |
| 通常1体を生成し追従開始 | `spawn` |
| 通常＋Dinnerboneの2体比較を開始 | `pair` / `start` |
| 追従を一時停止／再開 | `follow_off` / `follow_on` |
| 自分の本体・名前を削除し終了 | `stop` / `delete` |
| 全参加者の検証Entityを削除 | `clear_all`（管理者用、編集用Entityは対象外） |
| 主役をDinnerbone／Grumm／通常へ | `flip_on` / `flip_grumm` / `flip_off` |
| 両体の腕振りを比較 | `swing_main` / `swing_off` |
| 10tick間隔の腕振りデモON／OFF | `swing_demo_on` / `swing_demo_off`（追従中のみ） |
| 設定と本体NBTを確認 | `status` |
| 本人と自分の主役のプロフィール表示 | `profile` |
| 操作一覧 | `help` |

`spawn` / `pair` の再実行では自分の検証セットのみ置き換え、設定を既定値に戻します。
通常の設定変更では本体を再生成しません。名前モード変更でもDisplayのUUIDを維持します。
外部からDisplayだけを消した場合は追従tickで再作成します。

### 名前方式

| 関数名 | mode | 設定・観察対象 |
| --- | --- | --- |
| `name_custom_hidden` | 0 | Teamは表示許可、CustomNameVisible:0b、説明非表示。照準を合わせた時のDinnerboneを確認 |
| `name_team_hidden` | 1 | nametagVisibility never、説明非表示。名前を隠して反転が維持されるか確認 |
| `name_description` | 2 | Teamは表示許可、説明に本人名。Dinnerbone名称の非表示を保証するモードではない |
| `name_text_display` | 3 | **既定方式**。本体はTeamで名前非表示、説明非表示。別Displayに本人名 |
| `name_native_visible` | 4 | CustomNameVisible:1b。Dinnerbone文字を明示的に出す対照実験 |

モード0/1/2/4ではDisplayの `view_range` を0にして非表示にします。
`hide_description` は「NPC」など説明行のみの設定です。CustomNameを隠す代わりにはしません。
Mannequinのdescriptionはselectorをユーザー名に解決しないため、text_displayで解決済みの文字をコピーします。

### 位置・高さ・文字の調整

```mcfunction
/function space_editor:proxy_spike/offset {x:0,y:0,z:3}
/function space_editor:proxy_spike/flip_height {fy:0.0}
/function space_editor:proxy_spike/label_height {normal:2.1,inverted:-0.3}
/function space_editor:proxy_spike/label_style {scale:1.0,background:1073741824}
```

- `offset`: 本人からの固定ワールド座標差。比較体はさらにX+2。各値はブロック単位、±16へ制限し1/1000単位で保存。
- `flip_height`: 反転中の主役だけYへ加算する観察用補正。**座標のFlipYとは別**。既定0。
- `label_height`: 各本体座標からのUI高さ。通常は2.1、反転時は実機確認値-0.3で頭の下へ置く。
- ラベルは本体poseに応じ、通常高さからしゃがみ0.3、水泳／滑空1.2、睡眠1.6を引く。これらは未実測の調整用初期値。
- `label_style`: 文字倍率0.1〜3.0のみ受理。背景は符号付きARGB整数（1073741824 = 0x40000000、0なら透明）。billboard:center、影なし、遮蔽あり、位置補間3tick。反転時は文字もZ軸180度回転し、解除時は同じDisplayを単位回転へ戻す。
- オフセット・反転Y補正は次の追従tickから反映。follow_off中は位置を固定。名前方式、高さ、反転名称は停止中も変更可能。

### 後片付けと復帰

`follow_off` は観察用にEntityを残す一時停止です。**終了には `stop`** を使います。
`/reload` / `clear_all` は全検証Entityを回収し追従停止。復帰は `start` / `spawn`。

削除時は本体を同期対象から外し、透明化・装備除去・名前Display削除を行います。2tick後に同じロード済みチャンクのDimension内低高度（Overworld -63、Nether/End 1）へTPし、さらに4tick後にkillします。待機中は `sp.removing` で管理され、再追従・名前再生成の対象になりません。この方式で元位置の死亡演出が消えるかはクライアントで **UNVERIFIED** です。

退出した本人のEntityは次tickで回収します。退出時にチャンクが未ロードでも、再ログイン時のleave_game統計差分で古いセッションを無効化します。
生成世代IDを再利用せず、reload世代も別管理します。未ロード中に停止／再生成された古いEntityは再ロード時に回収します。
未ロード中の即時削除はできず、強制ロードもしません。

同一Dimensionが対象です。本人が別Dimensionへ移ると旧Dimensionのロード済みEntityは回収します。移動先では再びstartしてください。
対象はバニラ3Dimensionのみです。無敵でも `/kill` は削除でき、手動で所有者scoreやタグを書き換える操作までは保護しません。

## クライアントでの観察手順

起動中のMinecraftクライアントがなかったため、自動確認は隔離した公式26.1サーバーで実施しました。
次の目視検証をGameTest成功で代替しません。通常体と反転体を同じ動作で比較してください。

1. `start`。本人のスキン、防具4部位、両手を比較。`profile`でUUIDを確認。デフォルトスキンなら待機時間と通信／キャッシュ状態を記録。
2. `follow_off`。各方向からスキン・装備・頭と胴体の反転を観察。F3+Bで当たり判定、足の座標、表示高さを比較。
3. `name_native_visible` → `name_custom_hidden` → `name_team_hidden`。照準を合わせる／外す両方で、Dinnerbone文字と反転維持を確認。
4. `name_description` → `name_text_display`。本人名、文字の向き、背景、遮蔽、視距離を通常プレイヤーと比較。別プレイヤーを近くに置き名前が混線しないか確認。
5. `follow_on`。静止してYaw±180度、Pitch上下。歩行、ダッシュ、斜め／後ろ歩き、ジャンプ、落下を個別に観察。**座標移動だけで歩行PASSにしない**。脚の振り、胴体の追随、頭の独立回転、遅延を見る。
6. Shift、水泳、エリトラ滑空、ベッド睡眠を比較。`swing_demo_on`で腕振りと装備・反転を同時確認し、`swing_demo_off`で解除。
7. 天井下で停止してflip_heightを調整、一度追従再開で反映して再停止。各poseの足の表示位置、天井面、必要Y補正量を記録。
8. 2人でstart。片方だけ設定変更、stop、退出し、もう片方の本体・名前が残ることを確認。最後にclear_allとreloadで残留を確認。

記録は「通常／反転、pose、name mode、視点・距離、期待、実際、補正量」の組で残してください。
スキン解決失敗の理由はデータパックから取得できません。正しいUUIDかはprofile、詳細はクライアントログで調べます。

## 検証結果（2026-10-30）

PASSは確認方法に記した範囲のみ。描画全体のPASSではありません。

| 項目 | 結果 | 確認方法 | 制限 |
| --- | --- | --- | --- |
| 生成・停止・所有者別削除 | PARTIAL | 公式26.1 GameTestで2名の異なるUUID、削除範囲、不可視効果・装備除去・2+4tick待機・残留なしを検査 | 死亡モーションと白粒子が見えないかはUNVERIFIED |
| スキン | PARTIAL | profile.idと本人UUIDの完全一致 | スキン表示はUNVERIFIED。取得不能なら標準スキン |
| 座標・Yaw/Pitch・頭Yaw | PASS | 固定オフセット、Y移動、±180度越えのYawを数値比較 | 独立したbodyYawの完全コピー・描画補間は未確認 |
| 歩行・走行アニメーション | UNVERIFIED | 実機手順5 | TP移動からバニラ側が演算。座標成功で代替しない |
| ジャンプ・落下 | PARTIAL | Y座標追従を数値比較 | 表示と着地演出は未確認 |
| しゃがみ・水泳・滑空・睡眠 | PARTIAL | predicate／sleeping_posからposeとラベル高さを検査 | 滑空角、ベッド向き、実描画は未確認 |
| 腕振り | PARTIAL | swing後のswingingとoffhand状態、実際の近接命中からadvancement経由の転送をGameTestで確認 | 手動／デモも実装。描画は未確認。空振り・採掘・右クリックは完全同期しない |
| 装備 | PARTIAL | 防具4部位・両手・空スロットに戻す更新を検査 | 食事・弓引き・盾使用の進行、主利き手は同期しない |
| Dinnerbone反転 | UNVERIFIED | トリガー文字列・Grumm切替を検査、client jarの反転条件を調査 | モデル・スキン・装備・アニメの実描画は未確認 |
| Dinnerbone非表示 | PARTIAL | Team所属とCustomNameVisible、反転用名称の維持を検査 | 実描画はUNVERIFIED。旧レポートのCustomNameVisible単独で文字が見えた記録は今回未追試 |
| 元プレイヤー名 | PARTIAL | ProxyOne/ProxyTwoを文字列完全一致、3tick補間、通常単位回転、反転180度回転、反転解除、UUID再利用、高さを検査 | 標準ネームタグとの外見的一致は未確認 |
| description比較 | PARTIAL | 解決済みユーザー名を実データで検査 | 説明行は名前とは別位置。Dinnerboneの置換にはならない |
| ラベル再利用・姿勢追従 | PASS | モード変更でUUID維持、姿勢別高さ、欠損修復を検査 | ちらつきの目視は未確認 |
| 非干渉化 | PARTIAL | NBT、6実tickの停止、通常ダメージ拒否、削除後22tickで装備ドロップなし | collisionRule never設定済み。当たり判定・照準選択・重なりを完全には消さない |
| 退出・古いセッション回収 | PASS | 実際のプレイヤー退出、古いepoch/owner/leave_game差分による回収 | 実チャンクのunload/reload往復は未試験。再出現時の状態を模擬 |
| reload・再開 | PASS | 実際のserver resource reload後、回収と再生成を確認 | 設定は意図的に初期化 |
| Stage01〜05保存データ保護 | PASS | スパイク操作前後でdocument NBTが同一 | 永続documentへ書き込まない |
| Stage05回帰 | PASS | Stage05 GameTest、Region編集、SpaceLinkGroup、TP、2名・Dimension移動、保存とreload | クライアントでの既存ツール操作は今回未追試 |

## 技術的な結論

位置・Yaw/Pitch・装備・poseはコマンドで再現できます。独立bodyYaw、任意クリック、アイテム使用進行、個別スキンレイヤー設定は完全にはコピーしません。
poseは変化時のみ書き、装備同期後にTPして、NBT再読込が頭回転を上書きしにくい順序にしています。

26.1の `AvatarRenderer.isEntityUpsideDown` はケープレイヤーが有効な場合、非Player（Mannequin）に
`LivingEntityRenderer` のCustomName判定を適用します。正確なDinnerbone/Grummがトリガーで、Teamの名前表示条件とは独立です。
生成時の `hidden_layers:[]` でケープレイヤーを有効にします。**アカウントがケープの実テクスチャを持つことを要求する判定ではありません。**
これは利用可能性のコード上の根拠であり、描画の実機PASSではありません。
描画の高さ移動とZ軸180度回転にはpose別変換も絡むため、天井への足合わせは実測して補正してください。

本体名はTeamで隠し、別DisplayをUIとして表示する方式を採用します。文字はbillboardでモデル反転を受けません。
本物のプレイヤー名との主な差・未確認点は次のとおりです。

- しゃがみ時の半透明化、壁越し表示、32/64ブロックの標準距離ルールを厳密に再現していない。
- 本体とラベルは別パケットで動くため、実機確認値3tickを設定しても全pose・負荷時の一致は保証しない。
- 生成時にselectorで解決した名前を保持。後から本人のTeam色・prefixを変えた場合は再生成で取り直す。
- 名前の高さは未実測の初期値。反転した頭の近くと身体の上のUI位置は別々に選べる。

実機で反転しなければ、名称の完全一致、hidden_layersのcape、pose、Grumm比較を調査してください。
代替のitem_display/block_displayと変換行列は180度回転できますが、任意ユーザーの動的スキン・装備・バニラ歩行をそのまま維持できません。
固定スキンのRPモデルは代替候補に留まり、今回導入していません。Modは不要です。

## 06-2へ引き継ぐAPIと注意点

- 再利用単位: `set_profile`、`sync`/`set_pose`、`apply_name`、`update_labels`、所有者別生成／削除。
- `sp.owner` は生成セッションIDで、恒久プレイヤーIDではない。本人UUIDはprofile、reload世代はsp.epochで扱う。
- sp.selectedは関数内の一時タグ。同期実行を前提にし、scheduleを挟んで保持しない。
- 1人最大2本体＋2ラベル。tickは3Dimensionの専用タグ・型だけを掃除し、各所有者の各roleをlimit=1で選択。再帰投影はない。
- storage space_editor:proxy_spikeは一時scratch、設定はsp.* scoreboard、Teamはsp_hidden/sp_body。documentは未変更。
- 06-2では固定オフセットのmoveを、05のspace_group/map・mapping/positionへ差し替える。SpaceLinkは複数Regionグループ、TeleportRegionのみ従来ペア。
- 座標FlipYと描画反転を分離し、原則source.flipY XOR target.flipYで反転を選択。pose別Y補正は実測を引き継ぐ。
- 頭／胴体の自然さ、装備反転、名前の自然さ、天井補正は採用前の未完了実機項目。06-4の複数投影／TP継続管理へ単体セッションをそのまま流用しない。

## 生成と検証

```powershell
python -B tools/build_space_editor_stage6_1.py
pwsh -NoProfile -File tools/test_space_editor_stage6_1.ps1
pwsh -NoProfile -File tools/test_space_editor_stage5.ps1
```

06-1入口はStage05→04→03→02→01→resourcesを呼び、Stage05末尾が06-1を生成します。
通常のbuild_space_editor_stage5.pyでも機能が残ります。下位段階を単独生成した場合は最後に05か06-1を再生成してください。
Javaハーネスは開発用のみで、実ワールドにJavaコード／Modを導入する必要はありません。

隔離worldはbuild/test-server/run-stage6_1-*、ログとXMLはbuild/test-server/stage6_1-*です。
ValidateMinecraftのマクロ代表値による構文確認に加え、GameTestで実値を確認します。
今回の構文検証は5,721件・エラー0、06-1・正式06・05はいずれも明示PASS・終了コード0です。
今回も隔離テスト終了時にWindowsのworld rename警告が出ています。明示PASS・終了コード0を確認済みで、実ワールドは使用していません。

計測は専用tickのみ、warmup20回＋100回、コマンド実行枠と壁時計で測定。
最終計測（run-stage6_1-22a9c2c1eaa04ed79a1475dbde1a733c）では、1体: **171枠、中央値0.876ms、p95 2.392ms**、2体: **177枠、中央値0.547ms、p95 0.868ms**。
クライアント描画・通信・サーバー全tickの値ではなく、JIT/GCの影響で2体の値が短くなることもあります。
上限は65536のまま。GameTestでは専用tickが1000枠未満であることも確認しています。

JSONの追加は `space_editor_datapack/data/space_editor/advancement/proxy_spike/attack.json`。
既存 `space_editor_datapack/data/space_editor/predicate/proxy_spike/` の `crouching.json`、`swimming.json`、`fall_flying.json` は改行をLFへ統一しただけで条件は同じです。
データパック内JSON/mcmeta全21件を解析済み、関数参照解決、両生成入口のバイト一致、git diff --checkも通過しました。
テクスチャ・モデルに最終差分はなく、対象のスキップもありません。

## 参照

- [最新Notion06-1、2026-10-30節](https://app.notion.com/p/4041fd1a61518139a7f6ed7939cc5889)
- [26.1公式: swing、fetchprofile entity](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1)
- [Mannequin公式フィールド](https://feedback.minecraft.net/hc/en-us/articles/39966147272589-Minecraft-Java-Edition-1-21-9-The-Copper-Age)
- [動的profileの公式仕様](https://feedback.minecraft.net/hc/en-us/articles/39092387123469-Minecraft-Java-Edition-Snapshot-25w34a-b)

fetchprofile entityは既存プロフィールの表示用で、storageへコピーするAPIではありません。
今回は本人UUIDから動的profileを構成し、独自Web APIは使用していません。
