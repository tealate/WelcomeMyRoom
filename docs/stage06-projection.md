# Stage06 — SpaceLinkGroup代理プレイヤー投影

対象はMinecraft Java 26.1、Modなし。06-1のprofile・TP追従・pose・Dinnerbone・非表示Team・独立ネームタグを再利用し、06-2〜06-4の経路管理へ接続しました。SpaceLinkは対応座標だけを計算し、本人の転送は従来のTeleportRegionが担当します。Stage07の個人Dimension生成は含みません。

## ライブで最初に試す

今回の変更は **`/reload` のみ**で反映します。アセット変更はありません。既存ワールドのRegionや地形を初期化する必要はありません。

平坦な場所で、東側に32ブロック、南側に20ブロック程度の空間を用意してください。床の上に立って次を実行します。設定開始時の足元を切り下げた座標を `(X,Y,Z)` とします。通常は地面より1高いYです。

```mcfunction
/reload
/function space_editor:projection/demo/setup
/function space_editor:projection/demo/status
/function space_editor:play
```

`setup` は既存のRegion作成APIを使って8個のRegionを追加します。ブロック・床・天井は生成しません。再実行しても増えません。既に編集中の別プレイヤーがいれば実行を中止します。原点はX/Z約±500,000以内、Y=-60〜246を使用します。

|配置|X範囲|Y範囲|Z範囲|姿勢設定|
|---|---|---|---|---|
|SpaceLink A|X〜X+4|Y〜Y+4|Z+4〜Z+8|0度、通常|
|SpaceLink B|X+12〜X+16|同上|同上|90度、FlipY|
|SpaceLink C|X+24〜X+28|同上|同上|180度、FlipY|
|A存在範囲|X-4〜X+8|Y-4〜Y+10|Z〜Z+12|room A|
|B存在範囲|X+8〜X+20|同上|同上|room B|
|C存在範囲|X+20〜X+32|同上|同上|room C|
|Debug B|X+12〜X+16|Y〜Y+4|Z+16〜Z+20|0度、通常|
|Debug C|X+24〜X+28|同上|同上|0度、通常|

範囲はminを含みmaxを含みません。原点が `(0,64,0)` なら、Aは `(0,64,4)` から `(4,68,8)`、足元 `(1,64,5)` が入口内です。方角は視線に依存せず、X+が東、Z+が南です。

1. Aへ**外から歩いて侵入**します。BとCへ同時に本人の代理が現れます。Aを出ても、投影した足元が各存在範囲内なら代理は続きます。
2. 歩く・走る・ジャンプ・しゃがむ・視線を動かす・装備を持ち替える操作を行います。B/Cの回転、上下反転、名前、足元と高さを観察します。名前にDinnerboneが出ていないことを確認してください。
3. `/function space_editor:projection/debug/on` を実行すると、南側Debug B/Cにも追加表示します。元と同じローカル座標を別のRegionへ変換した結果です。`debug/off` はDebug表示だけを消します。
4. Aから東へ移動します。例えばA内のZ+5を維持してX+13まで進むと投影は存在範囲外になり削除されます。X+5に戻るだけでは復活しません。X+1まで戻りAへ再侵入すると再生成されます。経路IDは `projection/status` で比較できます。
5. 本人TPを追加する場合は次を実行します。Aを一度出て再侵入するとBへ転送されます。Cの代理は継続します。Bの本人位置への重複表示は隠します。Teleportの既存仕様により、出口に身体が入る空間とロード済みチャンクが必要です。

```mcfunction
/function space_editor:projection/demo/teleport
/function space_editor:projection/status
```

2人確認では、2人ともAの外へ出た後、同時にAへ入ってください。観測者はC近くから、それぞれの名前と追従が混線しないか確認できます。`/reload` 後も有効経路IDを維持し、表示を復帰します。

後片付けは `/function space_editor:projection/demo/cleanup`。この配置で作成したRegion・対応経路・名前・Debug設定だけを削除し、既存のRegionを保持します。受け取った編集棒は通常の編集用として残ります。正式投影全体を止める場合は `/function space_editor:projection/disable` を別途実行してください。

