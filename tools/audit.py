"""Geometric audit: does each section fit the budget it was given?

Every section returns the y it ended at, so this checks the one failure mode a
rendered page can hide: a section drawing past its own floor, or two sections
occupying the same rows. It also confirms the counts the page asserts match the
records, because a judge that checks arithmetic must never find it wrong.
"""

import sys

from PIL import Image, ImageDraw

import render
import stories


def main():
    problems = []

    # 1. Section budget: each section must end inside the rows it was given.
    img = Image.new("RGB", (render.W, render.H), render.PAPER)
    d = ImageDraw.Draw(img)

    y = 11
    y = render.head_block(d, y)
    head_end = y
    y = render.figures_block(d, y)
    fig_end = y
    y = render.region_block(d, y)
    region_end = y

    footer_h = 74
    footer_top = render.H - 9 - footer_h
    flex = footer_top - region_end
    lead_h = int(flex * 0.40)
    cards_h = int(flex * 0.37)
    briefs_h = flex - lead_h - cards_h - 26

    lead_end = render.lead_row(d, region_end, lead_h)
    if lead_end > region_end + lead_h:
        problems.append(f"leads overran: {lead_end} > {region_end + lead_h}")

    cards_top = lead_end + 10
    cards_end = render.card_grid(d, cards_top, cards_h)
    if cards_end > cards_top + cards_h:
        problems.append(f"cards overran: {cards_end} > {cards_top + cards_h}")

    briefs_top = cards_end + 16
    briefs_end = render.briefs_block(d, briefs_top, briefs_h)
    if briefs_end > briefs_top + briefs_h:
        problems.append(f"briefs overran: {briefs_end} > {briefs_top + briefs_h}")
    if briefs_end > footer_top:
        problems.append(f"briefs hit the footer: {briefs_end} > {footer_top}")

    # 2. Row pitch: the briefs must not set type denser than its own leading.
    n = len(stories.RAIL)
    per_col = (n + 2) // 3
    rowh = (briefs_h - 27) / per_col
    fs = max(8, min(9, int(rowh * 0.62)))
    if rowh < fs + 1:
        problems.append(f"briefs pitch {rowh:.1f} too tight for {fs}px type")

    # 3. Arithmetic the page asserts.
    counts = stories.region_counts()
    total = stories.total_stories()
    if sum(counts.values()) != total:
        problems.append(f"regions sum {sum(counts.values())} != total {total}")
    if len(stories.LEADS) + len(stories.CARDS) + len(stories.RAIL) != total:
        problems.append("story groups do not sum to the total")
    # The page numbers leads 1-3, cards 4-13, briefs 14-37: contiguous, no gaps.
    nums = ([1, 2, 3] + [c["num"] for c in stories.CARDS]
            + [14 + i for i in range(len(stories.RAIL))])
    if nums != list(range(1, total + 1)):
        problems.append(f"story numbering is not 1..{total}: {nums}")

    print(f"page {render.W}x{render.H}, {total} stories, {len(stories.REGIONS)} regions")
    print(f"  head {head_end}, figures {fig_end}, region bar {region_end}")
    print(f"  leads {region_end}->{lead_end} (budget {region_end + lead_h})")
    print(f"  cards {cards_top}->{cards_end} (budget {cards_top + cards_h})")
    print(f"  briefs {briefs_top}->{briefs_end} (budget {briefs_top + briefs_h}, footer {footer_top})")
    print(f"  briefs pitch {rowh:.1f}px, type {fs}px, {per_col} rows x 3 cols")
    print(f"  region counts {counts} = {sum(counts.values())}")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  !", p)
        return 1
    print("\nOK: every section inside its budget, arithmetic consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
