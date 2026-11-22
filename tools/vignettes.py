"""Flat-vector vignettes, drawn with Pillow primitives only.

Each vignette is a 16:9 panel of muted flat fills with no outlines, in one
consistent style, so a row of them reads as a single illustration programme.
Nothing here loads a file or reaches the network: every shape is placed by code.
"""

from PIL import Image, ImageDraw

# Muted editorial palette shared by every panel.
INK = (26, 26, 28)
NIGHT = (34, 46, 70)
DUSK = (58, 72, 104)
SLATE = (108, 122, 140)
STONE = (176, 172, 162)
CREAM = (232, 226, 212)
SAND = (206, 190, 158)
TEAL = (36, 96, 104)
GREEN = (58, 108, 78)
MOSS = (92, 116, 74)
RUST = (172, 84, 44)
EMBER = (214, 122, 52)
CRIMSON = (140, 31, 43)
WINE = (96, 28, 38)
VIOLET = (91, 61, 130)
ICE = (196, 216, 226)
STEEL = (74, 90, 108)


def _ground(d, box, top, bottom):
    """Fill a panel with a two-band ground: sky above, ground below."""
    x0, y0, x1, y1 = box
    split = y0 + int((y1 - y0) * 0.62)
    d.rectangle([x0, y0, x1, split], fill=top)
    d.rectangle([x0, split, x1, y1], fill=bottom)


