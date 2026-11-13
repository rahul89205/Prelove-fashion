#!/usr/bin/env python3
"""Thrice Loved - generate flat vector product illustrations (SVG -> PNG via rsvg-convert)."""
import os, math, random, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SVG_DIR = os.path.join(ROOT, "svg")
OUT_DIR = os.path.join(ROOT, "..", "store-data", "product-images")
os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 1200, 1500

# ---------- helpers ----------
def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb2hex(r):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(x)))) for x in r)

def shade(h, f):
    """f>0 lighten, f<0 darken"""
    r = hex2rgb(h)
    if f >= 0:
        return rgb2hex([c + (255 - c) * f for c in r])
    return rgb2hex([c * (1 + f) for c in r])

def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

def P(d, fill, stroke=None, sw=3, op=None, extra=""):
    s = f'<path d="{d}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
    if op is not None:
        s += f' opacity="{op}"'
    return s + f" {extra}/>"

def ST(d, col="#EBDDB5", sw=3, dash="10 8", op=0.9):
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-dasharray="{dash}" stroke-linecap="round" opacity="{op}"/>')

def LN(d, col, sw=3, op=1.0):
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')

def C(cx, cy, r, fill, stroke=None, sw=2, op=None):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        s += f' opacity="{op}"'
    return s + "/>"

def mirror(inner):
    return f'<g transform="translate(1200,0) scale(-1,1)">{inner}</g>'

def button(cx, cy, r, col, ring=None):
    ring = ring or shade(col, -0.3)
    return (C(cx, cy, r, col, ring, 2) + C(cx, cy, r * 0.55, shade(col, -0.12), None) +
            C(cx - r * 0.3, cy - r * 0.3, r * 0.18, "#ffffff", None, op=0.5))

