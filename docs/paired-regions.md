# Paired Region implementation

> 2026-10-29: SpaceLinkの現行仕様・検証結果は
> [SpaceLink groups](space-link-groups.md) を参照。
> 以下の「SpaceLinkも2個」「片側削除で両側削除」は旧仕様。
> Teleportのペアと共通座標変換に関する契約は引き続き有効。

Base: `0f54e46` (`codex/tool-wand-visuals`). Live assets and the verified world
junction remain in place. Stage 05 calls 04 -> 03 -> 02 -> 01 -> resources.

## Scope and compatibility

Keep `space_editor:document`, schemaVersion 1, Region IDs and the existing AABB
fields. Add `rotationY`, `flipY`, `localSize` and pair references only where used.
Add a `regionPairs` list; leave legacy `portalLinks` and unrelated data intact.
Teleport and SpaceLink share editing, but only Teleport executes TP. Existence
Regions are standalone. Proxy entities and instance deployment belong to 06/07.

Existing fixed milliblock bounds remain authoritative. Center is derived from
both endpoints, using doubled milliblocks in calculations. Quarter turns and
vertical reflections are signed axis permutations, with no trigonometry.
`mapping/position` maps source world -> local -> target world; its vector and
look outputs use the same poses. Pair resize maps a world face back to a local
face and then onto the partner. Both candidate Regions validate before commit.

## Geometry decision

The latest Notion 05 requests both fixed-center rotation and integer block-grid
boundaries. These cannot both hold for a 3 x 4 footprint. The user's explicit
fixed-center rule takes priority: half-block boundaries are retained exactly.
No implicit translation or rounding is allowed. Existing sub-block Region
editing continues to work. The world limits remain those of the editor.

## Branch dependencies and verification

1. `codex/region-transform-core`: common coordinate/orientation calculations;
   all 8 x 8 endpoint poses, inverse mapping, negative/fractional coordinates.
2. `codex/paired-region-editor` on 1: additive persistence, shared creation and
   placement, atomic local-face resize, independent pose/movement, pair deletion,
   orientation preview, standalone existence Region, reload and regressions.
3. `codex/teleport-regions` on 2: player snapshots, boundary checks, per-player
   re-entry lock/cooldown, destination load checks, 06-facing mapping API.

Each branch runs the Minecraft dispatcher and Stage 05 GameTest before commit.
The final implementation also runs Stage 02-04 regressions. GameTest evidence
does not establish client rendering or live mouse interaction.

## Runtime contracts for 06

All scratch values below are in `space_editor:runtime`. Persistent definitions
are in `space_editor:document`; runtime snapshots are not the saved document.

`mapping/position` accepts:

```snbt
map:{
  source:{dimension:"minecraft:overworld",x1m:0,x2m:3000,y1m:80000,y2m:84000,z1m:0,z2m:5000,rotationY:0,flipY:0b},
  target:{dimension:"minecraft:overworld",x1m:19000,x2m:24000,y1m:80000,y2m:84000,z1m:1000,z2m:4000,rotationY:90,flipY:1b},
  point:[0.5d,80.5d,1.5d],vector:[0d,0d,1d],yaw:15f,pitch:25f
}
```

It writes `map.result` with `dimension`, `point`, scalar `x/y/z`, `vector`,
`yaw/pitch`. Point and vector precision is 0.0005 block; look precision is
0.001 degree. The initial input is quantized down; values already emitted on
the fixed grid are read without repeated floating-point floor drift. Swapping
source and target gives the inverse. Missing poses mean identity, and vectors
and look are optional. Callers must supply valid Region records and coordinates
within the editor's supported range. Quarter turns use Minecraft positive yaw:
local +Z points to world -X at 90 degrees. FlipY reverses Y and pitch.

Tick order is fixed:

1. Capture all `playerSnapshots` (UUID, dimension, point, rotation, instanceId).
2. Build `spaceLinkContacts` from these snapshots using the common mapping.
3. Run `#space_editor:before_teleport` (empty extension tag in 05).
4. Execute player TP; append successful `transfers`, retaining pre-TP snapshots.
5. Run `#space_editor:after_teleport` (empty extension tag in 05).

Contacts and transfers include source/target Region and Room IDs, pairId,
source UUID/instanceId and mapped destination. Contacts are current overlap
samples, **not** persistent projection routes or enter/leave events. Stage 06
owns those routes, existence-volume membership, deduplication and Proxy cleanup.
Cooldown never suppresses contact sampling. Editing mode suppresses gameplay
hooks and TP while retaining snapshots. Dead players do not contact/transfer.
`se.instance` is an identification slot for 07, not an instance allocation system.

`mapping/contains` accepts `spatialRegion` and `#spx/#spy/#spz se.v` in doubled
milliblocks, runs in the point's dimension, and writes `#inside se.v`. It tests
the foot point against half-open AABB boundaries. It does not cast an editor ray.

## Pair APIs and transactions

### 編集棒と箱の色

TP接続棒は水色の門、SpaceLink接続棒はエメラルド色の連結形、Proxy存在範囲棒は黄色の立体枠です。
対応するRegionの箱も棒と同じテクスチャを使った12辺の枠で表示します。
TPは水色、SpaceLinkは緑、Proxy存在範囲は黄色、通常Regionは従来のシアンです。
配置プレビュー・確定後・選択解除・編集再描画でも種類の色を保持します。
前／上の方向矢印は従来どおり緑／黄色です。