def summit(d, box):
    """A negotiating hall: a warming globe, a thermometer, delegates at a table."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (40, 62, 78), (28, 40, 52))
    # Globe with a landmass.
    gr = int(h * 0.30)
    gx, gy = x0 + int(w * 0.18), y0 + int(h * 0.33)
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=TEAL)
    d.polygon([(gx - gr // 2, gy - gr // 3), (gx + gr // 3, gy - gr // 2),
               (gx + gr // 2, gy + gr // 4), (gx - gr // 4, gy + gr // 3)], fill=MOSS)
    # Thermometer: glass tube, bulb at the FOOT, column rising from the bulb.
    tw = max(3, int(w * 0.030))
    tx = x0 + int(w * 0.42)
    bulb_r = int(w * 0.026)
    bulb_cy = y0 + int(h * 0.62)
    tube_top = y0 + int(h * 0.14)
    d.rounded_rectangle([tx, tube_top, tx + tw, bulb_cy], radius=tw // 2, fill=CREAM)
    d.ellipse([tx + tw // 2 - bulb_r, bulb_cy - bulb_r,
               tx + tw // 2 + bulb_r, bulb_cy + bulb_r], fill=CREAM)
    # The mercury, from the bulb up: a warming planet, not a cooling one.
    inset = max(1, tw // 4)
    d.rounded_rectangle([tx + inset, y0 + int(h * 0.30), tx + tw - inset, bulb_cy],
                        radius=max(1, (tw - 2 * inset) // 2), fill=CRIMSON)
    d.ellipse([tx + tw // 2 - bulb_r + inset, bulb_cy - bulb_r + inset,
               tx + tw // 2 + bulb_r - inset, bulb_cy + bulb_r - inset], fill=CRIMSON)
    # Scale ticks on the glass.
    for k in range(4):
        ty = tube_top + int((bulb_cy - tube_top) * (0.18 + k * 0.2))
        d.line([tx + tw, ty, tx + tw + int(w * 0.012), ty], fill=SLATE,
               width=max(1, int(h * 0.008)))
    # Delegates behind a long table: round heads, square shoulders.
    table_top = y0 + int(h * 0.72)
    head_r = int(h * 0.055)
    for i in range(6):
        px = x0 + int(w * (0.50 + i * 0.084))
        hx, hy = px + head_r, table_top - int(h * 0.14)
        jacket = [STEEL, TEAL, CRIMSON, MOSS, DUSK, RUST][i % 6]
        d.rectangle([hx - head_r - int(w * 0.006), hy + head_r,
                     hx + head_r + int(w * 0.006), table_top], fill=jacket)
        d.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r], fill=SAND)
    d.rectangle([x0 + int(w * 0.46), table_top, x1, table_top + int(h * 0.05)], fill=CREAM)
    d.rectangle([x0 + int(w * 0.46), table_top + int(h * 0.05), x1, y1], fill=SLATE)
    # Wall clock.
    cx, cy, cr = x1 - int(w * 0.10), y0 + int(h * 0.16), int(h * 0.09)
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=CREAM)
    d.line([cx, cy, cx, cy - int(cr * 0.7)], fill=INK, width=max(1, int(w * 0.006)))
    d.line([cx, cy, cx + int(cr * 0.5), cy], fill=INK, width=max(1, int(w * 0.006)))


def drones(d, box):
    """A night sky over a city: searchlights up, a wave of drones coming down."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, NIGHT, (16, 22, 34))
    # Searchlight beams standing on the ground, fanning UP into the sky, so the
    # direction of fire is unambiguous.
    for bx, spread in ((0.20, 0.17), (0.60, 0.21), (0.86, 0.14)):
        gx = x0 + int(w * bx)
        d.polygon([(gx - int(w * 0.012), y1),
                   (gx - int(w * spread), y0 + int(h * 0.04)),
                   (gx + int(w * spread * 0.4), y0 + int(h * 0.04)),
                   (gx + int(w * 0.012), y1)], fill=(52, 66, 92))
    # Skyline along the horizon.
    for i, bh in enumerate((0.16, 0.24, 0.13, 0.30, 0.19, 0.26, 0.15, 0.22)):
        bxx = x0 + int(w * (0.02 + i * 0.122))
        bw = int(w * 0.10)
        d.rectangle([bxx, y1 - int(h * bh), bxx + bw, y1], fill=(20, 26, 40))
        for wy in range(3):
            for wx in range(2):
                if (i + wy + wx) % 3 == 0:
                    d.rectangle([bxx + int(bw * (0.2 + wx * 0.4)),
                                 y1 - int(h * bh) + int(h * 0.03) + wy * int(h * 0.045),
                                 bxx + int(bw * (0.34 + wx * 0.4)),
                                 y1 - int(h * bh) + int(h * 0.05) + wy * int(h * 0.045)],
                                fill=(196, 168, 96))
    # The wave: many small delta drones falling in ranks from the top right,
    # so the picture itself carries the scale the badge claims.
    dr = max(3, int(h * 0.030))
    rank = 0
    for gy_ in range(4):
        for gx_ in range(6):
            px = x0 + int(w * (0.30 + gx_ * 0.115 + gy_ * 0.012))
            py = y0 + int(h * (0.10 + gy_ * 0.115))
            if px > x1 - dr or py > y1 - int(h * 0.34):
                continue
            d.polygon([(px, py + dr), (px - dr, py - dr), (px + dr, py - dr)],
                      fill=(226, 132, 52))
            rank += 1
    # A few trails and two impacts on the city.
    for px, py in ((0.34, 0.48), (0.52, 0.56), (0.66, 0.44)):
        cx, cy = x0 + int(w * px), y0 + int(h * py)
        d.line([cx + int(w * 0.02), cy - int(h * 0.14), cx, cy],
               fill=(214, 150, 80), width=max(1, int(w * 0.006)))
        d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=EMBER)


