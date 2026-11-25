#!/usr/bin/env python3
"""Render THE WORLD TODAY for Tuesday 24 November 2026.

A single 1024x1024 front page: 33 sourced stories (3 features, 10 small
illustrated items, 20 briefs), a big-number strip, region counts, a world
map with dots for the 13 illustrated stories, and a DATE CHECK bar.

Everything is drawn with Pillow primitives from the data tables below.
Run:  python3 draw24.py   -> writes entry.png next to this file.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 24
CONTENT_W = PAGE_W - 2 * MARGIN

PAPER = (251, 247, 238)
INK = (26, 26, 26)
MUTED = (96, 90, 82)
RED = (179, 38, 30)
BLUE = (29, 78, 137)
GOLD = (176, 132, 24)
LINE = (205, 198, 186)
CARD_BG = (255, 255, 255)
MAP_SEA = (214, 230, 238)
MAP_LAND = (196, 205, 178)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(size, path, bold=False):
    return ImageFont.truetype(path, size)


def fonts():
    return {
        "mast": ImageFont.truetype(SERIF_B, 60),
        "date": ImageFont.truetype(SANS_B, 20),
        "sub": ImageFont.truetype(SANS, 11),
        "big": ImageFont.truetype(SANS_B, 26),
        "cap": ImageFont.truetype(SANS, 9),
        "region": ImageFont.truetype(SANS_B, 12),
        "feat_head": ImageFont.truetype(SANS_B, 18),
        "feat_body": ImageFont.truetype(SANS, 12),
        "feat_src": ImageFont.truetype(SANS_B, 9),
        "small_head": ImageFont.truetype(SANS_B, 12),
        "small_body": ImageFont.truetype(SANS, 10),
        "small_src": ImageFont.truetype(SANS_B, 8),
        "brief": ImageFont.truetype(SANS, 11),
        "brief_b": ImageFont.truetype(SANS_B, 11),
        "sect": ImageFont.truetype(SANS_B, 11),
        "mapnum": ImageFont.truetype(SANS_B, 8),
        "check": ImageFont.truetype(SANS, 10),
        "check_b": ImageFont.truetype(SANS_B, 10),
    }


def text_w(draw, s, font):
    box = draw.textbbox((0, 0), s, font=font)
    return box[2] - box[0]


def fit_lines(draw, s, font, max_w, max_lines=None):
    """Greedy word wrap. Returns list of lines (each fits max_w)."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def draw_centered(draw, y, s, font, color, x0=0, x1=PAGE_W):
    w = text_w(draw, s, font)
    draw.text(((x0 + x1 - w) / 2, y), s, font=font, fill=color)


