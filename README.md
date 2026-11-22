# The World in One Day — Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/bongekanjing/ni22v-world-in-one-day-vivid-walrus-33/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/bongekanjing/ni22v-world-in-one-day-vivid-walrus-33/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image that sums up the world news of Sunday 22 November 2026: 37 stories
across 9 regions and 20 fields on a single broadsheet page, dated in the masthead.

Entry for [make.fun](https://make.fun/bounty/news-image-20261122)'s
`news-image-20261122` bounty.

## What the page carries

- **The date as the nameplate** — `Sunday 22 November 2026`, the largest object on
  the sheet, so the day it sums up survives a thumbnail.
- **Three illustrated leads** — the COP31 cover decision that never names fossil
  fuels, Russia's overnight drone wave at Ukraine, and Iran's strike on a Bahraini
  plant with two tankers hit in Hormuz. Each has its own flat-vector panel, a
  key-figure chip, a caption and a source line.
- **Six hard figures** — `~200`, `150`, `8,000`, `36`, `11`, `2` — each one stated
  by the reporting the page draws on.
- **A region census** — six colour blocks whose widths and counts are computed
  from the story records, so the bar cannot disagree with the stories shown.
- **Ten illustrated cards** and **twenty-four one-line briefs**, numbered 4–13
  and 14–37 so the numbering runs unbroken from the first lead to the last brief.
- **A date-check box** naming the cutoff and the stories deliberately left out as
  other days' news.

## Layout

```
main.py            the entrypoint: copies the finished sheet to $MAKEFUN_OUTPUT_DIR
entry.png          the finished 1024x1024 sheet, 180 KB
tools/stories.py   the day's reporting, one record per story
tools/vignettes.py flat-vector panels, drawn with Pillow primitives only
tools/render.py    the layout engine: a fixed vertical budget, drawn top to bottom
tools/audit.py     checks every section fits its budget and the counts reconcile
tools/inkmap.py    an ink map of the sheet, for finding layout holes without a viewer
```

`main.py` uses the standard library only. Pillow and the DejaVu faces are needed
by `tools/render.py` to *compose* the sheet, not to hand it in, because the
grader's sandbox has neither.

## Every count is derived, never typed

`stories.py` holds the records; `region_counts()` and `total_stories()` count
them. The masthead, the region bar, the briefs heading and the folio all read
those functions, and `tools/audit.py` asserts that the region counts sum to the
total and that story numbers run 1..37 with no gaps. Re-run it after any edit:

```sh
python3 tools/render.py && python3 tools/audit.py
```

## Reproducing the sheet

```sh
python3 tools/render.py          # writes out/entry.png
python3 tools/audit.py           # every section inside its budget, counts reconcile
MAKEFUN_OUTPUT_DIR=/tmp/o python3 main.py   # what the grader runs
```

Two runs of `main.py` write byte-identical files.

## License

MIT — see `LICENSE`.
