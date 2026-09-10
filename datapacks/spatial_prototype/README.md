# 空間歪曲・マスク実験

Java 26.1用。リソースパック `testpack` とこのデータパックを両方有効にする。
新しいディメンションを登録するため、初回導入後はワールドを開き直す。
ワールドのブロック・エンティティ・接続はすべてmcfunctionで作る。

```mcfunction
/function prototype:boot
# ALL READY 表示後
/function prototype:goto/hub
/function prototype:goto/01
/function prototype:goto/02
/function prototype:goto/03
/function prototype:goto/04
/function prototype:goto/05
/function prototype:reset
```

`prototype:p01/setup` ～ `prototype:p05/setup` は単独で再生成可能。
setupは読み込み予約を行い、tickが全対象チャンクの読み込みを確認してbuildを呼ぶ。
bootは毎回全setupを呼ぶ。各buildが対象範囲と専用タグのエンティティを消してから再生成する。
実行場所・向き・ディメンションに依存しない。移動functionはプレイヤーとして実行する。

## 配置と操作

専用の空ディメンション `prototype:lab` を使用。通常ワールドの地形は変更しない。
ハブ=(0,64,0)、p01=(128,64,0)、p02=(256,64,0)、p03=(384,64,0)、
p04=(512,64,0)、p05=(640,64,0)。各地点は128ブロック間隔。
ハブの金色の床に乗ると対応する実験へ移動。各実験からは `goto/hub` で戻る。
通常ワールドへは元の座標を指定した `/execute in minecraft:overworld run tp @s X Y Z` を使用。

各原点に対してX=-16..31、Y=-1..20、Z=-16..63を再生成用として予約する。
この範囲への手動建築はboot/resetで消える。座標の編集元は
`tools/build_spatial_prototypes.py` のSITES、出力一覧は `sites.json`。
全体で90チャンクをforceloadする。resetは実験75チャンクを解放し、
落下防止用のハブ15チャンク・床・案内だけ残す。ラボ内のプレイヤーはハブへ退避する。
reset直後にbootしても、最後に指定された生成状態へ収束する。

## 作成した5案

| ID | 表現・仕組み | 観察方法／制限 |
| --- | --- | --- |
| 01 | 方向限定透視壁。通常設置の対象壁の手前へ薄いマスクDisplay。奥に赤青の立体 | 金色の線から正面・斜め・裏を比較。方向限定の強さは未検証 |
| 02 | 小屋より大きな内部。7×7の対象シェル、21×18のホール先行表示、別座標の同形ホールへTP | 入口の金色の床を進む。x/yと視線保持、z移動、20tickクールダウン。戻り入口あり。完全に継ぎ目のないポータルではなく実験配置 |
| 03 | 左右の覗き口から赤／青の違う部屋。2つのマスクと不透明な中央仕切り | 赤青の足場へ移動して覗く。同じ画素の空間差し替えではなく、静的な視差・遮蔽配置 |
| 04 | マスク壁の奥に上下反転した家具。DisplayをZ軸180度回転 | 金色の床から観察。室内と家具のみのジオラマ。重力変更・代理プレイヤー同期は含まない |
| 05 | 密着した対象ブロック／1ブロック間隔／同位置のDisplay群を比較 | 奥の緑壁、内部面の残り方、横からの欠けを比較。さらに奥に不透明版と対象版の対照壁 |

全Display/marker/text_displayに `prototype.entity` と `prototype.p01` 等を付与。
マスクDisplayには `prototype.mask`、装飾には `prototype.decor` も付与。
配置やスケールは各buildのsummon行で確認できる。変更を恒久化する場合は生成スクリプトを編集する。

## リソースの変更範囲

- `assets/minecraft/blockstates/smooth_basalt.json` → `prototype:block/mask_stone`
- `assets/minecraft/blockstates/calcite.json` → `prototype:block/mask_oak`
- 追加JSON: `assets/prototype/models/block/mask_stone.json`, `mask_oak.json`
- 追加PNG: `assets/prototype/textures/block/mask_stone.png`, `mask_oak.png`
- マスク本体専用: `assets/minecraft/blockstates/waxed_oxidized_cut_copper.json`
  → `assets/prototype/models/block/mask_body.json`
  → `assets/prototype/textures/block/mask_body.png`（全256画素がα1）。

通常版はsmooth_stone / oak_planks、対象版はsmooth_basalt / calcite。
対象用のmask_stone / mask_oakは通常版の複製で、RGBを変えず1ピクセルのα255だけを254へ変更。
マスク本体は別IDのwaxed_oxidized_cut_copperを使い、smooth_stone由来のRGBを保った全画素α1の専用画像へ分離。
`prototype.mask` のDisplay全10体だけをこのIDへ変更。比較用Displayや通常設置の対象は元のまま。
本体画像は生成スクリプトが保存後・置換前にRGBと全α値を検証する。既存の1画素半透明化スクリプトは変更しない。
このパックが有効な間は全ディメンションのsmooth_basaltとcalciteの外観も変わる。
waxed_oxidized_cut_copperも全ディメンションでほぼ不可視になるため、実験専用IDとして扱う。
既存のstone.pngはα102/155/163を含むため、不透明対照として使わない。
既存dirt.pngの未コミット変更と既存シェーダーは保持。force_translucent追加・スライム利用なし。

## 検証・再生成

リポジトリ直下で以下を実行する。PythonがPATHになければCodex bundled Pythonを指定。

```text
python tools/build_spatial_prototypes.py
python tools/mark_textures_translucent.py assets/prototype/textures/block/mask_stone.png assets/prototype/textures/block/mask_oak.png
python tools/mark_textures_translucent.py assets/prototype/textures/block/mask_stone.png assets/prototype/textures/block/mask_oak.png --dry-run
python tools/mark_textures_translucent.py assets/prototype/textures/block/mask_body.png --dry-run
python tools/validate_spatial_prototypes.py
```

PNGの保存前検証と再dry-runを実施。最終dry-runは3枚ともalready-translucent（追加変更をスキップ）。
マスク本体の変更を既存の配置へ反映するには、F3+Tでリソースを再読込し、`/reload` の後 `/function prototype:boot` で再生成する。
JSON全件、function参照、使用ブロックID、SNBT、fill容量、予約範囲の重複、アルファ差分を静的確認。
Minecraft自身のコマンドパーサー・生成実行・画面描画による検証は行っていない。
実機では初回ロードエラー、全地点のready、boot再実行の重複、p02の往復、resetの退避、
マスクの前後関係・カリング・斜め視点の欠けを確認する。

## 確認した既存資料

- 指定ワールドの既存 `datapacks/tameshi` はformat 15のpack.mcmetaとassetsが主体で、mcfunctionなし。変更しない。
- [Notion 技術検証](https://app.notion.com/p/3d61fd1a61518171a07cdeed0287dd1d) の最新Block Display方式を採用。
- [Minecraft 26.1公式](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1) とインストール済み26.1.jarのversion.jsonで、データ101.1／リソース84を確認。