def rule(draw, y, color=RED, width=2, x0=MARGIN, x1=PAGE_W - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- data
# art: key into the painters below; lon/lat only for the 13 drawn stories.

FEATURES = [
    {
        "n": 1, "region": "ASIA", "place": "HANOI, VIETNAM", "art": "blast",
        "lon": 105.85, "lat": 21.03,
        "head": "6 KILLED IN HANOI EATERY BLAST",
        "body": ("A gas cylinder exploded at a hot pot eatery on Nguyen Van Tuyet "
                 "Street in Dong Da district at about 8:30am. The blast partly "
                 "collapsed the building and trapped diners inside. Six people "
                 "were killed and at least 10 more were in intensive care."),
        "src": "AP / REUTERS",
    },
    {
        "n": 2, "region": "ASIA", "place": "JIUQUAN, CHINA", "art": "rocket",
        "lon": 98.7, "lat": 40.9,
        "head": "SHENZHOU 24 LIFTS OFF WITH PAKISTAN'S FIRST ASTRONAUT",
        "body": ("China launched Shenzhou 24 to the Tiangong space station carrying "
                 "Tang Hongbo and Wu Yi \u2014 and Pakistan's Muhammad Zeeshan Ali, "
                 "the first foreign astronaut to fly on the station. The crew "
                 "will spend about six months in orbit."),
        "src": "AP",
    },
    {
        "n": 3, "region": "AMERICAS", "place": "NEW YORK", "art": "court",
        "lon": -74.0, "lat": 40.7,
        "head": "HUAWEI GUILTY ON 10 OF 12 COUNTS",
        "body": ("A Brooklyn jury found Huawei guilty on 10 of 12 counts \u2014 bank "
                 "fraud, wire fraud, sanctions violations and conspiring to steal "
                 "trade secrets over its Iran business. It was acquitted on "
                 "racketeering and obstruction. Sentencing is set for 14 Sept 2027."),
        "src": "CNN",
    },
]

SMALL = [
    {
        "n": 4, "region": "AMERICAS", "place": "WASHINGTON", "art": "tariff",
        "lon": -77.0, "lat": 38.9,
        "head": "US READY TO SLAP TARIFFS ON CHINA, EU",
        "body": ("Washington is poised to hit China, the EU and others with "
                 "tariffs after a probe into subsidised production."),
        "src": "AP",
    },
    {
        "n": 5, "region": "MIDDLE EAST", "place": "TEHRAN", "art": "missile",
        "lon": 51.4, "lat": 35.7,
        "head": "IRAN SHOWS OFF NEW MISSILE LAUNCHER",
        "body": ("The Revolutionary Guard unveiled a launcher firing two "
                 "liquid-fuelled missiles as Tehran ruled out talks until "
                 "seven US conditions are met."),
        "src": "AL JAZEERA",
    },
    {
        "n": 6, "region": "EUROPE", "place": "BENGHAZI, LIBYA", "art": "drone",
        "lon": 20.1, "lat": 32.1,
        "head": "KYIV: LIBYA STRIKE WAS SELF-DEFENCE",
        "body": ("Ukraine defended its naval drone attack on Russian ships off "
                 "Libya; Tripoli demanded explanations. A Russian strike "
                 "killed 2 and wounded 48."),
        "src": "AP",
    },
    {
        "n": 7, "region": "GLOBAL", "place": "THE HAGUE", "art": "scales",
        "lon": 4.3, "lat": 52.1,
        "head": "14 NATIONS BACK ICJ ROHINGYA RULING",
        "body": ("The UK, Spain, Canada, Australia and 10 more countries "
                 "recognised the court's genocide finding against Myanmar."),
        "src": "HORIZON",
    },
    {
        "n": 8, "region": "ASIA", "place": "KUALA LUMPUR", "art": "boat",
        "lon": 101.7, "lat": 3.1,
        "head": "MALAYSIA TO RETURN 6,500 ROHINGYA",
        "body": ("More than 6,500 refugees are to be sent back to Myanmar in "
                 "a move condemned by rights groups."),
        "src": "ALL VOICES NEWS",
    },
    {
        "n": 9, "region": "AMERICAS", "place": "CARACAS", "art": "money",
        "lon": -66.9, "lat": 10.5,
        "head": "VENEZUELA REVEALS $237.5BN DEBT",
        "body": ("Caracas disclosed its debt pile in a key step toward a "
                 "restructuring of the country's obligations."),
        "src": "TEXAS POST",
    },
    {
        "n": 10, "region": "AMERICAS", "place": "WASHINGTON", "art": "medal",
        "lon": -77.9, "lat": 38.3,
        "head": "GIULIANI GETS MEDAL OF FREEDOM",
        "body": ("President Trump awarded the former New York mayor the "
                 "Presidential Medal of Freedom at the White House."),
        "src": "WASHINGTON POST",
    },
    {
        "n": 11, "region": "ASIA", "place": "BEIJING", "art": "flags",
        "lon": 116.4, "lat": 39.9,
        "head": "CHINA PRESSES MIDDLE EAST PEACE PUSH",
        "body": ("Wang Yi met Iran's security chief as Xi hosted Oman's "
                 "sultan \u2014 his first state visit since 1978 \u2014 "
                 "signing 14 cooperation deals."),
        "src": "AL JAZEERA",
    },
    {
        "n": 12, "region": "GLOBAL", "place": "ZURICH", "art": "ball",
        "lon": 8.5, "lat": 47.4,
        "head": "2031 WOMEN'S WORLD CUP: FOUR HOSTS",
        "body": ("FIFA picked the US, Mexico, Costa Rica and Jamaica to "
                 "co-host the expanded 48-team tournament; the UK hosts 2035."),
        "src": "AP",
    },
    {
        "n": 13, "region": "AFRICA", "place": "DAKAR", "art": "trophy",
        "lon": -17.4, "lat": 14.7,
        "head": "SENEGAL BACK AS AFCON CHAMPIONS",
        "body": ("Senegal were reinstated as 2025 Africa Cup of Nations "
                 "champions after winning their appeal."),
        "src": "TEXAS POST",
    },
]

# Each brief is one line: "NN · PLACE — headline" (kept short on purpose).
BRIEFS = [
    (14, "KATHMANDU", "5.6 quake strikes Nepal near the China border"),
    (15, "HARRISBURG", "Pennsylvania measles epidemic claims a 9th death"),
    (16, "ADEN", "Houthis close in on Aden as Saudi strikes kill dozens"),
    (17, "RIYADH", "Houthi drone attack on a Riyadh tower injures 11"),
    (18, "BEIJING", "China bars Bloomberg reporter from Trump\u2013Xi\u2013Putin meet"),
    (19, "SEOUL", "South Korea shelter warning as Russian jets near airspace"),
    (20, "SINGAPORE", "Singapore probes Nvidia-linked Megaspeed after US ban"),
    (21, "JERUSALEM", "Israel warns Iran is developing chemical weapons"),
    (22, "MINSK", "Lukashenko offers to fly with Zelenskiy to Moscow"),
    (23, "OTTAWA", "Pentagon rebukes Canada over defence and F-35 review"),
    (24, "DHAKA", "Bangladesh's Hasina plans return from exile on Dec 16"),
    (25, "LONDON", "Two arrested over burglary at William and Kate's home"),
    (26, "ROME", "Meloni shocked at death of ex-police chief De Gennaro"),
    (27, "WASHINGTON", "Kilmar Abrego Garcia self-deports to Spain"),
    (28, "BEIJING", "China sentences official to death for spying"),
    (29, "PYONGYANG", "North Korea demands Swiss diplomatic office shut"),
    (30, "HONIARA", "Solomon Islands picks Australia as security partner"),
    (31, "WASHINGTON", "Washington beats Cincinnati 22\u201320 on last-second kick"),
    (32, "MUNICH", "Bayern Munich posts record \u20ac988.2m revenue"),
    (33, "LUSAKA", "Zambia opposition leader Mundubile charged with treason"),
]

NUMBERS = [
    ("6", "DEAD \u00b7 10+ HURT", "HANOI EATERY BLAST"),
    ("3", "ASTRONAUTS ABOARD", "SHENZHOU 24"),
    ("10/12", "COUNTS \u2014 GUILTY", "HUAWEI VERDICT"),
    ("6,500", "ROHINGYA TO RETURN", "MALAYSIA \u2192 MYANMAR"),
    ("$237.5BN", "DEBT PILE REVEALED", "VENEZUELA"),
]

REGION_LINE = ("ASIA 11 \u00b7 EUROPE 5 \u00b7 MIDDLE EAST 4 \u00b7 AMERICAS 8 \u00b7 "
               "AFRICA 2 \u00b7 OCEANIA 1 \u00b7 GLOBAL 2")

DATE_CHECK = ("DATE CHECK \u2014 NOT 24 NOV NEWS: Trump\u2013Xi\u2013Putin summit met "
              "23 Nov (only the Bloomberg reporter's barring is today's news) \u00b7 "
              "COP31 ended with no deal 23 Nov \u00b7 Nvidia reinstated Jensen Huang "
              "23 Nov \u00b7 Cyclone Akvan made landfall 20 Nov")


# ------------------------------------------------------- illustrations
# Every painter draws inside the box (x, y, w, h) with flat shapes.

def art_blast(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(43, 32, 28))
    cx, cy = x + w * 0.62, y + h * 0.42
    for r, col in ((34, (255, 122, 26)), (24, (255, 176, 32)), (13, (255, 232, 130))):
        pts = []
        import math
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    for sx, sy, sr in ((0.2, 0.3, 9), (0.3, 0.22, 7), (0.85, 0.25, 8), (0.8, 0.55, 6)):
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr],
                  fill=(120, 110, 105))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(20, 16, 14))
    for bx, bw, bh in ((0.05, 0.22, 0.5), (0.32, 0.18, 0.62), (0.75, 0.2, 0.55)):
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h],
                    fill=(58, 46, 40))
        for wy in range(2):
            d.rectangle([x + w * bx + 3, y + h - h * bh + 4 + wy * 12,
                         x + w * bx + 8, y + h - h * bh + 10 + wy * 12],
                        fill=(255, 210, 110))