def refinery(d, box):
    """Fuel tanks, pipework and a jetty, with fire and smoke."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (58, 46, 48), (34, 30, 32))
    # Storage tanks.
    for i, (tx, tw, th) in enumerate(((0.06, 0.20, 0.30), (0.30, 0.16, 0.24),
                                      (0.50, 0.22, 0.34))):
        x = x0 + int(w * tx)
        top = y0 + int(h * (0.68 - th))
        d.rectangle([x, top + int(h * 0.04), x + int(w * tw), y0 + int(h * 0.70)], fill=STONE)
        d.ellipse([x, top, x + int(w * tw), top + int(h * 0.08)], fill=CREAM)
    # Pipework.
    d.rectangle([x0, y0 + int(h * 0.70), x1, y0 + int(h * 0.75)], fill=STEEL)
    for i in range(5):
        px = x0 + int(w * (0.08 + i * 0.2))
        d.rectangle([px, y0 + int(h * 0.60), px + int(w * 0.014), y0 + int(h * 0.70)], fill=SLATE)
    # Water, then the jetty, then two moored tankers with hulls and deck
    # houses: at 300 px a ship has to be a ship, not a shape in the water.
    d.rectangle([x0, y0 + int(h * 0.72), x1, y1], fill=(30, 42, 56))
    d.rectangle([x0 + int(w * 0.62), y0 + int(h * 0.66), x1, y0 + int(h * 0.725)], fill=SAND)

    def tanker(hx, hw, wl, col):
        """A hull sitting on the waterline, with a deck house and a mast."""
        top = y0 + int(h * wl)
        hull = y0 + int(h * (wl + 0.11))
        x = x0 + int(w * hx)
        wid = int(w * hw)
        # Hull: a long box with the bow cut back at the right.
        d.polygon([(x, top), (x + wid, top), (x + wid - int(wid * 0.18), hull),
                   (x, hull)], fill=col)
        # Waterline stripe.
        d.rectangle([x, hull - max(2, int(h * 0.018)), x + wid, hull], fill=CRIMSON)
        # Deck house aft, funnel, and a loading manifold forward.
        d.rectangle([x + int(wid * 0.04), top - int(h * 0.09),
                     x + int(wid * 0.26), top], fill=CREAM)
        d.rectangle([x + int(wid * 0.13), top - int(h * 0.15),
                     x + int(wid * 0.19), top - int(h * 0.08)], fill=SLATE)
        d.rectangle([x + int(wid * 0.62), top - int(h * 0.05),
                     x + int(wid * 0.72), top], fill=STEEL)

    tanker(0.70, 0.27, 0.76, CRIMSON)
    tanker(0.44, 0.22, 0.84, (150, 96, 74))
    # Fire and smoke over the tanks.
    for i, (fx, fr) in enumerate(((0.38, 0.09), (0.44, 0.13), (0.51, 0.08))):
        cx, cy = x0 + int(w * fx), y0 + int(h * (0.56 - i * 0.02))
        r = int(h * fr)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=EMBER if i % 2 == 0 else (236, 168, 72))
    for i, (sx, sr) in enumerate(((0.40, 0.11), (0.48, 0.15), (0.57, 0.09))):
        cx, cy = x0 + int(w * sx), y0 + int(h * (0.30 - i * 0.04))
        r = int(h * sr)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 48, 52))


def parliament(d, box):
    """A flag over a stone parliament, the independence-day setting."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (72, 84, 104), (44, 50, 62))
    # Colonnade.
    base = y0 + int(h * 0.74)
    d.rectangle([x0 + int(w * 0.10), base, x1 - int(w * 0.10), y0 + int(h * 0.82)], fill=STONE)
    d.polygon([(x0 + int(w * 0.10), base), (x0 + int(w * 0.50), y0 + int(h * 0.46)),
               (x1 - int(w * 0.10), base)], fill=CREAM)
    for i in range(7):
        px = x0 + int(w * (0.16 + i * 0.098))
        d.rectangle([px, y0 + int(h * 0.60), px + int(w * 0.028), base], fill=CREAM)
    d.rectangle([x0 + int(w * 0.10), y0 + int(h * 0.82), x1 - int(w * 0.10), y1], fill=SLATE)
    # Flag on a pole.
    px = x0 + int(w * 0.50)
    d.rectangle([px - int(w * 0.005), y0 + int(h * 0.06), px + int(w * 0.005),
                 y0 + int(h * 0.46)], fill=CREAM)
    d.rectangle([px + int(w * 0.005), y0 + int(h * 0.08), px + int(w * 0.20),
                 y0 + int(h * 0.26)], fill=CRIMSON)
    d.rectangle([px + int(w * 0.005), y0 + int(h * 0.17), px + int(w * 0.20),
                 y0 + int(h * 0.26)], fill=CREAM)
    d.polygon([(px + int(w * 0.085), y0 + int(h * 0.10)), (px + int(w * 0.12), y0 + int(h * 0.175)),
               (px + int(w * 0.05), y0 + int(h * 0.175))], fill=GREEN)


