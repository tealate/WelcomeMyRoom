# testpack working rules

## Project scope

- This repository is a Minecraft Java Edition 26.1 resource pack.
- `pack.mcmeta` targets resource-pack format 84.
- Keep changes small and directly tied to the user's requested experiment.
- Preserve unrelated working-tree changes. Never revert, replace, or delete them.
- Do not commit, push, or broadly rewrite assets unless the user explicitly asks.

## Live editing workflow

- The user-provided working folders are intended for direct use by Minecraft,
  with resource changes reflected through `F3+T` and datapack changes through
  `/reload`. Default to editing the active files in place.
- Deliver working changes in the existing live folder layout, not separate
  distribution folders that require the user to copy or install them manually.
- Check the actual resource-pack and datapack roots when choosing output paths.
  Do not assume that newly nested pack folders are automatically loaded, or
  describe a resource-pack folder as the world root without verifying it.
- Do not create ZIP archives or add packaging/install steps unless the user
  explicitly requests distribution or packaging.
- Existing ZIPs do not need to be deleted; leave them unless asked otherwise.
- Completion instructions should identify the applicable refresh action:
  `F3+T`, `/reload`, or both. Mention a restart only when the change requires it.
- Current live mapping: this checkout's root `assets/` is the active `testpack`;
  `space_editor_datapack/` is referenced by a directory junction at
  `C:\Users\yoshida_kaito\AppData\Roaming\.minecraft\saves\新規ワールド (2)\datapacks\space_editor`.
  Edit these sources directly. The current stage generators call
  `tools/build_space_editor_resources.py`, which synchronizes the declared
  rendering assets into root `assets/`.

## Space Editor namespaces and generation

- Runtime functions and saved data use `space_editor:`. Do not restore the
  removed `editor:` compatibility functions or `storage editor:data` workflow.
- The `assets/editor/` resource namespace is still active: current block
  displays reach its models through configured vanilla blockstate carriers.
  Do not remove those assets merely because the namespace is named `editor`.
- Generator dependency order is Stage 03 -> Stage 02 -> Stage 01. Stage 04 is
  developed on top of Stage 03 and must keep using that chain.
- `space_editor:document` is persistent world data. Generators may add fields
  through migrations, but cleanup work must not delete or reset the document.

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
- When changing generated `mcfunction` behavior, edit the generator, regenerate
  the live output, run `ValidateMinecraft`, and run the GameTest for the latest
  affected Space Editor stage. A successful parse alone is not enough because
  valid commands can still fail to create entities or mutate runtime state.
- Keep stage-specific Java GameTest harnesses and their PowerShell runners in
  `tools/`. They are development checks only and are not runtime dependencies
  of the resource pack or datapack.
- If validation is intentionally skipped for a particular experiment, retain
  the harness and report the result as unverified rather than complete.
- For PNG edits, rely on the script's save-before-replace pixel verification.
- After texture processing, run the same command with `--dry-run`; the selected
  textures should report `already-translucent` and receive no further changes.
- Report the exact textures and JSON files changed, plus skipped targets and the
  reason for each skip.
