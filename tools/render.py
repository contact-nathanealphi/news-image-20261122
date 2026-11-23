#!/usr/bin/env python3
"""Draw the 22 November 2026 front page: 40 stories, one 1024x1024 PNG.

Everything is drawn with Pillow primitives (DejaVu Serif headlines,
DejaVu Sans body, small original pictograms). No photos, no network,
no randomness, no timestamps, so the output is byte-identical on
every run. The story list lives in research.md; the text below is
kept short on purpose so every item fits its slot.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "entry.png")

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
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w, max_lines=None):
    """Greedy word wrap; optionally cap lines, adding an ellipsis."""
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
    """Amber sun over green hills, one dark leaf."""
    for k in range(8):
        a = math.radians(k * 45)
        d.line([x + s * 0.30 + s * 0.13 * math.cos(a),
                y + s * 0.26 + s * 0.13 * math.sin(a),
                x + s * 0.30 + s * 0.20 * math.cos(a),
                y + s * 0.26 + s * 0.20 * math.sin(a)],
               fill=(232, 164, 32), width=3)
    d.ellipse([x + s * 0.18, y + s * 0.14, x + s * 0.42, y + s * 0.38],
              fill=(232, 164, 32))
    d.pieslice([x - s * 0.05, y + s * 0.55, x + s * 0.55, y + s * 1.25],
               180, 360, fill=(46, 139, 87))
    d.pieslice([x + s * 0.45, y + s * 0.62, x + s * 1.05, y + s * 1.25],
               180, 360, fill=(34, 110, 68))
    d.ellipse([x + s * 0.62, y + s * 0.42, x + s * 0.88, y + s * 0.66],
              fill=(24, 90, 54))
    d.line([x + s * 0.66, y + s * 0.62, x + s * 0.84, y + s * 0.46],
           fill=CREAM, width=2)


def pic_burst(d, x, y, s):
    """Night sky, two interceptor trails, one orange burst."""
    d.rectangle([x, y, x + s, y + s], fill=NAVY)
    for cx in (0.26, 0.74):
        d.line([x + s * cx, y + s * 0.96, x + s * cx, y + s * 0.52],
               fill=(232, 164, 32), width=3)
        d.ellipse([x + s * cx - 4, y + s * 0.44, x + s * cx + 4,
                   y + s * 0.52], fill=CREAM)
    cx, cy = x + s * 0.50, y + s * 0.24
    for k in range(8):
        a = math.radians(k * 45)
        d.line([cx, cy, cx + s * 0.26 * math.cos(a),
                cy + s * 0.26 * math.sin(a)], fill=(232, 120, 32), width=3)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(232, 164, 32))


def pic_drone(d, x, y, s):
    """Quadcopter drone over a dark rooftop, orange blast below."""
    d.rectangle([x, y, x + s, y + s], fill=(228, 226, 220))
    d.rectangle([x + s * 0.06, y + s * 0.74, x + s * 0.94, y + s],
                fill=(40, 40, 40))
    for bx, bw in [(0.10, 0.18), (0.38, 0.22), (0.68, 0.16)]:
        d.rectangle([x + s * bx, y + s * 0.60, x + s * (bx + bw),
                     y + s * 0.74], fill=(40, 40, 40))
    # blast star on the middle rooftop
    cx, cy = x + s * 0.49, y + s * 0.62
    for k in range(8):
        a = math.radians(k * 45)
        d.line([cx, cy, cx + s * 0.16 * math.cos(a),
                cy + s * 0.16 * math.sin(a)], fill=(232, 120, 32), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(232, 164, 32))
    # drone above: body, arms, spinning rotors
    dx, dy = x + s * 0.50, y + s * 0.26
    d.line([dx - s * 0.30, dy, dx + s * 0.30, dy], fill=INK, width=3)
    d.rectangle([dx - s * 0.11, dy - s * 0.06, dx + s * 0.11,
                 dy + s * 0.06], fill=INK)
    for rx in (-0.30, 0.30):
        d.line([dx + s * rx - s * 0.12, dy - s * 0.05,
                dx + s * rx + s * 0.12, dy - s * 0.05],
               fill=INK, width=3)
        d.ellipse([dx + s * rx - 3, dy - s * 0.10, dx + s * rx + 3,
                   dy], fill=INK)


def pic_badge(d, x, y, s):
    """Gold sheriff-style star badge on navy."""
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
    """Red falling line chart with an arrowhead."""
    d.rectangle([x, y, x + s, y + s], fill=(255, 253, 247))
    d.line([x + s * 0.08, y + s * 0.88, x + s * 0.92, y + s * 0.88],
           fill=(180, 175, 165), width=2)
    pts = [(0.10, 0.22), (0.32, 0.38), (0.48, 0.30), (0.66, 0.55),
           (0.86, 0.78)]
    xy = [(x + s * px, y + s * py) for px, py in pts]
    d.line(xy, fill=RED, width=4, joint="curve")
    ex, ey = x + s * 0.86, y + s * 0.78
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)],
              fill=RED)


def pic_fire(d, x, y, s):
    """Factory with sawtooth roof and chimney, big flame above."""
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


# ---------------------------------------------------------------- content
LEADS = [
    ("CLIMATE — ANTALYA", TEAL, pic_climate,
     "COP31 collapses with no deal",
     "EU rejects a pact that never mentions fossil fuels; the longest "
     "COP ever ends with no deal."),
    ("MIDDLE EAST — BAHRAIN", RED, pic_burst,
     "Iran strikes Bahrain site",
     "Projectiles hit an industrial site, injuring two; Gulf states "
     "condemn the attack."),
    ("UKRAINE", NAVY, pic_drone,
     "186 drones rain on Ukraine",
     "Drone hits flats near Kyiv; 14 missing. Missile kills two in "
     "Kryvyi Rih, 60 wounded."),
    ("MEXICO", AMBER, pic_badge,
     "‘El Chapo Isidro’ captured",
     "Cartel boss seized in a Sinaloa raid; 11 killed, four of them "
     "soldiers."),
    ("MARKETS", RED, pic_chart,
     "Stocks slide into correction",
     "S&P 500 falls 3.7%, Nasdaq 5.3% on Friday as the AI sell-off "
     "spreads to Asia."),
    ("INDONESIA", OLIVE, pic_fire,
     "Candy factory fire kills 3",
     "Blaze in Cikande, Banten; dozens still missing as rescuers "
     "search the ruins."),
]

COLUMNS = [
    ("WORLD", RED, [
        "ICJ: Myanmar guilty of Rohingya genocide",
        "Settlers torch 12 vehicles in West Bank; Israel opens inquiry",
        "Drones hit Khartoum, damage a UN building",
        "Poland: Russia twice tried to kill a US-Ukrainian rapper",
        "Denmark expels Russian official over an alleged plot",
        "UN killer-robot talks pushed to 2028",
        "Gaza strike leaves one person critically hurt",
        "Lebanon seizes 264 kg of explosives, arrests three",
        "Sudan’s Burhan vows to fight on as RSF advances",
        "France calls UN meeting on Kyiv embassy attacks",
        "Spain faces uncertainty before its 29 Nov election",
        "UK and EU strike new deals after Brussels summit",
    ]),
    ("ASIA & INDONESIA", TEAL, [
        "EU–Indonesia trade deal signed; tariffs end on 98.5% of goods",
        "Nepal PM Balen Shah makes his first visit to India",
        "China–Japan ties worsen over Taiwan and minerals",
        "Lahore tops world pollution list; AQI over 500",
        "S. Korea education chief quits over AI cheating scandal",
        "Aftershock rattles Maluku after Saturday’s M7.2 quake",
        "M5.7 quake hits central Japan; 22 hurt, trains halted",
    ]),
    ("MARKETS & TECH", AMBER, [
        "AI sell-off spreads to Japan and Korea",
        "FBI crime database reportedly hacked; FBI investigates",
        "Trump: claimed FBI hack ‘not good’, may offer benefits",
        "Iran claims it destroyed two US Patriot radars",
        "Trump says Iran wants a deal as Gulf crisis deepens",
    ]),
    ("SPORT, CULTURE & SCIENCE", PLUM, [
        "Verstappen wins a thrilling Las Vegas Grand Prix",
        "BepiColombo enters orbit around Mercury",
        "Mlambo-Ngcuka, ex-SA deputy president, dies at 71",
        "Nigeria boat capsizes; at least 24 dead on way to funeral",
        "Protests over living costs spread across Europe",
        "Eisenkot invites Netanyahu’s Likud to coalition talks",
        "India declares 720/9 v New Zealand; Pant’s 9th Test ton",
    ]),
    ("MORE", SLATE, [
        "Salvadorans killed in Haiti — first deaths after deployment",
        "Yemen army: 149 Houthis killed or wounded in 816 attacks",
        "Croatians rally over a psychiatric hospital death",
        "Russia grasps US offer on European security",
    ]),
]

# columns of sections: (left) WORLD, (middle) ASIA + MARKETS,
# (right) SPORT + MORE
LAYOUT = [[0], [1, 2], [3, 4]]

TICKER = ("COP31: NO DEAL  —  IRAN HITS BAHRAIN  —  186 DRONES OVER "
          "UKRAINE  —  ‘EL CHAPO ISIDRO’ SEIZED  —  S&P 500 −3.7%")


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # masthead ------------------------------------------------------
    d.rectangle([mx, 10, W - mx, 14], fill=RED)
    d.rectangle([mx, 17, W - mx, 18], fill=INK)
    title = "THE WORLD TODAY"
    tf = font(SERIF, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 24), title,
           font=tf, fill=INK)
    date = "Sunday, 22 November 2026"
    df = font(SERIF, 26)
    d.text(((W - d.textlength(date, font=df)) / 2, 96), date,
           font=df, fill=INK)
    d.rectangle([mx, 132, W - mx, 158], fill=NAVY)
    bf = font(SANS_B, 15)
    left = "40 STORIES  •  7 REGIONS  •  ONE DAY"
    right = "THE DAY IN WORLD NEWS"
    d.text((mx + 10, 139), left, font=bf, fill=(255, 255, 255))
    d.text((W - mx - 10 - d.textlength(right, font=bf), 139), right,
           font=bf, fill=(255, 255, 255))

    # lead cards ----------------------------------------------------
    gap = 12
    cw = (W - 2 * mx - 2 * gap) // 3
    ch = 152
    top = 170
    for i, (kick, color, pic, head, deck) in enumerate(LEADS):
        r, c = divmod(i, 3)
        x = mx + c * (cw + gap)
        y = top + r * (ch + 10)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD,
                    outline=CARD_LINE, width=1)
        d.rectangle([x, y, x + cw, y + 5], fill=color)
        pic(d, x + cw - 52, y + 14, 40)
        kf = font(SANS_B, 12)
        d.text((x + 10, y + 14), kick, font=kf, fill=color)
        sf = font(SANS_B, 10)
        d.text((x + 10, y + 31), "LEAD STORY", font=sf, fill=MUTED)
        hf = font(SERIF, 20)
        lines = wrap(d, head, hf, cw - 20, max_lines=3)
        y2 = block(d, x + 10, y + 52, lines, hf, INK, 24)
        df2 = font(SANS, 12)
        lines = wrap(d, deck, df2, cw - 20, max_lines=2)
        block(d, x + 10, y2 + 4, lines, df2, MUTED, 15)

    # columns -------------------------------------------------------
    col_w = (W - 2 * mx - 2 * 16) // 3
    col_x = [mx, mx + col_w + 16, mx + 2 * (col_w + 16)]
    col_top = 500
    col_bottom = 962

    def measure(size):
        """Total height needed per column at this item font size."""
        fnt = font(SANS_B, size)
        lead = size + 4
        need = []
        for group in LAYOUT:
            h = 0
            for si in group:
                _, _, items = COLUMNS[si]
                h += 26  # section header
                for it in items:
                    n = len(wrap(d, it, fnt, col_w - 16))
                    h += n * lead + 8
            need.append(h)
        return need

    size = 14
    while size > 11 and max(measure(size)) > col_bottom - col_top:
        size -= 1
    fnt = font(SANS_B, size)
    lead = size + 4
    hf = font(SANS_B, 14)

    for ci, group in enumerate(LAYOUT):
        x = col_x[ci]
        y = col_top
        for si in group:
            name, color, items = COLUMNS[si]
            d.text((x, y), name, font=hf, fill=color)
            d.line([x, y + 20, x + col_w, y + 20], fill=color, width=2)
            y += 29
            for it in items:
                lines = wrap(d, it, fnt, col_w - 16)
                d.text((x, y + 1), "•", font=fnt, fill=RED)
                y = block(d, x + 16, y, lines, fnt, INK, lead) + 8

    # footer --------------------------------------------------------
    d.line([mx, 972, W - mx, 972], fill=INK, width=2)
    tf2 = font(SANS_B, 13)
    d.text(((W - d.textlength(TICKER, font=tf2)) / 2, 981), TICKER,
           font=tf2, fill=INK)
    cf = font(SANS, 11)
    credit = "All stories from Sunday 22 November 2026."
    d.text(((W - d.textlength(credit, font=cf)) / 2, 1003), credit,
           font=cf, fill=MUTED)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    draw()