## 既存のRoomへ組み込む

既存のSpaceLinkGroupをそのまま使います。各RegionにRoom名を割り当て、そのRoomの代理存在範囲を存在範囲指定棒で作成します。例ではRegion 2が投影先、Region 5がその存在範囲です。IDを実際の保存値に置き換えてください。

```mcfunction
/function space_editor:start
/function space_editor:space_group/set_room {id:2,roomId:"room_b"}
/function space_editor:proxy_existence/set_room {id:5,roomId:"room_b"}
/function space_editor:pair/set_pose {id:2,rotationY:90,flipY:1}
/function space_editor:projection/enable
/function space_editor:play
```

`set_room` はRegionを新規作成しません。存在範囲指定棒で作った `kind:"proxy_existence"` Regionを指定します。SpaceLinkGroupの作成・追加・編集は [SpaceLinkGroup仕様](space-link-groups.md) を参照してください。旧SpaceLinkの `partnerId` は使用しません。

Roomは任意の文字列IDで、同じDimensionの同じRoom名を持つ存在範囲の和集合を使います。別のRoomには別名を付けてください。存在範囲はリンク・TPとは独立です。移動・サイズ変更・削除は次の経路更新時に反映します。投影先のRoom名が空ならその経路は有効化しません。

|コマンド (`/function space_editor:` に続ける)|作用|
|---|---|
|`projection/enable`|正式投影を有効化。play中の侵入を検知|
|`projection/disable`|全正式経路・表示を削除して無効化。06-1検証Entityは別管理|
|`projection/status`|設定・ActiveProjection・当tickの拒否数を表示|
|`projection/clear`|全正式経路と侵入履歴を初期化。有効なら次tickの内部滞在も新規侵入として扱う管理用リセット|
|`projection/debug/map {target:3,region:7}`|本人の投影先Region 3をDebug Region 7にも表示する対応を保存|
|`projection/debug/on` / `projection/debug/off`|本人のDebug追加表示だけON/OFF。経路本体は変更しない|
|`projection/visual {pose:"standing",pivot:1.9}`|反転時の描画Y補正をブロック単位で調整。0〜4|
|`projection/swing`|本人の現在の代理へ腕振りイベントを送る|
|`projection/help`|ゲーム内ヘルプ|

Debug用Regionはリンクと同じローカルサイズを持つ通常Regionを推奨します。そのRegionの位置・回転・FlipYを使用するため、絶対座標のコピーにはなりません。Debugは親経路の存在判定に従い、独立した再侵入判定は持ちません。Debugも周囲の全プレイヤーに見えます。バニラで表示を本人だけに限定する機能ではありません。

`/reload` は経路を維持します。編集モードは表示を休止し、`space_editor:play` 後に再開します。退出・死亡・spectator化では経路を失効させます。再ログイン時は古い経路を引き継がず、現在位置から侵入状態を取り直します。

## 状態と処理順序

永続設定は `space_editor:document projection` に追加します。初期値は `enabled:0b`、`debugMaps:[]`、pose別ピボットとlabelGapです。既存Region・Mask・Template・履歴をリセットしません。

`storage space_editor:projection` の主要データは次のとおりです。`route` / `render` / `work` 等は同期関数内のscratchで、外部から書き換えないでください。

|データ|用途|
|---|---|
|`active[]`|有効な論理投影経路。Entityが未ロードでも保持|
|`players[]`|owner、UUID、leave統計、前tick/当tickの侵入接点|
|`nextId`|単調増加の経路ID|
|`schema`|現在1|
|`warning`|最後の未解決TP警告。履歴なので解消後も残ることがある|

経路キーは **owner + groupId + entrySourceId + targetId + sourceInstanceId**。同じRoomへ別Group・別入口から入る経路を潰しません。`id` はEntityとの結合キーです。`sourceId` はTPで変更できる現在の参照フレーム、`entrySourceId` は生成時から不変です。`uuid/currentInstanceId/targetInstanceId/roomId/dimension/point` も保持します。

