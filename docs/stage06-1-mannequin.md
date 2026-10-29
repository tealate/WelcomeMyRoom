# Stage06-1｜Mannequin単体技術検証

06-1は同一Dimensionのプレイヤー1人を基本とする単体スパイクです。05のSpaceLinkGroupには接続しません。`storage space_editor:document` は変更しません。実装の正本は `tools/build_space_editor_stage6_1.py` で、05の生成後に06-1専用関数を追加します。

## ゲーム内で使う

データパックはライブの `space_editor_datapack/` に配置済みです。**`/reload`** 後、チャットで以下を実行してください。リソース変更はないため `F3+T` は不要です。各関数は操作するプレイヤー自身が実行します。再生成は `python -B tools/build_space_editor_stage6_1.py` を使います。

| 操作 | コマンド |
| --- | --- |
| 自分のMannequinを約3ブロック前に生成し追従開始 | `/function space_editor:proxy_spike/spawn` |
| 通常とDinnerboneを左右に比較（主役は反転、左側に通常）。Dinnerboneの文字はTeamで隠し、両体に元プレイヤー名を別表示 | `/function space_editor:proxy_spike/pair` |
| 追従開始／再開 | `/function space_editor:proxy_spike/follow_on` |
| 追従停止（その場に残す） | `/function space_editor:proxy_spike/follow_off` |
| 主役をDinnerbone反転／通常へ | `/function space_editor:proxy_spike/flip_on` / `flip_off` |
| `CustomNameVisible:0b` を比較 | `/function space_editor:proxy_spike/name_custom_hidden` |
| Teamでネームタグを隠す | `/function space_editor:proxy_spike/name_team_hidden` |
| `description` に元プレイヤー名を表示 | `/function space_editor:proxy_spike/name_description` |
| 別の `text_display` で各Mannequinの頭付近に表示 | `/function space_editor:proxy_spike/name_text_display` |
| 腕振りを試す | `/function space_editor:proxy_spike/swing_main` / `swing_off` |
| 現在状態 | `/function space_editor:proxy_spike/status` |
| 自分の検証Entityを全削除 | `/function space_editor:proxy_spike/delete` |

状態表示の `follow` は1が追従中、`flip` は1がDinnerbone、`name mode` は0=`CustomNameVisible`、1=Team、2=`description`、3=`text_display`です。`/reload` は検証Entityを削除し追従を停止します。生成し直してください。プレイヤーが退出した場合も、対象チャンクがロードされた次のtickで検証Entityを回収します。未ロードチャンクは強制ロードしません。

`/fetchprofile entity @s` で本人のプロフィールを表示できます。`/fetchprofile entity @e[tag=sp.main,limit=1]` でMannequinのプロフィールも比較してください。`/fetchprofile` は表示用でstorageへコピーする機能ではありません。Mannequinの `profile` は本人のUUIDのみを設定して動的解決を試します。取得が遅い、または取得できない場合はデフォルトスキンで他の項目を続けてください。

## 観察順序

1. `pair` で通常と反転を並べ、F5などの三人称視点でスキン、防具、手持ち、胴体と頭、静止時の反転と描画高さを比較します。第三者視点でも確認してください。
2. `name_custom_hidden` で通常時・視線を合わせた時のDinnerbone文字と反転状態を確認します。次に `name_team_hidden` を同様に確認します。
3. `name_description` で文字が頭上ではなく `below_name` 相当の場所に出るか、名前が正しいかを確認します。`hide_description:1b` に戻すには `name_custom_hidden` を実行します。
4. `name_text_display` で頭上名の文字向き、背景、文字サイズ、視距離、カメラ追従、高さを本物のプレイヤーネームタグと比較します。近くに別のプレイヤーがいても元プレイヤー名になるか確認します。
   通常体は足元座標から約2.3ブロック上、Dinnerbone体は反転した頭に合わせて約0.7ブロック上に置きます。この高さは描画の実測前の仮値です。
5. 歩行、旋回、ジャンプ・落下、しゃがみ、水泳、滑空を個別に試します。`swing_main` / `swing_off` はクリック検出との連動ではなく、明示的な腕振りテストです。通常／反転で双方を試します。
6. 足場と天井で、反転時の表示足位置と実座標の差をF3+Bで確認します。必要な補正量を記録します。追従停止中の重力・押し出し・攻撃、`delete` と `/reload` 後の残留も確認します。

