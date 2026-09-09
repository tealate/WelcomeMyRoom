# testpack working rules

## Project scope

- This repository is a Minecraft Java Edition 26.1 resource pack.
- `pack.mcmeta` targets resource-pack format 84.
- Keep changes small and directly tied to the user's requested experiment.
- Preserve unrelated working-tree changes. Never revert, replace, or delete them.
- Do not commit, push, or broadly rewrite assets unless the user explicitly asks.

## Texture render-pass behavior

- Minecraft 26.1 chooses a block quad's render pass from the assigned sprite:
  - any alpha from 1 through 254: `translucent`
  - alpha 0 but no partial alpha: `cutout`
  - every pixel alpha 255: `solid`
- A texture-map object may set `"force_translucent": true` to force the
  translucent pass. There is no corresponding supported `force_opaque` field.
- `"force_translucent": false` leaves automatic sprite-content detection in
  effect; it does not force the solid pass.

## Marking a texture translucent

- Use `tools/mark_textures_translucent.py` when a selected texture should enter
  the translucent pass without a visible design change.
- Prefer a narrow texture ID or explicit PNG path, for example:
  `python tools/mark_textures_translucent.py block/dirt`.
- In Codex Desktop, if `python` is not on `PATH`, load the bundled workspace
  dependencies and run the script with the returned Python executable.
- Multiple explicit textures may be passed in one command.
- Run with `--dry-run` first when the target list is broad or uncertain.
- Do not pass the entire textures directory unless the user explicitly requests
  a bulk operation.
- The script must only change one pixel from alpha 255 to 254. It must not turn
  alpha-0 pixels opaque or alter any RGB channel.
- If a texture already contains partial alpha, leave it unchanged.
- If a texture contains no alpha-255 pixel, report it and leave it unchanged.
- To return a texture to the solid pass, all of its pixels must have alpha 255;
  do not invent an unsupported JSON field.

## Validation and reporting

- Parse every edited JSON file before reporting completion.
- For PNG edits, rely on the script's save-before-replace pixel verification.
- After texture processing, run the same command with `--dry-run`; the selected
  textures should report `already-translucent` and receive no further changes.
- Report the exact textures and JSON files changed, plus skipped targets and the
  reason for each skip.