Scoreboardは `pr.owner/id/epoch/debug/gc/v/leave`。`pr.leave` は `minecraft.custom:minecraft.leave_game`、他はdummyです。Entityは `space_editor.proxy` と `pr.production` または `pr.debug` を持ち、本体とtext_displayが同じ経路ID・owner・世代を共有します。Team `pr_hidden` が名前と衝突を抑制します。06-1の `sp.*`・Teamとは分離しています。

1. root tickで専用型・専用タグの古い世代、失効経路のEntityを分散回収。各Dimension・型ごと16体/tick、正常なEntityは40tick後に再確認。退出ownerは別途一括回収。
2. Stage05が全プレイヤーのTP前snapshotと `spaceLinkContacts` を生成。
3. `projection/before` が接点の外→内を比較し、到達可能な各targetへ経路を追加。有効経路だけを更新し、存在範囲外の経路だけを削除。
4. 既存 `#before_teleport` を実行後、Stage05が本人を転送。
5. `projection/after` が転送記録のUUIDごとにフレームを切り替え、既存 `#after_teleport` へ進む。

未転送時はStage05の既計算contact.destinationを再利用し、リンク外では `mapping/position` を呼びます。全Groupを毎経路再検証する `space_group/map` の重い経路を反復せず、Group所属とRegionの存在を確認して既存の同じ座標変換を呼びます。

本人TP時は、TPのsource/target回転・反転を現在のsourceフレームへ合成します。同Groupの候補フレームからTP後点を旧フレームへ逆変換し、TP前snapshotと0.0005ブロック以内で一致するものを選びます。Room名だけで決めないため、同Roomに複数の入口があっても変換で識別します。計算はownerのtransferごとに独立し、Groupと旧sourceの組でキャッシュします。到着接点を履歴へ追加し、TP到着だけで別経路を重複生成しません。Cの経路IDとロード中の本体UUIDは保持します。

同Groupに等価な到着フレームがない独立TPは自動継続できません。経路を `suspended:1b` として保持し表示を止め、warningを出します。該当入口へ再侵入すると再構築できます。任意の `/tp` はStage05の転送記録を発生させないため、この継続処理の対象外です。

## 描画・模倣の範囲

位置とYaw/PitchはStage05の半ミリブロック精度の座標変換を使います。反転状態は **source.flipY XOR target.flipY**。座標FlipYとモデルDinnerboneは別処理です。通常状態ではCustomNameを除去、反転状態では `Dinnerbone` を付与し、両状態でTeamの `nametagVisibility never` を維持します。`hide_description` と `CustomNameVisible:0b` だけには依存しません。

論理pointは常にプレイヤー足元の写像です。存在範囲判定もこの点を使います。反転時のEntity Yはpointからpose別ピボットを引き、名前は身体上側に独立表示します。初期ピボットはstanding=1.9、crouching=1.6、swimming/fall_flying=0.7、sleeping=0.3ブロック。公式26.1クライアントの `LivingEntityRenderer` が反転時に使う `getBbHeight()+0.1` に基づく値で、天井合わせの実測完了値ではありません。`projection/visual` で補正可能です。

スキンは元プレイヤーUUIDの動的 `profile`。防具4枠と両手を毎更新コピーし、poseは06-1 predicateとset_poseを再利用します。オフライン・プロフィール解決失敗ではデフォルトスキンになり得ます。`fetchprofile entity` のチャット出力をstorage取得APIとして扱いません。

TP追従で歩行・胴体回転をクライアント側に再現させます。プレイヤーの独立した頭角度・腕振り時刻・歩行位相をサーバーNBTから完全取得するものではありません。成功した直接攻撃はadvancementから `/swing` を送りますが、空振り・採掘・全使用モーションの完全同期はありません。泳ぎ・滑空はposeと座標に対応し、エフェクトや重力の共有はしません。