def pylon(d, box):
    """A transmission pylon and a dark city, the grid under strain."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (44, 44, 58), (24, 24, 32))
    # City blocks, unlit.
    for i, bh in enumerate((0.20, 0.28, 0.16, 0.24, 0.30, 0.18)):
        bxx = x0 + int(w * (0.02 + i * 0.163))
        d.rectangle([bxx, y1 - int(h * bh), bxx + int(w * 0.13), y1], fill=(18, 20, 30))
    # One lit window block, to show what is at stake.
    d.rectangle([x0 + int(w * 0.70), y0 + int(h * 0.42), x0 + int(w * 0.80),
                 y0 + int(h * 0.62)], fill=(196, 168, 96))
    # Pylon.
    apex = (x0 + int(w * 0.46), y0 + int(h * 0.10))
    for side in (-1, 1):
        d.line([apex, (apex[0] + side * int(w * 0.20), y1)], fill=STEEL,
               width=max(2, int(w * 0.010)))
    for i, fy in enumerate((0.40, 0.58, 0.74)):
        half = int(w * (0.06 + i * 0.05))
        d.line([(apex[0] - half, y0 + int(h * fy)), (apex[0] + half, y0 + int(h * fy))],
               fill=STEEL, width=max(1, int(w * 0.007)))
    # Slack cables.
    d.line([(x0, y0 + int(h * 0.34)), (apex[0], y0 + int(h * 0.40))], fill=SLATE,
           width=max(1, int(w * 0.005)))
    d.line([(apex[0], y0 + int(h * 0.40)), (x1, y0 + int(h * 0.30))], fill=SLATE,
           width=max(1, int(w * 0.005)))


def raid(d, box):
    """Helicopters over a lit street: the operation that took the boss."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (30, 34, 48), (40, 38, 40))
    # Street.
    d.rectangle([x0, y0 + int(h * 0.78), x1, y1], fill=(30, 30, 34))
    d.rectangle([x0, y0 + int(h * 0.86), x1, y1], fill=(24, 24, 28))
    # Buildings either side.
    for i, (bx, bh) in enumerate(((0.02, 0.34), (0.18, 0.46), (0.62, 0.40), (0.80, 0.30))):
        xx = x0 + int(w * bx)
        d.rectangle([xx, y1 - int(h * bh), xx + int(w * 0.16), y1], fill=(52, 46, 46))
    # Burning truck across the road.
    d.rectangle([x0 + int(w * 0.34), y0 + int(h * 0.66), x0 + int(w * 0.56),
                 y0 + int(h * 0.78)], fill=(70, 48, 36))
    d.rectangle([x0 + int(w * 0.34), y0 + int(h * 0.66), x0 + int(w * 0.40),
                 y0 + int(h * 0.72)], fill=(90, 62, 40))
    for fx, fr in ((0.44, 0.07), (0.50, 0.05)):
        cx = x0 + int(w * fx)
        r = int(h * fr)
        d.ellipse([cx - r, y0 + int(h * 0.62) - r, cx + r, y0 + int(h * 0.62) + r], fill=EMBER)
    # Two helicopters with search beams.
    for hx, hy in ((0.30, 0.16), (0.72, 0.10)):
        cx, cy = x0 + int(w * hx), y0 + int(h * hy)
        bw, bh = int(w * 0.10), int(h * 0.06)
        d.ellipse([cx - bw, cy - bh, cx + bw, cy + bh], fill=(38, 40, 46))
        d.line([cx - int(bw * 1.5), cy - bh, cx + int(bw * 1.5), cy - bh], fill=SLATE,
               width=max(1, int(w * 0.006)))
        d.polygon([(cx, cy + bh), (cx - int(w * 0.10), y0 + int(h * 0.72)),
                   (cx + int(w * 0.10), y0 + int(h * 0.72))], fill=(78, 82, 62))


