#!/usr/bin/env python3
"""Cards direction for 22 November 2026: hero features + illustrated
story cards + a compact 'also' list. Drawn with Pillow primitives
only. No photos, no network, no randomness, no timestamps.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT", os.path.join(HERE, "..", "assets", "entry.png"))
HERO_PIC = int(os.environ.get("HERO_PIC", "120"))
HERO_HEAD = int(os.environ.get("HERO_HEAD", "26"))
CARD_PIC = int(os.environ.get("CARD_PIC", "72"))
CARD_HEAD = int(os.environ.get("CARD_HEAD", "17"))
ALSO_SIZE = int(os.environ.get("ALSO_SIZE", "15"))
TITLE_SIZE = int(os.environ.get("TITLE_SIZE", "66"))
DATE_SIZE = int(os.environ.get("DATE_SIZE", "27"))
BAR_H = int(os.environ.get("BAR_H", "5"))
HERO_DECK = int(os.environ.get("HERO_DECK", "13"))
DECK_SIZE = int(os.environ.get("DECK_SIZE", "11"))

PAPER = (247, 243, 235)
INK = (24, 24, 24)
MUTED = (96, 89, 77)
RED = (178, 44, 32)
NAVY = (30, 56, 94)
TEAL = (16, 120, 105)
AMBER = (198, 128, 18)
SLATE = (70, 80, 95)
OLIVE = (110, 110, 40)
PLUM = (96, 70, 110)
CARD = (255, 253, 247)
CARD_LINE = (206, 198, 182)
CREAM = (248, 244, 236)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
COND_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w, max_lines=None):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + " …", font=fnt) > max_w:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += " …"
    return lines


def block(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- pictograms
def pic_climate(d, x, y, s):
    for k in range(8):
        a = math.radians(k * 45)
        d.line([x + s * 0.30 + s * 0.13 * math.cos(a),
                y + s * 0.26 + s * 0.13 * math.sin(a),
                x + s * 0.30 + s * 0.20 * math.cos(a),
                y + s * 0.26 + s * 0.20 * math.sin(a)],
               fill=(232, 164, 32), width=4)
    d.ellipse([x + s * 0.18, y + s * 0.14, x + s * 0.42, y + s * 0.38],
              fill=(232, 164, 32))
    d.pieslice([x - s * 0.05, y + s * 0.55, x + s * 0.55, y + s * 1.25],
               180, 360, fill=(46, 139, 87))
    d.pieslice([x + s * 0.45, y + s * 0.62, x + s * 1.05, y + s * 1.25],
               180, 360, fill=(34, 110, 68))


def pic_burst(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=NAVY)
    for cx in (0.26, 0.74):
        d.line([x + s * cx, y + s * 0.96, x + s * cx, y + s * 0.52],
               fill=(232, 164, 32), width=4)
        d.ellipse([x + s * cx - 5, y + s * 0.44, x + s * cx + 5,
                   y + s * 0.52], fill=CREAM)
    cx, cy = x + s * 0.50, y + s * 0.24
    for k in range(8):
        a = math.radians(k * 45)
        d.line([cx, cy, cx + s * 0.26 * math.cos(a),
                cy + s * 0.26 * math.sin(a)], fill=(232, 120, 32), width=4)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(232, 164, 32))


def pic_drone(d, x, y, s):
    """Quadcopter over slate rooftops, orange blast below."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 234, 226))
    d.rectangle([x + s * 0.08, y + s * 0.68, x + s * 0.38, y + s],
                fill=(70, 80, 95))
    d.rectangle([x + s * 0.44, y + s * 0.58, x + s * 0.78, y + s],
                fill=(52, 60, 74))
    d.rectangle([x + s * 0.82, y + s * 0.72, x + s * 0.94, y + s],
                fill=(70, 80, 95))
    for wx in (0.14, 0.24, 0.52, 0.64):
        d.rectangle([x + s * wx, y + s * 0.76, x + s * (wx + 0.05),
                     y + s * 0.84], fill=(232, 164, 32))
    cx, cy = x + s * 0.61, y + s * 0.55
    for k in range(8):
        a = math.radians(k * 45)
        d.line([cx, cy, cx + s * 0.13 * math.cos(a),
                cy + s * 0.13 * math.sin(a)], fill=(232, 120, 32), width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(232, 164, 32))
    dx, dy = x + s * 0.50, y + s * 0.24
    d.line([dx - s * 0.32, dy, dx + s * 0.32, dy], fill=INK, width=4)
    d.rectangle([dx - s * 0.12, dy - s * 0.07, dx + s * 0.12,
                 dy + s * 0.07], fill=INK)
    for rx in (-0.32, 0.32):
        d.line([dx + s * rx - s * 0.13, dy - s * 0.06,
                dx + s * rx + s * 0.13, dy - s * 0.06],
               fill=INK, width=4)