名前はbillboard center、背景0x40000000、shadowなし、see_throughなし、teleport_duration=1のtext_display。文字自体は反転しません。本物のネームタグとは壁越し表示、しゃがみ時の距離・透過、Team色の動的変更、身体との補間タイミングが異なります。名前は表示生成時に本人selectorから解決します。Debug名はGroup・入口→投影先・経路ID付きです。

本体は `immovable/NoGravity/Invulnerable/PersistenceRequired`、Teamの `collisionRule never` を使用します。押し出し・重力・通常ダメージを抑制しますが、視線のEntity選択や完全なヒットボックス消去を保証しません。敵MobのAI制御は対象外です。

## 予算と休止

通常は最大24経路/tickを更新します。接点が64件以上のtickは8経路（Debug有効なプレイヤーがいれば4経路）に抑え、未処理経路を先頭へ残すround-robinで次tickへ送ります。新規本体は本番・Debugを合わせて最大8体/tick。論理経路上限は全体256、接点走査4096、プレイヤー登録整理256、転送記録64です。上限拒否数はstatusに表示します。拒否された新規経路は自動的に再試行せず、再侵入が必要です。

少数経路は毎tick。大量経路では追従・削除が遅れます。126経路・8更新なら一巡16tickです。この負荷ケースを通常の描画品質の保証に使わないでください。24経路を超える利用ではStage07前に運用上限・優先度を設計してください。

表示先チャンクが未ロード、または96ブロック以内に実プレイヤーがいない場合、表示Entityを削除して論理経路を休止します。必要になれば同じ経路IDで表示を再作成します。この休止とreloadではEntity UUIDは変わり得ます。実Playerだけが投影元なので、代理から代理への再帰生成はありません。遅れてロードされた古いEntityは世代・owner・経路IDで回収します。強制チャンクロードはランタイムでは行いません。

## 自動検証と結果

```powershell
python tools/build_space_editor_stage6.py
pwsh -NoProfile -File tools/test_space_editor_stage6.ps1
pwsh -NoProfile -File tools/test_space_editor_stage5.ps1
pwsh -NoProfile -File tools/test_space_editor_stage6_1.ps1
```

生成は06入口→05→04→03→02→01→resources、05末尾で06-1と正式06を生成します。05入口でも正式06が残ります。下位段階を単独生成した後は最後に06を再生成してください。Javaとテストworldは開発専用で、ゲームのMod・外部API・実ワールドへのJava導入は不要です。

|項目|結果|確認方法・限界|
|---|---|---|
|Phase 1: 2Region座標・90度・FlipY・装備・名前|PASS（サーバー）|公式26.1 GameTestでXYZ/角度/pose/CustomName/Team/装備/名前をassert|
|Phase 2: A→B/C、同Roomへの別経路|PASS|同時生成、ID/UUID維持、20tick相当の増殖なしを確認|
|Phase 3: 存在範囲退出・再侵入・Debug|PASS|Cだけ削除、0.001境界minを含み0.0005外側を除外、戻るだけでは復活しない、再侵入のみ再生成、Debug OFFで本番UUID維持|
|Phase 4: 本人TP・2人同tick|PASS|分数座標でTP、CのID/UUID/論理点継続、相対Flip切替、名前分離|
|Region編集・削除、存在範囲削除|PASS|現行bounds追従、関係する本体・名前を回収|
|退出・再ログイン相当、load・実resource reload|PASS|owner分離、leaveカウンタ、経路IDの保存と復帰|
|未ロード先|PASS|実際に未ロードの位置へRegionを移し、経路保持・表示復帰をassert|
|任意の停止済みサーバーからの再起動|UNVERIFIED|reloadは確認済み。プロセス再起動を伴う再接続は別実機項目|
|スキン・歩行・頭/胴体の自然さ|UNVERIFIED（今回のクライアント）|06-1実現可能とのユーザー報告を継承。正式変換下の見た目は今回未操作|
|Dinnerbone反転・装備反転・名前の自然さ|UNVERIFIED（今回のクライアント）|設定とTeam/ラベルは確認。視覚上のPASSとはしない|
|非干渉化|PARTIAL|サーバー設定を実装。完全な当たり判定消去なし|
|additive demo|PASS|8Region、再実行、投影/Debug/TP、削除後に無関係Regionがバイト一致|