def rib_lines(p1, p2, p3, p4, n, col, sw=3, op=0.55):
    out = []
    for i in range(1, n):
        t = i / n
        a, b = lerp(p1, p2, t), lerp(p4, p3, t)
        out.append(LN(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", col, sw, op))
    return "".join(out)

def twill(u, col="#ffffff", op=0.1, size=8, angle=45, sw=2):
    return (f'<pattern id="tw{u}" width="{size}" height="{size}" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate({angle})"><line x1="0" y1="0" x2="0" y2="{size}" '
            f'stroke="{col}" stroke-opacity="{op}" stroke-width="{sw}"/></pattern>')

def herring(u, col="#ffffff", op=0.08):
    return (f'<pattern id="hb{u}" width="14" height="14" patternUnits="userSpaceOnUse">'
            f'<path d="M0,14 L7,2 L14,14" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="2"/></pattern>')

# ---------- garments (each centred ~ x=600) ----------
def jacket(u):
    base = "#4A6A94"; dk = shade(base, -0.3); st = "#E6D3A3"
    body_d = "M438,352 L522,326 Q600,380 678,326 L762,352 L792,430 L778,1128 Q600,1160 422,1128 L408,430 Z"
    half = (
        P("M432,362 C380,400 300,720 232,930 L345,978 C395,820 445,650 485,520 Z", shade(base, -0.05), dk) +
        P("M232,930 L345,978 L336,1032 L220,984 Z", shade(base, -0.2), dk) +
        ST("M238,948 L342,994", st) + ST("M432,372 Q455,470 450,600", st)
    )
    pocket = (
        P("M468,556 L566,556 L566,652 L468,652 Z", base, dk) + ST("M474,562 L560,562 L560,646 L474,646 Z", st, 2.5) +
        P("M468,560 L566,560 L566,612 L517,638 L468,612 Z", shade(base, -0.08), dk) +
        ST("M476,568 L558,568 L558,608 L517,628 L476,608 Z", st, 2.5) + button(517, 604, 10, "#D4B46A")
    )
    s = f"<defs>{twill(u)}</defs>"
    s += half + mirror(half)
    s += P(body_d, base, dk)
    s += P(body_d, f"url(#tw{u})", None)
    s += P("M522,326 Q600,400 678,326 L600,470 Z", shade(base, -0.55))
    s += pocket + mirror(pocket)
    s += P("M422,1092 L778,1092 L778,1128 Q600,1160 422,1128 Z", shade(base, -0.12), dk)
    s += ST("M426,1100 L774,1100", st)
    s += ST("M424,640 L428,1090", st)
    s += mirror(ST("M424,640 L428,1090", st))
    col = P("M520,326 L598,356 L600,468 L528,440 L470,356 Z", shade(base, -0.1), dk) + \
        ST("M524,340 L592,366 L594,454 L532,430", st, 2.5)
    s += col + mirror(col)
    s += ST("M578,476 L578,1100", st) + ST("M622,476 L622,1100", st)
    for y in (520, 650, 780, 910, 1040):
        s += button(600, y, 15, "#D4B46A")
    return s

def jumper(u):
    base = "#C65D3B"; dk = shade(base, -0.3); lt = shade(base, 0.22)
    sl_pts = ((250, 1010), (352, 1038), (338, 1098), (234, 1068))
    half = (
        P("M436,384 C360,430 290,790 250,1010 L352,1038 C400,870 452,670 482,540 Z", shade(base, -0.05), dk) +
        P("M250,1010 L352,1038 L338,1098 L234,1068 Z", shade(base, -0.18), dk) +
        rib_lines(*sl_pts, 7, dk, 3, 0.6)
    )
    body_d = "M436,372 Q520,340 540,352 Q600,430 660,352 Q680,340 764,372 L794,440 L780,1092 L420,1092 L406,440 Z"
    s = f'<defs><pattern id="rb{u}" width="10" height="10" patternUnits="userSpaceOnUse"><line x1="5" y1="0" x2="5" y2="10" stroke="{dk}" stroke-opacity=".14" stroke-width="3"/></pattern></defs>'
    s += half + mirror(half)
    s += P(body_d, base, dk) + P(body_d, f"url(#rb{u})", None)
    # cables
    for cx in (546, 600, 654):
        d = f"M{cx},520 " + "".join("q14,20 0,40 q-14,20 0,40 " for _ in range(6))
        s += LN(d, dk, 8, 0.28) + LN(d, lt, 5, 0.55)
    # hem
    s += P("M420,1092 L780,1092 L784,1166 L416,1166 Z", shade(base, -0.15), dk)
    s += rib_lines((420, 1092), (780, 1092), (784, 1166), (416, 1166), 26, dk, 3, 0.55)
    # neck
    s += P("M540,352 Q600,432 660,352 Q600,374 540,352 Z", shade(base, -0.6))
    s += P("M528,348 Q600,452 672,348 L702,358 Q600,496 498,358 Z", shade(base, -0.12), dk)
    s += LN("M520,356 Q600,470 680,356", dk, 3, 0.35)
    return s

def jeans(u):
    base = "#5B7DA8"; dk = shade(base, -0.32); st = "#E3C98A"
    outline = "M440,330 L760,330 L800,1250 L612,1250 L600,640 L588,1250 L400,1250 Z"
    s = f"<defs>{twill(u, op=0.1)}</defs>"
    s += P(outline, base, dk) + P(outline, f"url(#tw{u})", None)
    # fades
    s += '<ellipse cx="500" cy="520" rx="62" ry="95" fill="#ffffff" opacity=".10"/>'
    s += '<ellipse cx="700" cy="520" rx="62" ry="95" fill="#ffffff" opacity=".10"/>'
    s += '<ellipse cx="505" cy="890" rx="44" ry="80" fill="#ffffff" opacity=".08"/>'
    s += '<ellipse cx="695" cy="890" rx="44" ry="80" fill="#ffffff" opacity=".08"/>'
    # inner seam
    s += LN("M600,640 L590,1250", dk, 3, 0.55) + LN("M600,640 L612,1250", dk, 3, 0.55)
    # waistband
    s += P("M440,330 L760,330 L760,392 L440,392 Z", shade(base, -0.14), dk)
    s += ST("M446,384 L754,384", st, 2.5)
    for x in (470, 535, 665, 730):
        s += P(f"M{x-9},322 L{x+9},322 L{x+9},404 L{x-9},404 Z", shade(base, -0.24), dk, 2)
    s += button(600, 361, 15, "#C9B27A")
    # fly + pockets
    s += ST("M600,396 L600,530 Q600,566 566,560", st) + ST("M612,396 L612,520", st, 2.5)
    s += ST("M456,392 Q470,526 566,548", st) + ST("M744,392 Q730,526 636,548", st)
    s += LN("M456,392 Q472,520 566,548", dk, 3, 0.45) + LN("M744,392 Q728,520 636,548", dk, 3, 0.45)
    s += ST("M470,420 L520,426", st, 2.5) + ST("M730,420 L680,426", st, 2.5)
    # side seams
    s += ST("M446,400 L408,1240", st, 2.5) + ST("M754,400 L792,1240", st, 2.5)
    # whiskers
    for d in ("M520,610 Q585,640 650,606", "M510,630 Q580,664 660,626"):
        s += LN(d, "#ffffff", 3, 0.16)
    # hems
    s += ST("M404,1220 L586,1220", st, 2.5) + ST("M614,1220 L796,1220", st, 2.5)
    # back-pocket hint none; knee fades
    s += LN("M440,980 Q500,1000 575,982", dk, 3, 0.18) + LN("M625,982 Q700,1000 760,980", dk, 3, 0.18)
    return s

def dress(u):
    base = "#F4ECDA"; dk = shade(base, -0.24); mid = shade(base, -0.1)
    d = "M472,500 Q520,470 548,462 Q600,520 652,462 Q680,470 728,500 L716,760 L890,1240 Q600,1320 310,1240 L484,760 Z"
    s = f'<defs><clipPath id="cp{u}"><path d="{d}"/></clipPath></defs>'
    s += P("M505,320 L530,320 L548,462 L520,468 Z", mid, dk) + P("M695,320 L670,320 L652,462 L680,468 Z", mid, dk)
    s += P(d, base, dk)
    # fabric texture
    rnd = random.Random(5)
    tex = ""
    for _ in range(260):
        x, y = rnd.uniform(300, 900), rnd.uniform(470, 1300)
        l = rnd.uniform(14, 34)
        tex += f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+l:.0f}" y2="{y:.0f}" stroke="{dk}" stroke-opacity=".22" stroke-width="2"/>'
    s += f'<g clip-path="url(#cp{u})">{tex}'
    for i in range(-5, 6):
        xb = 600 + i * 80
        uu = (xb - 600) / 290
        yb = 1240 + 40 * (1 - uu * uu)
        xt = 600 + i * 18
        s += LN(f"M{xt},780 Q{(xt+xb)/2+i*3},{(780+yb)/2} {xb},{yb}", dk, 3, 0.32)
        s += LN(f"M{xt+9},780 Q{(xt+xb)/2+i*3+14},{(780+yb)/2} {xb+40},{yb}", "#ffffff", 4, 0.5)
    s += "</g>"
    # waistband
    s += P("M484,740 L716,740 L720,792 L480,792 Z", mid, dk) + ST("M486,752 L714,752", dk, 2.5, "8 7", 0.6)
    # bodice details
    s += LN("M472,500 Q520,470 548,462 Q600,520 652,462 Q680,470 728,500", dk, 5)
    s += LN("M600,520 L600,740", dk, 3, 0.35)
    for y in (560, 610, 660, 710):
        s += C(600, y, 8, shade(base, -0.28), shade(base, -0.4), 2)
    s += LN("M548,462 Q540,600 520,740", dk, 3, 0.3) + LN("M652,462 Q660,600 680,740", dk, 3, 0.3)
    s += LN("M716,820 L726,900", dk, 3, 0.5)
    return s

def trench(u):
    base = "#C9A47A"; dk = shade(base, -0.32); lt = shade(base, 0.14)
    half = (
        P("M432,364 C372,410 300,760 262,1040 L378,1068 C410,880 450,690 484,540 Z", shade(base, -0.04), dk) +
        P("M268,985 L388,1015 L380,1058 L260,1028 Z", shade(base, -0.16), dk) +
        P("M262,1040 L378,1068", "none", dk, 3) +
        ST("M440,380 C400,470 360,700 330,900", "#F0DDB8", 2.5) +
        P("M472,372 Q500,380 520,340 L526,372 L446,396 Z", "none", None)
    )
    body_d = "M432,360 L520,334 L600,420 L680,334 L768,360 L800,440 L846,1260 L354,1260 L400,440 Z"
    s = f"<defs>{twill(u, op=0.07, size=6)}</defs>"
    s += half + mirror(half)
    s += P(body_d, base, dk) + P(body_d, f"url(#tw{u})", None)
    # underlap edge
    s += LN("M530,620 L530,1260", dk, 4, 0.35) + ST("M538,640 L538,1250", "#F0DDB8", 2.5)
    # lapels
    lap = P("M520,334 L466,424 L506,452 L492,510 L552,640 L598,676 L600,430 Z", lt, dk) + \
        ST("M514,350 L474,426 L512,458 L498,514 L554,634", "#F0DDB8", 2.5)
    s += P("M520,334 Q600,400 680,334 L690,350 Q600,440 510,350 Z", shade(base, -0.14), dk)
    s += lap + mirror(lap)
    # epaulettes
    ep = P("M436,366 L520,342 L526,376 L446,402 Z", shade(base, -0.1), dk) + button(505, 366, 8, "#6B4B2A")
    s += ep + mirror(ep)
    # belt
    s += P("M382,800 L818,800 L822,852 L378,852 Z", shade(base, -0.14), dk) + ST("M384,811 L816,811", "#F0DDB8", 2.5)
    for x in (430, 770):
        s += P(f"M{x-10},794 L{x+10},794 L{x+10},858 L{x-10},858 Z", shade(base, -0.24), dk, 2)
    s += P("M640,846 L690,846 L700,990 L650,996 Z", shade(base, -0.14), dk)
    s += '<rect x="556" y="790" width="88" height="72" rx="10" fill="none" stroke="#B8A061" stroke-width="9"/>'
    s += LN("M600,792 L600,860", "#B8A061", 7)
    # pockets
    pk = LN("M446,940 L526,960", dk, 5) + ST("M446,950 L522,970", "#F0DDB8", 2.5)
    s += pk + mirror(pk)
    # buttons
    for y in (720, 920, 1050, 1180):
        s += button(580, y, 14, "#5C4026") + button(682, y, 14, "#5C4026")
    s += ST("M360,1236 L840,1236", "#F0DDB8", 2.5)
    return s

def tee(u):
    base = "#34383D"
    d = "M436,352 L522,330 Q600,420 678,330 L764,352 L912,530 L816,612 L778,566 L778,1110 L422,1110 L422,566 L384,612 L288,530 Z"
    s = f'<defs><clipPath id="cg{u}"><circle cx="600" cy="770" r="132"/></clipPath></defs>'
    s += P(d, base, shade(base, -0.5))
    s += P("M422,1000 Q600,1040 778,1000 L778,1110 L422,1110 Z", "#000000", None, op=0.1)
    hem = ST("M300,548 L388,626", "#6B7077", 2.5)
    s += hem + mirror(hem)
    s += ST("M424,1088 L776,1088", "#6B7077", 2.5)
    s += P("M522,330 Q600,432 678,330 L696,348 Q600,478 504,348 Z", shade(base, -0.45), shade(base, -0.6))
    # graphic
    s += f'<g clip-path="url(#cg{u})">'
    s += C(600, 770, 132, "#D9A441") + C(600, 770, 92, "#C65D3B") + C(600, 770, 52, "#F6F1E7")
    for y, h in ((788, 6), (810, 10), (836, 14), (866, 20), (900, 28)):
        s += f'<rect x="440" y="{y}" width="320" height="{h}" fill="{base}"/>'
    rnd = random.Random(2)
    for _ in range(70):
        x, y = rnd.uniform(470, 730), rnd.uniform(640, 900)
        s += C(f"{x:.0f}", f"{y:.0f}", rnd.uniform(1.5, 4), base, None, op=0.6)
    s += "</g>"
    s += LN("M560,470 Q600,490 640,470", "#ffffff", 3, 0.08)
    return s

def skirt(u):
    base = "#7F9FB3"; dk = shade(base, -0.32)
    n = 16
    s = ""
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        xt0, xt1 = 480 + 240 * t0, 480 + 240 * t1
        xb0, xb1 = 300 + 600 * t0, 300 + 600 * t1
        yb0 = 1230 + (6 if i % 2 else 0)
        yb1 = 1230 + (6 if (i + 1) % 2 else 0)
        fill = shade(base, -0.1) if i % 2 else shade(base, 0.08)
        s += P(f"M{xt0:.1f},372 L{xt1:.1f},372 L{xb1:.1f},{yb1} L{xb0:.1f},{yb0} Z", fill, None)
        s += LN(f"M{xt0:.1f},372 L{xb0:.1f},{yb0}", dk, 2.5, 0.45)
    s += P("M480,372 L720,372 L900,1236 L300,1236 Z", "none", dk, 3)
    s += P("M474,300 L726,300 L722,378 L478,378 Z", shade(base, -0.2), dk)
    s += ST("M480,364 L720,364", "#D9E4EC", 2.5)
    s += button(600, 336, 13, "#E8DCC8")
    s += LN("M705,380 L722,520", dk, 3, 0.5)
    return s

def bag(u):
    base = "#9A5B34"; dk = shade(base, -0.34); lt = shade(base, 0.2); gold = "#C9A24A"
    strap = "M412,660 C380,260 820,260 788,660"
    s = f'<defs><linearGradient id="lg{u}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".14"/></linearGradient></defs>'
    s += f'<path d="{strap}" fill="none" stroke="{dk}" stroke-width="44" stroke-linecap="round"/>'
    s += f'<path d="{strap}" fill="none" stroke="{base}" stroke-width="34" stroke-linecap="round"/>'
    s += f'<path d="{strap}" fill="none" stroke="#E6C79C" stroke-width="2.5" stroke-dasharray="9 8" stroke-linecap="round" opacity=".9"/>'
    s += P("M390,630 L438,630 L434,708 L394,708 Z", dk, None)
    s += P("M762,630 L810,630 L806,708 L766,708 Z", dk, None)
    body = "M360,690 Q360,650 400,650 L800,650 Q840,650 840,690 L850,1080 Q850,1110 820,1110 L380,1110 Q350,1110 350,1080 Z"
    s += P(body, base, dk) + P(body, f"url(#lg{u})", None)
    s += P("M350,1060 L850,1060 L850,1080 Q850,1110 820,1110 L380,1110 Q350,1110 350,1080 Z", dk, None, op=0.35)
    flap = "M360,660 L840,660 L836,840 Q834,900 770,915 L640,945 Q600,962 560,945 L430,915 Q366,900 364,840 Z"
    s += P(flap, shade(base, 0.06), dk, 4) + P(flap, f"url(#lg{u})", None)
    s += f'<path d="{flap}" transform="translate(600,720) scale(.93) translate(-600,-720)" fill="none" stroke="#E6C79C" stroke-width="2.5" stroke-dasharray="9 8" opacity=".85"/>'
    s += P("M600,930 L600,990", "none", dk, 22) + P("M600,930 L600,990", "none", base, 16)
    s += '<rect x="560" y="900" width="80" height="62" rx="12" fill="none" stroke="%s" stroke-width="10"/>' % gold
    s += LN("M600,904 L600,958", gold, 8) + C(600, 931, 6, shade(gold, -0.3))
    s += ST("M372,1090 L828,1090", "#E6C79C", 2.5, "9 8", 0.7)
    return s

def scarf(u):
    base = "#C65D3B"; mus = "#D9A441"; cream = "#F6F1E7"; dk = shade(base, -0.3)
    d = ("M470,290 C430,480 530,640 480,860 C440,1020 500,1130 470,1230 L770,1230 "
         "C800,1130 740,1020 780,860 C830,640 730,480 770,290 Z")
    s = f'<defs><clipPath id="cp{u}"><path d="{d}"/></clipPath>{twill(u, op=0.1, size=7, angle=35)}'
    s += f'<linearGradient id="lg{u}" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".2"/><stop offset=".25" stop-color="#000" stop-opacity="0"/><stop offset=".75" stop-color="#fff" stop-opacity=".0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient></defs>'
    # fringe
    for yy, sgn in ((290, -1), (1230, 1)):
        x0, x1 = (470, 770) if yy == 290 else (470, 770)
        for i in range(0, 22):
            x = x0 + i * (x1 - x0) / 21
            dx = (i - 10.5) * 1.1
            s += LN(f"M{x:.1f},{yy} L{x+dx:.1f},{yy + sgn * 62}", shade(base, -0.05) if i % 3 else mus, 6, 1)
    s += f'<g clip-path="url(#cp{u})">' + f'<rect x="380" y="280" width="500" height="960" fill="{base}"/>'
    y = 330
    while y < 1230:
        s += f'<rect x="380" y="{y}" width="500" height="34" fill="{cream}"/>'
        s += f'<rect x="380" y="{y+46}" width="500" height="14" fill="{mus}"/>'
        y += 160
    s += f'<path d="{d}" fill="url(#tw{u})"/><path d="{d}" fill="url(#lg{u})"/></g>'
    s += P(d, "none", dk, 3)
    s += LN("M520,300 C500,520 590,700 540,900 C510,1020 540,1120 525,1220", "#ffffff", 3, 0.18)
    return s

def hoodie(u):
    base = "#A9B8A0"; dk = shade(base, -0.34); lt = shade(base, 0.16)
    sl = ((262, 1030), (376, 1058), (364, 1112), (250, 1084))
    half = (
        P("M452,420 C370,470 300,800 262,1030 L376,1058 C410,880 456,690 490,560 Z", shade(base, -0.05), dk) +
        P("M262,1030 L376,1058 L364,1112 L250,1084 Z", shade(base, -0.16), dk) +
        rib_lines(*sl, 7, dk, 3, 0.55)
    )
    s = f'<defs>{twill(u, op=0.08, size=5, angle=0)}</defs>'
    s += P("M468,396 Q470,226 600,214 Q730,226 732,396 Z", shade(base, -0.14), dk)
    s += half + mirror(half)
    body_d = "M446,408 L545,420 Q600,470 655,420 L754,408 L842,480 L826,1110 L374,1110 L358,480 Z"
    s += P(body_d, base, dk) + P(body_d, f"url(#tw{u})", None)
    s += P("M486,396 Q490,262 600,246 Q710,262 714,396 Q600,478 486,396 Z", lt, dk)
    s += P("M520,396 Q524,296 600,280 Q676,296 680,396 Q600,452 520,396 Z", shade(base, -0.58), None)
    s += ST("M498,396 Q502,270 600,256 Q698,270 702,396", "#F2F4EE", 2.5)
    # drawstrings
    for x, sx in ((566, 1), (634, -1)):
        s += LN(f"M{x},440 Q{x-sx*8},530 {x-sx*2},620", "#F6F1E7", 7)
        s += f'<rect x="{x-sx*2-5}" y="612" width="10" height="30" rx="4" fill="{dk}"/>'
        s += C(x - sx * 4, 436, 6, dk)
    # pouch
    s += P("M468,820 L732,820 L764,1030 L436,1030 Z", shade(base, -0.07), dk)
    s += LN("M468,820 L444,930", dk, 4, 0.7) + LN("M732,820 L756,930", dk, 4, 0.7)
    s += ST("M476,832 L724,832 L752,1020 L448,1020 Z", "#EEF1E8", 2.5, "9 8", 0.7)
    s += P("M374,1110 L826,1110 L830,1176 L370,1176 Z", shade(base, -0.16), dk)
    s += rib_lines((374, 1110), (826, 1110), (830, 1176), (370, 1176), 30, dk, 3, 0.55)
    s += ST("M376,480 L392,1100", "#EEF1E8", 2.5, op=0.6) + ST("M824,480 L808,1100", "#EEF1E8", 2.5, op=0.6)
    return s

def blazer(u):
    base = "#1F3D2F"; dk = shade(base, -0.5); lt = shade(base, 0.2); st = "#6E8F7C"
    half = (
        P("M434,362 C376,410 306,780 270,1050 L378,1076 C410,890 452,700 486,540 Z", shade(base, 0.02), dk) +
        P("M270,1050 L378,1076 L372,1100 L262,1072 Z", shade(base, -0.1), dk, 2) +
        ST("M284,1020 L388,1046", st, 2.5)
    )
    for t in (0.0, 0.5, 1.0):
        pass
    body_d = "M440,352 L525,330 L600,400 L675,330 L760,352 L796,430 L806,1160 L394,1160 L404,430 Z"
    s = f"<defs>{herring(u)}</defs>"
    s += half + mirror(half)
    for (x, y) in ((296, 1030), (322, 1040), (348, 1050)):
        s += button(x, y, 7, "#D4C9A8")
    for (x, y) in ((904, 1030), (878, 1040), (852, 1050)):
        s += button(x, y, 7, "#D4C9A8")
    s += P(body_d, base, dk) + P(body_d, f"url(#hb{u})", None)
    s += P("M524,330 Q600,420 676,330 L690,356 L600,742 L510,356 Z", "#F4ECDA", "#cdbf9d", 2)
    s += P("M524,330 L600,398 L676,330 L668,352 L600,430 L532,352 Z", shade(base, -0.12), dk)
    lap = P("M522,332 L452,408 L498,436 L488,488 L600,742 Z", lt, dk) + ST("M458,414 L500,440 L490,486 L596,736", st, 2.5)
    s += lap + mirror(lap)
    s += LN("M600,742 L600,1080 Q604,1152 660,1162", dk, 4)
    s += button(600, 775, 15, "#C9BE9A") + button(600, 890, 15, "#C9BE9A")
    # pockets
    flap = P("M440,960 L548,966 L548,1006 L440,1000 Z", shade(base, 0.05), dk) + ST("M446,968 L542,973", st, 2.5)
    s += flap + mirror(flap)
    s += P("M652,640 L732,650 L728,672 L648,662 Z", dk, None)
    s += P("M660,640 L690,632 L722,642 L690,652 Z", "#F4ECDA", None)
    s += ST("M398,1140 L802,1140", st, 2.5)
    return s

def overshirt(u):
    base = "#7E8559"; dk = shade(base, -0.34); lt = shade(base, 0.12); st = "#D8D2A8"
    half = (
        P("M432,362 C380,400 300,740 244,960 L356,1002 C400,830 448,660 486,520 Z", shade(base, -0.04), dk) +
        P("M244,960 L356,1002 L346,1054 L232,1012 Z", shade(base, -0.16), dk) +
        ST("M248,974 L352,1016", st, 2.5) + button(300, 1012, 7, "#D8D2A8") +
        ST("M432,372 Q455,470 450,600", st, 2.5)
    )
    body_d = "M438,352 L522,328 Q600,372 678,328 L762,352 L796,430 L790,1140 Q600,1196 410,1140 L404,430 Z"
    s = f'<defs><pattern id="cv{u}" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0,0 L6,6 M6,0 L0,6" stroke="#fff" stroke-opacity=".07" stroke-width="1.5"/></pattern></defs>'
    s += half + mirror(half)
    s += P(body_d, base, dk) + P(body_d, f"url(#cv{u})", None)
    s += P("M522,328 Q600,380 678,328 L600,460 Z", shade(base, -0.55))
    pk = (P("M458,600 L552,600 L552,702 L458,702 Z", base, dk) + ST("M464,606 L546,606 L546,696 L464,696 Z", st, 2.5) +
          P("M458,600 L552,600 L552,642 L505,666 L458,642 Z", shade(base, -0.08), dk) + button(505, 634, 10, "#D8D2A8"))
    s += pk + mirror(pk)
    s += P("M584,452 L616,452 L616,1176 L584,1176 Z", lt, dk, 2) + ST("M588,458 L588,1170", st, 2.5) + ST("M612,458 L612,1170", st, 2.5)
    for y in (500, 620, 740, 860, 980, 1100):
        s += button(600, y, 11, "#E4DFC0")
    col = P("M522,328 L598,364 L598,452 L536,432 L494,372 Z", lt, dk) + ST("M524,342 L590,372 L590,444 L540,426", st, 2.5)
    s += col + mirror(col)
    s += ST("M410,1118 Q600,1174 790,1118", st, 2.5)
    s += ST("M424,640 L420,1100", st, 2.5) + mirror(ST("M424,640 L420,1100", st, 2.5))
    return s

# ---------- registry ----------
PRODUCTS = [
    ("vintage-denim-jacket", jacket, "#EBDCC4", 745),
    ("merino-knit-jumper", jumper, "#DCE5D6", 750),
    ("high-waist-straight-jeans", jeans, "#F4E6D8", 790),
    ("linen-summer-dress", dress, "#B9C7B1", 800),
    ("classic-trench-coat", trench, "#D3DFE6", 800),
    ("vintage-graphic-tee", tee, "#F1DFAE", 730),
    ("pleated-midi-skirt", skirt, "#F6F1E7", 765),
    ("leather-crossbody-bag", bag, "#C7D3C0", 685),
    ("wool-blend-scarf", scarf, "#C9D8E0", 760),
    ("oversized-fleece-hoodie", hoodie, "#F3E6D3", 700),
    ("tailored-wool-blazer", blazer, "#E9D3C6", 745),
    ("canvas-overshirt", overshirt, "#DDE3E8", 745),
]

DEFS = ('<filter id="sh" x="-20%" y="-20%" width="140%" height="150%">'
        '<feDropShadow dx="0" dy="16" stdDeviation="16" flood-color="#1B1B1B" flood-opacity=".20"/></filter>')

def product_svg(handle, fn, bg, cy):
    # centre garment vertically around y=750
    dy = 750 - cy
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{DEFS}<radialGradient id="vg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity=".07"/></radialGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="{bg}"/><rect width="{W}" height="{H}" fill="url(#vg)"/>'
            f'<g filter="url(#sh)" transform="translate(600,750) scale(1.2) translate(-600,-750) translate(0,{dy})">{fn(handle[:6].replace("-", ""))}</g></svg>')

def hero_svg():
    items = [
        (blazer, 940, 430, 0.50, 6, 745, "bl"),
        (jacket, 330, 430, 0.56, -7, 745, "jk"),
        (jeans, 1260, 800, 0.50, 5, 790, "jn"),
        (jumper, 690, 800, 0.52, -4, 750, "ju"),
        (bag, 330, 940, 0.50, 6, 685, "bg"),
    ]
    g = ""
    for fn, cx, cy, sc, rot, ny, uid in items:
        g += (f'<g filter="url(#sh)" transform="translate({cx},{cy}) rotate({rot}) scale({sc}) translate(-600,-{ny})">'
              f'{fn(uid)}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200">'
            f'<defs>{DEFS}</defs><rect width="1600" height="1200" fill="#F6F1E7"/>'
            f'<circle cx="900" cy="620" r="520" fill="#E8DCC8" opacity=".55"/>'
            f'<circle cx="1400" cy="200" r="190" fill="#DCE5D6" opacity=".8"/>'
            f'<circle cx="170" cy="1080" r="150" fill="#F1DFAE" opacity=".7"/>{g}</svg>')

def render(svg_text, name, w, h):
    svg_path = os.path.join(SVG_DIR, name + ".svg")
    png_path = os.path.join(OUT_DIR, name + ".png")
    with open(svg_path, "w") as f:
        f.write(svg_text)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", png_path, svg_path], check=True)

if __name__ == "__main__":
    only = set(sys.argv[1:])
    for handle, fn, bg, cy in PRODUCTS:
        if only and handle not in only:
            continue
        render(product_svg(handle, fn, bg, cy), handle, W, H)
        print("ok", handle)
    if not only or "hero-flatlay" in only:
        render(hero_svg(), "hero-flatlay", 1600, 1200)
        print("ok hero-flatlay")
