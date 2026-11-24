# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/gtumbal51/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/gtumbal51/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Tuesday 24 November 2026's world news on one page — the *Meridian Ledger* edition: a broadsheet front page carrying **38 stories** — 4 illustrated lead stories, 10 illustrated panels and 24 one-line briefs — with a day-in-numbers strip, a world map with numbered pins matched to the stories, a region tally, a source tag on every pictured story, and a date-check box listing the adjacent-day stories deliberately left out. Built from the reports available by Tuesday morning UTC.

The leads: Nvidia's board reinstates Jensen Huang and the shares soar 31% in a historic snapback · Iran steps up strikes on Gulf targets and files a $290bn claim as a US blockade bites · China prepares to fly Shenzhou-24 with the first foreign astronaut aboard Tiangong · Kyiv confirms it sank a Russian warship at Benghazi. Panels and briefs cover the Russian jets breaching Korea's air zone, Trump's new path to fight his conviction, South Africa bowling Bangladesh out for 91, Liverpool's 4-0 rout of United on Pochettino's debut, Brent sliding below $90 — and 24 more.

## Run it

```sh
python3 main.py
```

`main.py` is a standard-library-only copier: it writes the pre-rendered `entry.png` (1024x1024) shipped in this repository to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to `/output`, then the working directory), byte for byte, so every run produces exactly the same image. The page itself is drawn by `draw_frontpage.py` (Pillow), which renders every illustration — bar chart, starburst, planet, ship, drone, scales, shield and the dot-matrix world map — in code; there are no photos and no external assets. The copier shape is deliberate: the grading sandbox guarantees no fonts or third-party packages, and the competition rules explicitly allow a repository that holds the image with a program that copies it.

## How the page was made

The stories were gathered Tuesday morning (UTC) from the day's wire and broadsheet reports and cross-checked across at least two outlets for every lead. Each story is dated to Tuesday 24 November: events that merely continued from Monday are framed by what was new on Tuesday (the reinstatement, the claim, the blame game, the rising toll), and the footer's date-check box names the adjacent-day items that were left out on purpose. `draw_frontpage.py` validates its own story tables before drawing (38 stories, numbered 1–38, every pictured story tagged and pinned, regions tallying to 38), so a data typo fails the render instead of reaching the page.

## Competition

[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124) — a make.fun bounty. The entry program writes one image of the day's news; an AI judge compares the images two at a time, and the 50 best-ranked entries share $100.
