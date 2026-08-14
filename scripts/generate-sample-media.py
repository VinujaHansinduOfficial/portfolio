#!/usr/bin/env python
"""
Generate sample project media into public/projects/<id>/.

These are mock UI screenshots — placeholders that look like the real thing so the
portfolio reads properly before the actual captures exist. Replace them file by
file as you collect real screenshots; the filenames are what Portfolio.jsx points at.

    python scripts/generate-sample-media.py

Needs Pillow (stills) and OpenCV (the one .mp4 clip).
"""

import colorsys
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "projects")

W, H = 1600, 900
BG = (2, 6, 23)
PANEL = (15, 23, 42)
CARD = (19, 29, 51)
LINE = (35, 47, 69)
TEXT = (226, 232, 240)
MUTED = (148, 163, 184)
WHITE = (255, 255, 255)

FONTS = {
    "r": "C:/Windows/Fonts/segoeui.ttf",
    "b": "C:/Windows/Fonts/segoeuib.ttf",
    "m": "C:/Windows/Fonts/consola.ttf",
}
_fcache = {}


def F(size, w="r"):
    key = (size, w)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(FONTS[w], size)
    return _fcache[key]


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def accent_of(hue):
    return hsl(hue, 0.75, 0.60)


def txt(d, xy, s, size=20, w="r", fill=TEXT, anchor="la"):
    d.text(xy, s, font=F(size, w), fill=fill, anchor=anchor)


