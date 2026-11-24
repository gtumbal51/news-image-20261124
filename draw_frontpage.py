#!/usr/bin/env python3
"""Draw the news-image-20261124 front page (edition: Meridian Ledger).

Renders "Tuesday 24 November 2026" as a dense one-page broadsheet:
4 illustrated lead stories, 10 illustrated panels, 24 one-line briefs,
a six-figure day-in-numbers strip, a dot-matrix world map with numbered
pins, a region tally and a date-check box. Everything is drawn in code
with Pillow; there are no photos and no external assets.

The story tables are validated before any drawing happens, so a data
typo fails the render instead of reaching the page.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- data ---

EDITION = "Meridian Ledger"
DAY_LINE = "Tuesday 24 November 2026"
EYEBROW = "THE WORLD ON ONE PAGE \u00b7 38 STORIES \u00b7 SIX CONTINENTS"

LEADS = [
    {
        "n": 1, "place": "NEW YORK, USA", "kicker": "MARKETS",
        "headline": "HUANG IS BACK AS NVIDIA SOARS 31%",
        "summary": ("Nvidia's board reinstated Jensen Huang as chief "
                    "executive, eleven days after he quit. "
                    "Shares jumped 31%."),
        "tag": "CONFIRMED", "bignum": "+31%", "icon": "chart",
        "lon": -74.0, "lat": 40.7, "region": "N AMERICA",
    },
    {
        "n": 2, "place": "THE GULF", "kicker": "GEOPOLITICS",
        "headline": "IRAN HITS GULF TARGETS AS BLOCKADE BITES",
        "summary": ("Iran stepped up strikes on Gulf targets and filed "
                    "a $290bn claim as a US blockade squeezes "
                    "its oil trade."),
        "tag": "CONFIRMED", "bignum": "$290BN", "icon": "burst",
        "lon": 51.5, "lat": 25.3, "region": "ASIA",
    },
    {
        "n": 3, "place": "JIUQUAN, CHINA", "kicker": "SPACE",
        "headline": "SHENZHOU-24 TO FLY FIRST FOREIGN ASTRONAUT",
        "summary": ("China launches Shenzhou-24 on Wednesday, carrying "
                    "Pakistan's Zeeshan Ali \u2014 the first foreign "
                    "astronaut on Tiangong."),
        "tag": "REUTERS \u00b7 CONFIRMED", "bignum": "1ST", "icon": "planet",
        "lon": 100.3, "lat": 40.9, "region": "ASIA",
    },
    {
        "n": 4, "place": "BENGHAZI, LIBYA", "kicker": "WAR AT SEA",
        "headline": "KYIV CONFIRMS IT SANK RUSSIAN WARSHIP",
        "summary": ("Ukraine says it sank the Russian corvette Merkury "
                    "at Libya's Benghazi naval base, taking the war "
                    "far from home."),
        "tag": "CONFIRMED", "bignum": "1", "icon": "ship",
        "lon": 20.1, "lat": 32.1, "region": "AFRICA",
    },
]

PANELS = [
    {"n": 5, "headline": "RUSSIAN JETS BREACH KOREA AIR ZONE",
     "tag": "CONFIRMED", "bignum": "1", "icon": "drone",
     "lon": 127.0, "lat": 37.5, "region": "ASIA"},
    {"n": 6, "headline": "TRUMP GETS NEW PATH TO FIGHT CONVICTION",
     "tag": "CONFIRMED", "bignum": "34", "icon": "scales",
     "lon": -74.0, "lat": 40.7, "region": "N AMERICA"},
    {"n": 7, "headline": "US BLACKLISTS SINGAPORE CHIP FIRM MEGASPEED",
     "tag": "CONFIRMED", "bignum": "1", "icon": "shield",
     "lon": -77.0, "lat": 38.9, "region": "N AMERICA"},
    {"n": 8, "headline": "SOUTH AFRICA BOWL BANGLADESH OUT FOR 91",
     "tag": "CONFIRMED", "bignum": "91", "icon": "burst",
     "lon": 28.2, "lat": -25.9, "region": "AFRICA"},
    {"n": 9, "headline": "LIVERPOOL ROUT UNITED 4-0 ON POCHETTINO DEBUT",
     "tag": "CONFIRMED", "bignum": "4-0", "icon": "burst",
     "lon": -3.0, "lat": 53.4, "region": "EUROPE"},
    {"n": 10, "headline": "BRENT SLIDES BELOW $90 AS GULF FLOWS RESUME",
     "tag": "CONFIRMED", "bignum": "-3%", "icon": "chart",
     "lon": -0.1, "lat": 51.5, "region": "EUROPE"},
    {"n": 11, "headline": "TWO STATES SUE SPACEX OVER GROK IMAGERY",
     "tag": "CONFIRMED", "bignum": "2", "icon": "case",
     "lon": -77.5, "lat": 37.5, "region": "N AMERICA"},
    {"n": 12, "headline": "SPAIN'S RIGHT LEADS POLLS BEFORE NOV 29 VOTE",
     "tag": "REPORTED", "bignum": "29", "icon": "debate",
     "lon": -3.7, "lat": 40.4, "region": "EUROPE"},
    {"n": 13, "headline": "SOFTBANK WEIGHS $2BN BET ON INTEL",
     "tag": "REPORTED", "bignum": "$2BN", "icon": "robot",
     "lon": 139.7, "lat": 35.7, "region": "ASIA"},
    {"n": 14, "headline": "AMAZON NEARS $7.5BN DECART AI DEAL",
     "tag": "REPORTED", "bignum": "$7.5BN", "icon": "chart",
     "lon": -122.3, "lat": 47.6, "region": "N AMERICA"},
]

BRIEFS = [
    (15, "Kyiv", "Drone-strike toll rises to 11 as rescuers keep digging (follow-up)"),
    (16, "Antalya", "Blame game after COP31 collapse; Saudis in the frame (follow-up)"),
    (17, "Helsinki", "Finland summons Russian envoy over helicopter breach"),
    (18, "Berlin", "Merz tells Kremlin to halt \u201cdangerous provocations\u201d"),
    (19, "Brussels", "EU unveils new sanctions plan aimed at Russia's shadow fleet"),
    (20, "Cikande", "Search goes on for 30 missing as DNA tests begin (follow-up)"),
    (21, "Bangkok", "Thai-Cambodia border truce holds after talks"),
    (22, "Dhaka", "Bangladesh starts typhoid jabs for 50 million children"),
    (23, "New Delhi", "Ex-lawmaker Prajwal Revanna jailed for life for rape"),
    (24, "Beijing", "Official sentenced to death for leaking 35 state secrets"),
    (25, "Seoul", "President names new foreign minister and spy chief"),
    (26, "Singapore", "City-state lifts GDP outlook to about 6% on AI boom"),
    (27, "Washington", "Jeffries wins caucus vote, set to be first Black speaker (follow-up)"),
    (28, "Washington", "Senate GOP open to cutting Iran war funds as shutdown nears"),
    (29, "Washington", "DNC sets broad rules for 2028 presidential debates"),
    (30, "Mexico City", "Mexico to try \u2018El Chapo Isidro\u2019 at home, defying US (follow-up)"),
    (31, "Des Moines", "Trump and Iowa governor-elect spar over lead-azide blast"),
    (32, "Denver", "Nuggets edge Bulls 151-145 in OT; Jokic's 202nd triple-double"),
    (33, "Kinshasa", "Fighting in Ituri traps Ebola responders, WHO warns (follow-up)"),
    (34, "Khartoum", "Drone strikes hit homes and a UN building"),
    (35, "Banjul", "Gambia intercepts 491 would-be migrants"),
    (36, "Brazil", "Storm toll rises to five in the south, thousands displaced"),
    (37, "Doha", "Chile rally from 2-0 down to beat Algeria 4-2 at U-17 World Cup"),
    (38, "Canberra", "Coalition blocks Vanuatu treaty over climate clauses"),
]

REGIONS = [
    ("N AMERICA", 11), ("EUROPE", 8), ("ASIA", 11),
    ("AFRICA", 5), ("S AMERICA", 2), ("OCEANIA", 1),
]

FIGURES = [
    ("+31%", "NVIDIA'S ONE-DAY JUMP ON HUANG'S RETURN"),
    ("+6.5%", "NASDAQ'S MONDAY REBOUND AFTER THE ROUT"),
    ("50M", "CHILDREN IN BANGLADESH'S TYPHOID DRIVE"),
    ("$2BN", "SOFTBANK'S PLANNED INTEL INVESTMENT"),
    ("91", "BANGLADESH BOWLED OUT AT CENTURION"),
    ("30", "STILL MISSING AFTER THE CIKANDE FIRE"),
]

DATECHECK = (
    "LEFT OUT \u2014 OTHER DAYS: the Cikande toll (24) was confirmed Monday and the search "
    "goes on \u00b7 COP31 collapsed Sunday; today brings the blame game \u00b7 the Benghazi "
    "warship sank Sunday; today Ukraine claims the strike \u00b7 the Kyiv boy was pulled out "
    "Monday; today the toll rises to 11 \u00b7 the Democrats' 258 House seats and Jeffries' "
    "caucus win were Monday's news; today is the follow-through \u00b7 \u2018El Chapo Isidro\u2019 "
    "was seized Monday; today Mexico says it will try him at home. NOT YET: Shenzhou-24 "
    "lifts off Wednesday 08:18 Beijing time \u00b7 Spain votes Sunday 29 November \u00b7 "
    "US markets shut Thursday for Thanksgiving."
)

# Coarse equirectangular land mask, 72 columns (5 deg each, -180..180)
# by 27 rows (5 deg each, 75..-60). Each row is a list of inclusive
# (first, last) column ranges holding land. Hand-plotted from an atlas.
LAND_ROWS = [
    [(3, 8), (12, 20), (24, 32), (39, 42), (44, 71)],
    [(2, 8), (10, 24), (25, 31), (37, 42), (42, 71)],
    [(3, 8), (9, 25), (31, 31), (37, 41), (41, 71)],
    [(6, 10), (10, 25), (35, 35), (37, 39), (41, 71)],
    [(11, 25), (34, 42), (42, 63), (68, 68)],
    [(11, 23), (34, 42), (44, 62), (62, 64)],
    [(11, 22), (34, 42), (44, 61), (62, 64)],
    [(11, 21), (34, 43), (43, 48), (51, 60), (62, 64)],
    [(12, 20), (34, 42), (43, 54), (56, 60)],
    [(13, 19), (33, 42), (43, 47), (49, 53), (55, 57)],
    [(15, 18), (32, 43), (50, 53), (55, 60)],
    [(17, 19), (32, 44), (51, 52), (55, 57), (60, 60)],
    [(18, 20), (32, 44), (55, 57)],
    [(20, 25), (33, 44), (55, 60)],
    [(20, 26), (34, 44), (55, 64)],
    [(20, 28), (34, 44), (56, 65)],
    [(20, 29), (34, 44), (58, 64)],
    [(21, 28), (33, 44), (44, 46), (58, 66)],
    [(22, 28), (33, 43), (44, 45), (58, 66)],
    [(22, 28), (33, 42), (58, 66)],
    [(22, 26), (33, 42), (58, 66)],
    [(22, 25), (32, 41), (59, 66), (69, 71)],
    [(21, 24), (32, 41), (69, 71)],
    [(21, 23), (32, 40)],
    [(21, 23)],
    [(21, 22)],
    [(22, 22)],
]

# ---------------------------------------------------------------- style ---

W, H = 1024, 1024
PAPER = (246, 241, 229)
CARD = (236, 228, 205)
PANEL_BG = (243, 236, 218)
INK = (26, 26, 26)
RED = (155, 28, 28)
RED_DK = (120, 18, 18)
GREY = (90, 84, 72)
RULE = (26, 26, 26)
DOT = (168, 158, 134)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_block(draw, text, path, size, max_w, max_lines, min_size=9):
    """Wrap text, shrinking the font until it fits max_lines lines.

    Returns (font, lines). Raises if it still does not fit at min_size.
    """
    s = size
    while s >= min_size:
        fnt = font(path, s)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        s -= 1
    raise ValueError("text does not fit: %r" % text[:60])


def fit_single(draw, text, path, size, max_w, min_size=9):
    """Shrink one line of text until it fits max_w. Returns the font."""
    s = size
    while s >= min_size:
        fnt = font(path, s)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        s -= 1
    raise ValueError("line does not fit: %r" % text[:60])


# ------------------------------------------------------------- validation ---

def validate():
    """Data self-check: 38 stories, numbered 1-38, regions and pins sane."""
    assert len(LEADS) == 4, "need 4 leads"
    assert len(PANELS) == 10, "need 10 panels"
    assert len(BRIEFS) == 24, "need 24 briefs"
    assert len(FIGURES) == 6, "need 6 figures"
    pictured = LEADS + PANELS
    nums = [s["n"] for s in pictured] + [b[0] for b in BRIEFS]
    assert nums == list(range(1, 39)), "story numbers must run 1..38, got %r" % nums
    tally = {}
    for s in pictured:
        tally[s["region"]] = tally.get(s["region"], 0) + 1
    for b in BRIEFS:
        pass
    # briefs carry no region field; count them from their region tags below
    brief_regions = BRIEF_REGIONS
    assert len(brief_regions) == 24, "need 24 brief regions"
    for r in brief_regions:
        tally[r] = tally.get(r, 0) + 1
    for name, want in REGIONS:
        assert tally.get(name, 0) == want, "region %s: %d != %d" % (
            name, tally.get(name, 0), want)
    assert sum(tally.values()) == 38, "region tally must sum to 38"
    for s in pictured:
        assert s["tag"] in ("CONFIRMED", "REPORTED", "REUTERS \u00b7 CONFIRMED"), (
            "bad tag on story %d" % s["n"])
        assert s["icon"] in ICONS, "unknown icon %r" % s["icon"]
        assert -180 <= s["lon"] <= 180 and -60 <= s["lat"] <= 75, (
            "pin out of map range on story %d" % s["n"])
        assert s["bignum"], "story %d needs a big number" % s["n"]
        assert s["headline"] and s["headline"] == s["headline"].upper(), (
            "headline %d must be caps" % s["n"])
    assert "24 November" in DAY_LINE and "Tuesday" in DAY_LINE
    return tally


BRIEF_REGIONS = [
    "EUROPE", "EUROPE", "EUROPE", "EUROPE", "EUROPE",
    "ASIA", "ASIA", "ASIA", "ASIA", "ASIA", "ASIA", "ASIA",
    "N AMERICA", "N AMERICA", "N AMERICA", "N AMERICA", "N AMERICA",
    "N AMERICA",
    "AFRICA", "AFRICA", "AFRICA",
    "S AMERICA", "S AMERICA",
    "OCEANIA",
]

# ----------------------------------------------------------------- icons ---

def icon_chart(d, x, y, s, ink, red):
    d.rectangle([x, y + s * 0.55, x + s * 0.22, y + s], fill=ink)
    d.rectangle([x + s * 0.38, y + s * 0.30, x + s * 0.60, y + s], fill=red)
    d.rectangle([x + s * 0.76, y + s * 0.08, x + s * 0.98, y + s], fill=ink)
    d.line([x, y + s, x + s, y + s], fill=ink, width=2)


def icon_burst(d, x, y, s, ink, red):
    cx, cy = x + s / 2, y + s / 2
    for k in range(8):
        import math
        a = math.pi * k / 4
        d.line([cx + math.cos(a) * s * 0.18, cy + math.sin(a) * s * 0.18,
                cx + math.cos(a) * s * 0.5, cy + math.sin(a) * s * 0.5],
               fill=red if k % 2 == 0 else ink, width=3)
    d.ellipse([cx - s * 0.12, cy - s * 0.12, cx + s * 0.12, cy + s * 0.12],
              fill=ink)


def icon_planet(d, x, y, s, ink, red):
    d.ellipse([x + s * 0.18, y + s * 0.12, x + s * 0.82, y + s * 0.76],
              outline=ink, width=3)
    d.ellipse([x + s * 0.05, y + s * 0.38, x + s * 0.95, y + s * 0.62],
              outline=red, width=3)
    d.ellipse([x + s * 0.60, y + s * 0.22, x + s * 0.70, y + s * 0.32],
              fill=red)


def icon_ship(d, x, y, s, ink, red):
    d.polygon([(x, y + s * 0.62), (x + s, y + s * 0.62),
               (x + s * 0.82, y + s * 0.95), (x + s * 0.18, y + s * 0.95)],
              fill=ink)
    d.line([x + s * 0.5, y + s * 0.62, x + s * 0.5, y + s * 0.10],
           fill=ink, width=3)
    d.polygon([(x + s * 0.5, y + s * 0.10), (x + s * 0.82, y + s * 0.22),
               (x + s * 0.5, y + s * 0.34)], fill=red)


def icon_drone(d, x, y, s, ink, red):
    d.line([x + s * 0.15, y + s * 0.15, x + s * 0.85, y + s * 0.85],
           fill=ink, width=3)
    d.line([x + s * 0.85, y + s * 0.15, x + s * 0.15, y + s * 0.85],
           fill=ink, width=3)
    for cx, cy in [(0.15, 0.15), (0.85, 0.15), (0.15, 0.85), (0.85, 0.85)]:
        d.ellipse([x + s * (cx - 0.10), y + s * (cy - 0.10),
                   x + s * (cx + 0.10), y + s * (cy + 0.10)],
                  outline=red, width=2)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
                fill=ink)


def icon_scales(d, x, y, s, ink, red):
    d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.85],
           fill=ink, width=3)
    d.line([x + s * 0.12, y + s * 0.28, x + s * 0.88, y + s * 0.28],
           fill=ink, width=3)
    for cx in (0.12, 0.88):
        d.line([x + s * cx, y + s * 0.28, x + s * (cx - 0.14), y + s * 0.55],
               fill=ink, width=2)
        d.line([x + s * cx, y + s * 0.28, x + s * (cx + 0.14), y + s * 0.55],
               fill=ink, width=2)
        d.arc([x + s * (cx - 0.14), y + s * 0.42, x + s * (cx + 0.14),
               y + s * 0.72], 0, 180, fill=red, width=2)
    d.line([x + s * 0.32, y + s * 0.92, x + s * 0.68, y + s * 0.92],
           fill=ink, width=3)


def icon_shield(d, x, y, s, ink, red):
    d.polygon([(x + s * 0.08, y + s * 0.10), (x + s * 0.92, y + s * 0.10),
               (x + s * 0.92, y + s * 0.55), (x + s * 0.5, y + s * 0.95),
               (x + s * 0.08, y + s * 0.55)], outline=ink, width=3)
    d.line([x + s * 0.30, y + s * 0.50, x + s * 0.46, y + s * 0.68,
            x + s * 0.74, y + s * 0.32], fill=red, width=3)


def icon_case(d, x, y, s, ink, red):
    d.rectangle([x + s * 0.06, y + s * 0.32, x + s * 0.94, y + s * 0.92],
                outline=ink, width=3)
    d.arc([x + s * 0.34, y + s * 0.08, x + s * 0.66, y + s * 0.40],
          180, 360, fill=ink, width=3)
    d.line([x + s * 0.06, y + s * 0.58, x + s * 0.94, y + s * 0.58],
           fill=red, width=2)
    d.rectangle([x + s * 0.44, y + s * 0.52, x + s * 0.56, y + s * 0.66],
                fill=red)


def icon_debate(d, x, y, s, ink, red):
    r = 4
    d.rounded_rectangle([x, y + s * 0.08, x + s * 0.58, y + s * 0.58],
                        radius=r, outline=ink, width=2)
    d.polygon([(x + s * 0.12, y + s * 0.58), (x + s * 0.22, y + s * 0.78),
               (x + s * 0.28, y + s * 0.58)], fill=ink)
    d.rounded_rectangle([x + s * 0.38, y + s * 0.42, x + s, y + s * 0.92],
                        radius=r, outline=red, width=2)
    d.polygon([(x + s * 0.80, y + s * 0.92), (x + s * 0.72, y + s * 0.78),
               (x + s * 0.88, y + s * 0.92)], fill=red)


def icon_robot(d, x, y, s, ink, red):
    d.line([x + s * 0.5, y, x + s * 0.5, y + s * 0.16], fill=ink, width=2)
    d.ellipse([x + s * 0.44, y - s * 0.02, x + s * 0.56, y + s * 0.10],
              fill=red)
    d.rounded_rectangle([x + s * 0.08, y + s * 0.16, x + s * 0.92,
                         y + s * 0.92], radius=8, outline=ink, width=3)
    d.ellipse([x + s * 0.26, y + s * 0.38, x + s * 0.38, y + s * 0.50],
              fill=ink)
    d.ellipse([x + s * 0.62, y + s * 0.38, x + s * 0.74, y + s * 0.50],
              fill=ink)
    d.line([x + s * 0.34, y + s * 0.70, x + s * 0.66, y + s * 0.70],
           fill=red, width=3)


ICONS = {
    "chart": icon_chart, "burst": icon_burst, "planet": icon_planet,
    "ship": icon_ship, "drone": icon_drone, "scales": icon_scales,
    "shield": icon_shield, "case": icon_case, "debate": icon_debate,
    "robot": icon_robot,
}


# Small display nudges (pixels) for pins that would otherwise sit on top
# of each other: the four US east-coast stories and the London/Liverpool
# pair share nearly the same coordinates, so they are spread into a
# readable cluster instead of one unreadable blob.
PIN_OFFSETS = {
    1: (-12, -11), 6: (12, -11), 7: (-12, 11), 11: (12, 11),
    9: (-11, -8), 10: (9, -8), 12: (9, 9),
}


def number_badge(d, cx, cy, r, n, fnt):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    label = str(n)
    w = d.textlength(label, font=fnt)
    d.text((cx - w / 2, cy - r + 2), label, font=fnt, fill=(255, 255, 255))


# ------------------------------------------------------------------ draw ---

def draw_map(d, box):
    """Dot-matrix world map with numbered pins for stories 1-14."""
    x0, y0, x1, y1 = box
    mw, mh = x1 - x0, y1 - y0
    cw, ch = mw / 72.0, mh / 27.0
    for row, ranges in enumerate(LAND_ROWS):
        cy = y0 + (row + 0.5) * ch
        for a, b in ranges:
            for col in range(a, b + 1):
                cx = x0 + (col + 0.5) * cw
                d.ellipse([cx - 1.2, cy - 1.2, cx + 1.2, cy + 1.2], fill=DOT)
    pin_fnt = font(SANS_B, 9)
    for s in LEADS + PANELS:
        px = x0 + (s["lon"] + 180.0) / 360.0 * mw
        py = y0 + (75.0 - s["lat"]) / 135.0 * mh
        ox, oy = PIN_OFFSETS.get(s["n"], (0, 0))
        px, py = px + ox, py + oy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(s["n"])
        w = d.textlength(label, font=pin_fnt)
        d.text((px - w / 2, py - 6.5), label, font=pin_fnt,
               fill=(255, 255, 255))


def render(path):
    tally = validate()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 22
    CW = W - 2 * M

    # --- masthead ------------------------------------------------------
    eb = font(SANS_B, 14)
    w = d.textlength(EYEBROW, font=eb)
    d.text(((W - w) / 2, 12), EYEBROW, font=eb, fill=INK)
    mast = fit_single(d, DAY_LINE, SERIF_B, 64, CW - 20, min_size=40)
    w = d.textlength(DAY_LINE, font=mast)
    d.text(((W - w) / 2, 30), DAY_LINE, font=mast, fill=INK)
    d.rectangle([M, 106, W - M, 110], fill=RED)
    d.rectangle([M, 113, W - M, 114], fill=RULE)

    # --- day in numbers -------------------------------------------------
    y = 122
    col_w = CW / 6.0
    for i, (num, cap) in enumerate(FIGURES):
        cx = M + i * col_w
        nf = fit_single(d, num, SERIF_B, 30, col_w - 14, min_size=18)
        d.text((cx + 6, y), num, font=nf, fill=RED)
        cf, lines = fit_block(d, cap, SANS_R, 9, col_w - 12, 2, min_size=8)
        for j, line in enumerate(lines):
            d.text((cx + 6, y + 30 + j * 11), line, font=cf, fill=INK)
        if i:
            d.line([cx, y + 2, cx, y + 48], fill=(200, 192, 172), width=1)

    # --- leads -----------------------------------------------------------
    ly, lh = 182, 210
    lw = (CW - 3 * 9) / 4.0
    for i, s in enumerate(LEADS):
        x = M + i * (lw + 9)
        d.rectangle([x, ly, x + lw, ly + lh], fill=CARD, outline=RULE, width=2)
        # badge, icon, big number
        number_badge(d, x + 16, ly + 16, 11, s["n"], font(SANS_B, 11))
        ICONS[s["icon"]](d, x + 34, ly + 8, 46, INK, RED)
        bf = fit_single(d, s["bignum"], SERIF_B, 30, lw - 96, min_size=16)
        bw = d.textlength(s["bignum"], font=bf)
        d.text((x + lw - bw - 8, ly + 12), s["bignum"], font=bf, fill=RED)
        # kicker
        d.text((x + 10, ly + 66), "%s \u2014 %s" % (s["place"], s["kicker"]),
               font=font(SANS_B, 10), fill=RED)
        # headline
        hf, hlines = fit_block(d, s["headline"], SERIF_B, 19, lw - 20, 3,
                               min_size=14)
        for j, line in enumerate(hlines):
            d.text((x + 10, ly + 84 + j * 22), line, font=hf, fill=INK)
        # summary (starts just below however many headline lines there are)
        sf, slines = fit_block(d, s["summary"], SANS_R, 12, lw - 20, 3,
                               min_size=10)
        sy = ly + 84 + len(hlines) * 22 + 4
        for j, line in enumerate(slines):
            d.text((x + 10, sy + j * 14), line, font=sf, fill=INK)
        # source tag
        d.text((x + 10, ly + lh - 12), s["tag"], font=font(SANS_R, 9),
               fill=GREY)

    # --- map + region tally ----------------------------------------------
    my, mh = 400, 104
    d.rectangle([M, my, M + 700, my + mh], fill=PANEL_BG, outline=RULE,
                width=1)
    d.text((M + 10, my + 6), "WHERE IT HAPPENED \u2014 NUMBERED PINS MATCH THE STORIES",
           font=font(SANS_B, 11), fill=INK)
    draw_map(d, (M + 8, my + 24, M + 692, my + mh - 6))
    tx = M + 710
    d.rectangle([tx, my, W - M, my + mh], fill=PANEL_BG, outline=RULE,
                width=1)
    d.text((tx + 10, my + 6), "STORIES BY REGION", font=font(SANS_B, 11),
           fill=INK)
    rf = font(SANS_R, 11)
    for j, (name, count) in enumerate(REGIONS):
        yy = my + 22 + j * 11
        d.text((tx + 10, yy), name, font=rf, fill=INK)
        cw_ = d.textlength(str(count), font=rf)
        d.text((W - M - cw_ - 10, yy), str(count), font=rf, fill=RED)
    ty = my + 22 + 6 * 11 + 2
    d.text((tx + 10, ty), "TOTAL 38 STORIES", font=font(SANS_B, 10), fill=INK)

    # --- panels ------------------------------------------------------------
    py, ph = 512, 92
    pw = (CW - 4 * 10) / 5.0
    for i, s in enumerate(PANELS):
        row, col = divmod(i, 5)
        x = M + col * (pw + 10)
        y = py + row * (ph + 8)
        d.rectangle([x, y, x + pw, y + ph], fill=PANEL_BG, outline=RULE,
                    width=1)
        ICONS[s["icon"]](d, x + 8, y + 7, 24, INK, RED)
        bf = fit_single(d, s["bignum"], SERIF_B, 22, pw - 44, min_size=13)
        bw = d.textlength(s["bignum"], font=bf)
        d.text((x + pw - bw - 7, y + 6), s["bignum"], font=bf, fill=RED)
        hf, hlines = fit_block(d, s["headline"], SANS_B, 12, pw - 14, 3,
                               min_size=10)
        for j, line in enumerate(hlines):
            d.text((x + 7, y + 36 + j * 14), line, font=hf, fill=INK)
        d.text((x + 7, y + ph - 14), s["tag"], font=font(SANS_R, 8),
               fill=GREY)
        number_badge(d, x + pw - 12, y + ph - 12, 9, s["n"],
                     font(SANS_B, 9))

    # --- briefs --------------------------------------------------------------
    by = 712
    d.line([M, by, W - M, by], fill=RULE, width=2)
    d.text((M, by + 6), "ALSO ON TUESDAY \u2014 24 MORE STORIES IN BRIEF",
           font=font(SANS_B, 13), fill=RED)
    col_w = (CW - 20) / 2.0
    for i, (n, city, line) in enumerate(BRIEFS):
        col, row = divmod(i, 12)
        x = M + col * (col_w + 20)
        yy = by + 28 + row * 18
        text = "%d. %s \u2014 %s" % (n, city, line)
        fnt = fit_single(d, text, SANS_R, 12, col_w, min_size=10)
        d.text((x, yy), text, font=fnt, fill=INK)

    # --- date-check footer ----------------------------------------------------
    fy = by + 28 + 12 * 18 + 8
    df, dlines = fit_block(d, DATECHECK, SANS_R, 11, CW - 20, 3, min_size=9)
    fh = 10 + len(dlines) * 14
    d.rectangle([M, fy, W - M, fy + fh], outline=RULE, width=1)
    for j, line in enumerate(dlines):
        d.text((M + 10, fy + 5 + j * 14), line, font=df, fill=INK)
    assert fy + fh <= H - 8, "page overflows: footer ends at %d" % (fy + fh)

    img.save(path, "PNG", optimize=True)
    size = os.path.getsize(path)
    assert size <= 1048576, "entry.png too big: %d bytes" % size
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))
    print("regions: %s" % (tally,))
    return size


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render(out)