def pic_badge(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=NAVY)
    cx, cy, r1, r2 = x + s * 0.5, y + s * 0.5, s * 0.34, s * 0.15
    pts = []
    for k in range(10):
        r = r1 if k % 2 == 0 else r2
        a = math.radians(-90 + k * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(232, 164, 32))
    d.ellipse([cx - s * 0.09, cy - s * 0.09, cx + s * 0.09,
               cy + s * 0.09], fill=NAVY)


def pic_chart(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(255, 253, 247))
    d.line([x + s * 0.08, y + s * 0.88, x + s * 0.92, y + s * 0.88],
           fill=(180, 175, 165), width=3)
    pts = [(0.10, 0.22), (0.32, 0.38), (0.48, 0.30), (0.66, 0.55),
           (0.86, 0.78)]
    xy = [(x + s * px, y + s * py) for px, py in pts]
    d.line(xy, fill=RED, width=5, joint="curve")
    ex, ey = x + s * 0.86, y + s * 0.78
    d.polygon([(ex, ey), (ex - 14, ey - 2), (ex - 2, ey - 14)], fill=RED)


def pic_fire(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(228, 226, 220))
    d.rectangle([x + s * 0.08, y + s * 0.66, x + s * 0.92, y + s],
                fill=(70, 80, 95))
    d.rectangle([x + s * 0.12, y + s * 0.44, x + s * 0.24, y + s * 0.66],
                fill=(70, 80, 95))
    d.polygon([(x + s * 0.08, y + s * 0.66), (x + s * 0.32, y + s * 0.50),
               (x + s * 0.56, y + s * 0.66)], fill=(70, 80, 95))
    d.polygon([(x + s * 0.56, y + s * 0.66), (x + s * 0.72, y + s * 0.52),
               (x + s * 0.92, y + s * 0.66)], fill=(70, 80, 95))
    cx, cy = x + s * 0.62, y + s * 0.30
    d.polygon([(cx, cy - s * 0.28), (cx + s * 0.20, cy + s * 0.02),
               (cx + s * 0.09, cy + s * 0.16), (cx - s * 0.09, cy + s * 0.16),
               (cx - s * 0.20, cy + s * 0.02)], fill=(232, 120, 32))
    d.ellipse([cx - s * 0.06, cy - s * 0.02, cx + s * 0.06,
               cy + s * 0.12], fill=(232, 164, 32))


def pic_scales(d, x, y, s):
    """Balance scales: post, beam, two pans."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 234, 226))
    cx = x + s * 0.50
    d.rectangle([cx - 3, y + s * 0.12, cx + 3, y + s * 0.82], fill=INK)
    d.ellipse([cx - 6, y + s * 0.06, cx + 6, y + s * 0.18], fill=RED)
    d.rectangle([x + s * 0.30, y + s * 0.82, x + s * 0.70, y + s * 0.88],
                fill=INK)
    d.line([x + s * 0.14, y + s * 0.24, x + s * 0.86, y + s * 0.24],
           fill=INK, width=4)
    for px in (0.14, 0.86):
        d.line([x + s * px, y + s * 0.24, x + s * px, y + s * 0.44],
               fill=INK, width=3)
        d.pieslice([x + s * (px - 0.13), y + s * 0.40,
                    x + s * (px + 0.13), y + s * 0.62], 0, 180,
                   fill=(198, 128, 18))


def pic_trade(d, x, y, s):
    """Open shipping box with an upward arrow."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 234, 226))
    d.polygon([(x + s * 0.16, y + s * 0.78), (x + s * 0.50, y + s * 0.58),
               (x + s * 0.84, y + s * 0.78), (x + s * 0.84, y + s * 0.92),
               (x + s * 0.16, y + s * 0.92)], fill=(198, 128, 18))
    d.polygon([(x + s * 0.16, y + s * 0.78), (x + s * 0.50, y + s * 0.58),
               (x + s * 0.50, y + s * 0.78)], fill=(232, 164, 32))
    d.polygon([(x + s * 0.84, y + s * 0.78), (x + s * 0.50, y + s * 0.58),
               (x + s * 0.50, y + s * 0.78)], fill=(160, 100, 10))
    d.line([x + s * 0.50, y + s * 0.52, x + s * 0.50, y + s * 0.14],
           fill=TEAL, width=5)
    d.polygon([(x + s * 0.50, y + s * 0.06), (x + s * 0.38, y + s * 0.20),
               (x + s * 0.62, y + s * 0.20)], fill=TEAL)


