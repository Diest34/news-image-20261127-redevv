# News Image — 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Diest34/news-image-20261127-redevv/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Diest34/news-image-20261127-redevv/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image that sums up the world news of Friday, 27 November 2026.

## The entry

`entry.png` (1024 × 1024) is a single-panel news digest: the day's biggest
stories, distilled into one picture you can read at a glance. It was made
for the make.fun **News Image 20261127** bounty.

- **Bounty:** https://make.fun/bounty/news-image-20261127
- **Referral code:** `y12bs3e6`
- **Image:** `entry.png` — 1024 × 1024 PNG

The five stories on the page:

1. **Ukraine diplomacy** — Zelensky tells the BBC the US is "too focused
   on the Middle East" and not pushing Russia hard enough, and calls
   Trump's embrace of Putin "strange"; Trump says Putin "would like to
   make a deal".
2. **ECB** — EU leaders recommend Spain's Pablo Hernández de Cos to succeed
   Christine Lagarde as ECB president.
3. **Somalia** — Al-Shabaab claims a deadly ambush on Somali troops.
4. **Cricket** — Gill bowls first in the 2nd Test v New Zealand; Gurnoor
   Brar debuts as Siraj sits out.
5. **Gaza** — Gaza cities warn winter rains may flood 1,000 displacement
   camps.

Also noted: EU–Canada plan closer AI cooperation, French students prepare
nationwide protests, and the US East Coast counts the cost of the
Thanksgiving storm.

## Reproduce it

```bash
python3 main.py
```

`main.py` copies the bundled `entry.png` to `/output/entry.png` (creating
`/output` if needed) and verifies the copy byte for byte: it prints the
SHA-256 of the output and only succeeds when it matches the source.

## How it works

1. `main.py` locates `entry.png` next to itself and checks the PNG magic
   bytes, so a corrupt or wrong file fails loudly instead of silently.
2. It copies the file to `/output/entry.png`, creating the folder first.
3. It hashes both files with SHA-256 and compares them; any difference
   aborts with an error. A successful run prints the output path, size,
   and hash.

`build_image.py` is the script that drew `entry.png` with Pillow: every
element — masthead, flags, icons, text — is drawn by the program, with no
photographs and no network. It is kept in the repo so the picture can be
rebuilt from scratch; the grader only runs `main.py`, which needs the
standard library alone.

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The entry image, 1024 × 1024 |
| `main.py` | Deterministic reproduction script (Python 3.13) |
| `build_image.py` | Composer that drew `entry.png` with Pillow |
| `LICENSE` | MIT license |

## License

MIT — see [LICENSE](LICENSE).
