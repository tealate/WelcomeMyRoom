"""Mark selected PNG textures as translucent with a negligible alpha change.

Each target can be a PNG, a directory, or a texture ID such as ``block/dirt``.
The script changes exactly one pixel whose alpha is 255 to alpha 254. Pixels
with any other alpha value, including fully transparent pixels (alpha 0), are
never selected or changed.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import tempfile

from PIL import Image

TEXTURE_ROOT = Path("assets/minecraft/textures")


def image_pixels(image: Image.Image) -> list[tuple[int, int, int, int]]:
    """Support both current Pillow and versions before get_flattened_data."""
    getter = getattr(image, "get_flattened_data", image.getdata)
    return list(getter())


def resolve_target(value: str) -> list[Path]:
    direct = Path(value)
    if direct.is_file():
        if direct.suffix.lower() != ".png":
            raise ValueError(f"target is not a PNG: {value}")
        return [direct]
    if direct.is_dir():
        return sorted(direct.rglob("*.png"))

    texture_id = value.removeprefix("minecraft:").replace("\\", "/")
    shorthand = TEXTURE_ROOT / texture_id
    if shorthand.suffix.lower() != ".png":
        shorthand = shorthand.with_suffix(".png")

    root = TEXTURE_ROOT.resolve()
    resolved = shorthand.resolve()
    if root not in resolved.parents or not resolved.is_file():
        raise FileNotFoundError(f"texture not found: {value}")
    return [shorthand]


def process_png(path: Path, dry_run: bool) -> str:
    with Image.open(path) as source:
        source.load()
        before = source.convert("RGBA")
        metadata = {
            key: source.info[key]
            for key in ("icc_profile", "dpi")
            if key in source.info
        }

    pixels = image_pixels(before)
    if any(0 < pixel[3] < 255 for pixel in pixels):
        return "already-translucent"
    # Prefer the last opaque pixel so a common opaque top-left corner is not
    # needlessly chosen, while remaining deterministic across runs.
    selected = next(
        (index for index in range(len(pixels) - 1, -1, -1) if pixels[index][3] == 255),
        None,
    )
    if selected is None:
        return "no-opaque-pixel"

    original_pixel = pixels[selected]
    red, green, blue, _ = original_pixel
    pixels[selected] = (red, green, blue, 254)
    if dry_run:
        return "would-change"

    after = Image.new("RGBA", before.size)
    after.putdata(pixels)

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=f".{path.stem}.", suffix=".png", delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)
        after.save(temp_path, format="PNG", **metadata)

        with Image.open(temp_path) as check_source:
            check = check_source.convert("RGBA")
            check.load()
        changed = [
            index
            for index, (old, new) in enumerate(
                zip(image_pixels(before), image_pixels(check))
            )
            if old != new
        ]
        expected = original_pixel
        actual = image_pixels(check)[selected]
        if changed != [selected] or expected[:3] != actual[:3] or expected[3] != 255 or actual[3] != 254:
            raise RuntimeError(f"verification failed for {path}")

        try:
            os.replace(temp_path, path)
        except PermissionError:
            # Some Windows live-pack setups reject replacing a watched PNG.
            # The temporary image has already passed pixel verification, so
            # fall back to a byte copy and verify the final file as well.
            shutil.copyfile(temp_path, path)
            if path.read_bytes() != temp_path.read_bytes():
                raise RuntimeError(f"final copy verification failed for {path}")
            temp_path.unlink()
        temp_path = None
        return "changed"
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Change one opaque pixel to alpha 254 in selected textures."
    )
    parser.add_argument(
        "targets",
        nargs="+",
        help="PNG path, directory, or texture ID (for example: block/dirt)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    paths: list[Path] = []
    seen: set[Path] = set()
    for target in args.targets:
        for path in resolve_target(target):
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                paths.append(path)

    counts: dict[str, int] = {}
    for path in paths:
        result = process_png(path, args.dry_run)
        counts[result] = counts.get(result, 0) + 1
        print(f"{result}: {path.as_posix()}")

    print("--- summary ---")
    for result, count in sorted(counts.items()):
        print(f"{result}: {count}")


if __name__ == "__main__":
    main()