def pic_planet(d, x, y, s):
    """Ringed planet with craters and a small probe."""
    d.rectangle([x, y, x + s, y + s], fill=(30, 56, 94))
    cx, cy, r = x + s * 0.50, y + s * 0.52, s * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 148, 140))
    for ox, oy, orr in [(-0.12, -0.08, 0.06), (0.10, 0.06, 0.08),
                        (-0.02, 0.14, 0.05)]:
        d.ellipse([cx + s * ox - s * orr, cy + s * oy - s * orr,
                   cx + s * ox + s * orr, cy + s * oy + s * orr],
                  fill=(110, 108, 100))
    d.ellipse([x + s * 0.06, y + s * 0.38, x + s * 0.94, y + s * 0.66],
              outline=(232, 164, 32), width=4)
    d.ellipse([x + s * 0.76, y + s * 0.16, x + s * 0.84, y + s * 0.24],
              fill=CREAM)


def pic_flag(d, x, y, s):
    """Checkered racing flag on a pole."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 234, 226))
    d.line([x + s * 0.16, y + s * 0.08, x + s * 0.16, y + s * 0.94],
           fill=INK, width=5)
    cw, chh = s * 0.16, s * 0.16
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([x + s * 0.20 + c * cw, y + s * 0.14 + r * chh,
                             x + s * 0.20 + (c + 1) * cw,
                             y + s * 0.14 + (r + 1) * chh], fill=INK)
    d.rectangle([x + s * 0.20, y + s * 0.14,
                 x + s * 0.20 + 4 * cw, y + s * 0.14 + 3 * chh],
                outline=INK, width=2)


def pic_ballot(d, x, y, s):
    """Ballot box with a paper slip and a check mark."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 234, 226))
    d.rectangle([x + s * 0.18, y + s * 0.52, x + s * 0.82, y + s * 0.90],
                fill=(30, 56, 94))
    d.rectangle([x + s * 0.38, y + s * 0.46, x + s * 0.62, y + s * 0.52],
                fill=(24, 24, 24))
    d.polygon([(x + s * 0.34, y + s * 0.46), (x + s * 0.44, y + s * 0.14),
               (x + s * 0.66, y + s * 0.22), (x + s * 0.56, y + s * 0.46)],
              fill=CARD, outline=INK)
    d.line([x + s * 0.46, y + s * 0.34, x + s * 0.52, y + s * 0.40,
            x + s * 0.62, y + s * 0.24], fill=RED, width=4)


def pic_shield(d, x, y, s):
    """Shield with a keyhole: the hacked database."""
    d.rectangle([x, y, x + s, y + s], fill=(238, 234, 226))
    cx = x + s * 0.50
    d.polygon([(cx - s * 0.30, y + s * 0.10), (cx + s * 0.30, y + s * 0.10),
               (cx + s * 0.30, y + s * 0.48), (cx, y + s * 0.88),
               (cx - s * 0.30, y + s * 0.48)], fill=(30, 56, 94))
    d.ellipse([cx - s * 0.07, y + s * 0.30, cx + s * 0.07, y + s * 0.44],
              fill=CREAM)
    d.polygon([(cx - s * 0.04, y + s * 0.42), (cx + s * 0.04, y + s * 0.42),
               (cx + s * 0.08, y + s * 0.62), (cx - s * 0.08, y + s * 0.62)],
              fill=CREAM)