def art_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 58))
    import random
    rnd = random.Random(24)
    for _ in range(18):
        sx, sy = rnd.uniform(0, 1), rnd.uniform(0, 1)
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    cx = x + w * 0.5
    d.polygon([(cx - 13, y + h * 0.62), (cx + 13, y + h * 0.62),
               (cx, y + h * 0.18)], fill=(232, 232, 232))
    d.rectangle([cx - 13, y + h * 0.58, cx + 13, y + h * 0.66], fill=(232, 232, 232))
    d.rectangle([cx - 13, y + h * 0.52, cx + 13, y + h * 0.56], fill=RED)
    d.polygon([(cx - 20, y + h * 0.66), (cx - 8, y + h * 0.62),
               (cx - 8, y + h * 0.72)], fill=(180, 180, 180))
    d.polygon([(cx + 20, y + h * 0.66), (cx + 8, y + h * 0.62),
               (cx + 8, y + h * 0.72)], fill=(180, 180, 180))
    d.polygon([(cx - 8, y + h * 0.66), (cx + 8, y + h * 0.66),
               (cx, y + h * 0.95)], fill=(255, 150, 30))
    d.polygon([(cx - 4, y + h * 0.66), (cx + 4, y + h * 0.66),
               (cx, y + h * 0.85)], fill=(255, 220, 90))
    d.ellipse([x + w * 0.78 - 8, y + h * 0.14 - 8, x + w * 0.78 + 8, y + h * 0.14 + 8],
              fill=(230, 230, 220))


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 230, 236))
    d.polygon([(x + w * 0.1, y + h * 0.30), (x + w * 0.9, y + h * 0.30),
               (x + w * 0.5, y + h * 0.10)], fill=(120, 128, 140))
    d.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.88, y + h * 0.36],
                fill=(150, 158, 170))
    for i, cx in enumerate((0.22, 0.5, 0.78)):
        d.rectangle([x + w * cx - 5, y + h * 0.36, x + w * cx + 5, y + h * 0.82],
                    fill=(245, 245, 245), outline=(150, 158, 170))
        d.rectangle([x + w * cx - 8, y + h * 0.33, x + w * cx + 8, y + h * 0.36],
                    fill=(245, 245, 245))
        d.rectangle([x + w * cx - 8, y + h * 0.82, x + w * cx + 8, y + h * 0.85],
                    fill=(245, 245, 245))
    d.rectangle([x + w * 0.08, y + h * 0.85, x + w * 0.92, y + h * 0.92],
                fill=(150, 158, 170))
    d.rectangle([x + w * 0.50, y + h * 0.55, x + w * 0.98, y + h * 0.72], fill=RED)
    d.text((x + w * 0.55, y + h * 0.58), "10/12",
           font=ImageFont.truetype(SANS_B, 10), fill=(255, 255, 255))


