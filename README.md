# The World Today — Sunday, 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/contact-nathanealphi/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/contact-nathanealphi/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A classic broadsheet front page summing up the world's news of
Sunday, 22 November 2026 — **39 verified stories in one image** — for
[news-image-20261122](https://make.fun/bounty/news-image-20261122).

Two hero features (COP31 collapses in Antalya with no deal after the
EU rejects a pact that never mentions fossil fuels; Iran strikes a
site in Bahrain), ten illustrated story cards (186 drones over
Ukraine, 'El Chapo Isidro' captured, Wall Street slides into
correction, the Cikande factory fire, the ICJ's Myanmar genocide
verdict, the EU–Indonesia trade deal, BepiColombo reaching Mercury,
Verstappen winning the Las Vegas Grand Prix, Hong Kong's record
turnout vote, the FBI database hack), and 27 more stories in the
"Also on 22 November" list.

## How it is made

`tools/cards.py` draws the whole page with Pillow primitives
(DejaVu Serif headlines, Noto Sans Condensed body, original
vector-style pictograms) from the story list in `research.md` — no
photos, no network, no randomness, no timestamps. `tools/render.py`
is the earlier broadsheet variant (kept for reference). `main.py`
(standard library only) copies `assets/entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, so repeated runs are byte-identical.

Rebuild the image:

```sh
python3 tools/cards.py
```

Run the entry:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7053etrm&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