# ---------------------------------------------------------------- content
HERO = [
    ("CLIMATE — ANTALYA", TEAL, pic_climate,
     "COP31 collapses with no deal",
     "The EU rejects a pact that never mentions fossil fuels; 194 "
     "countries leave with no deal."),
    ("MIDDLE EAST — BAHRAIN", RED, pic_burst,
     "Iran strikes Bahrain site",
     "Iranian projectiles hit an industrial site, injuring two; Gulf "
     "states condemn the attack."),
]

CARDS = [
    ("UKRAINE", NAVY, pic_drone, "186 drones rain on Ukraine",
     "Air defences down 161 of 186; flats hit near Kyiv, 14 missing."),
    ("MEXICO", AMBER, pic_badge, "‘El Chapo Isidro’ captured",
     "Cartel boss seized in Sinaloa; 11 killed, four of them soldiers."),
    ("MARKETS", RED, pic_chart, "Stocks slide into correction",
     "S&P 500 −3.7%, Nasdaq −5.3% as the AI sell-off spreads to Asia."),
    ("INDONESIA", OLIVE, pic_fire, "Candy factory fire kills 3",
     "Blaze in Cikande, Banten; dozens still missing in the ruins."),
    ("WORLD", RED, pic_scales, "Myanmar guilty of genocide",
     "World Court finds Myanmar guilty of genocide."),
    ("ASIA", TEAL, pic_trade, "EU–Indonesia trade deal signed",
     "Tariffs scrapped on up to 98.5% of goods after a decade of talks."),
    ("SPACE", PLUM, pic_planet, "BepiColombo reaches Mercury",
     "European-Japanese probe enters orbit after an eight-year journey."),
    ("SPORT", PLUM, pic_flag, "Verstappen wins Las Vegas GP",
     "Norris 2nd, Piastri 3rd after 35 lead changes under the lights."),
    ("ASIA", TEAL, pic_ballot, "Hong Kong votes in record poll",
     "Election Committee poll: 98.79% turnout."),
    ("TECH", AMBER, pic_shield, "FBI database reportedly hacked",
     "The FBI investigates a breach of its crime database, the NCIC."),
]

ALSO = [
    "Settlers torch 12 West Bank vehicles",
    "Drones hit Khartoum, damage UN building",
    "Poland: Russia plotted to kill US rapper",
    "Denmark expels Russian over murder plot",
    "UN killer-robot talks pushed to 2028",
    "Gaza strike leaves one critically hurt",
    "Lebanon seizes 264 kg of explosives",
    "Sudan’s Burhan vows to fight on",
    "France calls UN meeting on Kyiv attacks",
    "Drone hits Vyshneve supermarket; 3 killed",
    "Odesa grid ‘unable to cope’ after strikes",
    "Nepal PM Shah makes first visit to India",
    "China–Japan ties worsen over Taiwan",
    "Lahore tops pollution list; AQI over 500",
    "S. Korea minister quits over AI cheating",
    "M5.7 quake hits central Japan; 22 hurt",
    "AI sell-off spreads to Japan and Korea",
    "Trump says Iran wants a deal",
    "Spain faces uncertainty before 29 Nov vote",
    "Croatians rally over a hospital death",
    "Russia grasps US offer on European security",
    "Ex-SA deputy president dies at 71",
    "Nigeria boat capsizes; at least 24 dead",
    "Cost-of-living protests spread in Europe",
    "Eisenkot invites Likud to coalition talks",
    "India declares 720/9 v New Zealand",
    "Jet drone crosses into Moldova twice",
]

