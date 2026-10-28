# Paired Region implementation

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

Sources (read 2026-10-28):
- https://app.notion.com/p/4041fd1a615181159d48dea3d575a76e
- https://app.notion.com/p/4041fd1a61518139a7f6ed7939cc5889