def art_tariff(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    base = y + h * 0.85
    bars = [(0.12, 0.35, BLUE), (0.32, 0.55, RED), (0.52, 0.45, BLUE), (0.72, 0.75, RED)]
    for bx, bh, col in bars:
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + 0.14), base], fill=col)
    d.line([(x + w * 0.08, base), (x + w * 0.92, base)], fill=INK, width=2)
    d.line([(x + w * 0.10, y + h * 0.28), (x + w * 0.9, y + h * 0.12)],
           fill=RED, width=2)
    d.polygon([(x + w * 0.9, y + h * 0.12), (x + w * 0.82, y + h * 0.12),
               (x + w * 0.88, y + h * 0.22)], fill=RED)
    d.text((x + w * 0.06, y + h * 0.06), "$",
           font=ImageFont.truetype(SANS_B, 16), fill=GOLD)


def art_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 220, 196))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(196, 168, 128))
    d.polygon([(x + w * 0.30, y + h * 0.62), (x + w * 0.62, y + h * 0.20),
               (x + w * 0.68, y + h * 0.26), (x + w * 0.36, y + h * 0.68)],
              fill=(120, 126, 118))
    d.polygon([(x + w * 0.62, y + h * 0.20), (x + w * 0.72, y + h * 0.14),
               (x + w * 0.76, y + h * 0.24), (x + w * 0.68, y + h * 0.26)],
              fill=RED)
    d.rectangle([x + w * 0.08, y + h * 0.62, x + w * 0.5, y + h * 0.72], fill=(80, 88, 78))
    for wx in (0.16, 0.30, 0.44):
        d.ellipse([x + w * wx - 4, y + h * 0.72 - 4, x + w * wx + 4, y + h * 0.72 + 4],
                  fill=(30, 30, 30))
    for i, (sx, sy, sr) in enumerate(((0.72, 0.3, 6), (0.8, 0.22, 8), (0.88, 0.32, 5))):
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr, y + h * sy + sr],
                  fill=(240, 240, 235))


