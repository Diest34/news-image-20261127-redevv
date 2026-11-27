#!/usr/bin/env python3
"""Compose the entry image for 27 November 2026 world news.

Builds a 1024x1024 newspaper front page with Pillow: masthead, lead
story, four story cards and an "also today" strip. Every element is
drawn by this script (shapes, flags, icons, text) -- no photographs,
no pasted images, no network. Run from this directory:

    python3 build_image.py

Writes entry.png next to this script. Deterministic: the same inputs
give the same bytes (Pillow writes no timestamps into PNGs).
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
WIDTH = 1024
HEIGHT = 1024

NAVY = (13, 38, 71)
NAVY_DARK = (9, 28, 54)
GOLD = (217, 164, 65)
GOLD_DARK = (176, 128, 42)
PAPER = (251, 247, 236)
CARD = (255, 255, 255)
INK = (18, 18, 18)
GREY = (86, 92, 100)
LINE = (203, 206, 211)
RED = (176, 32, 32)
TEAL = (18, 110, 105)
BLUE = (31, 58, 95)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         max_w: int) -> list[str]:
    """Greedy word wrap of *text* to lines no wider than *max_w*."""
    lines: list[str] = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
                 fnt: ImageFont.FreeTypeFont, max_w: int,
                 fill: tuple[int, int, int], leading: int) -> int:
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def flag_us(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    stripe = h / 13.0
    for i in range(13):
        colour = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                       fill=colour)
    canton_w = w * 0.4
    canton_h = stripe * 7
    draw.rectangle([x, y, x + canton_w, y + canton_h], fill=(60, 59, 110))
    for row in range(5):
        for col in range(6):
            cx = x + 8 + col * (canton_w - 14) / 5
            cy = y + 7 + row * (canton_h - 12) / 4
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=(90, 90, 90))


def flag_ua(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    draw.rectangle([x, y, x + w, y + h / 2], fill=(0, 91, 187))
    draw.rectangle([x, y + h / 2, x + w, y + h], fill=(255, 213, 0))
    draw.rectangle([x, y, x + w, y + h], outline=(90, 90, 90))


def flag_ru(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    third = h / 3.0
    for i, colour in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * third, x + w, y + (i + 1) * third],
                       fill=colour)
    draw.rectangle([x, y, x + w, y + h], outline=(90, 90, 90))


def draw_bank(draw: ImageDraw.ImageDraw, x: int, y: int, s: int) -> None:
    """A small bank / central-bank icon, *s* pixels wide."""
    draw.polygon([(x, y + 18), (x + s, y + 18), (x + s / 2, y)], fill=NAVY)
    draw.rectangle([x + 2, y + 18, x + s - 2, y + 26], fill=NAVY)
    for i in range(4):
        cx = x + 10 + i * (s - 20) / 3
        draw.rectangle([cx - 4, y + 30, cx + 4, y + 58], fill=NAVY)
    draw.rectangle([x, y + 58, x + s, y + 66], fill=NAVY)
    draw.rectangle([x - 4, y + 66, x + s + 4, y + 72], fill=GOLD_DARK)
    draw.text((x + s / 2 - 13, y + 78), "\u20ac", font=font(SANS_BOLD, 34),
              fill=GOLD_DARK)


def draw_warning(draw: ImageDraw.ImageDraw, x: int, y: int, s: int) -> None:
    draw.polygon([(x + s / 2, y), (x + s, y + s), (x, y + s)], fill=(212, 160, 23))
    draw.polygon([(x + s / 2, y + 12), (x + s - 12, y + s - 6),
                  (x + 12, y + s - 6)], fill=(255, 255, 255))
    draw.text((x + s / 2 - 7, y + 26), "!", font=font(SANS_BOLD, 44),
              fill=(140, 20, 20))


def draw_cricket(draw: ImageDraw.ImageDraw, x: int, y: int, s: int) -> None:
    """Stumps, a ball and a bat."""
    for i in range(3):
        sx = x + 14 + i * 14
        draw.rectangle([sx, y + 18, sx + 7, y + 78], fill=(200, 164, 90))
    draw.rectangle([x + 14, y + 12, x + 49, y + 18], fill=(176, 128, 42))
    draw.ellipse([x + 66, y + 8, x + 96, y + 38], fill=RED)
    draw.ellipse([x + 66, y + 8, x + 96, y + 38], outline=(120, 10, 10), width=2)
    draw.arc([x + 70, y + 12, x + 92, y + 34], 200, 340, fill=(255, 255, 255),
             width=2)
    draw.polygon([(x + 108, y + 30), (x + 128, y + 26), (x + 132, y + 96),
                  (x + 112, y + 100)], fill=(222, 184, 120))
    draw.rectangle([x + 116, y + 96, x + 124, y + 118], fill=(120, 82, 30))
    draw.line([x + 108, y + 30, x + 128, y + 26], fill=(150, 110, 50), width=2)


def draw_rain(draw: ImageDraw.ImageDraw, x: int, y: int, s: int) -> None:
    """A rain cloud over a tent."""
    draw.ellipse([x + 8, y + 10, x + 58, y + 52], fill=(120, 132, 148))
    draw.ellipse([x + 34, y + 2, x + 92, y + 52], fill=(140, 151, 165))
    draw.ellipse([x + 66, y + 14, x + 112, y + 52], fill=(120, 132, 148))
    draw.rectangle([x + 10, y + 34, x + 110, y + 54], fill=(120, 132, 148))
    for i, dx in enumerate((18, 48, 78, 104)):
        y0 = y + 62 + (i % 2) * 8
        draw.line([dx + x, y0, dx + x - 6, y0 + 16], fill=TEAL, width=4)
    draw.polygon([(x + 60, y + 96), (x + 8, y + 128), (x + 112, y + 128)],
                 fill=(196, 120, 60))
    draw.polygon([(x + 60, y + 96), (x + 38, y + 128), (x + 82, y + 128)],
                 fill=(120, 70, 40))
    draw.line([x + 8, y + 128, x + 112, y + 128], fill=(90, 55, 30), width=3)


def draw_speech(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int,
                text: str) -> None:
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(255, 255, 255),
                           outline=GOLD_DARK, width=3)
    draw.polygon([(x + 22, y + h - 2), (x + 40, y + h - 2), (x + 26, y + h + 16)],
                 fill=(255, 255, 255), outline=GOLD_DARK)
    fnt = font(SANS_BOLD, 26)
    tw = draw.textlength(text, font=fnt)
    draw.text((x + (w - tw) / 2, y + (h - 34) / 2), text, font=fnt,
              fill=NAVY)


def build() -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    draw.rectangle([0, 0, WIDTH, 148], fill=NAVY)
    draw.rectangle([0, 148, WIDTH, 154], fill=GOLD)
    title = "THE WORLD IN ONE DAY"
    f_title = font(SERIF_BOLD, 62)
    tw = draw.textlength(title, font=f_title)
    draw.text(((WIDTH - tw) / 2, 18), title, font=f_title, fill=(255, 255, 255))
    date = "FRIDAY  \u00b7  27 NOVEMBER 2026"
    f_date = font(SANS_BOLD, 32)
    tw = draw.textlength(date, font=f_date)
    draw.text(((WIDTH - tw) / 2, 96), date, font=f_date, fill=GOLD)

    # --- lead story ----------------------------------------------------
    lx, ly, lw, lh = 24, 172, 976, 296
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD,
                           outline=LINE, width=2)
    tag_text = "LEAD  \u00b7  UKRAINE"
    tag_font = font(SANS_BOLD, 20)
    tag_w = int(draw.textlength(tag_text, font=tag_font)) + 28
    draw.rounded_rectangle([lx + 16, ly + 14, lx + 16 + tag_w, ly + 46], radius=5,
                           fill=RED)
    draw.text((lx + 30, ly + 19), tag_text, font=tag_font,
              fill=(255, 255, 255))
    head = "Zelensky: US \u201ctoo focused on Middle East\u201d as Trump calls Putin a friend"
    y = draw_wrapped(draw, lx + 16, ly + 58, head, font(SERIF_BOLD, 36),
                     640, INK, 44)
    deck = ("Kyiv's president tells the BBC the US is not pushing Russia hard "
            "enough \u2014 and calls Putin \u201can aggressor, and a killer\u201d. "
            "Trump says Putin \u201cwould like to make a deal\u201d.")
    draw_wrapped(draw, lx + 16, y + 6, deck, font(SANS, 21), 640, GREY, 28)

    # Lead illustration: three flags and a speech bubble.
    ix = lx + 676
    flag_ua(draw, ix, ly + 62, 84, 52)
    lab = font(SANS_BOLD, 15)
    flag_us(draw, ix + 96, ly + 62, 84, 52)
    flag_ru(draw, ix + 192, ly + 62, 84, 52)
    for fx, name in ((ix, "KYIV"), (ix + 96, "WASH."),
                     (ix + 192, "MOSCOW")):
        lw_ = draw.textlength(name, font=lab)
        draw.text((fx + (84 - lw_) / 2, ly + 120), name, font=lab, fill=GREY)
    draw_speech(draw, ix + 2, ly + 168, 264, 62, "\u201cPULL BACK\u201d")
    draw.text((ix + 2, ly + 240), "Trump to Putin, in China talks",
              font=font(SANS, 16), fill=GREY)

    # --- four story cards ----------------------------------------------
    cards = [
        ("EUROPE  \u00b7  ECONOMY", BLUE, "bank",
         "Hern\u00e1ndez de Cos picked to lead the ECB",
         "Spain's bank chief is the EU pick to succeed Lagarde."),
        ("AFRICA  \u00b7  SECURITY", RED, "warning",
         "Al-Shabaab claims deadly ambush on Somali troops",
         "Militants say hundreds of soldiers died; unverified."),
        ("ASIA  \u00b7  SPORT", TEAL, "cricket",
         "Gill bowls first in 2nd Test v New Zealand",
         "Gurnoor Brar debuts as Siraj sits out for the second Test."),
        ("MIDDLE EAST  \u00b7  GAZA", (120, 70, 40), "rain",
         "Gaza cities warn rains may flood 1,000 camps",
         "Winter storms threaten displacement sites in the Strip."),
    ]
    cw, ch, gap = 482, 208, 12
    gx, gy = 24, 484
    for i, (tag, colour, icon, headline, deck) in enumerate(cards):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                               fill=CARD, outline=LINE, width=2)
        draw.text((cx + 16, cy + 12), tag, font=font(SANS_BOLD, 17), fill=colour)
        tx = cx + 16
        if icon == "bank":
            draw_bank(draw, cx + 342, cy + 34, 118)
        elif icon == "warning":
            draw_warning(draw, cx + 356, cy + 40, 96)
        elif icon == "cricket":
            draw_cricket(draw, cx + 336, cy + 34, 130)
        else:
            draw_rain(draw, cx + 344, cy + 30, 120)
        y = draw_wrapped(draw, tx, cy + 40, headline, font(SERIF_BOLD, 27),
                         316, INK, 32)
        draw_wrapped(draw, tx, y + 6, deck, font(SANS, 19), 316, GREY, 25)

    # --- also today ------------------------------------------------------
    ay = 924
    draw.rectangle([24, ay, 1000, ay + 2], fill=GOLD_DARK)
    also = ("ALSO TODAY  \u2014  EU and Canada plan closer AI cooperation  \u00b7  "
            "French students prepare nationwide protests  \u00b7  US East Coast "
            "counts the cost of the Thanksgiving storm")
    draw_wrapped(draw, 24, ay + 12, also, font(SANS_BOLD, 19), 976, INK, 25)

    # --- footer ----------------------------------------------------------
    draw.rectangle([24, 992, 1000, 993], fill=LINE)
    foot = ("Sources: BBC, Reuters, European Council, AP  \u00b7  Every picture drawn "
            "by this program; no photographs  \u00b7  27 November 2026")
    f_foot = font(SANS, 15)
    tw = draw.textlength(foot, font=f_foot)
    draw.text(((WIDTH - tw) / 2, 998), foot, font=f_foot, fill=GREY)

    return img


def main() -> None:
    img = build()
    out = HERE / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