## 技術検証レポート（2026-10-30）

ここでのPASSは26.1サーバーのGameTestで実体状態を確認できたものだけです。クライアント描画を伴う事項は実機で未確認です。

| 項目 | 判定 | 証拠・次の確認 |
| --- | --- | --- |
| 生成・比較用2体・所有者別削除 | PASS | GameTestで生成、参照体、削除を確認。2人同時の見た目はUNVERIFIED。 |
| `profile`へ本人UUID | PASS | GameTestでMannequinの`profile.id`を確認。 |
| 本人のスキン表示 | UNVERIFIED | `/fetchprofile entity @s` とMannequinを比較し、スキン解決を目視。 |
| 防具・両手装備 | PARTIAL | GameTestで頭防具と両手の内容を確認。表示と更新の見た目は目視。 |
| 座標・Yaw/Pitch追従 | PARTIAL | GameTestで3ブロック前へのTPと追従を確認。頭・胴体のクライアント回転は未確認。 |
| 歩行・ジャンプ・落下 | UNVERIFIED | TP追従中の歩行アニメーションと上下動、描画遅延を目視。 |
| しゃがみ・水泳・滑空 | PARTIAL | プレイヤーのpredicateフラグからMannequin `pose`へ同期し、GameTestで3種の保存値を確認。アニメーションは目視。プレイヤーの`Pose`は`/data get`で取得できなかった。 |
| `/swing` | PARTIAL | 26.1の構文を検証。表示の腕振り、元プレイヤーのクリックとの自動同期は未確認。 |
| Dinnerbone文字列を設定 | PASS | GameTestで`CustomName:"Dinnerbone"`を確認。 |
| Dinnerbone反転、スキン・装備・アニメ・回転 | UNVERIFIED | `pair`で通常体と比較。静止、歩行、しゃがみ、水泳、腕振りを個別に確認。 |
| 反転時の描画基準点・天井補正 | UNVERIFIED | F3+Bで座標と表示位置を比較。補正は実測後に決める。 |
| `CustomNameVisible`で文字を隠す | FAIL | 初回実機確認でDinnerboneの文字が見えた。視線を合わせた時だけか常時かは追加確認。 |
| Teamで文字を隠し反転を維持 | UNVERIFIED | `pair`と`name_team_hidden`で文字と反転を目視。Team所属はGameTestで確認。 |
| `description`による名前 | PARTIAL | 公式仕様上、表示位置は`below_name`相当。GameTestでモード切替を確認。実際の文字・位置は目視。 |
| `text_display`による両体の名前 | PARTIAL | GameTestで2体それぞれの表示Entityと元プレイヤーUUIDからのユーザー名解決、通常／反転の配置座標を確認。背景・サイズ・見た目の高さ・追従は実機確認。 |
| 重力・ダメージ・衝突抑制 | PARTIAL | `immovable`、`NoGravity`、`Invulnerable`の保存状態をGameTestで確認。両Teamの`collisionRule never`を設定。実際の押し出しは目視。 |
| 05回帰 | PASS | Stage05 GameTestとMinecraftコマンド構文検証が成功。 |

`description`は本物の頭上ネームタグとは位置が異なります。`text_display`も別Entityなので、プレイヤー名の描画規則（しゃがみ時の半透明化、視距離、深度、サイズ、背景、他Teamの色）と完全一致する保証はありません。クライアント実測で差を記録し、06-2以降の表示方式を決めてください。スキン取得に失敗した場合は、UUIDを維持したままデフォルトスキンで他の検証を続行します。

26.1の公式仕様は [`/swing` と `/fetchprofile entity`](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1)、[Mannequinのフィールドと`description`](https://feedback.minecraft.net/hc/en-us/articles/39966147272589-Minecraft-Java-Edition-1-21-9-The-Copper-Age)、[プロフィールの動的解決](https://feedback.minecraft.net/hc/en-us/articles/39092387123469-Minecraft-Java-Edition-Snapshot-25w34a-b) を参照。仕様の最新06-1は [Notion 06](https://app.notion.com/p/4041fd1a61518139a7f6ed7939cc5889) の2026-10-30節を優先しています。
