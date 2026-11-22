"""A coarse ink map of the sheet, printed to the terminal.

Rows of 16px and columns of 8px, one character per cell by how much ink lands in
it. This is how a layout bug is found without an image viewer: a section that
runs into another, a column that never fills, a panel that failed to draw.
"""

import sys

from PIL import Image

PAPER = (250, 248, 243)
RAMP = " .:-=+*#%@"


def main(path, cell_w=8, cell_h=16):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    print(f"ink map of {path} ({w}x{h}), cell {cell_w}x{cell_h}")
    print("    " + "".join(str((i // 10) % 10) for i in range((w + cell_w - 1) // cell_w)))
    for gy in range(0, h, cell_h):
        line = []
        for gx in range(0, w, cell_w):
            n = 0
            for y in range(gy, min(gy + cell_h, h), 2):
                for x in range(gx, min(gx + cell_w, w), 2):
                    p = px[x, y]
                    if abs(p[0] - PAPER[0]) + abs(p[1] - PAPER[1]) + abs(p[2] - PAPER[2]) > 24:
                        n += 1
            frac = n / ((cell_w / 2) * (cell_h / 2))
            line.append(RAMP[min(len(RAMP) - 1, int(frac * len(RAMP)))])
        print(f"{gy:4d}" + "".join(line))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out/entry.png")