def art_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 68, 110))
    for i in range(3):
        yy = y + h * (0.55 + i * 0.14)
        d.arc([x + w * 0.1, yy - 4, x + w * 0.9, yy + 6], 0, 180, fill=(160, 200, 225))
    d.rectangle([x + w * 0.18, y + h * 0.42, x + w * 0.5, y + h * 0.52], fill=(40, 40, 40))
    d.rectangle([x + w * 0.3, y + h * 0.34, x + w * 0.38, y + h * 0.42], fill=(40, 40, 40))
    cx, cy = x + w * 0.72, y + h * 0.38
    import math
    for i in range(12):
        ang = math.pi * i / 6
        rr = 16 if i % 2 == 0 else 8
        d.line([(cx, cy), (cx + rr * math.cos(ang), cy + rr * math.sin(ang))],
               fill=(255, 190, 60), width=2)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 120, 30))


def art_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 242))
    cx = x + w * 0.5
    d.line([(cx, y + h * 0.15), (cx, y + h * 0.85)], fill=INK, width=3)
    d.line([(x + w * 0.18, y + h * 0.28), (x + w * 0.82, y + h * 0.28)], fill=INK, width=3)
    d.ellipse([cx - 4, y + h * 0.12, cx + 4, y + h * 0.12 + 8], fill=GOLD)
    for side in (-1, 1):
        px = cx + side * w * 0.32
        d.line([(cx, y + h * 0.28), (px, y + h * 0.28)], fill=INK, width=2)
        d.line([(px, y + h * 0.28), (px, y + h * 0.52)], fill=INK, width=2)
        d.polygon([(px - 14, y + h * 0.52), (px + 14, y + h * 0.52),
                   (px, y + h * 0.66)], fill=GOLD)
    d.rectangle([cx - 14, y + h * 0.85, cx + 14, y + h * 0.90], fill=INK)


def art_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(176, 214, 232))
    d.ellipse([x + w * 0.78 - 9, y + h * 0.12 - 9, x + w * 0.78 + 9, y + h * 0.12 + 9],
              fill=(255, 200, 60))
    d.polygon([(x + w * 0.15, y + h * 0.55), (x + w * 0.85, y + h * 0.55),
               (x + w * 0.72, y + h * 0.72), (x + w * 0.28, y + h * 0.72)],
              fill=(120, 70, 40))
    for px in (0.3, 0.42, 0.54, 0.66):
        d.ellipse([x + w * px - 3, y + h * 0.42 - 3, x + w * px + 3, y + h * 0.42 + 3],
                  fill=INK)
        d.rectangle([x + w * px - 2, y + h * 0.45, x + w * px + 2, y + h * 0.55],
                    fill=INK)
    for i in range(3):
        yy = y + h * (0.78 + i * 0.08)
        d.arc([x + w * 0.08, yy - 3, x + w * 0.92, yy + 5], 0, 180, fill=(255, 255, 255))


