# Friday 27 November 2026: 36 stories, 9 regions

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/diablosan19/newsimage-20261127-v5/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/diablosan19/newsimage-20261127-v5/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image that sums up the world's news of **Friday 27 November 2026**:
36 stories across 9 regions and 14 fields, each with a region tag, a UTC
first-wire time and a sourcing label (OFFICIAL / CONFIRMED / REPORTED /
CLAIM). Three big illustrated lead stories, seven more illustrated panels,
a numbered day-in-brief list, a world pin map, a UTC timeline strip, a
printed DATE CHECK box, and a region-count bar.

Every headline was re-verified on 27 November 2026 against two live
sources (wire or primary source plus a second independent outlet). Big
stories first reported on 26 November — the Kuwait drone attack, the Gaza
strikes toll, the Jazan refinery attack, the ECB choice of de Cos, UK net
migration, the Bangkok refinery blast, the Lukoil deal, the North Korea
missile-aid halt — are named only in the DATE CHECK box as excluded, never
presented as 27 November news.

## How it is built

`build_frontpage.py` draws `entry.png` (1024×1024, PNG) from scratch with
PIL primitives — shapes only, no photographs, no external assets, no
network. `main.ts` (Node standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR` after verifying its magic bytes, size (≤ 1 MiB) and
dimensions (≤ 1024×1024), and exits non-zero on any problem.

```sh
python3 build_frontpage.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Research notes

See `RESEARCH.md` for the per-story verification log (two sources per
headline, first-wire times, and the prior-day exclusions).