反映は `/reload` と `F3+T`。古い棒のモデル指定がない場合は
`/function space_editor:start` で再支給します。リソースパックはtestpackを優先してください。
箱は既存selection用キャリアのfacing別モデルを使用し、Regionの保存座標・回転には影響しません。
自動試験は配置／確定／選択と解除のブロック状態を検証し、実際の描画はクライアントで確認します。

- `pair/create {source:ID,kind:"teleport"}` or `kind:"space_link"` uses the
  prepared `pairCandidate` Region. Both records validate and local sizes must
  match before mutation. `#pair_ok se.v` is 1 only after a successful commit.
- `pair/set_pose {id:REGION_ID,rotationY:90,flipY:1}` changes only that member.
- `pair/delete {pairId:PAIR_ID}` removes the two members, attached Masks and
  pair link. One Action contains the pair/members/attached-Mask/group snapshot.
- `pair/configure {id:PAIR_ID,groupId:1,roomA:"a",roomB:"b",direction:"both",cooldownTicks:20}`
  attaches a group. Group 0 means independent; `one_way` means A -> B. Group
  Room ordering must match. Cooldown accepts 0..1200 ticks. No automatic pose
  reconciliation occurs. Empty groups are removed when their final reference
  is deleted or moved to another group.
- `proxy_existence/set_room {id:REGION_ID,roomId:"a"}` associates a standalone
  existence volume. It cannot turn a paired Region into an existence Region.
- `link/validate_groups` / `link/status` populate `linkWarnings`. Every TP /
  SpaceLink pair sharing a group is checked for affine mapping equality and
  containment on both sides. An ungrouped pair remains independently usable.

Existing move/resize wands still compute the edited face and the candidate AABB.
The new hook intercepts the save before Document mutation, computes corresponding
partner changes via the same signed-axis basis, validates both, then commits.
The pair and its Action are saved synchronously in one function chain. Undo/Redo
execution itself is not added. Displays are derived and rebuilt on load/resume.

Teleport locks are player scoreboard state and survive `/reload`. The lock clears
once outside both members of the last pair; cooldown independently limits repeat
activation. Deleting a pair makes the stale lock clear on the next evaluation.
Destination checks use the corners of an upright 0.6 x 1.8 player envelope and
the existing passable-block tag; this is conservative, not a general voxel-shape
collision solver. Solid/non-passable cells cause a retry without changing terrain.
No new chunk tickets are created. Vanilla player gravity/body/roll and velocity
are not transformed; the vector output remains available for 06 consumers.

## Asset changes

No PNG changes are part of this implementation. Existing authored Mask and
selection-candidate textures remain intact. The following ten JSON files are
new in **each** of `assets/editor/` and `space_editor_resources/assets/editor/`:

- `items/tool_teleport.json`, `items/tool_space_link.json`, `items/tool_proxy_existence.json`
- `models/item/tool_teleport.json`, `models/item/tool_space_link.json`, `models/item/tool_proxy_existence.json`
- `items/direction_front.json`, `items/direction_up.json`
- `models/item/direction_front.json`, `models/item/direction_up.json`

The two added datapack JSON files are
`space_editor_datapack/data/space_editor/tags/function/before_teleport.json` and
`space_editor_datapack/data/space_editor/tags/function/after_teleport.json`.
All 22 files are parsed and the resource copies are synchronized. No texture
targets were requested, processed or skipped as part of the final changes.

## Validation evidence

Final run on 2026-10-28:

- `ValidateMinecraft`: **2944 commands, 0 errors**.
- `SPACE_EDITOR_STAGE5_RUNTIME_PASS` and all required tests passed.
- Stage 02, Stage 03 and Stage 04 runtime regressions: PASS on the final pack.
- 97 relevant JSON files parsed, including every edited/added JSON file.
- All static `space_editor:` function references resolve; ten new live model/item
  files exactly match their resource-source copies; `git diff --check` passed.
- No PNG remains changed. The pre-existing resource generator rewrites several
  generated PNGs while building; those unrelated outputs were restored to the
  clean starting checkout's bytes before delivery.

The isolated server emits Windows `level.dat` rename warnings during shutdown.
Command validation, explicit runtime assertions, required-test results and
process exit codes succeeded. This test server is separate from the live world.

Stage 05 covers all 64 pose pairs, repeated fractional point/look round trips,
384 face combinations with fixed opposite faces, whole-size grow/shrink,
mixed-parity center rotation, atomic height rejection, independent movement,
single pair IDs, save/load compatibility, pair deletion isolation, live preview
entity reuse, arrow orientation, visibility, Group warnings, TP position/look,
re-entry lock, reload lock, dead/editing players, unloaded/blocked destinations,
maxExclusive, two distinct players in the same tick, pre-TP SpaceLink contacts
and real Overworld-to-Nether transfer in an isolated GameTest world.

The client has not been used to confirm actual mouse gestures, rendering, TP
smoothness or observer-visible effects. Stage 06 Proxy rendering is out of scope.

Sources (read 2026-10-28):
- https://app.notion.com/p/4041fd1a615181159d48dea3d575a76e
- https://app.notion.com/p/4041fd1a61518139a7f6ed7939cc5889