def art_money(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 226))
    for sx, sy, n in ((0.18, 0.55, 4), (0.45, 0.42, 5), (0.72, 0.6, 3)):
        for i in range(n):
            yy = y + h * sy - i * 7
            d.ellipse([x + w * sx - 12, yy - 5, x + w * sx + 12, yy + 5], fill=GOLD,
                      outline=(140, 105, 20))
    d.text((x + w * 0.06, y + h * 0.06), "$",
           font=ImageFont.truetype(SANS_B, 18), fill=(60, 120, 60))


def art_medal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(242, 236, 220))
    cx = x + w * 0.5
    d.polygon([(cx - 26, y + h * 0.08), (cx - 6, y + h * 0.08),
               (cx - 2, y + h * 0.45)], fill=RED)
    d.polygon([(cx + 26, y + h * 0.08), (cx + 6, y + h * 0.08),
               (cx + 2, y + h * 0.45)], fill=BLUE)
    d.ellipse([cx - 20, y + h * 0.42, cx + 20, y + h * 0.42 + 40], fill=GOLD,
              outline=(140, 105, 20))
    d.ellipse([cx - 13, y + h * 0.42 + 7, cx + 13, y + h * 0.42 + 33], outline=(140, 105, 20))
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + math.pi * i / 5
        rr = 8 if i % 2 == 0 else 3.5
        pts.append((cx + rr * math.cos(ang), y + h * 0.42 + 20 + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 255, 255))


def art_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    d.rectangle([x + w * 0.12, y + h * 0.10, x + w * 0.14, y + h * 0.92], fill=INK)
    d.rectangle([x + w * 0.58, y + h * 0.10, x + w * 0.60, y + h * 0.92], fill=INK)
    d.rectangle([x + w * 0.14, y + h * 0.12, x + w * 0.46, y + h * 0.38], fill=(222, 41, 16))
    for sx, sy in ((0.18, 0.18), (0.24, 0.16), (0.2, 0.24), (0.28, 0.22)):
        d.ellipse([x + w * sx - 1.5, y + h * sy - 1.5, x + w * sx + 1.5, y + h * sy + 1.5],
                  fill=(255, 222, 0))
    d.rectangle([x + w * 0.60, y + h * 0.12, x + w * 0.9, y + h * 0.38], fill=(255, 255, 255))
    d.rectangle([x + w * 0.60, y + h * 0.12, x + w * 0.9, y + h * 0.20], fill=(0, 122, 61))
    d.rectangle([x + w * 0.60, y + h * 0.30, x + w * 0.9, y + h * 0.38], fill=(206, 17, 38))
    d.rectangle([x + w * 0.60, y + h * 0.12, x + w * 0.66, y + h * 0.38], fill=(206, 17, 38))
    d.ellipse([x + w * 0.5 - 8, y + h * 0.62 - 8, x + w * 0.5 + 8, y + h * 0.62 + 8],
              fill=(255, 255, 255), outline=GOLD)


def art_ball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 140, 70))
    d.line([(x, y + h * 0.5), (x + w, y + h * 0.5)], fill=(255, 255, 255), width=1)
    cx, cy, r = x + w * 0.5, y + h * 0.5, min(w, h) * 0.30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK)
    import math
    pts = []
    for i in range(5):
        ang = -math.pi / 2 + 2 * math.pi * i / 5
        pts.append((cx + r * 0.45 * math.cos(ang), cy + r * 0.45 * math.sin(ang)))
    d.polygon(pts, fill=INK)
    for i in range(5):
        ang = -math.pi / 2 + 2 * math.pi * i / 5
        px, py = cx + r * 0.8 * math.cos(ang), cy + r * 0.8 * math.sin(ang)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)


def art_trophy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 210))
    cx = x + w * 0.5
    d.polygon([(cx - 18, y + h * 0.18), (cx + 18, y + h * 0.18),
               (cx + 12, y + h * 0.48), (cx - 12, y + h * 0.48)], fill=GOLD)
    d.arc([cx - 30, y + h * 0.18, cx - 8, y + h * 0.44], 90, 270, fill=GOLD, width=3)
    d.arc([cx + 8, y + h * 0.18, cx + 30, y + h * 0.44], -90, 90, fill=GOLD, width=3)
    d.rectangle([cx - 3, y + h * 0.48, cx + 3, y + h * 0.66], fill=GOLD)
    d.rectangle([cx - 16, y + h * 0.66, cx + 16, y + h * 0.74], fill=GOLD)
    d.rectangle([cx - 22, y + h * 0.74, cx + 22, y + h * 0.80], fill=(120, 90, 30))
    import random
    rnd = random.Random(13)
    for _ in range(14):
        px, py = rnd.uniform(0.08, 0.92), rnd.uniform(0.06, 0.3)
        d.rectangle([x + w * px, y + h * py, x + w * px + 3, y + h * py + 3],
                    fill=rnd.choice([RED, BLUE, (60, 160, 80)]))


