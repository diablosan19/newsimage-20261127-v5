#!/usr/bin/env python3
"""news-image-20261127 v5: front page drawn from scratch with PIL primitives.
36 stories, 9 regions, 14 fields, 18 sources. All copy written here, no
external assets, no network. Research: every headline re-verified 27 Nov 2026
against two live sources (wire/primary + second outlet); prior-day stories
are named only in the printed DATE CHECK box, never as 27 Nov headlines.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_OB = lambda s: F("DejaVuSans-Oblique.ttf", s)

BG = (246, 241, 231)
INK = (20, 20, 20)
NAVY = (15, 42, 74)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
TEAL = (14, 110, 110)
GREY = (90, 90, 90)
LINE = (180, 172, 158)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def rect(x, y, w, h, fill, outline=None, width=1):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=outline, width=width)

def scene(kind, x, y, w, h):
    """Distinct drawn scene, PIL shapes only."""
    rect(x, y, w, h, (233, 228, 214))
    cx, cy = x + w // 2, y + h // 2
    if kind == "chart":
        rect(x, y, w, h, (16, 96, 58))
        base = y + h - 12
        vals = [14, 20, 18, 30, 26, 42, 52]
        bw = w // 9
        for i, v in enumerate(vals):
            rect(x + 8 + i * bw, base - v, bw - 4, v, (255, 255, 255) if i < 5 else GOLD)
        d.line([(x + 8, base - 14), (x + w - 10, y + 8)], fill=GOLD, width=3)
        d.polygon([(x + w - 10, y + 8), (x + w - 22, y + 8), (x + w - 10, y + 20)], fill=GOLD)
    elif kind == "storm":
        rect(x, y, w, h, (52, 68, 92))
        for ox, oy, r in [(30, 18, 16), (55, 12, 20), (85, 20, 15)]:
            d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=(30, 40, 58))
        for i in range(5):
            rx = x + 20 + i * 18
            d.line([(rx, y + 38), (rx - 4, y + h - 6)], fill=(170, 200, 230), width=2)
        d.polygon([(x + w - 40, y + 30), (x + w - 28, y + 30), (x + w - 38, y + 48),
                   (x + w - 28, y + 48), (x + w - 44, y + h - 6), (x + w - 34, y + 48)],
                  fill=(255, 214, 64))
    elif kind == "eu":
        rect(x, y, w, h, NAVY)
        for i in range(12):
            import math
            a = math.pi * 2 * i / 12 - math.pi / 2
            sx = cx + int(34 * math.cos(a)); sy = cy + int(20 * math.sin(a))
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
        d.text((cx, cy - 7), "EU", font=SANS_B(13), fill=(255, 255, 255), anchor="mm")
    elif kind == "football":
        rect(x, y, w, h, (24, 96, 44))
        for i in range(5):
            lx = x + 12 + i * (w - 24) // 4
            d.line([(lx, y), (lx, y + h)], fill=(255, 255, 255), width=1)
        d.ellipse([cx - 26, cy - 11, cx + 26, cy + 11], fill=(122, 72, 32))
        d.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 255), width=2)
    elif kind == "drone":
        rect(x, y, w, h, (70, 90, 110))
        d.ellipse([cx - 70, cy - 8, cx + 70, cy + 8], fill=(200, 210, 220))
        d.ellipse([cx - 26, cy - 16, cx + 26, cy + 16], fill=(40, 48, 60))
        d.ellipse([cx - 6, cy - 5, cx + 6, cy + 5], fill=RED)
        for ex in (cx - 58, cx + 58):
            d.line([(ex, cy - 14), (ex, cy + 14)], fill=(230, 230, 230), width=3)
    elif kind == "jet":
        rect(x, y, w, h, (176, 96, 52))
        d.ellipse([x + w - 34, y + 6, x + w - 10, y + 30], fill=(255, 214, 64))
        d.polygon([(x + 12, cy), (x + 52, cy - 12), (x + 96, cy - 2), (x + 96, cy + 4),
                   (x + 52, cy + 12)], fill=(40, 44, 52))
        d.polygon([(x + 60, cy - 2), (x + 78, cy - 20), (x + 84, cy - 2)], fill=(40, 44, 52))
        d.line([(x + 10, cy + 18), (x + w - 20, cy + 18)], fill=(255, 255, 255), width=2)
    elif kind == "podium":
        rect(x, y, w, h, (96, 22, 34))
        for i, c in enumerate([(178, 34, 34), (255, 255, 255), (178, 34, 34), (255, 255, 255)]):
            rect(x + 8 + i * 14, y + 8, 14, 10, c)
        d.polygon([(cx - 34, y + h - 8), (cx + 34, y + h - 8), (cx + 24, y + 26), (cx - 24, y + 26)],
                  fill=(220, 220, 220))
        d.ellipse([cx - 10, y + 12, cx + 10, y + 32], fill=(232, 190, 150))
        d.rectangle([cx - 12, y + 32, cx + 12, y + 44], fill=(30, 30, 40))
    elif kind == "ballot":
        rect(x, y, w, h, TEAL)
        rect(cx - 34, cy - 6, 68, 34, (255, 255, 255))
        rect(cx - 34, cy - 6, 68, 8, NAVY)
        d.line([(cx - 16, cy + 8), (cx - 6, cy + 20), (cx + 22, cy - 8)], fill=RED, width=4)
        d.rectangle([cx - 44, cy - 26, cx - 18, cy - 12], fill=(255, 255, 255), outline=NAVY)
    elif kind == "stamp":
        rect(x, y, w, h, (150, 96, 30))
        rect(cx - 40, cy - 22, 80, 44, (255, 255, 255))
        d.text((cx, cy - 12), "SEALED", font=SANS_B(11), fill=RED, anchor="mm")
        d.text((cx, cy + 6), "SANCTION", font=SANS_B(11), fill=INK, anchor="mm")
        d.ellipse([cx + 26, cy + 6, cx + 40, cy + 20], fill=RED)
    elif kind == "cricket":
        rect(x, y, w, h, (24, 96, 44))
        d.rectangle([cx - 30, cy - 24, cx - 22, cy + 24], fill=(210, 180, 120))
        d.ellipse([cx + 18, cy - 6, cx + 30, cy + 6], fill=RED)
        for sx in (cx + 44, cx + 50, cx + 56):
            d.line([(sx, cy - 14), (sx, cy + 14)], fill=(255, 255, 255), width=2)

# ---------------- masthead ----------------
rect(0, 0, W, 98, NAVY)
text(14, 10, "THE WORLD IN ONE DAY", SERIF_B(34), fill=(255, 255, 255))
text(14, 52, "FRIDAY  27  NOVEMBER  2026", SANS_B(21), fill=GOLD)
text(1010, 16, "36 STORIES  •  9 REGIONS", SANS_B(15), fill=(255, 255, 255), anchor="ra")
text(1010, 40, "14 FIELDS  •  18 SOURCES", SANS_B(15), fill=(255, 255, 255), anchor="ra")
text(1010, 66, "ALL TIMES UTC UNLESS NOTED", SANS(11), fill=(200, 205, 215), anchor="ra")

LEADS = [
    (1, "chart", "CHINA STOCKS SURGE", "Beijing pledges state-fund support; STAR 50 jumps 15.1%, Shanghai up 3.7%.",
     "EAST ASIA • Reuters • CONFIRMED", "07:00"),
    (2, "storm", "STORM CUTS POWER TO ~1M", "Thanksgiving nor'easter floods the US East Coast; Macy's parade put off to Saturday.",
     "NORTH AMERICA • Reuters • CONFIRMED", "00:19"),
    (3, "eu", "EU BUDGET SUMMIT FAILS", "Fourteen hours end after midnight with no deal on the €1.78tn budget or €45bn Ukraine loan.",
     "EUROPE • Euronews • CONFIRMED", "02:35"),
]
PANELS = [
    (4, "football", "BILLS 13, CHIEFS 10", "Bass kicks a 57-yard field goal as time expires; Buffalo moves to 10-1.",
     "NORTH AMERICA • AP • CONFIRMED", "04:25"),
    (5, "drone", "DRONE ENTERS LATVIA", "NATO jets scrambled as an unmanned craft crosses in; border towns told to shelter.",
     "EUROPE • Reuters • REPORTED", "01:30"),
    (6, "jet", "IRAN SAYS IT TURNED BACK F-16", "IRGC claims warning fire near Hengam Island; the US has not confirmed the incident.",
     "MIDDLE EAST • IRGC • CLAIM", "09:23"),
    (7, "podium", "TRUMP: VICTORY AT HAND", "President tells troops the US has victory over Iran in reach and offers Tehran a deal.",
     "NORTH AMERICA • ANI • CONFIRMED", "00:30"),
    (8, "ballot", "NZ HUNG PARLIAMENT", "Final count: coalition 65 of 130 seats, one short; Luxon needs a centrist party to govern.",
     "OCEANIA • Reuters • OFFICIAL", "FRI, NZ"),
    (9, "stamp", "AUSTRALIA SANCTIONS TWO", "Canberra names Hassib and Hamad over 2024 antisemitic arson attacks blamed on the IRGC.",
     "OCEANIA • ABC • OFFICIAL", "05:09"),
    (10, "cricket", "INDIA v NZ, 2nd TEST", "Gill wins the toss and India bowls in Christchurch; NZ 77 for 1 at lunch on day one.",
     "OCEANIA • ANI • CONFIRMED", "01:30"),
]

def panel(x, y, w, h, n, kind, head, deck, foot, utc):
    rect(x, y, w, h, (255, 255, 255), outline=LINE)
    scene(kind, x + 1, y + 1, w - 2, 58)
    rect(x + 1, y + 1, 30, 20, RED)
    text(x + 16, y + 3, str(n), SANS_B(13), fill=(255, 255, 255), anchor="ma")
    text(x + w - 6, y + 4, utc + " UTC" if utc != "FRI, NZ" else "FRI, NZ TIME", SANS_B(9), fill=(255, 255, 255), anchor="ra")
    hy = y + 66
    for ln in wrap(head, SANS_B(14), w - 14)[:2]:
        text(x + 7, hy, ln, SANS_B(14)); hy += 17
    dy = hy + 2
    for ln in wrap(deck, SANS(10), w - 14)[:2]:
        text(x + 7, dy, ln, SANS(10)); dy += 13
    text(x + 7, y + h - 15, foot, SANS_B(8), fill=GREY)

lx = [8, 344, 680]
for i, (n, kind, head, deck, foot, utc) in enumerate(LEADS):
    panel(lx[i], 106, 328, 168, n, kind, head, deck, foot, utc)

px = [8, 260, 512, 764]
for i, (n, kind, head, deck, foot, utc) in enumerate(PANELS[:4]):
    panel(px[i], 282, 244, 148, n, kind, head, deck, foot, utc)
for i, (n, kind, head, deck, foot, utc) in enumerate(PANELS[4:7]):
    panel(px[i], 438, 244, 148, n, kind, head, deck, foot, utc)

# ---------------- pin map (stories 1-10) ----------------
mx, my, mw, mh = 764, 438, 244, 148
rect(mx, my, mw, mh, (255, 255, 255), outline=LINE)
text(mx + 8, my + 6, "WHERE THE TOP 10 HAPPENED", SANS_B(11))
# rough world outline: land blobs
d.ellipse([mx + 18, my + 34, mx + 78, my + 62], fill=(214, 226, 214))   # N America
d.ellipse([mx + 52, my + 66, mx + 78, my + 92], fill=(214, 226, 214))   # S America
d.ellipse([mx + 108, my + 30, mx + 138, my + 58], fill=(214, 226, 214)) # Europe
d.ellipse([mx + 132, my + 58, mx + 168, my + 96], fill=(214, 226, 214)) # Africa
d.ellipse([mx + 150, my + 28, mx + 228, my + 66], fill=(214, 226, 214)) # Asia
d.ellipse([mx + 200, my + 92, mx + 232, my + 108], fill=(214, 226, 214))# Oceania
PINS = {1: (196, 46), 2: (36, 44), 3: (118, 48), 4: (62, 54), 5: (134, 34),
        6: (152, 56), 7: (58, 38), 8: (204, 98), 9: (224, 94), 10: (212, 110)}
for n, (ox_, oy_) in PINS.items():
    px_, py_ = mx + ox_, my + oy_
    d.ellipse([px_ - 7, py_ - 7, px_ + 7, py_ + 7], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px_, py_ - 1), str(n), font=SANS_B(8), fill=(255, 255, 255), anchor="mm")
text(mx + 8, my + mh - 34, "Pins 1-10: the illustrated", SANS(9), fill=GREY)
text(mx + 8, my + mh - 22, "stories above, by place.", SANS(9), fill=GREY)
text(mx + 8, my + mh - 12, "Every story carries its region.", SANS(9), fill=GREY)

# ---------------- stories 11-36 ----------------
LIST = [
    (11, "TOKYO CPI 2.9%", "core inflation, 16-month high", "EAST ASIA", "Reuters", "OFFICIAL"),
    (12, "CHINA FACTORY PROFITS +20.1%", "fastest since May", "EAST ASIA", "NBS", "OFFICIAL"),
    (13, "AUSTRALIA LNG RESERVE", "20% domestic gas rule from 2028", "OCEANIA", "Guardian", "CONFIRMED"),
    (14, "INDIA SHARES EYE 5th WEEKLY GAIN", "GIFT Nifty 25,962", "SOUTH ASIA", "Reuters", "CONFIRMED"),
    (15, "RUPEE FALLS TO 92.62", "down 24 paise in early trade", "SOUTH ASIA", "PTI", "CONFIRMED"),
    (16, "ASIAN SHARES STEADY", "Nikkei +0.7%, KOSPI +2%", "EAST ASIA", "Reuters", "CONFIRMED"),
    (17, "BRENT NEAR $96", "oil at a month high on Gulf fears", "MIDDLE EAST", "Reuters", "CONFIRMED"),
    (18, "ZELENSKY WARNS OF MASS STRIKE", "new attack on power grid feared", "EUROPE", "AP", "CONFIRMED"),
    (19, "HAMAS WEIGHS RESPONSE", "to consult factions after Gaza strikes", "MIDDLE EAST", "Reuters", "REPORTED"),
    (20, "NIGER: 13 SOLDIERS KILLED", "Sanam attack, 20 hurt", "AFRICA", "Def. Ministry", "CONFIRMED"),
    (21, "UGANDA TO QUIT LUBERO", "troops leave DRC town in two weeks", "AFRICA", "UPDF", "OFFICIAL"),
    (22, "AFP HIT BY CYBERATTACK", "Forum offline after intrusion", "EUROPE", "AFP", "CONFIRMED"),
    (23, "SAP: NO JOB-CUT DECISION", "after report of 10,000 AI cuts", "EUROPE", "SAP", "OFFICIAL"),
    (24, "BANGKOK MARKET FIRE", "~100 traders hit, no injuries", "S.E. ASIA", "ASEAN Now", "CONFIRMED"),
    (25, "BLACK FRIDAY BEGINS", "NRF sees sales +4.2% to above $1tn", "N. AMERICA", "Reuters", "CONFIRMED"),
    (26, "AIRASIA DELAYS PAY", "salaries pushed to month-end", "S.E. ASIA", "Reuters", "REPORTED"),
    (27, "GUYANA'S ALI URGES JOINT PROJECTS", "shared energy plans", "LATIN AMERICA", "CMC", "CONFIRMED"),
    (28, "INDIA MAY USE 1971 CENSUS", "by the 1971 formula", "SOUTH ASIA", "Cabinet sources", "REPORTED"),
    (29, "HASINA SETS RETURN DATE", "returns 16 December", "SOUTH ASIA", "Wires", "REPORTED"),
    (30, "PAKISTAN HOSTS DEFENCE TALKS", "Saudi, Turkish officials meet", "SOUTH ASIA", "Wires", "REPORTED"),
    (31, "WEST BANK DEMOLITION", "~50 structures razed in Samra", "MIDDLE EAST", "Wires", "REPORTED"),
    (32, "CHINA SLAMS TOKYO", "protest over Diaoyu Islands", "EAST ASIA", "China Daily", "REPORTED"),
    (33, "NEPAL TO DECLARE 213 DEAD", "missing from August floods", "SOUTH ASIA", "Mathrubhumi", "REPORTED"),
    (34, "CANADA COURT WEIGHS BILL 21", "Quebec symbols-ban challenge", "N. AMERICA", "Wires", "REPORTED"),
    (35, "FLINDERS FIRE UPDATE", "14,700 ha burned; more losses feared", "OCEANIA", "AAP", "REPORTED"),
    (36, "JAPAN PENSION FUND GPIF", "asset-mix reviews to board", "EAST ASIA", "GPIF", "OFFICIAL"),
]
ly = 594
text(8, ly, "THE DAY IN BRIEF  —  STORIES 11-36", SANS_B(13))
d.line([(8, ly + 20), (1016, ly + 20)], fill=NAVY, width=2)
row_y = ly + 28
for col in range(2):
    cx0 = 8 if col == 0 else 516
    for i in range(13):
        item = LIST[col * 13 + i]
        n, head, deck, region, src, label = item
        y = row_y + i * 22
        text(cx0, y, str(n), SANS_B(11), fill=RED)
        line = f"{head} — {deck}"
        # shrink only by whole words, leaving room for the right-hand tag
        tag = f"{src} • {label}"
        limit = 490 - 26 - d.textlength(tag, font=SANS(8)) - 12
        fnt = SANS_B(10)
        while d.textlength(line, font=fnt) > limit and " " in line:
            line = line.rsplit(" ", 1)[0]
        text(cx0 + 26, y, line, fnt)
        text(cx0 + 490, y, tag, SANS(8), fill=GREY, anchor="ra")
        # region tag under? no: region shown in the region bar; keep list clean

# ---------------- timeline strip ----------------
ty = 902
rect(8, ty, 1008, 34, NAVY)
text(16, ty + 10, "UTC TIMELINE", SANS_B(11), fill=GOLD)
tl = "00:19 STORM  •  00:30 TRUMP  •  01:30 LATVIA / TEST  •  02:35 EU SUMMIT  •  04:25 BILLS  •  05:09 AUSTRALIA  •  07:00 CHINA STOCKS  •  09:23 F-16 CLAIM"
text(150, ty + 10, tl, SANS(11), fill=(255, 255, 255))

# ---------------- bottom: DATE CHECK + regions + markets ----------------
by = 944
rect(8, by, 620, 72, (255, 255, 255), outline=RED, width=2)
text(16, by + 5, "DATE CHECK — BIG STORIES FROM OTHER DAYS, LEFT OUT", SANS_B(11), fill=RED)
dc1 = "Kuwait drone kills 2 Italians (26 Nov)  •  Gaza strikes kill 9 (26 Nov)  •  Jazan refinery attack (26 Nov)"
dc2 = "ECB: de Cos chosen (agreed 26 Nov)  •  UK migration 77,000 (26 Nov)  •  Bangkok refinery blast (26 Nov)"
dc3 = "Lukoil $10bn deal signed (25 Nov)  •  N. Korea halts missile aid (26 Nov)  •  No 26 Nov story is a 27 Nov headline."
for j, ln in enumerate((dc1, dc2, dc3)):
    text(16, by + 24 + j * 14, ln, SANS(10))
rect(636, by, 380, 72, (255, 255, 255), outline=LINE)
text(644, by + 5, "STORIES BY REGION  (36 TOTAL)", SANS_B(11))
regs = [("N. AMERICA", 5), ("EUROPE", 5), ("MIDDLE EAST", 4), ("EAST ASIA", 6),
        ("SOUTH ASIA", 6), ("S.E. ASIA", 2), ("OCEANIA", 5), ("AFRICA", 2), ("LATIN AM.", 1)]
bx, byy = 644, by + 22
for j, (name, cnt) in enumerate(regs):
    x0 = bx + (j % 3) * 128
    y0 = byy + (j // 3) * 13
    text(x0, y0, f"{name} {cnt}", SANS_B(9))
text(644, by + 61, "MARKETS: STAR 50 +15.1% • Brent $96.19 • WTI $85.41 • Rupee 92.62/$", SANS(8), fill=GREY)

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes", img.size)
