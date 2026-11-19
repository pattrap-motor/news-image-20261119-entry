[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/pattrap-motor/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/pattrap-motor/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119)

# The World in One Day — 19 November 2026

Entry for the [news-image-20261119 bounty on make.fun](https://make.fun/bounty/news-image-20261119).

A newspaper front page that sums up Thursday 19 November 2026 in one image:

- **Lead — VICE CITY OPENS ITS GATES:** After 13 years, Rockstar's Grand
  Theft Auto VI launches worldwide today, rolling out at midnight in each
  region on PlayStation 5 and Xbox; critics put it at 99 on Metacritic and
  pre-orders are near $1 billion.
- **Shenzhen:** Trump, Xi and Putin meet today at APEC — the first-ever
  three-way summit; Ukraine, Iran, trade and nuclear arms on the table, no
  deal expected.
- **The Hague:** the ICJ reads its judgment in Gambia v. Myanmar at 10:00 —
  whether the state committed genocide against the Rohingya; a first-ever
  finding is on the table.
- **New York:** Anthropic's ANT debuts on Nasdaq — priced at $83, above its
  $70–78 range, in a 980m-share, $81bn offering.
- **Bay of Bengal:** severe Cyclone Akvan bears down on India's east coast;
  red alerts, extremely heavy rain today and tomorrow, landfall expected
  Friday between Narsapur and Puri.
- **Also today:** NASA confirms Voyager 1 one light-day away at a live event;
  the Gulf on alert as the Iran file heads to Shenzhen; Pew: Islam on track
  to be the world's largest faith by 2035; UK Covid inquiry publishes its
  Module 7 report.

## How it is made

`draw.py` draws the whole front page with Pillow (flat illustrations, DejaVu fonts —
no AI-generated text, so nothing can come out garbled). `main.py` (standard library
only, no network) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. The program
is deterministic: two runs write identical bytes.

Rebuild the image: `python3 draw.py`
