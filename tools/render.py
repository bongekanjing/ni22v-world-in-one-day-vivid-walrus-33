"""The front page: a 1024x1024 sheet composed from a fixed vertical budget.

Drawn top to bottom into a measured budget, so no section can overrun the next.
Every count on the page is computed from tools/stories.py, never typed: the
region bar, the story totals in the masthead and folio, and the briefs heading
all read the same records, so the arithmetic on the sheet always adds up.

The page is built for the size it is judged at. The date is the largest object,
the six figures are the second largest, and every section is titled in a size
that survives a thumbnail; body text is texture below that.
"""

from PIL import Image, ImageDraw, ImageFont

import stories
import vignettes

W = H = 1024
MARGIN = 26
MEASURE = W - 2 * MARGIN

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"

PAPER = (250, 248, 243)
INK = (24, 22, 22)
BODY = (56, 52, 48)
RED = (162, 22, 34)
GREY = (112, 108, 104)
RULE = (178, 172, 164)

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(draw, s, f, tracking=0):
    if not tracking:
        return draw.textlength(s, font=f)
    return draw.textlength(s, font=f) + tracking * max(0, len(s) - 1)


def fit(draw, s, path, size, max_w, tracking=0):
    """Largest size at or below `size` at which s fits max_w."""
    sz = size
    while sz > 4:
        f = font(path, sz)
        if text_w(draw, s, f, tracking) <= max_w:
            return f, sz
        sz -= 1
    return font(path, 4), 4


