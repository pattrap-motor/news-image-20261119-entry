#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024, deterministic).

Run: python3 draw.py  -> writes entry.png next to this file.
Only Pillow is used; no network, no randomness, no clock.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 30  # page margin
CW = W - 2 * M  # content width = 964
PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (176, 30, 36)
GREY = (96, 91, 80)
RULE = (40, 40, 40)
NIGHT = (24, 18, 54)
NEON = (255, 64, 170)
ORANGE = (255, 140, 40)
TEAL = (18, 120, 110)
GOLD = (198, 148, 32)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def wrap(d, s, f, width):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if tw(d, trial, f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, f, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def centered(d, y, s, f, fill, cx=W // 2):
    d.text((cx - tw(d, s, f) // 2, y), s, font=f, fill=fill)


def hline(d, x0, x1, y, fill=RULE, w=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def palm(d, x, y, s, fill):
    """Flat palm tree, base at (x, y), height ~ s."""
    d.line([(x, y), (x, y - s)], fill=fill, width=max(3, s // 18))
    top = (x, y - s)
    for dx, dy, ex, ey in [(-s // 3, -s // 6, -s // 2, s // 10),
                           (s // 3, -s // 6, s // 2, s // 10),
                           (-s // 4, -s // 3, -s // 3, -s // 12),
                           (s // 4, -s // 3, s // 3, -s // 12),
                           (0, -s // 2, 0, -s // 4)]:
        d.line([top, (x + dx, y - s + dy)], fill=fill, width=max(2, s // 28))
        d.line([(x + dx, y - s + dy), (x + ex, y - s + ey)], fill=fill,
               width=max(2, s // 28))


def skyline(d, x0, y0, x1, y1, seed_heights, fill, win):
    """Flat building silhouettes between x0..x1, bases at y1, tops from seed_heights."""
    n = len(seed_heights)
    bw = (x1 - x0) // n
    for i, h in enumerate(seed_heights):
        bx = x0 + i * bw + 2
        d.rectangle([bx, y1 - h, bx + bw - 4, y1], fill=fill)
        for wy in range(y1 - h + 8, y1 - 6, 14):
            for wx in range(bx + 5, bx + bw - 8, 12):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=win)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = M, W - M

    # ---- Masthead ----
    y = 28
    centered(d, y, "THE WORLD IN ONE DAY", font(SERIF_B, 56), INK)
    y = 100
    hline(d, x0, x1, y, RULE, 3)
    y = 108
    centered(d, y, "THURSDAY  ·  19 NOVEMBER 2026", font(SANS_B, 25), RED)
    y = 142
    hline(d, x0, x1, y, RULE, 2)

    # ---- Lead: GTA VI (panel y 152..452) ----
    ly, lh = 152, 300
    d.rectangle([x0, ly, x1, ly + lh], outline=RULE, width=2)
    iw = 480  # illustration width
    ix0, ix1 = x0, x0 + iw
    # night sky bands
    for i, c in enumerate([(24, 18, 54), (48, 26, 84), (86, 34, 96), (150, 52, 96)]):
        d.rectangle([ix0 + 2, ly + 2 + i * (lh // 4), ix1, ly + 2 + (i + 1) * (lh // 4)], fill=c)
    # sun / moon
    d.ellipse([ix0 + 330, ly + 26, ix0 + 420, ly + 116], fill=(255, 190, 90))
    d.ellipse([ix0 + 348, ly + 40, ix0 + 402, ly + 94], fill=(255, 214, 140))
    # skyline
    skyline(d, ix0 + 2, ly, ix1, ly + lh - 42, [120, 170, 95, 200, 140, 185, 110, 155],
            (16, 12, 40), (255, 200, 110))
    # street
    d.rectangle([ix0 + 2, ly + lh - 42, ix1, ly + lh - 2], fill=(12, 10, 30))
    d.line([(ix0 + 2, ly + lh - 22), (ix1, ly + lh - 22)], fill=(255, 220, 90), width=2)
    # palms (kept inside the panel, clear of the neon sign)
    palm(d, ix0 + 105, ly + lh - 42, 64, (8, 26, 14))
    palm(d, ix0 + 395, ly + lh - 42, 56, (8, 26, 14))
    # neon sign
    d.text((ix0 + 150, ly + 150), "GTA VI", font=font(SANS_B, 58), fill=(255, 30, 150),
           stroke_width=2, stroke_fill=(255, 120, 200))
    d.text((ix0 + 152, ly + 152), "GTA VI", font=font(SANS_B, 58), fill=(255, 220, 240))

    # lead text column
    tx = ix1 + 22
    twd = x1 - tx - 6
    y = ly + 14
    d.text((tx, y), "GAMING  ·  LAUNCH DAY", font=font(SANS_B, 15), fill=RED)
    y = ly + 42
    y = draw_lines(d, tx, y, ["VICE CITY OPENS", "ITS GATES"], font(SERIF_B, 37), INK, 44)
    y += 6
    body = ("After 13 years, Rockstar's Grand Theft Auto VI launches "
            "worldwide today — rolling out at midnight in each region on "
            "PlayStation 5 and Xbox. Critics, whose embargo lifted "
            "yesterday, put it at 99 on Metacritic; pre-orders are "
            "near $1 billion.")
    y = draw_lines(d, tx, y, wrap(d, body, font(SANS, 16), twd), font(SANS, 16), INK, 21)
    y += 8
    hline(d, tx, x1 - 6, y, GREY, 1)
    y += 10
    y = draw_lines(d, tx, y, ["99 Metacritic  ·  $79.99  ·  PS5 + Xbox",
                            "Pre-orders near $1bn"],
                   font(SANS_B, 14), TEAL, 19)

    # ---- Grid 2x2 (y 466..846) ----
    gy = 466
    cell_w = (CW - 14) // 2
    cell_h = 184
    gap = 14

    def grid_cell(cx, cy, kicker, headline, body, art):
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], outline=RULE, width=2)
        art(cx + 8, cy + 8, 132, cell_h - 16)
        tx = cx + 152
        twd = cx + cell_w - tx - 10
        y = cy + 12
        d.text((tx, y), kicker, font=font(SANS_B, 13), fill=RED)
        y += 22
        y = draw_lines(d, tx, y, wrap(d, headline, font(SERIF_B, 21), twd),
                       font(SERIF_B, 21), INK, 25)
        y += 4
        draw_lines(d, tx, y, wrap(d, body, font(SANS, 13), twd),
                   font(SANS, 13), INK, 17)

    def art_flags(ax, ay, aw, ah):
        # three flags on poles: US, China, Russia
        d.rectangle([ax, ay, ax + aw, ay + ah], fill=(232, 226, 210))
        poles = [(ax + 16, 0), (ax + 62, 1), (ax + 108, 2)]
        cols = [[(178, 34, 52), (255, 255, 255), (60, 59, 110)],
                [(222, 41, 16), (255, 222, 0), (222, 41, 16)],
                [(255, 255, 255), (0, 57, 166), (213, 0, 50)]]
        for (px, _), bands in zip(poles, cols):
            d.line([(px, ay + 12), (px, ay + ah - 8)], fill=INK, width=2)
            for i, c in enumerate(bands):
                d.rectangle([px, ay + 12 + i * 12, px + 30, ay + 24 + i * 12], fill=c)
        d.rectangle([ax + 8, ay + ah - 26, ax + aw - 8, ay + ah - 8], fill=(90, 86, 76))
        d.text((ax + 8, ay + ah - 24), "APEC · SHENZHEN", font=font(SANS_B, 10), fill=(255, 255, 255))

    def art_scales(ax, ay, aw, ah):
        d.rectangle([ax, ay, ax + aw, ay + ah], fill=(222, 214, 196))
        cx, cy = ax + aw // 2, ay + 40
        d.line([(cx, cy), (cx, ay + ah - 30)], fill=INK, width=4)
        d.line([(cx - 38, cy), (cx + 38, cy)], fill=INK, width=4)
        for s in (-1, 1):
            ex = cx + s * 38
            d.line([(ex, cy), (ex, cy + 34)], fill=INK, width=2)
            d.polygon([(ex - 20, cy + 34), (ex + 20, cy + 34), (ex, cy + 62)],
                      outline=INK, width=2)
        d.ellipse([cx - 6, cy - 8, cx + 6, cy + 4], fill=INK)
        d.rectangle([ax + 8, ay + ah - 22, ax + aw - 8, ay + ah - 8], fill=INK)
        d.text((ax + 12, ay + ah - 20), "THE HAGUE", font=font(SANS_B, 11), fill=(255, 255, 255))

    def art_chart(ax, ay, aw, ah):
        d.rectangle([ax, ay, ax + aw, ay + ah], fill=(16, 42, 40))
        pts = [(ax + 12, ay + ah - 40), (ax + 36, ay + ah - 66), (ax + 58, ay + ah - 56),
               (ax + 82, ay + ah - 88), (ax + 108, ay + ah - 70), (ax + 122, ay + ah - 96)]
        d.line(pts, fill=(80, 220, 160), width=4, joint="curve")
        d.polygon([(ax + 108, ay + ah - 96), (ax + 122, ay + ah - 96), (ax + 122, ay + ah - 78)],
                  fill=(80, 220, 160))
        d.text((ax + 10, ay + 12), "ANT", font=font(SANS_B, 26), fill=(255, 255, 255))
        d.text((ax + 10, ay + 44), "$83  ▲", font=font(SANS_B, 20), fill=(80, 220, 160))
        d.text((ax + 10, ay + ah - 26), "NASDAQ DEBUT", font=font(SANS_B, 11), fill=(200, 220, 210))

    def art_storm(ax, ay, aw, ah):
        d.rectangle([ax, ay, ax + aw, ay + ah], fill=(196, 214, 222))
        cx, cy = ax + aw // 2, ay + ah // 2 - 6
        for r in (52, 40, 28, 16):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(20, 60, 110), width=5)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(20, 60, 110))
        d.rectangle([ax, ay + ah - 18, ax + aw, ay + ah], fill=(120, 90, 60))
        for rx in range(ax + 10, ax + aw - 6, 18):
            d.line([(rx, ay + 14), (rx - 6, ay + 30)], fill=(60, 90, 130), width=2)
        d.text((ax + 8, ay + ah - 16), "BAY OF BENGAL", font=font(SANS_B, 10), fill=(255, 255, 255))

    grid_cell(x0, gy, "SHENZHEN  ·  DIPLOMACY",
              "Three leaders, one room",
              "Trump, Xi and Putin meet today at APEC — the first-ever "
              "three-way summit. Ukraine, Iran, trade and nuclear arms on "
              "the table; no deal is expected.", art_flags)
    grid_cell(x0 + cell_w + gap, gy, "THE HAGUE  ·  JUSTICE",
              "The court decides today",
              "The ICJ reads its judgment in Gambia v. Myanmar at 10:00 — "
              "whether the state committed genocide against the Rohingya. "
              "A first-ever finding is on the table.", art_scales)
    grid_cell(x0, gy + cell_h + gap, "NEW YORK  ·  MARKETS",
              "ANT debuts on Nasdaq",
              "Anthropic priced its IPO at $83 — above its $70–78 range — "
              "in a 980m-share, $81bn offering. Trading in the Claude "
              "maker starts at today's open.", art_chart)
    grid_cell(x0 + cell_w + gap, gy + cell_h + gap, "BAY OF BENGAL  ·  WEATHER",
              "Akvan bears down",
              "The severe cyclone nears India's east coast: red alerts, "
              "extremely heavy rain today and tomorrow, landfall expected "
              "Friday between Narsapur and Puri.", art_storm)

    # ---- Ticker ----
    ty = 862
    d.rectangle([x0, ty, x1, ty + 62], fill=INK)
    d.text((x0 + 14, ty + 8), "ALSO TODAY:", font=font(SANS_B, 15), fill=(255, 210, 80))
    t1 = ("NASA confirms Voyager 1 one light-day away at a live event today  ·  "
          "Gulf on alert as the Iran file heads to Shenzhen")
    t2 = ("Pew: Islam on track to be the world's largest faith by 2035  ·  "
          "UK Covid inquiry publishes its Module 7 report")
    d.text((x0 + 14, ty + 28), t1, font=font(SANS, 13), fill=(255, 255, 255))
    d.text((x0 + 14, ty + 46), t2, font=font(SANS, 13), fill=(255, 255, 255))

    # ---- Footer ----
    fy = 936
    hline(d, x0, x1, fy, RULE, 1)
    centered(d, fy + 10, "Sources: AP · Reuters · NASA · IMD · Nasdaq · ICJ — all stories reported 19 November 2026",
             font(SANS, 12), GREY)
    centered(d, fy + 30, "THE WORLD IN ONE DAY — THURSDAY 19 NOVEMBER 2026",
             font(SANS_B, 12), GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
