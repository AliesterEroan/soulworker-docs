#!/usr/bin/env python3
"""Write icon.ico from icon.png so a later native shell can carry the app identity.

icon.png is a 64x64 master, so this file holds 16, 24, 32, 48 and 64 - each one a real
downscale. 128 and 256 are deliberately absent: they would be upscales and look soft at
Explorer's extra-large tile. Re-run this with a 256x256 icon.png when the master is redrawn.

Run after any change to icon.png:  python make_icon.py
"""

import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE = ROOT / "icon.png"
OUTPUT = ROOT / "icon.ico"
SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)]


def main():
    master = Image.open(SOURCE)
    if master.mode != "RGBA":
        raise SystemExit("icon.png must be RGBA, got %s" % master.mode)
    side = min(master.size)
    if side < max(s for s, _ in SIZES):
        raise SystemExit("icon.png is %dx%s, too small for %s" % (*master.size, SIZES[-1]))

    square = master.crop(((master.width - side) // 2, (master.height - side) // 2,
                          (master.width + side) // 2, (master.height + side) // 2))
    square.save(OUTPUT, format="ICO", sizes=SIZES)

    written = Image.open(OUTPUT)
    print("%s: %d bytes, entries %s" % (OUTPUT.name, OUTPUT.stat().st_size, written.info["sizes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