def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def pill(d, x, y, label, color, size=15, pad=12, h=26):
    tw = d.textlength(label, font=F(size, "b"))
    rr(d, (x, y, x + tw + pad * 2, y + h), h // 2, fill=color[:3] + (40,), outline=color[:3] + (150,))
    txt(d, (x + pad, y + h / 2), label, size, "b", color, anchor="lm")
    return tw + pad * 2


def star(d, cx, cy, r, color):
    """Five-pointed star — Segoe UI has no ★ glyph, so draw it."""
    pts = []
    for k in range(10):
        ang = math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.44
        pts.append((cx + math.cos(ang) * rad, cy - math.sin(ang) * rad))
    d.polygon(pts, fill=color)


def padlock(d, cx, cy, h, color):
    w = h * 0.78
    d.rounded_rectangle((cx - w / 2, cy - h * 0.08, cx + w / 2, cy + h * 0.5), h * 0.16, fill=color)
    d.arc((cx - w * 0.32, cy - h * 0.60, cx + w * 0.32, cy + h * 0.10), 180, 360,
          fill=color, width=max(int(h * 0.14), 3))


def canvas(hue, glow=True):
    """Site-matching backdrop: near-black slate, faint grid, one soft accent glow."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im, "RGBA")
    for x in range(0, W, 44):
        d.line([(x, 0), (x, H)], fill=(148, 163, 184, 14))
    for y in range(0, H, 44):
        d.line([(0, y), (W, y)], fill=(148, 163, 184, 14))
    if glow:
        g = Image.new("RGB", (W, H), BG)
        gd = ImageDraw.Draw(g)
        gd.ellipse((-200, 250, 620, 1000), fill=hsl(hue, 0.8, 0.22))
        gd.ellipse((1100, -260, 1900, 420), fill=hsl(hue + 40, 0.7, 0.16))
        im = Image.blend(im, g.filter(ImageFilter.GaussianBlur(150)), 0.55)
    return im


# ----------------------------------------------------------------------------
# frames
# ----------------------------------------------------------------------------

def browser(im, url, box=(70, 60, 1530, 840)):
    """Draw a browser window; return the inner content box."""
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 + 6, y0 + 12, x1 + 6, y1 + 14), 18, fill=(0, 0, 0, 120))
    rr(d, box, 16, fill=PANEL, outline=LINE, width=2)
    bar = y0 + 52
    rr(d, (x0, y0, x1, bar + 16), 16, fill=(13, 20, 38))
    d.rectangle((x0, bar, x1, bar + 16), fill=(13, 20, 38))
    d.line([(x0, bar), (x1, bar)], fill=LINE)
    for i, c in enumerate(((244, 107, 94), (247, 191, 79), (98, 198, 108))):
        cx = x0 + 26 + i * 22
        d.ellipse((cx - 6, y0 + 20, cx + 6, y0 + 32), fill=c)
    rr(d, (x0 + 110, y0 + 14, x0 + 620, y0 + 38), 12, fill=(2, 6, 23), outline=LINE)
    txt(d, (x0 + 126, y0 + 26), url, 15, "r", MUTED, anchor="lm")
    return (x0, bar + 1, x1, y1)


def phone(im, cx, cy, pw=372, ph=744, time="9:41"):
    """Draw a phone body centred at (cx, cy); return the inner screen box."""
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = cx - pw // 2, cy - ph // 2, cx + pw // 2, cy + ph // 2
    d.rounded_rectangle((x0 + 8, y0 + 16, x1 + 8, y1 + 18), 48, fill=(0, 0, 0, 130))
    rr(d, (x0, y0, x1, y1), 46, fill=(8, 12, 26), outline=(51, 65, 85), width=3)
    s = (x0 + 11, y0 + 11, x1 - 11, y1 - 11)
    rr(d, s, 38, fill=PANEL)
    rr(d, (cx - 52, y0 + 20, cx + 52, y0 + 40), 10, fill=(4, 8, 20))
    txt(d, (s[0] + 22, y0 + 30), time, 14, "b", TEXT, anchor="lm")
    for i, w_ in enumerate((5, 7, 9)):
        d.rectangle((s[2] - 74 + i * 8, y0 + 34 - w_, s[2] - 69 + i * 8, y0 + 34), fill=MUTED)
    rr(d, (s[2] - 44, y0 + 24, s[2] - 22, y0 + 35), 3, fill=MUTED)
    return (s[0], y0 + 48, s[2], s[3])


# ----------------------------------------------------------------------------
# widgets
# ----------------------------------------------------------------------------

def sidebar(im, box, accent, brand, items, active=0, w=228):
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    d.rectangle((x0, y0, x0 + w, y1), fill=(11, 17, 33))
    d.line([(x0 + w, y0), (x0 + w, y1)], fill=LINE)
    rr(d, (x0 + 22, y0 + 26, x0 + 54, y0 + 58), 10, fill=accent)
    txt(d, (x0 + 66, y0 + 42), brand, 17, "b", WHITE, anchor="lm")
    for i, it in enumerate(items):
        yy = y0 + 96 + i * 46
        if i == active:
            rr(d, (x0 + 14, yy - 4, x0 + w - 14, yy + 34), 10, fill=accent[:3] + (38,))
            d.rectangle((x0 + 14, yy - 4, x0 + 18, yy + 34), fill=accent)
        rr(d, (x0 + 32, yy + 7, x0 + 48, yy + 23), 4,
           fill=accent if i == active else (71, 85, 105))
        txt(d, (x0 + 62, yy + 15), it, 15, "b" if i == active else "r",
            WHITE if i == active else MUTED, anchor="lm")
    return (x0 + w + 1, y0, x1, y1)


def topbar(im, box, title, accent, sub=None, h=76):
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    d.rectangle((x0, y0, x1, y0 + h), fill=(13, 20, 38))
    d.line([(x0, y0 + h), (x1, y0 + h)], fill=LINE)
    txt(d, (x0 + 30, y0 + (30 if sub else h / 2)), title, 21, "b", WHITE,
        anchor="lm" if sub else "lm")
    if sub:
        txt(d, (x0 + 30, y0 + 54), sub, 14, "r", MUTED, anchor="lm")
    d.ellipse((x1 - 66, y0 + h / 2 - 19, x1 - 28, y0 + h / 2 + 19), fill=accent[:3] + (60,),
              outline=accent, width=2)
    txt(d, (x1 - 47, y0 + h / 2), "VH", 15, "b", accent, anchor="mm")
    rr(d, (x1 - 250, y0 + h / 2 - 17, x1 - 90, y0 + h / 2 + 17), 17, fill=(2, 6, 23), outline=LINE)
    txt(d, (x1 - 232, y0 + h / 2), "Search…", 14, "r", (100, 116, 139), anchor="lm")
    return (x0, y0 + h + 1, x1, y1)


def stat_cards(im, box, cards, accent, h=104):
    """cards: [(label, value, delta)] — returns the box below the row."""
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, _ = box
    pad, gap = 26, 18
    n = len(cards)
    cw = (x1 - x0 - pad * 2 - gap * (n - 1)) / n
    for i, (label, value, delta) in enumerate(cards):
        cx = x0 + pad + i * (cw + gap)
        rr(d, (cx, y0 + 22, cx + cw, y0 + 22 + h), 14, fill=CARD, outline=LINE)
        txt(d, (cx + 20, y0 + 46), label.upper(), 12, "b", MUTED)
        txt(d, (cx + 20, y0 + 66), value, 30, "b", WHITE)
        if delta:
            up = not delta.startswith("-")
            c = (74, 222, 128) if up else (248, 113, 113)
            txt(d, (cx + cw - 20, y0 + 78), delta, 14, "b", c, anchor="rm")
        rr(d, (cx + cw - 52, y0 + 40, cx + cw - 20, y0 + 62), 8, fill=accent[:3] + (45,))
    return (x0, y0 + 22 + h + 22, x1, box[3])


def panel(im, box, title, accent, note=None):
    d = ImageDraw.Draw(im, "RGBA")
    rr(d, box, 14, fill=CARD, outline=LINE)
    txt(d, (box[0] + 22, box[1] + 30), title, 17, "b", WHITE, anchor="lm")
    if note:
        txt(d, (box[2] - 22, box[1] + 30), note, 14, "r", MUTED, anchor="rm")
    return (box[0] + 22, box[1] + 58, box[2] - 22, box[3] - 22)


def bar_chart(im, box, values, accent, labels=None):
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    y1 -= 26 if labels else 0
    top = max(values) * 1.18
    for i in range(4):
        gy = y1 - (y1 - y0) * i / 3
        d.line([(x0, gy), (x1, gy)], fill=(148, 163, 184, 26))
    n = len(values)
    slot = (x1 - x0) / n
    bw = min(slot * 0.52, 46)
    for i, v in enumerate(values):
        cx = x0 + slot * (i + 0.5)
        bh = (y1 - y0) * (v / top)
        rr(d, (cx - bw / 2, y1 - bh, cx + bw / 2, y1), 6, fill=accent[:3] + (215,))
        rr(d, (cx - bw / 2, y1 - bh, cx + bw / 2, y1 - bh + min(bh, 10)), 5, fill=accent)
        if labels:
            txt(d, (cx, y1 + 16), labels[i], 13, "r", MUTED, anchor="mm")


def line_chart(im, box, series, accent, band=False, dash_from=None, labels=None):
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    y1 -= 26 if labels else 0
    lo, hi = min(series) * 0.82, max(series) * 1.12
    n = len(series)
    pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - (y1 - y0) * (v - lo) / (hi - lo))
           for i, v in enumerate(series)]
    for i in range(4):
        gy = y1 - (y1 - y0) * i / 3
        d.line([(x0, gy), (x1, gy)], fill=(148, 163, 184, 26))
    if band:
        up = [(x, y - 16 - 34 * (i / n)) for i, (x, y) in enumerate(pts)]
        dn = [(x, y + 16 + 34 * (i / n)) for i, (x, y) in enumerate(pts)]
        d.polygon(up + dn[::-1], fill=accent[:3] + (34,))
    fill_poly = pts + [(x1, y1), (x0, y1)]
    d.polygon(fill_poly, fill=accent[:3] + (46,))
    solid = pts if dash_from is None else pts[:dash_from]
    d.line(solid, fill=accent, width=4, joint="curve")
    if dash_from is not None:  # forecast tail, drawn dashed
        tail = pts[dash_from - 1:]
        for i in range(len(tail) - 1):
            (ax, ay), (bx, by) = tail[i], tail[i + 1]
            steps = 7
            for s in range(0, steps, 2):
                d.line([(ax + (bx - ax) * s / steps, ay + (by - ay) * s / steps),
                        (ax + (bx - ax) * (s + 1) / steps, ay + (by - ay) * (s + 1) / steps)],
                       fill=accent, width=4)
    for i, (px, py) in enumerate(pts):
        if i % 2 == 0:
            d.ellipse((px - 5, py - 5, px + 5, py + 5), fill=PANEL, outline=accent, width=3)
    if labels:
        for i, lb in enumerate(labels):
            txt(d, (x0 + (x1 - x0) * i / (len(labels) - 1), y1 + 16), lb, 13, "r", MUTED, anchor="mm")


def donut(im, cx, cy, r, parts, accent):
    d = ImageDraw.Draw(im, "RGBA")
    a = -90
    for frac, col in parts:
        d.pieslice((cx - r, cy - r, cx + r, cy + r), a, a + 360 * frac, fill=col)
        a += 360 * frac
    d.ellipse((cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62), fill=CARD)
    txt(d, (cx, cy - 8), "72%", 26, "b", WHITE, anchor="mm")
    txt(d, (cx, cy + 16), "on time", 13, "r", MUTED, anchor="mm")


def table(im, box, cols, rows, accent, row_h=44):
    """cols: [(label, x_offset)]; cell may be str or ('pill', text, color)."""
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    for label, off in cols:
        txt(d, (x0 + off, y0), label.upper(), 12, "b", (110, 126, 150))
    y = y0 + 26
    d.line([(x0, y), (x1, y)], fill=LINE)
    for r_i, row in enumerate(rows):
        ry = y + 10 + r_i * row_h
        if ry + row_h > y1:  # loudly, so a too-short panel isn't silently truncated
            print("    ! panel too short — %d row(s) skipped" % (len(rows) - r_i))
            break
        if r_i % 2 == 0:
            rr(d, (x0 - 8, ry - 4, x1 + 8, ry + row_h - 10), 8, fill=(255, 255, 255, 7))
        for (label, off), cell in zip(cols, row):
            if isinstance(cell, tuple):
                pill(d, x0 + off, ry + 1, cell[1], cell[2], size=13, pad=10, h=24)
            else:
                bold = off == cols[0][1]
                txt(d, (x0 + off, ry + 13), cell, 15, "b" if bold else "r",
                    TEXT if bold else MUTED, anchor="lm")


def avatar(d, cx, cy, r, initials, accent):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=accent[:3] + (60,), outline=accent, width=2)
    txt(d, (cx, cy), initials, int(r * 0.9), "b", accent, anchor="mm")


def phone_card(d, box, title, sub, accent, r=14):
    rr(d, box, r, fill=CARD, outline=LINE)
    rr(d, (box[0] + 14, box[1] + 14, box[0] + 46, box[1] + 46), 9, fill=accent[:3] + (60,))
    txt(d, (box[0] + 60, box[1] + 24), title, 15, "b", WHITE)
    txt(d, (box[0] + 60, box[1] + 45), sub, 13, "r", MUTED)


def save(im, project, name):
    folder = os.path.join(OUT, project)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    im.convert("RGB").save(path, quality=84, optimize=True)
    print("  %-46s %6.0f KB" % (os.path.relpath(path, ROOT), os.path.getsize(path) / 1024))


# ============================================================================
# 1. mental-health-ai  (hue 265)
# ============================================================================

HUE_MH = 265


def mh_app_home():
    a = accent_of(HUE_MH)
    im = canvas(HUE_MH)
    d = ImageDraw.Draw(im, "RGBA")
    txt(d, (150, 300), "Student app", 40, "b", WHITE)
    txt(d, (150, 356), "Daily check-in, mood tracking and\nguided journalling in one Flutter app.", 20, "r", MUTED)
    for i, t in enumerate(("Check-in", "Journal", "Insights")):
        pill(d, 150 + i * 132, 470, t, a, size=15)
    s = phone(im, 1090, 450)
    d = ImageDraw.Draw(im, "RGBA")
    txt(d, (s[0] + 26, s[1] + 30), "Good evening,", 15, "r", MUTED)
    txt(d, (s[0] + 26, s[1] + 52), "Vinuja", 26, "b", WHITE)
    avatar(d, s[2] - 46, s[1] + 52, 22, "VH", a)
    rr(d, (s[0] + 20, s[1] + 108, s[2] - 20, s[1] + 236), 16, fill=a[:3] + (48,), outline=a)
    txt(d, (s[0] + 40, s[1] + 132), "HOW ARE YOU FEELING?", 12, "b", a)
    for i, (lab, col) in enumerate((("😖", (248, 113, 113)), ("😕", (251, 146, 60)),
                                    ("😐", (250, 204, 21)), ("🙂", (74, 222, 128)),
                                    ("😄", (52, 211, 153)))):
        cx = s[0] + 52 + i * 58
        sel = i == 3
        d.ellipse((cx - 22, s[1] + 164, cx + 22, s[1] + 208),
                  fill=col[:3] + (70 if sel else 26,), outline=col if sel else LINE, width=2)
        txt(d, (cx, s[1] + 186), str(i + 1), 16, "b", col, anchor="mm")
    txt(d, (s[0] + 26, s[1] + 264), "This week", 16, "b", WHITE)
    bar_chart(im, (s[0] + 26, s[1] + 296, s[2] - 26, s[1] + 400), [3, 4, 2, 5, 4, 4, 5], a,
              ["M", "T", "W", "T", "F", "S", "S"])
    d = ImageDraw.Draw(im, "RGBA")
    phone_card(d, (s[0] + 20, s[1] + 430, s[2] - 20, s[1] + 500), "Write today's journal",
               "2 min · analysed privately", a)
    phone_card(d, (s[0] + 20, s[1] + 512, s[2] - 20, s[1] + 582), "Breathing exercise",
               "Recommended for you", a)
    rr(d, (s[0] + 20, s[3] - 76, s[2] - 20, s[3] - 14), 18, fill=(13, 20, 38), outline=LINE)
    for i in range(4):
        cx = s[0] + 60 + i * 78
        rr(d, (cx - 13, s[3] - 56, cx + 13, s[3] - 34), 6, fill=a if i == 0 else (71, 85, 105))
    return im


def mh_journal():
    a = accent_of(HUE_MH)
    im = canvas(HUE_MH + 15)
    d = ImageDraw.Draw(im, "RGBA")
    txt(d, (150, 300), "NLP journal analysis", 40, "b", WHITE)
    txt(d, (150, 356), "Entries are scored for sentiment and\nrecurring themes on the server.", 20, "r", MUTED)
    txt(d, (150, 452), "FastAPI  ·  spaCy  ·  MongoDB", 15, "b", a)
    s = phone(im, 1090, 450)
    d = ImageDraw.Draw(im, "RGBA")
    txt(d, (s[0] + 26, s[1] + 34), "Journal", 24, "b", WHITE)
    txt(d, (s[0] + 26, s[1] + 68), "12 August 2026", 14, "r", MUTED)
    rr(d, (s[0] + 20, s[1] + 100, s[2] - 20, s[1] + 262), 14, fill=CARD, outline=LINE)
    for i, ln in enumerate([
        "Deadlines piled up again this week and I",
        "barely slept before the review. Talking to",
        "my group afterwards helped more than I",
        "expected, and the feedback was fair. Still",
        "anxious about the next sprint though.",
    ]):
        txt(d, (s[0] + 38, s[1] + 122 + i * 27), ln, 14, "r", (203, 213, 225))
    txt(d, (s[0] + 26, s[1] + 292), "Sentiment", 16, "b", WHITE)
    for i, (lab, v, col) in enumerate((("Positive", 0.42, (74, 222, 128)),
                                       ("Neutral", 0.33, (148, 163, 184)),
                                       ("Negative", 0.25, (248, 113, 113)))):
        y = s[1] + 326 + i * 42
        txt(d, (s[0] + 26, y + 9), lab, 14, "r", MUTED)
        rr(d, (s[0] + 130, y, s[2] - 66, y + 18), 9, fill=(255, 255, 255, 18))
        rr(d, (s[0] + 130, y, s[0] + 130 + (s[2] - 196 - s[0]) * v, y + 18), 9, fill=col)
        txt(d, (s[2] - 26, y + 9), "%d%%" % (v * 100), 13, "b", col, anchor="rm")
    txt(d, (s[0] + 26, s[1] + 470), "Themes detected", 16, "b", WHITE)
    x, y = s[0] + 26, s[1] + 502
    for t in ("deadlines", "sleep", "peer support", "exam stress", "workload"):
        w = pill(d, x, y, t, a, size=13, pad=10, h=26)
        x += w + 8
        if x > s[2] - 130:
            x, y = s[0] + 26, y + 34
    rr(d, (s[0] + 20, s[3] - 92, s[2] - 20, s[3] - 26), 14, fill=(250, 204, 21, 30),
       outline=(250, 204, 21, 160))
    txt(d, (s[0] + 40, s[3] - 70), "Flagged for counsellor review", 14, "b", (250, 204, 21))
    txt(d, (s[0] + 40, s[3] - 50), "Stress markers rising 3 entries in a row", 12, "r", MUTED)
    return im


def mh_risk_dashboard():
    a = accent_of(HUE_MH)
    im = canvas(HUE_MH, glow=False)
    box = browser(im, "wellbeing.sliit.lk/counsellor/dashboard")
    box = sidebar(im, box, a, "Wellbeing AI",
                  ["Dashboard", "Students", "Journals", "Alerts", "Reports"], 0)
    box = topbar(im, box, "Risk dashboard", a, "Cohort overview · updated 4 min ago")
    box = stat_cards(im, box, [("Monitored", "412", "+18"), ("At risk", "24", "+3"),
                               ("Alerts today", "7", "-2"), ("Avg. mood", "3.6", "+0.2")], a)
    x0, y0, x1, y1 = box
    inner = panel(im, (x0 + 26, y0, x0 + 640, y1 - 26), "Risk by faculty", a, "this term")
    bar_chart(im, inner, [18, 26, 12, 31, 22, 15], a,
              ["Comp", "Eng", "Biz", "Sci", "Arch", "Law"])
    inner = panel(im, (x0 + 664, y0, x1 - 26, y1 - 26), "Highest risk students", a, "top 5")
    table(im, inner, [("Student", 0), ("Faculty", 250), ("Score", 400), ("Status", 500)],
          [["S. Perera", "Computing", "0.87", ("pill", "High", (248, 113, 113))],
           ["A. Fernando", "Engineering", "0.81", ("pill", "High", (248, 113, 113))],
           ["N. Silva", "Science", "0.68", ("pill", "Medium", (250, 204, 21))],
           ["K. Jayasuriya", "Business", "0.61", ("pill", "Medium", (250, 204, 21))],
           ["R. de Mel", "Computing", "0.44", ("pill", "Watch", (56, 189, 248))]], a)
    return im


def mh_forecast():
    a = accent_of(HUE_MH)
    im = canvas(HUE_MH, glow=False)
    box = browser(im, "wellbeing.sliit.lk/counsellor/forecast")
    box = sidebar(im, box, a, "Wellbeing AI",
                  ["Dashboard", "Students", "Journals", "Alerts", "Reports"], 4)
    box = topbar(im, box, "Wellbeing forecast", a, "LSTM + ARIMA ensemble · 8 week horizon")
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(im, "RGBA")
    x = x0 + 26
    for i, t in enumerate(("LSTM", "ARIMA", "Ensemble")):
        w = pill(d, x, y0 + 22, t, a if i == 2 else (100, 116, 139), size=14)
        x += w + 10
    inner = panel(im, (x0 + 26, y0 + 64, x1 - 26, y0 + 340), "Predicted cohort risk index", a,
                  "shaded band = 90% confidence")
    line_chart(im, inner, [42, 45, 41, 48, 52, 50, 57, 61, 64, 68, 71, 74], a,
               band=True, dash_from=8,
               labels=["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12"])
    inner = panel(im, (x0 + 26, y0 + 362, x0 + 500, y1 - 26), "Model accuracy", a)
    donut(im, (inner[0] + inner[2]) / 2, (inner[1] + inner[3]) / 2 + 4, 72,
          [(0.72, a), (0.16, (100, 116, 139)), (0.12, (51, 65, 85))], a)
    inner = panel(im, (x0 + 524, y0 + 362, x1 - 26, y1 - 26), "Drivers of predicted change", a)
    table(im, inner, [("Signal", 0), ("Weight", 420), ("Trend", 560)],
          [["Sleep hours logged", "0.31", ("pill", "Falling", (248, 113, 113))],
           ["Assessment density", "0.27", ("pill", "Rising", (250, 204, 21))],
           ["Journal sentiment", "0.22", ("pill", "Falling", (248, 113, 113))]], a)
    return im


def mh_cover():
    a = accent_of(HUE_MH)
    im = canvas(HUE_MH, glow=False)
    box = browser(im, "wellbeing.sliit.lk/counsellor", box=(70, 60, 1210, 840))
    b2 = sidebar(im, box, a, "Wellbeing AI", ["Dashboard", "Students", "Journals", "Alerts"], 0)
    b2 = topbar(im, b2, "Cohort overview", a, "412 students monitored")
    b2 = stat_cards(im, b2, [("At risk", "24", "+3"), ("Alerts", "7", "-2"),
                             ("Avg. mood", "3.6", "+0.2")], a)
    inner = panel(im, (b2[0] + 26, b2[1], b2[2] - 26, b2[3] - 26), "Risk index trend", a)
    line_chart(im, inner, [42, 45, 41, 48, 52, 50, 57, 61, 64, 68], a, band=True, dash_from=7)
    s = phone(im, 1290, 470, pw=330, ph=660)
    d = ImageDraw.Draw(im, "RGBA")
    txt(d, (s[0] + 24, s[1] + 40), "Good evening", 14, "r", MUTED)
    txt(d, (s[0] + 24, s[1] + 62), "Vinuja", 24, "b", WHITE)
    rr(d, (s[0] + 18, s[1] + 112, s[2] - 18, s[1] + 216), 16, fill=a[:3] + (48,), outline=a)
    txt(d, (s[0] + 36, s[1] + 134), "DAILY CHECK-IN", 12, "b", a)
    for i in range(5):
        cx = s[0] + 46 + i * 52
        sel = i == 3
        d.ellipse((cx - 19, s[1] + 162, cx + 19, s[1] + 200),
                  fill=a[:3] + (70 if sel else 20,), outline=a if sel else LINE, width=2)
    bar_chart(im, (s[0] + 24, s[1] + 250, s[2] - 24, s[1] + 356), [3, 4, 2, 5, 4, 4, 5], a)
    d = ImageDraw.Draw(im, "RGBA")
    phone_card(d, (s[0] + 18, s[1] + 386, s[2] - 18, s[1] + 452), "Write journal", "2 min", a)
    phone_card(d, (s[0] + 18, s[1] + 464, s[2] - 18, s[1] + 530), "Breathing", "Recommended", a)
    return im


# ============================================================================
# 2. frd  (hue 210)
# ============================================================================

HUE_FRD = 210


def frd_login():
    a = accent_of(HUE_FRD)
    im = canvas(HUE_FRD, glow=False)
    box = browser(im, "frd.slt.lk/login")
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    d.rectangle((x0, y0, (x0 + x1) / 2, y1), fill=(11, 20, 40))
    g = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse((120, 300, 780, 900), fill=hsl(HUE_FRD, 0.8, 0.30))
    im.paste(Image.blend(im.crop((x0, y0, int((x0 + x1) / 2), y1)),
                         g.filter(ImageFilter.GaussianBlur(160)).crop((x0, y0, int((x0 + x1) / 2), y1)),
                         0.55), (x0, y0))
    d = ImageDraw.Draw(im, "RGBA")
    rr(d, (x0 + 90, y0 + 120, x0 + 146, y0 + 176), 16, fill=a)
    txt(d, (x0 + 90, y0 + 214), "FRD Security", 40, "b", WHITE)
    txt(d, (x0 + 90, y0 + 268), "Attendance Management", 40, "b", a)
    txt(d, (x0 + 90, y0 + 340), "Shift marking, two-step approval and\nmonthly reporting for security officers\nacross SLT Mobitel sites.", 19, "r", MUTED)
    for i, t in enumerate(("Azure AD sign-in", "Role based access", "Audit trail")):
        yy = y0 + 470 + i * 42
        d.ellipse((x0 + 90, yy, x0 + 110, yy + 20), outline=a, width=3)
        d.line([(x0 + 95, yy + 10), (x0 + 99, yy + 15), (x0 + 105, yy + 5)], fill=a, width=3)
        txt(d, (x0 + 124, yy + 10), t, 16, "r", (203, 213, 225), anchor="lm")
    cx = (x1 + (x0 + x1) / 2) / 2
    rr(d, (cx - 230, y0 + 150, cx + 230, y0 + 610), 18, fill=CARD, outline=LINE)
    txt(d, (cx, y0 + 200), "Sign in", 28, "b", WHITE, anchor="mm")
    txt(d, (cx, y0 + 236), "Use your SLT Mobitel account", 14, "r", MUTED, anchor="mm")
    for i, (lab, val) in enumerate((("EMAIL", "officer@slt.lk"), ("PASSWORD", "••••••••••••"))):
        yy = y0 + 280 + i * 92
        txt(d, (cx - 190, yy), lab, 12, "b", MUTED)
        rr(d, (cx - 190, yy + 22, cx + 190, yy + 68), 10, fill=(2, 6, 23),
           outline=a if i == 0 else LINE, width=2 if i == 0 else 1)
        txt(d, (cx - 172, yy + 45), val, 16, "r", TEXT, anchor="lm")
    rr(d, (cx - 190, y0 + 470, cx + 190, y0 + 518), 10, fill=a)
    txt(d, (cx, y0 + 494), "Sign in", 17, "b", (5, 10, 25), anchor="mm")
    d.line([(cx - 190, y0 + 546), (cx - 40, y0 + 546)], fill=LINE)
    d.line([(cx + 40, y0 + 546), (cx + 190, y0 + 546)], fill=LINE)
    txt(d, (cx, y0 + 546), "or", 13, "r", MUTED, anchor="mm")
    rr(d, (cx - 190, y0 + 566, cx + 190, y0 + 610), 10, fill=(2, 6, 23), outline=LINE)
    for i in range(4):
        d.rectangle((cx - 162 + (i % 2) * 13, y0 + 578 + (i // 2) * 13,
                     cx - 152 + (i % 2) * 13, y0 + 588 + (i // 2) * 13),
                    fill=[(242, 80, 34), (127, 186, 0), (0, 164, 239), (255, 185, 0)][i])
    txt(d, (cx - 122, y0 + 588), "Continue with Microsoft Azure AD", 15, "b", TEXT, anchor="lm")
    return im


def frd_dashboard():
    a = accent_of(HUE_FRD)
    im = canvas(HUE_FRD, glow=False)
    box = browser(im, "frd.slt.lk/manager/dashboard")
    box = sidebar(im, box, a, "FRD Security",
                  ["Dashboard", "Attendance", "Approvals", "Officers", "Reports"], 0)
    box = topbar(im, box, "Manager dashboard", a, "Head Office · 12 August 2026")
    box = stat_cards(im, box, [("On duty", "86", "+4"), ("Absent", "5", "-1"),
                               ("Pending approvals", "12", "+6"), ("Sites covered", "9", None)], a)
    x0, y0, x1, y1 = box
    inner = panel(im, (x0 + 26, y0, x0 + 620, y1 - 26), "Attendance this week", a, "officers/day")
    bar_chart(im, inner, [82, 88, 79, 91, 86, 64, 58], a, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    inner = panel(im, (x0 + 644, y0, x1 - 26, y1 - 26), "Today's shifts", a, "9 sites")
    table(im, inner, [("Officer", 0), ("Site", 210), ("Shift", 370), ("Status", 490)],
          [["W. Bandara", "Head Office", "06:00–14:00", ("pill", "Present", (74, 222, 128))],
           ["M. Rathnayake", "Welikada", "06:00–14:00", ("pill", "Present", (74, 222, 128))],
           ["T. Gunawardena", "Kollupitiya", "14:00–22:00", ("pill", "Pending", (250, 204, 21))],
           ["S. Dias", "Head Office", "22:00–06:00", ("pill", "Present", (74, 222, 128))],
           ["P. Kumara", "Nugegoda", "14:00–22:00", ("pill", "Absent", (248, 113, 113))]], a)
    return im


def frd_approvals():
    a = accent_of(HUE_FRD)
    im = canvas(HUE_FRD, glow=False)
    box = browser(im, "frd.slt.lk/approvals/history")
    box = sidebar(im, box, a, "FRD Security",
                  ["Dashboard", "Attendance", "Approvals", "Officers", "Reports"], 2)
    box = topbar(im, box, "Approval history", a, "Two-step workflow · supervisor then manager")
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(im, "RGBA")
    x = x0 + 26
    for i, t in enumerate(("All", "Approved", "Pending", "Rejected")):
        w = pill(d, x, y0 + 22, t, a if i == 0 else (100, 116, 139), size=14)
        x += w + 10
    rr(d, (x1 - 240, y0 + 20, x1 - 26, y0 + 50), 8, fill=(2, 6, 23), outline=LINE)
    txt(d, (x1 - 222, y0 + 35), "August 2026", 14, "r", MUTED, anchor="lm")
    inner = panel(im, (x0 + 26, y0 + 72, x1 - 26, y1 - 26), "Requests", a, "148 records")
    table(im, inner, [("Reference", 0), ("Officer", 190), ("Date", 400),
                      ("Supervisor", 560), ("Manager", 760), ("Result", 950)],
          [["FRD-2408-091", "W. Bandara", "11 Aug", ("pill", "Approved", (74, 222, 128)),
            ("pill", "Approved", (74, 222, 128)), ("pill", "Closed", (148, 163, 184))],
           ["FRD-2408-090", "P. Kumara", "11 Aug", ("pill", "Approved", (74, 222, 128)),
            ("pill", "Pending", (250, 204, 21)), ("pill", "In review", (56, 189, 248))],
           ["FRD-2408-089", "S. Dias", "10 Aug", ("pill", "Approved", (74, 222, 128)),
            ("pill", "Approved", (74, 222, 128)), ("pill", "Closed", (148, 163, 184))],
           ["FRD-2408-088", "T. Gunawardena", "10 Aug", ("pill", "Rejected", (248, 113, 113)),
            ("pill", "—", (100, 116, 139)), ("pill", "Returned", (248, 113, 113))],
           ["FRD-2408-087", "M. Rathnayake", "09 Aug", ("pill", "Approved", (74, 222, 128)),
            ("pill", "Approved", (74, 222, 128)), ("pill", "Closed", (148, 163, 184))],
           ["FRD-2408-086", "N. Wickrama", "09 Aug", ("pill", "Approved", (74, 222, 128)),
            ("pill", "Approved", (74, 222, 128)), ("pill", "Closed", (148, 163, 184))],
           ["FRD-2408-085", "A. Silva", "08 Aug", ("pill", "Pending", (250, 204, 21)),
            ("pill", "—", (100, 116, 139)), ("pill", "Waiting", (250, 204, 21))]], a)
    return im


def frd_report():
    a = accent_of(HUE_FRD)
    im = canvas(HUE_FRD, glow=False)
    box = browser(im, "frd.slt.lk/reports/monthly")
    box = sidebar(im, box, a, "FRD Security",
                  ["Dashboard", "Attendance", "Approvals", "Officers", "Reports"], 4)
    box = topbar(im, box, "Monthly report", a, "August 2026 · all sites")
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(im, "RGBA")
    rr(d, (x1 - 190, y0 + 20, x1 - 26, y0 + 56), 9, fill=a)
    txt(d, ((x1 - 190 + x1 - 26) / 2, y0 + 38), "Export PDF", 15, "b", (5, 10, 25), anchor="mm")
    box = stat_cards(im, (x0, y0 + 46, x1, y1),
                     [("Working days", "22", None), ("Total shifts", "1,848", "+112"),
                      ("Overtime hrs", "236", "+18"), ("Attendance", "96.4%", "+0.8")], a)
    x0, y0, x1, y1 = box
    inner = panel(im, (x0 + 26, y0, x0 + 600, y1 - 26), "Attendance by month", a, "2026")
    bar_chart(im, inner, [92, 94, 91, 95, 93, 96, 94, 96], a,
              ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"])
    inner = panel(im, (x0 + 624, y0, x1 - 26, y1 - 26), "Per site summary", a, "4 sites")
    table(im, inner, [("Site", 0), ("Officers", 240), ("Shifts", 330), ("Overtime", 420),
                      ("Rate", 490)],
          [["Head Office", "24", "528", "72 h", "97.8%"],
           ["Welikada", "16", "352", "41 h", "96.1%"],
           ["Kollupitiya", "14", "308", "38 h", "95.4%"],
           ["Nugegoda", "12", "264", "29 h", "96.9%"]], a)
    return im


def frd_cover():
    a = accent_of(HUE_FRD)
    im = canvas(HUE_FRD, glow=False)
    box = browser(im, "frd.slt.lk/manager/dashboard", box=(110, 90, 1490, 810))
    box = sidebar(im, box, a, "FRD Security", ["Dashboard", "Attendance", "Approvals", "Reports"], 0)
    box = topbar(im, box, "Manager dashboard", a, "Head Office · today")
    box = stat_cards(im, box, [("On duty", "86", "+4"), ("Absent", "5", "-1"),
                               ("Pending", "12", "+6")], a)
    x0, y0, x1, y1 = box
    inner = panel(im, (x0 + 26, y0, x0 + 560, y1 - 26), "This week", a)
    bar_chart(im, inner, [82, 88, 79, 91, 86, 64, 58], a, ["M", "T", "W", "T", "F", "S", "S"])
    inner = panel(im, (x0 + 584, y0, x1 - 26, y1 - 26), "Pending approvals", a)
    table(im, inner, [("Officer", 0), ("Shift", 250), ("Status", 420)],
          [["W. Bandara", "06:00–14:00", ("pill", "Level 1", (250, 204, 21))],
           ["S. Dias", "22:00–06:00", ("pill", "Level 2", (56, 189, 248))],
           ["P. Kumara", "14:00–22:00", ("pill", "Level 1", (250, 204, 21))]], a)
    return im


# ============================================================================
# 3. skillsync  (hue 175)
# ============================================================================

HUE_SS = 175


def _ss_nav(im, box, a, active=0):
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, _ = box
    d.rectangle((x0, y0, x1, y0 + 72), fill=(11, 20, 38))
    d.line([(x0, y0 + 72), (x1, y0 + 72)], fill=LINE)
    rr(d, (x0 + 30, y0 + 22, x0 + 58, y0 + 50), 8, fill=a)
    txt(d, (x0 + 70, y0 + 36), "SkillSync", 19, "b", WHITE, anchor="lm")
    for i, t in enumerate(("Find work", "Find talent", "How it works", "Pricing")):
        txt(d, (x0 + 230 + i * 132, y0 + 36), t, 15, "b" if i == active else "r",
            WHITE if i == active else MUTED, anchor="lm")
    rr(d, (x1 - 260, y0 + 20, x1 - 150, y0 + 52), 8, fill=None, outline=LINE)
    txt(d, (x1 - 205, y0 + 36), "Log in", 14, "b", TEXT, anchor="mm")
    rr(d, (x1 - 134, y0 + 20, x1 - 30, y0 + 52), 8, fill=a)
    txt(d, (x1 - 82, y0 + 36), "Sign up", 14, "b", (5, 20, 18), anchor="mm")
    return (x0, y0 + 73, x1, box[3])


def ss_landing(win=(70, 60, 1530, 840)):
    a = accent_of(HUE_SS)
    im = canvas(HUE_SS, glow=False)
    box = browser(im, "skillsync.lk", box=win)
    box = _ss_nav(im, box, a, 0)
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    g = Image.new("RGB", im.size, BG)
    gd = ImageDraw.Draw(g)
    gd.ellipse((900, 120, 1700, 780), fill=hsl(HUE_SS, 0.8, 0.24))
    im.paste(Image.blend(im.crop(box), g.filter(ImageFilter.GaussianBlur(170)).crop(box), 0.5),
             (x0, y0))
    d = ImageDraw.Draw(im, "RGBA")
    pill(d, x0 + 70, y0 + 60, "Sri Lankan talent · global clients", a, size=14)
    txt(d, (x0 + 70, y0 + 116), "Hire the skills", 46, "b", WHITE)
    txt(d, (x0 + 70, y0 + 172), "your project needs", 46, "b", a)
    txt(d, (x0 + 70, y0 + 244), "Post a job in minutes and shortlist verified freelancers\nfrom Sri Lanka — design, development, writing and more.", 19, "r", MUTED)
    rr(d, (x0 + 70, y0 + 330, x0 + 700, y0 + 386), 12, fill=(2, 6, 23), outline=LINE)
    txt(d, (x0 + 96, y0 + 358), "Search 4,200+ freelancers…", 16, "r", (100, 116, 139), anchor="lm")
    rr(d, (x0 + 560, y0 + 338, x0 + 692, y0 + 378), 9, fill=a)
    txt(d, (x0 + 626, y0 + 358), "Search", 15, "b", (5, 20, 18), anchor="mm")
    for i, (v, lab) in enumerate((("4.2k", "freelancers"), ("1.8k", "jobs posted"), ("96%", "hire rate"))):
        cx = x0 + 90 + i * 200
        txt(d, (cx, y0 + 430), v, 30, "b", WHITE, anchor="lm")
        txt(d, (cx, y0 + 470), lab, 14, "r", MUTED, anchor="lm")
    for i, (t, n) in enumerate((("Web development", "820 jobs"), ("Mobile apps", "410 jobs"),
                                ("UI/UX design", "356 jobs"), ("Data & AI", "214 jobs"))):
        cx = x0 + 70 + i * 236
        rr(d, (cx, y0 + 530, cx + 214, y0 + 660), 14, fill=CARD, outline=LINE)
        rr(d, (cx + 20, y0 + 552, cx + 56, y0 + 588), 10, fill=a[:3] + (55,))
        txt(d, (cx + 20, y0 + 606), t, 16, "b", WHITE)
        txt(d, (cx + 20, y0 + 630), n, 13, "r", MUTED)
    rr(d, (x1 - 470, y0 + 90, x1 - 60, y0 + 640), 18, fill=CARD, outline=LINE)
    txt(d, (x1 - 440, y0 + 128), "Top rated this week", 17, "b", WHITE)
    for i, (nm, role, rate, ini, score) in enumerate((
            ("Ishara N.", "Flutter developer", "$28/hr", "IN", "4.9 · 32 jobs"),
            ("Dilshan P.", "React & Node", "$32/hr", "DP", "4.8 · 57 jobs"),
            ("Tharushi M.", "Product designer", "$24/hr", "TM", "5.0 · 19 jobs"),
            ("Kavindu S.", "Data engineer", "$35/hr", "KS", "4.7 · 41 jobs"))):
        yy = y0 + 176 + i * 112
        rr(d, (x1 - 442, yy, x1 - 88, yy + 92), 12, fill=(24, 36, 60), outline=LINE)
        avatar(d, x1 - 400, yy + 46, 26, ini, a)
        txt(d, (x1 - 360, yy + 26), nm, 16, "b", WHITE)
        txt(d, (x1 - 360, yy + 50), role, 13, "r", MUTED)
        star(d, x1 - 353, yy + 78, 8, (250, 204, 21))
        txt(d, (x1 - 338, yy + 70), score, 12, "b", (250, 204, 21))
        txt(d, (x1 - 110, yy + 46), rate, 15, "b", a, anchor="rm")
    return im


def ss_jobs():
    a = accent_of(HUE_SS)
    im = canvas(HUE_SS, glow=False)
    box = browser(im, "skillsync.lk/jobs?category=development")
    box = _ss_nav(im, box, a, 0)
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    d.rectangle((x0, y0, x0 + 300, y1), fill=(11, 18, 34))
    d.line([(x0 + 300, y0), (x0 + 300, y1)], fill=LINE)
    txt(d, (x0 + 30, y0 + 34), "Filters", 18, "b", WHITE)
    yy = y0 + 80
    for title, opts in (("Category", ("Development", "Design", "Writing", "Data")),
                        ("Experience", ("Entry", "Intermediate", "Expert"))):
        txt(d, (x0 + 30, yy), title.upper(), 12, "b", (110, 126, 150))
        yy += 26
        for j, o in enumerate(opts):
            on = j == 0
            rr(d, (x0 + 30, yy, x0 + 48, yy + 18), 5, fill=a if on else None, outline=LINE if not on else a)
            if on:
                d.line([(x0 + 35, yy + 9), (x0 + 38, yy + 13), (x0 + 44, yy + 5)], fill=(5, 20, 18), width=2)
            txt(d, (x0 + 62, yy + 9), o, 14, "r", TEXT if on else MUTED, anchor="lm")
            yy += 32
        yy += 16
    txt(d, (x0 + 30, yy), "BUDGET", 12, "b", (110, 126, 150))
    rr(d, (x0 + 30, yy + 34, x0 + 260, yy + 42), 4, fill=(51, 65, 85))
    rr(d, (x0 + 30, yy + 34, x0 + 190, yy + 42), 4, fill=a)
    d.ellipse((x0 + 178, yy + 28, x0 + 202, yy + 52), fill=a)
    txt(d, (x0 + 30, yy + 66), "$500 – $3,000", 14, "b", TEXT)
    txt(d, (x0 + 336, y0 + 34), "312 jobs matched", 20, "b", WHITE)
    txt(d, (x1 - 30, y0 + 40), "Sort: Newest", 14, "r", MUTED, anchor="rm")
    jobs = [("Flutter app for a delivery startup", "Fixed · $1,800", ("Flutter", "Firebase", "Maps"), "12 proposals", "2 h ago"),
            ("React dashboard for logistics SaaS", "Hourly · $25–35/hr", ("React", "TypeScript", "REST"), "8 proposals", "5 h ago"),
            ("Spring Boot API for an LMS", "Fixed · $2,400", ("Spring Boot", "MySQL", "Docker"), "21 proposals", "yesterday"),
            ("Landing page redesign", "Fixed · $650", ("Figma", "Tailwind"), "34 proposals", "yesterday"),
            ("Data pipeline for retail analytics", "Hourly · $30–40/hr", ("Python", "Airflow"), "6 proposals", "2 d ago")]
    for i, (t, budget, tags, props, when) in enumerate(jobs):
        yy = y0 + 76 + i * 122
        rr(d, (x0 + 336, yy, x1 - 30, yy + 106), 14, fill=CARD, outline=LINE)
        txt(d, (x0 + 362, yy + 24), t, 18, "b", WHITE)
        txt(d, (x0 + 362, yy + 52), budget, 14, "b", a)
        x = x0 + 362
        for tg in tags:
            x += pill(d, x, yy + 72, tg, (148, 163, 184), size=12, pad=9, h=24) + 8
        txt(d, (x1 - 56, yy + 30), when, 13, "r", (100, 116, 139), anchor="rm")
        txt(d, (x1 - 56, yy + 76), props, 13, "r", MUTED, anchor="rm")
    return im


def ss_profile():
    a = accent_of(HUE_SS)
    im = canvas(HUE_SS, glow=False)
    box = browser(im, "skillsync.lk/u/ishara-n")
    box = _ss_nav(im, box, a, 1)
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    d.rectangle((x0, y0, x1, y0 + 190), fill=(13, 24, 44))
    g = Image.new("RGB", im.size, (13, 24, 44))
    ImageDraw.Draw(g).ellipse((x0 - 100, y0 - 60, x0 + 700, y0 + 320), fill=hsl(HUE_SS, 0.7, 0.26))
    im.paste(Image.blend(im.crop((x0, y0, x1, y0 + 190)),
                         g.filter(ImageFilter.GaussianBlur(140)).crop((x0, y0, x1, y0 + 190)), 0.5),
             (x0, y0))
    d = ImageDraw.Draw(im, "RGBA")
    avatar(d, x0 + 110, y0 + 96, 56, "IN", a)
    txt(d, (x0 + 190, y0 + 60), "Ishara Nawoda", 30, "b", WHITE)
    txt(d, (x0 + 190, y0 + 102), "Senior Flutter & React developer · Colombo, LK", 16, "r", (203, 213, 225))
    star(d, x0 + 199, y0 + 141, 11, (250, 204, 21))
    txt(d, (x0 + 216, y0 + 132), "4.9  (32 reviews)", 14, "b", (250, 204, 21))
    rr(d, (x1 - 210, y0 + 74, x1 - 40, y0 + 118), 10, fill=a)
    txt(d, (x1 - 125, y0 + 96), "Hire me", 16, "b", (5, 20, 18), anchor="mm")
    txt(d, (x1 - 250, y0 + 96), "$28/hr", 22, "b", WHITE, anchor="rm")
    inner = panel(im, (x0 + 30, y0 + 216, x0 + 720, y0 + 380), "About", a)
    for i, ln in enumerate(["Six years building cross-platform apps and dashboards for",
                            "startups in the UK and Australia. I work in small teams,",
                            "ship weekly and write tests for anything that touches money."]):
        txt(d, (inner[0], inner[1] + i * 28), ln, 15, "r", (203, 213, 225))
    inner = panel(im, (x0 + 744, y0 + 216, x1 - 30, y0 + 380), "Skills", a)
    x, yy = inner[0], inner[1]
    for s in ("Flutter", "Dart", "React", "TypeScript", "Node.js", "Firebase", "REST", "CI/CD"):
        w = pill(d, x, yy, s, a, size=13, pad=11, h=28)
        x += w + 9
        if x > inner[2] - 110:
            x, yy = inner[0], yy + 38
    inner = panel(im, (x0 + 30, y0 + 404, x1 - 30, y1 - 30), "Portfolio", a, "12 projects")
    cw = (inner[2] - inner[0] - 60) / 4
    ch = inner[3] - inner[1] - 32          # leave room for the caption under each tile
    for i, t in enumerate(("Delivery app", "Fintech dashboard", "Booking platform", "IoT monitor")):
        cx, top = inner[0] + i * (cw + 20), inner[1]
        rr(d, (cx, top, cx + cw, top + ch), 12, fill=(24, 36, 60), outline=LINE)
        rr(d, (cx + 16, top + 16, cx + cw - 16, top + ch * 0.5), 8, fill=(15, 25, 45))
        for j in range(2):
            yy = top + ch * 0.58 + j * 24
            rr(d, (cx + 16, yy, cx + cw - 16 - j * 34, yy + 15), 5, fill=a[:3] + (95 - j * 30,))
        txt(d, (cx + 4, top + ch + 8), t, 14, "b", TEXT)
    return im


def ss_client_dashboard():
    a = accent_of(HUE_SS)
    im = canvas(HUE_SS, glow=False)
    box = browser(im, "skillsync.lk/client/dashboard")
    box = sidebar(im, box, a, "SkillSync",
                  ["Overview", "My jobs", "Proposals", "Contracts", "Payments"], 0)
    box = topbar(im, box, "Client dashboard", a, "Northwind Studio · 3 active contracts")
    box = stat_cards(im, box, [("Active jobs", "5", "+2"), ("Proposals", "48", "+11"),
                               ("Hired", "9", "+1"), ("Spend (MTD)", "$6.4k", "+18%")], a)
    x0, y0, x1, y1 = box
    inner = panel(im, (x0 + 26, y0, x0 + 600, y1 - 26), "Proposals per week", a)
    bar_chart(im, inner, [6, 11, 8, 14, 12, 17], a, ["W1", "W2", "W3", "W4", "W5", "W6"])
    inner = panel(im, (x0 + 624, y0, x1 - 26, y1 - 26), "Recent proposals", a, "48 total")
    table(im, inner, [("Freelancer", 0), ("Job", 220), ("Bid", 470), ("Status", 580)],
          [["Ishara N.", "Flutter delivery app", "$1,750", ("pill", "Shortlisted", (56, 189, 248))],
           ["Dilshan P.", "React dashboard", "$28/hr", ("pill", "Interview", (250, 204, 21))],
           ["Tharushi M.", "Landing redesign", "$620", ("pill", "Hired", (74, 222, 128))],
           ["Kavindu S.", "Data pipeline", "$34/hr", ("pill", "New", (148, 163, 184))],
           ["Ruwan A.", "Spring Boot API", "$2,300", ("pill", "Declined", (248, 113, 113))]], a)
    return im


def ss_cover():
    # Same hero as slide 1, framed tighter so the card thumbnail reads at small sizes.
    return ss_landing(win=(120, 100, 1480, 800))


# ============================================================================
# 4. numenor  (hue 30) — 2D game screens
# ============================================================================

HUE_NM = 30
SKY_TOP = (26, 18, 46)
SKY_BOT = (92, 46, 58)


def game_bg(w, h):
    """Sky gradient + stars, cached per size."""
    key = ("bg", w, h)
    if key in _fcache:
        return _fcache[key].copy()
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * (t ** 1.4)) for i in range(3)))
    rnd = random.Random(11)
    for _ in range(90):
        sx, sy = rnd.uniform(0, w), rnd.uniform(0, h * 0.55)
        r = rnd.uniform(0.6, 1.8)
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(255, 250, 235))
    d.ellipse((w * 0.74, h * 0.10, w * 0.74 + h * 0.17, h * 0.10 + h * 0.17), fill=(255, 236, 200))
    _fcache[key] = im
    return im.copy()


def game_scene(w, h, t=0.0, hud=True):
    """A frame of the 2D platformer. t advances the run cycle / parallax."""
    im = game_bg(w, h)
    d = ImageDraw.Draw(im, "RGBA")
    a = accent_of(HUE_NM)
    scroll = t * w * 0.6

    for depth, col, base, amp in ((0.25, (46, 32, 62), 0.60, 0.10),
                                  (0.5, (34, 24, 48), 0.70, 0.075)):
        off = (scroll * depth) % (w / 2)
        pts = [(0, h)]
        for i in range(0, int(w) + 40, 20):
            xx = i + off
            pts.append((i, h * base - math.sin((xx / w) * 6.2) * h * amp))
        pts.append((w, h))
        d.polygon(pts, fill=col)

    ground_y = h * 0.74
    d.rectangle((0, ground_y, w, h), fill=(38, 26, 30))
    d.rectangle((0, ground_y, w, ground_y + h * 0.02), fill=(72, 48, 40))
    tile = w / 14
    off = scroll % tile
    for i in range(-1, 15):
        x = i * tile - off
        d.line([(x, ground_y), (x, h)], fill=(28, 19, 24), width=2)

    for i, (px, py, pw_) in enumerate(((0.18, 0.44, 0.16), (0.52, 0.33, 0.14), (0.80, 0.47, 0.13))):
        x = ((px * w - scroll * 0.85) % (w * 1.35)) - w * 0.18
        y, pw2 = py * h, pw_ * w
        rr(d, (x, y, x + pw2, y + h * 0.035), 8, fill=(72, 48, 40), outline=(104, 70, 52), width=2)

    for i, (cx, cy) in enumerate(((0.30, 0.37), (0.44, 0.27), (0.66, 0.40), (0.88, 0.31))):
        x = ((cx * w - scroll * 0.85) % (w * 1.25)) - w * 0.12
        y = cy * h + math.sin(t * 6.2 + i) * h * 0.012
        rw = abs(math.cos(t * 4.4 + i * 1.3)) * h * 0.022 + h * 0.006
        d.ellipse((x - rw, y - h * 0.024, x + rw, y + h * 0.024), fill=(250, 204, 21),
                  outline=(180, 130, 20), width=2)

    # knight — scaled so the feet land on the ground line
    s = h / 520.0
    bob = math.sin(t * 12.5) * h * 0.012
    cx, cy = w * 0.34, ground_y - 36 * s + h * 0.004 + bob
    swing = math.sin(t * 12.5)
    d.polygon([(cx - 26 * s, cy - 34 * s), (cx - 6 * s, cy - 40 * s),
               (cx - 12 * s, cy + 30 * s), (cx - 40 * s, cy + 18 * s)], fill=(150, 42, 52))
    for k in (-1, 1):
        lx = cx + k * 9 * s
        ly = cy + 36 * s
        d.line([(lx, cy + 18 * s), (lx + swing * k * 16 * s, ly)], fill=(58, 44, 92), width=int(9 * s) or 3)
    rr(d, (cx - 20 * s, cy - 34 * s, cx + 20 * s, cy + 22 * s), int(10 * s) or 4, fill=a)
    rr(d, (cx - 20 * s, cy - 6 * s, cx + 20 * s, cy + 4 * s), int(4 * s) or 2, fill=(120, 70, 20))
    d.ellipse((cx - 17 * s, cy - 70 * s, cx + 17 * s, cy - 34 * s), fill=(240, 200, 170))
    d.pieslice((cx - 19 * s, cy - 76 * s, cx + 19 * s, cy - 38 * s), 180, 360, fill=(190, 190, 200))
    d.rectangle((cx - 19 * s, cy - 58 * s, cx + 19 * s, cy - 52 * s), fill=(190, 190, 200))
    d.line([(cx + 22 * s, cy + 6 * s), (cx + 62 * s + swing * 10 * s, cy - 46 * s)],
           fill=(226, 232, 240), width=int(7 * s) or 3)
    d.line([(cx + 20 * s, cy + 2 * s), (cx + 34 * s, cy - 8 * s)], fill=(120, 70, 20), width=int(9 * s) or 3)

    if hud:
        for i in range(3):
            hx, hy = w * 0.035 + i * h * 0.052, h * 0.07
            full = i < 2
            col = (239, 68, 68) if full else (90, 60, 70)
            r = h * 0.017
            d.ellipse((hx - r, hy - r, hx + r * 0.15, hy + r * 0.6), fill=col)
            d.ellipse((hx - r * 0.15, hy - r, hx + r, hy + r * 0.6), fill=col)
            d.polygon([(hx - r, hy), (hx + r, hy), (hx, hy + r * 1.5)], fill=col)
        fs = max(int(h * 0.036), 12)
        txt(d, (w * 0.965, h * 0.062), "SCORE  %05d" % (1240 + int(t * 260)), fs, "b", WHITE, anchor="rm")
        txt(d, (w * 0.965, h * 0.115), "LEVEL 3", int(fs * 0.72), "b", (250, 204, 21), anchor="rm")
        # joystick
        jx, jy, jr = w * 0.10, h * 0.79, h * 0.085
        d.ellipse((jx - jr, jy - jr, jx + jr, jy + jr), fill=(255, 255, 255, 26), outline=(255, 255, 255, 90), width=3)
        kx = jx + math.cos(t * 5.0) * jr * 0.42
        ky = jy + math.sin(t * 3.1) * jr * 0.22
        kr = jr * 0.42
        d.ellipse((kx - kr, ky - kr, kx + kr, ky + kr), fill=(255, 255, 255, 165))
        bx, by, br = w * 0.90, h * 0.80, h * 0.062
        d.ellipse((bx - br, by - br, bx + br, by + br), fill=a[:3] + (150,), outline=(255, 255, 255, 120), width=3)
        txt(d, (bx, by), "A", int(br * 0.9), "b", WHITE, anchor="mm")
    return im


def landscape_phone(im, cx, cy, pw=1180, ph=666):
    """Landscape handset shell; returns the inner screen box."""
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = cx - pw // 2, cy - ph // 2, cx + pw // 2, cy + ph // 2
    d.rounded_rectangle((x0 + 10, y0 + 18, x1 + 10, y1 + 20), 46, fill=(0, 0, 0, 140))
    rr(d, (x0, y0, x1, y1), 44, fill=(8, 12, 26), outline=(51, 65, 85), width=3)
    s = (x0 + 13, y0 + 13, x1 - 13, y1 - 13)
    rr(d, s, 34, fill=(0, 0, 0))
    return s


def _paste_screen(im, screen_box, content):
    x0, y0, x1, y1 = [int(v) for v in screen_box]
    c = content.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    mask = Image.new("L", c.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, c.size[0] - 1, c.size[1] - 1), 32, fill=255)
    im.paste(c, (x0, y0), mask)


def nm_title():
    a = accent_of(HUE_NM)
    im = canvas(HUE_NM, glow=True)
    box = landscape_phone(im, 800, 450)
    scene = game_scene(1180, 666, t=0.35, hud=False)
    sd = ImageDraw.Draw(scene, "RGBA")
    sd.rectangle((0, 0, 1180, 666), fill=(6, 4, 18, 150))
    txt(sd, (590, 168), "LEGEND OF THE", 34, "b", (250, 204, 21), anchor="mm")
    txt(sd, (590, 232), "NUMENOR", 76, "b", WHITE, anchor="mm")
    sd.line([(400, 288), (780, 288)], fill=a, width=4)
    for i, (lab, primary) in enumerate((("PLAY", True), ("LEVELS", False), ("SETTINGS", False))):
        yy = 350 + i * 82
        rr(sd, (420, yy, 760, yy + 62), 14,
           fill=a if primary else (255, 255, 255, 22),
           outline=None if primary else (255, 255, 255, 90), width=2)
        txt(sd, (590, yy + 31), lab, 26, "b", (28, 14, 4) if primary else WHITE, anchor="mm")
    txt(sd, (590, 620), "v1.2  ·  tap to begin", 16, "r", (203, 213, 225), anchor="mm")
    _paste_screen(im, box, scene)
    return im


def nm_levels():
    a = accent_of(HUE_NM)
    im = canvas(HUE_NM, glow=True)
    box = landscape_phone(im, 800, 450)
    scene = game_scene(1180, 666, t=0.6, hud=False)
    sd = ImageDraw.Draw(scene, "RGBA")
    sd.rectangle((0, 0, 1180, 666), fill=(6, 4, 18, 215))
    txt(sd, (590, 74), "SELECT LEVEL", 38, "b", WHITE, anchor="mm")
    txt(sd, (590, 118), "World 1 — The Grey Havens", 18, "r", (203, 213, 225), anchor="mm")
    for i in range(10):
        col, row = i % 5, i // 5
        cx = 190 + col * 200
        cy = 240 + row * 190
        unlocked = i < 6
        rr(sd, (cx - 74, cy - 66, cx + 74, cy + 66), 18,
           fill=a[:3] + (48,) if unlocked else (255, 255, 255, 14),
           outline=a if unlocked else (255, 255, 255, 60), width=3)
        if unlocked:
            txt(sd, (cx, cy - 12), str(i + 1), 44, "b", WHITE, anchor="mm")
            stars = 3 if i < 3 else (2 if i < 5 else 1)
            for s_i in range(3):
                star(sd, cx - 40 + s_i * 40, cy + 38, 15,
                     (250, 204, 21) if s_i < stars else (255, 255, 255, 45))
        else:
            padlock(sd, cx, cy - 4, 52, (148, 163, 184))
    _paste_screen(im, box, scene)
    return im


def nm_score():
    a = accent_of(HUE_NM)
    im = canvas(HUE_NM, glow=True)
    box = landscape_phone(im, 800, 450)
    scene = game_scene(1180, 666, t=0.15, hud=False)
    sd = ImageDraw.Draw(scene, "RGBA")
    sd.rectangle((0, 0, 1180, 666), fill=(6, 4, 18, 165))
    rr(sd, (270, 90, 910, 590), 24, fill=(20, 14, 32, 235), outline=a, width=3)
    txt(sd, (590, 146), "LEVEL COMPLETE", 36, "b", WHITE, anchor="mm")
    for s_i in range(3):
        star(sd, 470 + s_i * 120, 226, 44,
             (250, 204, 21) if s_i < 2 else (255, 255, 255, 45))
    for i, (lab, val) in enumerate((("Coins collected", "38 / 45"), ("Enemies defeated", "12"),
                                    ("Time", "01:42"), ("Score", "24,860"))):
        yy = 320 + i * 52
        big = i == 3
        txt(sd, (330, yy), lab, 22 if not big else 26, "b" if big else "r",
            WHITE if big else (203, 213, 225), anchor="lm")
        txt(sd, (850, yy), val, 24 if not big else 30, "b", a if big else WHITE, anchor="rm")
        if i < 3:
            sd.line([(330, yy + 24), (850, yy + 24)], fill=(255, 255, 255, 26))
    rr(sd, (330, 512, 570, 566), 14, fill=(255, 255, 255, 22), outline=(255, 255, 255, 90), width=2)
    txt(sd, (450, 539), "RETRY", 22, "b", WHITE, anchor="mm")
    rr(sd, (610, 512, 850, 566), 14, fill=a)
    txt(sd, (730, 539), "NEXT", 22, "b", (28, 14, 4), anchor="mm")
    _paste_screen(im, box, scene)
    return im


def nm_cover():
    im = canvas(HUE_NM, glow=True)
    box = landscape_phone(im, 800, 450, pw=1300, ph=734)
    _paste_screen(im, box, game_scene(1300, 734, t=0.42, hud=True))
    return im


def nm_gameplay_mp4(path, seconds=4, fps=24, size=(854, 480)):
    """H.264 via OpenCV. The backend ignores VIDEOWRITER_PROP_QUALITY and encodes at a
    fixed ~8 Mbps, so frame size and duration are the only levers on file size."""
    import cv2
    import numpy as np
    w, h = size
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    vw = cv2.VideoWriter(path, fourcc, fps, (w, h))
    if not vw.isOpened():
        raise RuntimeError("could not open VideoWriter for " + path)
    n = seconds * fps
    for i in range(n):
        frame = game_scene(w, h, t=i / fps, hud=True)
        vw.write(np.array(frame)[:, :, ::-1])
    vw.release()
    print("  %-46s %6.0f KB  (%d frames)" % (os.path.relpath(path, ROOT),
                                             os.path.getsize(path) / 1024, n))


# ============================================================================

def main():
    random.seed(7)
    print("mental-health-ai")
    save(mh_cover(), "mental-health-ai", "cover.jpg")
    save(mh_app_home(), "mental-health-ai", "1.jpg")
    save(mh_journal(), "mental-health-ai", "2.jpg")
    save(mh_risk_dashboard(), "mental-health-ai", "3.jpg")
    save(mh_forecast(), "mental-health-ai", "4.jpg")

    print("frd")
    save(frd_cover(), "frd", "cover.jpg")
    save(frd_login(), "frd", "1.jpg")
    save(frd_dashboard(), "frd", "2.jpg")
    save(frd_approvals(), "frd", "3.jpg")
    save(frd_report(), "frd", "4.jpg")

    print("skillsync")
    save(ss_cover(), "skillsync", "cover.jpg")
    save(ss_landing(), "skillsync", "1.jpg")
    save(ss_jobs(), "skillsync", "2.jpg")
    save(ss_profile(), "skillsync", "3.jpg")
    save(ss_client_dashboard(), "skillsync", "4.jpg")

    print("numenor")
    save(nm_cover(), "numenor", "cover.jpg")
    save(nm_title(), "numenor", "1.jpg")
    save(nm_levels(), "numenor", "3.jpg")
    save(nm_score(), "numenor", "4.jpg")
    if "--no-video" in sys.argv:
        print("  (skipped gameplay.mp4)")
    else:
        os.makedirs(os.path.join(OUT, "numenor"), exist_ok=True)
        nm_gameplay_mp4(os.path.join(OUT, "numenor", "gameplay.mp4"))


if __name__ == "__main__":
    main()