負荷測定は公式サーバー上で **`space_editor:tick` 全体**のExecutionContext消費枠を取得。上限65536をassertしています。Stage05・06を含みますが、サーバー全処理/描画/通信を含むMSPTではありません。時間はウォームアップ後10回の関数壁時計、JIT/GC/マシン負荷の影響を受けます。最大枠は入口での生成・同tick TPと定常処理を含みます。

|SpaceLink数|存在範囲数|人数|論理経路|本番/Debug本体|最大コマンド枠|中央値ms|p90相当ms|
|---:|---:|---:|---:|---:|---:|---:|---:|
|4|4|1|3|3/0|3,107|3.741|13.898|
|16|16|1|15|15/0|10,847|10.865|13.274|
|64|64|1|63|55/0|33,541|21.291|25.062|
|64|64|2|126|117/0|63,558|24.524|37.354|
|64|64|2|126|117/119|63,650|25.960|33.740|

最終上表の測定worldは `run-stage6-9b282975894548d1a3f213bea8883403`。64+64+TP2のケースは130 Regionで、ユーザーが挙げた64総Regionより重い構成です。96ブロック範囲外などの本体は休止しています。最大ケースの余裕は1,886枠で、追加の大規模機能を同じtickに載せられるという保証ではありません。Debugありは一巡32tickに低下します。上限を上げる変更はありません。

最終ValidateMinecraftは **5,651コマンド・エラー0**。Stage06の全Phase・reload・負荷・demoは明示PASS・終了コード0。Stage01〜05と06-1の既存GameTestもそれぞれrequired-test成功・終了コード0を確認しました。下位段階のランナーは `tools/test_space_editor_stage1.ps1`〜`stage5.ps1` です。Stage05では64接続先・2人の既存tickが51,925枠で完了しています。

JSON/mcmeta 6,822件の解析、関数参照解決、05/06生成入口のバイト一致、`git diff --check`を確認しました。追加JSONは `space_editor_datapack/data/space_editor/advancement/projection/attack.json` のみ。テクスチャ・モデルに差分はありません。

ログは `build/test-server/stage6-command-validation.log`、`stage6-runtime-validation.log`、`stage6-runtime-report.xml`。Windowsで隔離world終了時のlevel.dat rename警告が出る場合があります。required-test成功、明示PASS、終了コードを判定に使用し、実ワールドで試験を実行していません。

## 実機で残る確認とStage07への引き継ぎ

上のdemoで、通常/反転それぞれの歩行・走行・ジャンプ・しゃがみ、視線だけ動かした頭と胴体、装備・両手・攻撃、名前の背景と遮蔽を確認してください。水泳・滑空・睡眠は対応poseの成立する場所を別途用意します。天井合わせは、ブロック面と反転した足を比較してpose別pivotを調整します。TP中の身体と名前の見かけの連続性もクライアントで確認が必要です。

Stage07への接続点は `route_actor/update` のowner/instance照合、`debug_frame`・`render_*` のtarget座標解決、`after` の転送記録です。現在は同一Dimensionの離れたRoom、通常 `se.instance=0` で利用します。保存済み `sourceInstanceId` と `currentInstanceId` を、将来のInstance移動に合わせて更新するadapterを追加してください。`targetInstanceId` はRegion.instanceIdまたは0を保存するだけで、別Instanceの実体配置を生成しません。

現行のGC/削除はバニラ3Dimensionを列挙しています。独自Dimensionを追加する際はその列挙もInstance registryへ差し替える必要があります。共有scratchにscheduleを挟まず、UUID・経路ID・世代を維持してください。Room IDだけへキーを縮約したり、Mannequinを投影元にしたりしないでください。

参照: [最新Stage06仕様](https://app.notion.com/p/4041fd1a61518139a7f6ed7939cc5889)、[06-1の既存検証](stage06-1-mannequin.md)、[Minecraft 26.1公式変更履歴](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1)。