def storm(d, box):
    """A supercell over a roofless town."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (52, 58, 74), (44, 52, 44))
    # Cloud mass.
    for cx, cy, cr in ((0.20, 0.20, 0.16), (0.42, 0.14, 0.20), (0.66, 0.20, 0.17),
                       (0.86, 0.16, 0.12)):
        px, py, r = x0 + int(w * cx), y0 + int(h * cy), int(h * cr)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(64, 68, 82))
    # Rain shafts.
    for i in range(10):
        sx = x0 + int(w * (0.05 + i * 0.098))
        d.line([(sx, y0 + int(h * 0.34)), (sx - int(w * 0.03), y0 + int(h * 0.66))],
               fill=(96, 108, 124), width=max(1, int(w * 0.004)))
    # Houses with roofs torn off.
    for i, bx in enumerate((0.06, 0.24, 0.44, 0.62, 0.80)):
        xx = x0 + int(w * bx)
        bh = int(h * (0.18 if i % 2 else 0.14))
        d.rectangle([xx, y1 - bh, xx + int(w * 0.15), y1], fill=STONE)
        if i % 2:
            d.polygon([(xx - int(w * 0.01), y1 - bh), (xx + int(w * 0.075), y1 - bh - int(h * 0.09)),
                       (xx + int(w * 0.16), y1 - bh)], fill=RUST)
        else:
            d.rectangle([xx, y1 - bh, xx + int(w * 0.15), y1 - bh + int(h * 0.02)], fill=(30, 30, 30))
    # A snapped pole.
    d.line([(x0 + int(w * 0.70), y1), (x0 + int(w * 0.76), y0 + int(h * 0.52))], fill=(60, 52, 44),
           width=max(2, int(w * 0.008)))


def factory(d, box):
    """A long industrial shed with smoke and fire at its windows."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (72, 74, 78), (46, 46, 48))
    # Shed with a sawtooth roof.
    base = y0 + int(h * 0.80)
    d.rectangle([x0 + int(w * 0.06), y0 + int(h * 0.40), x1 - int(w * 0.06), base], fill=STONE)
    for i in range(4):
        sx = x0 + int(w * (0.06 + i * 0.22))
        d.polygon([(sx, y0 + int(h * 0.40)), (sx + int(w * 0.11), y0 + int(h * 0.28)),
                   (sx + int(w * 0.22), y0 + int(h * 0.40))], fill=SLATE)
    # Windows, some alight.
    for i in range(6):
        wx = x0 + int(w * (0.10 + i * 0.13))
        lit = i in (2, 3)
        d.rectangle([wx, y0 + int(h * 0.58), wx + int(w * 0.07), y0 + int(h * 0.70)],
                    fill=EMBER if lit else (36, 38, 42))
    # Chimney and smoke.
    d.rectangle([x1 - int(w * 0.24), y0 + int(h * 0.14), x1 - int(w * 0.18), y0 + int(h * 0.42)],
                fill=(150, 146, 140))
    for i, (cx, cy, cr) in enumerate(((0.80, 0.10, 0.09), (0.86, 0.06, 0.07), (0.74, 0.05, 0.06))):
        px, py, r = x0 + int(w * cx), y0 + int(h * cy), int(h * cr)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(58, 56, 58))


def space(d, box):
    """Mercury and two spacecraft settling into orbit."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(12, 14, 26))
    for i in range(26):
        sx = x0 + int(w * ((i * 37) % 100) / 100)
        sy = y0 + int(h * ((i * 61) % 100) / 100)
        d.ellipse([sx, sy, sx + max(1, int(w * 0.006)), sy + max(1, int(w * 0.006))],
                  fill=(180, 186, 200))
    # Mercury: grey, cratered, lit from the left.
    cx, cy = x0 + int(w * 0.60), y0 + int(h * 0.56)
    r = int(h * 0.30)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(140, 134, 128))
    d.ellipse([cx - r, cy - r, cx - int(r * 0.1), cy + r], fill=(96, 92, 88))
    for dx, dy, dr in ((-0.4, -0.3, 0.13), (0.2, 0.1, 0.09), (-0.1, 0.5, 0.07)):
        px, py = cx + int(r * dx), cy + int(r * dy)
        rr = int(r * dr)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(112, 108, 104))
    # Orbit arc.
    for ox0, oy0, ox1, oy1 in ((cx - int(r * 1.8), cy - int(r * 0.7), cx + int(r * 1.8), cy + int(r * 0.7)),):
        d.arc([ox0, oy0, ox1, oy1], start=200, end=340, fill=(78, 96, 128),
              width=max(1, int(h * 0.010)))
    # Two small craft.
    for sx, sy in ((cx - int(r * 1.5), cy - int(r * 0.55)), (cx + int(r * 1.2), cy + int(r * 0.42))):
        d.rectangle([sx, sy, sx + int(w * 0.05), sy + int(h * 0.05)], fill=(214, 210, 198))
        d.rectangle([sx - int(w * 0.03), sy + int(h * 0.015), sx, sy + int(h * 0.035)], fill=(70, 110, 176))


def boat(d, box):
    """A small boat low in dark water, a creek at dusk."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (86, 70, 62), (28, 44, 46))
    # Far bank.
    d.rectangle([x0, y0 + int(h * 0.58), x1, y0 + int(h * 0.66)], fill=MOSS)
    # Water.
    d.rectangle([x0, y0 + int(h * 0.66), x1, y1], fill=(24, 48, 52))
    for i in range(5):
        wy = y0 + int(h * (0.72 + i * 0.05))
        d.line([(x0 + int(w * (0.04 + i * 0.03)), wy), (x1 - int(w * 0.06), wy)],
               fill=(36, 64, 68), width=max(1, int(h * 0.008)))
    # Boat, listing.
    bx, by = x0 + int(w * 0.50), y0 + int(h * 0.70)
    d.polygon([(bx - int(w * 0.20), by), (bx + int(w * 0.18), by),
               (bx + int(w * 0.12), by + int(h * 0.13)), (bx - int(w * 0.15), by + int(h * 0.13))],
              fill=(150, 116, 74))
    d.rectangle([bx - int(w * 0.02), by - int(h * 0.10), bx + int(w * 0.13),
                 by + int(h * 0.01)], fill=CREAM)
    d.line([(bx, by - int(h * 0.10)), (bx, by - int(h * 0.26))], fill=(90, 70, 48),
           width=max(1, int(w * 0.006)))
    # Passenger heads above the gunwale.
    for i in range(3):
        px = bx - int(w * 0.14) + i * int(w * 0.09)
        d.ellipse([px, by - int(h * 0.06), px + int(w * 0.035), by - int(h * 0.02)], fill=(46, 36, 32))