PAINTERS = {
    "blast": art_blast, "rocket": art_rocket, "court": art_court,
    "tariff": art_tariff, "missile": art_missile, "drone": art_drone,
    "scales": art_scales, "boat": art_boat, "money": art_money,
    "medal": art_medal, "flags": art_flags, "ball": art_ball,
    "trophy": art_trophy,
}


# ------------------------------------------------------- page sections

def section_masthead(d, f):
    draw_centered(d, 14, "THE WORLD TODAY", f["mast"], INK)
    rule(d, 84, RED, 2)
    draw_centered(d, 92, "TUESDAY 24 NOVEMBER 2026", f["date"], INK)
    draw_centered(d, 116, "33 STORIES \u00b7 7 REGIONS \u00b7 EVERY STORY SOURCED & DATE-CHECKED",
                  f["sub"], MUTED)


def section_numbers(d, f):
    y = 134
    cell = CONTENT_W / 5
    for i, (big, cap, sub) in enumerate(NUMBERS):
        cx0 = MARGIN + i * cell
        draw_centered(d, y, big, f["big"], RED, cx0, cx0 + cell)
        draw_centered(d, y + 30, cap, f["cap"], MUTED, cx0, cx0 + cell)
        draw_centered(d, y + 42, sub, f["cap"], INK, cx0, cx0 + cell)
        if i:
            d.line([(cx0, y + 2), (cx0, y + 52)], fill=LINE, width=1)
    rule(d, 192, LINE, 1)
    draw_centered(d, 198, REGION_LINE, f["region"], INK)


def section_features(d, f):
    y = 216
    row_h, gap = 94, 4
    for s in FEATURES:
        d.rectangle([MARGIN, y, PAGE_W - MARGIN, y + row_h], fill=CARD_BG,
                    outline=LINE)
        PAINTERS[s["art"]](d, MARGIN, y, 100, row_h)
        tx = MARGIN + 112
        tw = PAGE_W - MARGIN - tx
        d.text((tx, y + 6), "%02d \u00b7 %s \u2014 %s" % (s["n"], s["region"], s["place"]),
               font=f["feat_src"], fill=RED)
        d.text((tx, y + 20), s["head"], font=f["feat_head"], fill=INK)
        lines = fit_lines(d, s["body"], f["feat_body"], tw, 2)
        yy = y + 46
        for ln in lines:
            d.text((tx, yy), ln, font=f["feat_body"], fill=INK)
            yy += 15
        d.text((tx, y + 80), "SOURCE: " + s["src"], font=f["feat_src"], fill=MUTED)
        y += row_h + gap


# Simplified continent outlines (equirectangular, lon/lat).
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    [(-55, 60), (-40, 64), (-30, 68), (-20, 70), (-25, 76), (-45, 78), (-58, 72)],
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -8), (-38, -15), (-48, -25), (-58, -35), (-65, -45), (-70, -52),
     (-73, -40), (-72, -25), (-78, -10), (-81, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (13, -5), (9, 4), (-8, 5), (-15, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 68), (12, 62), (5, 60), (-2, 57), (-5, 50), (-10, 44)],
    [(30, 62), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (145, 45),
     (135, 43), (127, 40), (122, 32), (120, 25), (110, 20), (105, 10),
     (100, 8), (95, 15), (90, 22), (85, 20), (80, 10), (75, 8), (72, 20),
     (65, 25), (58, 25), (52, 28), (48, 30), (42, 35), (35, 36), (30, 38)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14),
     (122, -17), (118, -20)],
]


