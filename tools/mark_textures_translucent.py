"""Mark PNG textures as translucent with one visually negligible alpha change.

For every PNG below the target directory, this script changes exactly one pixel
whose alpha is 255 to alpha 254. Pixels with any other alpha value, including
fully transparent pixels (alpha 0), are never selected or changed.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from PIL import Image


def process_png(path: Path, dry_run: bool) -> str:
    with Image.open(path) as source:
        source.load()
        before = source.convert("RGBA")
        metadata = {
            key: source.info[key]
            for key in ("icc_profile", "dpi")
            if key in source.info
        }

    pixels = list(before.get_flattened_data())
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
                zip(before.get_flattened_data(), check.get_flattened_data())
            )
            if old != new
        ]
        expected = original_pixel
        actual = list(check.get_flattened_data())[selected]
        if changed != [selected] or expected[:3] != actual[:3] or expected[3] != 255 or actual[3] != 254:
            raise RuntimeError(f"verification failed for {path}")

        os.replace(temp_path, path)
        temp_path = None
        return "changed"
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path, help="Directory containing PNG textures")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    counts: dict[str, int] = {}
    for path in sorted(args.target.rglob("*.png")):
        result = process_png(path, args.dry_run)
        counts[result] = counts.get(result, 0) + 1

    for result, count in sorted(counts.items()):
        print(f"{result}: {count}")


if __name__ == "__main__":
    main()