def displaced(d, box):
    """Shelter tarpaulins on a bare plain, a border crossing."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (188, 176, 152), (170, 156, 132))
    # Distant ridge.
    d.polygon([(x0, y0 + int(h * 0.56)), (x0 + int(w * 0.34), y0 + int(h * 0.44)),
               (x0 + int(w * 0.62), y0 + int(h * 0.52)), (x1, y0 + int(h * 0.46)),
               (x1, y0 + int(h * 0.58)), (x0, y0 + int(h * 0.58))], fill=(150, 138, 118))
    # A line of shelters.
    for i, bx in enumerate((0.05, 0.24, 0.43, 0.62, 0.81)):
        xx = x0 + int(w * bx)
        bw = int(w * 0.17)
        top = y0 + int(h * (0.52 + (i % 2) * 0.03))
        d.polygon([(xx, y1 - int(h * 0.10)), (xx + bw // 2, top),
                   (xx + bw, y1 - int(h * 0.10))], fill=CREAM if i % 2 else (198, 190, 174))
        d.rectangle([xx + bw // 2 - int(bw * 0.10), y1 - int(h * 0.22),
                     xx + bw // 2 + int(bw * 0.10), y1 - int(h * 0.10)], fill=(52, 46, 42))
    # Vehicle and two walking figures.
    vx = x0 + int(w * 0.44)
    d.rectangle([vx, y1 - int(h * 0.20), vx + int(w * 0.16), y1 - int(h * 0.11)], fill=(70, 86, 96))
    for i in range(2):
        px = x0 + int(w * (0.22 + i * 0.06))
        d.ellipse([px, y1 - int(h * 0.26), px + int(w * 0.025), y1 - int(h * 0.22)], fill=(48, 40, 36))
        d.rectangle([px + int(w * 0.004), y1 - int(h * 0.22), px + int(w * 0.020), y1 - int(h * 0.10)],
                    fill=(64, 56, 50))


def table(d, box):
    """A coalition table: two blocs and a paper between them."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (60, 66, 78), (40, 42, 48))
    # Table.
    d.ellipse([x0 + int(w * 0.14), y0 + int(h * 0.58), x1 - int(w * 0.14), y0 + int(h * 0.90)],
              fill=(112, 84, 58))
    # Chairs either side.
    for i in range(3):
        px = x0 + int(w * (0.20 + i * 0.09))
        d.ellipse([px, y0 + int(h * 0.26), px + int(w * 0.06), y0 + int(h * 0.36)], fill=SAND)
        d.rectangle([px - int(w * 0.004), y0 + int(h * 0.36), px + int(w * 0.064),
                     y0 + int(h * 0.58)], fill=STEEL)
        px2 = x0 + int(w * (0.62 + i * 0.09))
        d.ellipse([px2, y0 + int(h * 0.26), px2 + int(w * 0.06), y0 + int(h * 0.36)], fill=SAND)
        d.rectangle([px2 - int(w * 0.004), y0 + int(h * 0.36), px2 + int(w * 0.064),
                     y0 + int(h * 0.58)], fill=DUSK)
    # Papers on the table.
    for i in range(3):
        px = x0 + int(w * (0.34 + i * 0.11))
        d.rectangle([px, y0 + int(h * 0.66), px + int(w * 0.07), y0 + int(h * 0.74)], fill=CREAM)
        for ln in range(3):
            d.line([(px + int(w * 0.006), y0 + int(h * (0.675 + ln * 0.02))),
                    (px + int(w * 0.062), y0 + int(h * (0.675 + ln * 0.02)))],
                   fill=(120, 116, 108), width=1)