def section_small(d, f):
    y = 512
    cell_w, cell_h, gap = 188, 112, 8
    for r in range(2):
        for c in range(5):
            s = SMALL[r * 5 + c]
            x0 = MARGIN + c * (cell_w + gap)
            d.rectangle([x0, y, x0 + cell_w, y + cell_h], fill=CARD_BG, outline=LINE)
            PAINTERS[s["art"]](d, x0, y, cell_w, 52)
            d.text((x0 + 6, y + 56), "%02d \u00b7 %s" % (s["n"], s["place"]),
                   font=f["small_src"], fill=RED)
            lines = fit_lines(d, s["head"], f["small_head"], cell_w - 12, 2)
            yy = y + 68
            for ln in lines:
                d.text((x0 + 6, yy), ln, font=f["small_head"], fill=INK)
                yy += 14
            d.text((x0 + 6, y + cell_h - 12), s["src"], font=f["small_src"],
                   fill=MUTED)
        y += cell_h + 6


def section_briefs(d, f):
    y = 744
    d.text((MARGIN, y), "THE REST OF THE DAY", font=f["sect"], fill=RED)
    rule(d, y + 16, LINE, 1)
    y = 766
    col_w = (CONTENT_W - 24) // 2
    for i, (n, place, head) in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        x0 = MARGIN + col * (col_w + 24)
        yy = y + row * 15
        lead = "%02d \u00b7 %s \u2014 " % (n, place)
        d.text((x0, yy), lead, font=f["brief_b"], fill=INK)
        lx = text_w(d, lead, f["brief_b"])
        d.text((x0 + lx, yy), head, font=f["brief"], fill=INK)
        total = lx + text_w(d, head, f["brief"])
        if total > col_w:
            print("WARN brief %d too wide: %d > %d" % (n, total, col_w),
                  file=sys.stderr)


def section_map(d, f):
    y0, mh = 918, 66
    d.rectangle([MARGIN, y0, PAGE_W - MARGIN, y0 + mh], fill=MAP_SEA, outline=LINE)

    def proj(lon, lat):
        lat = max(-42.0, min(72.0, lat))
        return (MARGIN + (lon + 180) / 360.0 * CONTENT_W,
                y0 + (72 - lat) / 114.0 * mh)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=MAP_LAND)
    d.text((MARGIN + 6, y0 + 3), "THE 13 ILLUSTRATED STORIES",
           font=f["mapnum"], fill=MUTED)
    # (n, lon, lat, dot lon, dot lat): dot position may be offset from the
    # true spot when neighbours crowd (leader line points back to it).
    dots = []
    for s in FEATURES + SMALL:
        dots.append((s["n"], s["lon"], s["lat"], s["lon"], s["lat"]))
    dots[2] = (3, -74.0, 40.7, -68.0, 46.0)    # New York
    dots[9] = (10, -77.0, 38.9, -84.0, 32.0)   # Washington (Giuliani)
    dots[11] = (12, 8.5, 47.4, 14.0, 43.0)    # Zurich
    for n, lon, lat, dlon, dlat in dots:
        px, py = proj(lon, lat)
        dx, dy = proj(dlon, dlat)
        if (dx, dy) != (px, py):
            d.line([(px, py), (dx, dy)], fill=RED, width=1)
        d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=RED, outline=(255, 255, 255))
        num = str(n)
        nw = text_w(d, num, f["mapnum"])
        d.text((dx - nw / 2, dy - 4), num, font=f["mapnum"], fill=(255, 255, 255))


def section_datecheck(d, f):
    y = 988
    rule(d, y - 4, RED, 1)
    lines = fit_lines(d, DATE_CHECK, f["check"], CONTENT_W, 2)
    yy = y
    for ln in lines:
        d.text((MARGIN, yy), ln, font=f["check"], fill=INK)
        yy += 11
    if len(lines) > 2:
        print("WARN date check needs %d lines" % len(lines), file=sys.stderr)


def build():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    f = fonts()
    section_masthead(d, f)
    section_numbers(d, f)
    section_features(d, f)
    section_small(d, f)
    section_briefs(d, f)
    section_map(d, f)
    section_datecheck(d, f)
    img.save(OUT, "PNG", optimize=True)
    print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))


if __name__ == "__main__":
    build()