TICKER = ("COP31: NO DEAL  —  IRAN HITS BAHRAIN  —  186 DRONES OVER "
          "UKRAINE  —  ‘EL CHAPO ISIDRO’ SEIZED  —  S&P 500 −3.7%")


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28

    # masthead ------------------------------------------------------
    d.rectangle([mx, 10, W - mx, 14], fill=RED)
    d.rectangle([mx, 17, W - mx, 18], fill=INK)
    title = "THE WORLD TODAY"
    tf = font(SERIF, TITLE_SIZE)
    d.text(((W - d.textlength(title, font=tf)) / 2, 24), title,
           font=tf, fill=INK)
    date = "Sunday, 22 November 2026"
    df = font(SERIF, DATE_SIZE)
    d.text(((W - d.textlength(date, font=df)) / 2, 96), date,
           font=df, fill=INK)
    d.rectangle([mx, 132, W - mx, 158], fill=NAVY)
    bf = font(SANS_B, 15)
    left = "39 STORIES  •  7 REGIONS  •  ONE DAY"
    right = "THE DAY IN WORLD NEWS"
    d.text((mx + 10, 139), left, font=bf, fill=(255, 255, 255))
    d.text((W - mx - 10 - d.textlength(right, font=bf), 139), right,
           font=bf, fill=(255, 255, 255))

    # hero features ---------------------------------------------------
    gap = 12
    hw = (W - 2 * mx - gap) // 2
    hy = 170
    hh = 154
    for i, (kick, color, pic, head, deck) in enumerate(HERO):
        x = mx + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD,
                    outline=CARD_LINE, width=1)
        d.rectangle([x, hy, x + hw, hy + BAR_H], fill=color)
        pic(d, x + 12, hy + 16, HERO_PIC)
        kx = x + 12 + HERO_PIC + 12
        kf = font(COND_B, 15)
        d.text((kx, hy + 16), kick, font=kf, fill=color)
        sf = font(SANS_B, 11)
        d.text((kx, hy + 36), "LEAD STORY", font=sf, fill=MUTED)
        hf = font(SERIF, HERO_HEAD)
        lines = wrap(d, head, hf, hw - (12 + HERO_PIC + 12) - 12, max_lines=2)
        y2 = block(d, kx, hy + 58, lines, hf, INK, HERO_HEAD + 4)
        df2 = font(SANS, HERO_DECK)
        lines = wrap(d, deck, df2, hw - (12 + HERO_PIC + 12) - 12, max_lines=2)
        block(d, kx, y2 + 4, lines, df2, MUTED, HERO_DECK + 3)

    # illustrated cards -------------------------------------------------
    cw = (W - 2 * mx - 4 * 10) // 5
    chh = 185
    top = hy + hh + 12
    for i, (kick, color, pic, head, deck) in enumerate(CARDS):
        r, c = divmod(i, 5)
        x = mx + c * (cw + 10)
        y = top + r * (chh + 10)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD,
                    outline=CARD_LINE, width=1)
        d.rectangle([x, y, x + cw, y + BAR_H], fill=color)
        pic(d, x + (cw - CARD_PIC) // 2, y + 12, CARD_PIC)
        kf = font(COND_B, 13)
        kw = d.textlength(kick, font=kf)
        d.text((x + (cw - kw) / 2, y + 86), kick, font=kf, fill=color)
        hf = font(SERIF, CARD_HEAD)
        lines = wrap(d, head, hf, cw - 16, max_lines=3)
        y2 = block(d, x + 8, y + 106, lines, hf, INK, CARD_HEAD + 3)
        df2 = font(SANS, DECK_SIZE)
        lines = wrap(d, deck, df2, cw - 16, max_lines=3)
        block(d, x + 8, y2 + 3, lines, df2, MUTED, DECK_SIZE + 3)

    # also list ---------------------------------------------------------
    ay = top + 2 * chh + 10 + 14
    hf2 = font(COND_B, 16)
    d.text((mx, ay), "ALSO ON 22 NOVEMBER", font=hf2, fill=RED)
    d.line([mx, ay + 22, W - mx, ay + 22], fill=RED, width=2)
    col_w = (W - 2 * mx - 2 * 16) // 3
    fnt = font(COND_B, ALSO_SIZE)
    lead = ALSO_SIZE + 4
    for ci in range(3):
        x = mx + ci * (col_w + 16)
        y = ay + 30
        for it in ALSO[ci * 9:(ci + 1) * 9]:
            lines = wrap(d, it, fnt, col_w - 14)
            d.text((x, y + 1), "•", font=fnt, fill=RED)
            y = block(d, x + 14, y, lines, fnt, INK, lead) + 5

    # footer --------------------------------------------------------
    d.line([mx, 972, W - mx, 972], fill=INK, width=2)
    tf2 = font(SANS_B, 13)
    d.text(((W - d.textlength(TICKER, font=tf2)) / 2, 981), TICKER,
           font=tf2, fill=INK)
    cf = font(SANS, 11)
    credit = ("Sources: Reuters, AP, AFP, CNN, Ukrainian Air Force, "
              "info.gov.hk, BMKG — all stories from Sunday 22 Nov 2026.")
    d.text(((W - d.textlength(credit, font=cf)) / 2, 1003), credit,
           font=cf, fill=MUTED)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