def plane(d, box):
    """An airliner on a closed apron, a controller's tower behind."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _ground(d, box, (78, 86, 102), (60, 62, 66))
    # Tower.
    tx = x0 + int(w * 0.74)
    d.rectangle([tx, y0 + int(h * 0.22), tx + int(w * 0.10), y0 + int(h * 0.62)], fill=STONE)
    d.rectangle([tx - int(w * 0.02), y0 + int(h * 0.14), tx + int(w * 0.12), y0 + int(h * 0.24)],
                fill=(44, 62, 78))
    # Terminal.
    d.rectangle([x0, y0 + int(h * 0.42), x0 + int(w * 0.52), y0 + int(h * 0.62)], fill=SLATE)
    for i in range(6):
        wx = x0 + int(w * (0.04 + i * 0.08))
        d.rectangle([wx, y0 + int(h * 0.46), wx + int(w * 0.05), y0 + int(h * 0.56)], fill=(60, 74, 90))
    # Apron.
    d.rectangle([x0, y0 + int(h * 0.62), x1, y1], fill=(72, 70, 68))
    for i in range(8):
        lx = x0 + int(w * (0.04 + i * 0.13))
        d.rectangle([lx, y0 + int(h * 0.80), lx + int(w * 0.06), y0 + int(h * 0.82)], fill=CREAM)
    # Airliner, three-quarter view.
    bx, by = x0 + int(w * 0.34), y0 + int(h * 0.68)
    d.polygon([(bx, by), (bx + int(w * 0.34), by), (bx + int(w * 0.30), by + int(h * 0.09)),
               (bx + int(w * 0.04), by + int(h * 0.09))], fill=CREAM)
    d.polygon([(bx + int(w * 0.12), by + int(h * 0.03)), (bx + int(w * 0.02), by + int(h * 0.14)),
               (bx + int(w * 0.10), by + int(h * 0.14))], fill=SLATE)
    d.polygon([(bx + int(w * 0.22), by - int(h * 0.10)), (bx + int(w * 0.30), by + int(h * 0.02)),
               (bx + int(w * 0.20), by + int(h * 0.02))], fill=(190, 186, 176))
    d.polygon([(bx + int(w * 0.34), by), (bx + int(w * 0.40), by - int(h * 0.10)),
               (bx + int(w * 0.40), by + int(h * 0.01))], fill=CRIMSON)
    for i in range(6):
        wx = bx + int(w * (0.07 + i * 0.04))
        d.rectangle([wx, by + int(h * 0.025), wx + int(w * 0.014), by + int(h * 0.04)],
                    fill=(70, 84, 100))


PANELS = {
    "summit": summit,
    "drones": drones,
    "refinery": refinery,
    "parliament": parliament,
    "pylon": pylon,
    "raid": raid,
    "storm": storm,
    "factory": factory,
    "space": space,
    "boat": boat,
    "displaced": displaced,
    "table": table,
    "plane": plane,
}


def draw_panel(draw, name, box):
    """Draw one named vignette into box, clipped to it.

    Each vignette is drawn onto a transparent layer the size of the whole sheet
    and then only the box's own pixels are pasted through. That is what keeps a
    beam, a trail or a shadow from ever landing on the headline above the panel:
    the panel cannot draw outside itself, whatever shape it asks for.
    """
    x0, y0, x1, y1 = [int(v) for v in box]
    if x1 <= x0 or y1 <= y0:
        return
    fn = PANELS.get(name)
    canvas = draw._image
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    if fn is None:
        ld.rectangle([x0, y0, x1, y1], fill=SLATE + (255,))
    else:
        fn(ld, (x0, y0, x1, y1))
    canvas.paste(layer.crop((x0, y0, x1, y1)), (x0, y0))