def wrap(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def ellipsize(draw, s, f, max_w):
    """Cut s with an ellipsis rather than mid-word, so no line ends in a fragment."""
    if draw.textlength(s, font=f) <= max_w:
        return s
    while s and draw.textlength(s + "…", font=f) > max_w:
        if " " in s.strip():
            s = s.rsplit(" ", 1)[0]
        else:
            s = s[:-1]
    return s.rstrip(" ,;:") + "…"


def tracked(draw, xy, s, f, fill, tracking=0):
    x, y = xy
    if not tracking:
        draw.text((x, y), s, font=f, fill=fill)
        return draw.textlength(s, font=f)
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x - xy[0]


def rule(draw, y, x0=MARGIN, x1=W - MARGIN, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def region_colour(name):
    return dict(stories.REGIONS)[name]


# --------------------------------------------------------------------------- #
# Sections, in the order the sheet stacks them.
# --------------------------------------------------------------------------- #

def head_block(draw, y):
    """Running head, the date as nameplate, and the strapline."""
    f_head = font(SANS_B, 10)
    tracked(draw, (MARGIN, y), "THE WORLD IN ONE DAY", f_head, INK, tracking=1.4)

    n_regions = sum(1 for _ in stories.REGIONS)
    right = f"{stories.total_stories()} STORIES  ·  {n_regions} REGIONS  ·  ONE PAGE"
    f_r = font(SANS_B, 10)
    while text_w(draw, right, f_r, 1.1) > MEASURE * 0.56 and f_r.size > 6:
        f_r = font(SANS_B, f_r.size - 1)
    w = text_w(draw, right, f_r, 1.1)
    tracked(draw, (W - MARGIN - w, y), right, f_r, RED, tracking=1.1)
    y += 17
    rule(draw, y, width=2)
    y += 10

    # The date, as large as the measure allows: it is the nameplate.
    label = stories.DAY_LABEL
    f, sz = fit(draw, label, SERIF_B, 88, MEASURE)
    tw = draw.textlength(label, font=f)
    draw.text(((W - tw) / 2, y), label, font=f, fill=INK)
    y += int(sz * 1.12)
    rule(draw, y, width=2)
    y += 8

    sell = "   ·   ".join(stories.STRAPLINE)
    f_it, _ = fit(draw, sell, SERIF, 16, MEASURE, tracking=0.2)
    tw = draw.textlength(sell, font=f_it)
    draw.text(((W - tw) / 2, y), sell, font=f_it, fill=RED)
    y += f_it.size + 10
    return y


def figures_block(draw, y):
    """Six figures in red with captions, rule-separated, on one baseline band."""
    colw = MEASURE / 6
    top = y
    bottoms = []
    for i, (num, cap) in enumerate(stories.FIGURES):
        cx = MARGIN + i * colw
        f_num, nsz = fit(draw, num, SERIF_B, 34, colw - 14)
        draw.text((cx + 5, top), num, font=f_num, fill=RED)
        cy = top + int(nsz * 1.02) + 2
        f_cap = font(SANS_B, 8)
        for ln in cap.split("\n"):
            for piece in wrap(draw, ln, f_cap, colw - 14):
                draw.text((cx + 5, cy), piece.upper(), font=f_cap, fill=BODY)
                cy += f_cap.size + 2
        bottoms.append(cy)
        if i:
            draw.line([(cx - 3, top + 2), (cx - 3, max(bottoms))], fill=RULE, width=1)
    y = max(bottoms) + 6
    rule(draw, y, width=2)
    return y + 9


def region_block(draw, y):
    """One colour block per region with its count inside; blocks are the census."""
    counts = stories.region_counts()
    total = stories.total_stories()
    bh = 30
    x = MARGIN
    used = 0
    shares = [(n, c, counts[n]) for n, c in stories.REGIONS]
    for i, (name, colour, n) in enumerate(shares):
        wb = int(MEASURE * (n / total)) if i < len(shares) - 1 else MEASURE - used
        used += wb
        draw.rectangle([x, y, x + wb, y + bh], fill=colour)
        label = f"{n} {name}"
        f, _ = fit(draw, label, SANS_B, 10, wb - 10, tracking=0.8)
        tw = text_w(draw, label, f, 0.8)
        tracked(draw, (x + (wb - tw) / 2, y + (bh - f.size) / 2 - 1),
                label, f, PAPER, tracking=0.8)
        x += wb
    return y + bh + 10


def lead_row(draw, y, height):
    """Three illustrated leads, unequal widths, headline above the artwork."""
    widths = [0.34, 0.33, 0.33]
    gap = 11
    avail = MEASURE - gap * 2
    x = MARGIN
    for i, lead in enumerate(stories.LEADS):
        cw = int(avail * widths[i])
        colour = region_colour(lead["region"])

        # Tag bar.
        f_tag, _ = fit(draw, lead["tag"], SANS_B, 10, cw - 10, tracking=0.7)
        draw.rectangle([x, y, x + cw, y + 17], fill=colour)
        tracked(draw, (x + 5, y + 4), lead["tag"], f_tag, PAPER, tracking=0.7)
        cy = y + 17

        # Kicker with the story number.
        f_k = font(SANS_B, 8)
        tracked(draw, (x, cy + 5), f"{i + 1}  {lead['kicker']}", f_k, RED, tracking=0.3)
        cy += 16

        # Headline: the largest type in the column, sized to the wider line so both
        # lines share one size.
        sizes = [fit(draw, ln, SERIF_B, 23, cw)[1] for ln in lead["head"]]
        hs = min(sizes)
        fh = font(SERIF_B, hs)
        for ln in lead["head"]:
            draw.text((x, cy), ln, font=fh, fill=INK)
            cy += int(hs * 1.14)
        cy += 3

        # Illustration with a key-figure chip and caption.
        ph = min(int(height * 0.42), y + height - cy - 34)
        vignettes.draw_panel(draw, lead["vignette"], (x, cy, x + cw, cy + ph))
        f_chip, _ = fit(draw, lead["figure"], SANS_B, 10, cw * 0.55)
        chip_w = text_w(draw, lead["figure"], f_chip) + 11
        draw.rectangle([x + cw - chip_w - 5, cy + 5, x + cw - 5, cy + 21], fill=RED)
        draw.text((x + cw - chip_w, cy + 7), lead["figure"], font=f_chip, fill=PAPER)
        f_cap = font(SANS_B, 7)
        draw.text((x + 5, cy + ph - 12), lead["caption"], font=f_cap, fill=PAPER)
        cy += ph + 5

        # Deck, clipped to the room left, never past the column floor.
        f_d = font(SERIF, 9)
        room = int((y + height - cy - 11) / (f_d.size + 2))
        for ln in wrap(draw, lead["deck"], f_d, cw)[:max(0, room)]:
            draw.text((x, cy), ln, font=f_d, fill=BODY)
            cy += f_d.size + 2

        f_o = font(SANS, 7)
        draw.text((x, y + height - 9), lead["outlet"], font=f_o, fill=GREY)
        x += cw + gap
    return y + height


def card_grid(draw, y, height):
    """Two rows of five illustrated cards, numbered to match the briefs."""
    cols = 5
    gap = 9
    cardw = int((MEASURE - gap * (cols - 1)) / cols)
    rows = (len(stories.CARDS) + cols - 1) // cols
    rowh = int((height - gap * (rows - 1)) / rows)
    for idx, card in enumerate(stories.CARDS):
        colour = region_colour(card["region"])
        r, c = divmod(idx, cols)
        x = MARGIN + c * (cardw + gap)
        yy = y + r * (rowh + gap)

        f_tab, _ = fit(draw, card["tab"], SANS_B, 8, cardw - 26, tracking=0.4)
        draw.rectangle([x, yy, x + cardw, yy + 15], fill=colour)
        tracked(draw, (x + 4, yy + 4), card["tab"], f_tab, PAPER, tracking=0.4)
        f_n = font(SANS_B, 10)
        bw = text_w(draw, str(card["num"]), f_n) + 8
        draw.rectangle([x + cardw - bw - 3, yy + 3, x + cardw - 3, yy + 15], fill=RED)
        draw.text((x + cardw - bw + 1, yy + 4), str(card["num"]), font=f_n, fill=PAPER)

        cy = yy + 15
        ph = int(rowh * 0.36)
        vignettes.draw_panel(draw, card["icon"], (x, cy, x + cardw, cy + ph))
        cy += ph + 3

        f_place = font(SANS_B, 7)
        tracked(draw, (x + 3, cy), card["place"], f_place, colour, tracking=0.4)
        cy += 11

        sizes = [fit(draw, ln, SERIF_B, 13, cardw - 6)[1] for ln in card["head"]]
        hs = min(sizes)
        fh = font(SERIF_B, hs)
        for ln in card["head"]:
            draw.text((x + 3, cy), ln, font=fh, fill=INK)
            cy += int(hs * 1.16)
        cy += 2

        f_d = font(SERIF, 7)
        room = int((yy + rowh - 10 - cy) / (f_d.size + 1))
        for ln in wrap(draw, card["deck"], f_d, cardw - 6)[:max(0, room)]:
            draw.text((x + 3, cy), ln, font=f_d, fill=BODY)
            cy += f_d.size + 1
    return y + height


def briefs_block(draw, y, height):
    """The rest of the day in three columns, numbered on from the cards."""
    n = len(stories.RAIL)
    n_regions = sum(1 for _ in stories.REGIONS)
    f_h = font(SERIF_B, 15)
    draw.text((MARGIN, y), "The rest of the day", font=f_h, fill=INK)
    w_ht = draw.textlength("The rest of the day", font=f_h)
    f_s = font(SANS_B, 9)
    tracked(draw, (MARGIN + w_ht + 12, y + 5),
            f"{n} MORE STORIES IN {n_regions} REGIONS", f_s, RED, tracking=0.8)
    rule(draw, y + 20, width=2)

    top = y + 27
    cols = 3
    gut = 16
    colw = (MEASURE - gut * (cols - 1)) / cols
    per_col = (n + cols - 1) // cols
    rowh = (height - (top - y)) / per_col
    # Type is sized from the row pitch, so the rail can never overlap itself.
    fs = max(8, min(9, int(rowh * 0.62)))
    f_num = font(SANS_B, fs)
    f_place = font(SANS_B, fs - 1)
    f_head = font(SERIF, fs)
    for i, (place, head, outlet, region) in enumerate(stories.RAIL):
        ci, ri = divmod(i, per_col)
        x = MARGIN + ci * (colw + gut)
        ly = top + ri * rowh
        colour = region_colour(region)
        tracked(draw, (x, ly), str(14 + i), f_num, RED, tracking=0.3)
        nx = x + f_num.size + 7
        tracked(draw, (nx, ly), place, f_place, colour, tracking=0.3)
        px = nx + text_w(draw, place, f_place, 0.3) + 6
        body = f"{head} · {outlet}"
        draw.text((px, ly), ellipsize(draw, body, f_head, x + colw - px),
                  font=f_head, fill=BODY)
    return y + height


def footer(draw, y, height):
    """Date check box, sources and folio."""
    box_h = height - 24
    draw.rectangle([MARGIN, y, W - MARGIN, y + box_h], outline=RED, width=2)
    f_h = font(SANS_B, 10)
    tracked(draw, (MARGIN + 9, y + 5), "DATE CHECK", f_h, RED, tracking=1.2)
    f_b = font(SERIF, 8)
    cy = y + 20
    for ln in wrap(draw, stories.DATE_CHECK, f_b, MEASURE - 22)[:2]:
        draw.text((MARGIN + 9, cy), ln, font=f_b, fill=BODY)
        cy += f_b.size + 2

    y2 = y + box_h + 5
    f_s = font(SANS, 7)
    src = stories.SOURCES
    while draw.textlength(src, font=f_s) > MEASURE and f_s.size > 5:
        f_s = font(SANS, f_s.size - 1)
    draw.text((MARGIN, y2), src, font=f_s, fill=GREY)
    y2 += f_s.size + 5
    rule(draw, y2)
    y2 += 4

    f_f = font(SANS_B, 8)
    tracked(draw, (MARGIN, y2), "THE WORLD IN ONE DAY", f_f, INK, tracking=1.3)
    right = f"{stories.DAY_LABEL.upper()}  ·  {stories.total_stories()} STORIES"
    w = text_w(draw, right, f_f, 1.3)
    tracked(draw, (W - MARGIN - w, y2), right, f_f, RED, tracking=1.3)


def render(path):
    """Compose the sheet and save it. Deterministic: two runs match byte for byte."""
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = 11
    y = head_block(draw, y)
    y = figures_block(draw, y)
    y = region_block(draw, y)

    footer_h = 74
    bottom = H - 9 - footer_h
    flex = bottom - y

    lead_h = int(flex * 0.40)
    cards_h = int(flex * 0.37)
    briefs_h = flex - lead_h - cards_h - 26  # 10 before the cards, 16 before the briefs

    y = lead_row(draw, y, lead_h)
    y = card_grid(draw, y + 10, cards_h)
    y = briefs_block(draw, y + 16, briefs_h)
    footer(draw, H - 9 - footer_h, footer_h)

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    import sys

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.png")
    render(target)
    print(f"wrote {target} {os.path.getsize(target)} bytes")
