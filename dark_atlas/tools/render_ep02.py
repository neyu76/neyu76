"""render_ep02.py — EP02 "Belsnickel" (Pennsylvania, USA) in the Dark Atlas Tales style, Milo narration.
Usage: python -I render_ep02.py <dark_atlas_dir> [stills "t1,t2,..."]
Built from render_ep01.py (approved standard): same engine/style/captions/cut rhythm, new scenes + style.json palette.
Culture markers: stone farmhouse with window candles, red bank barn with hex signs, covered bridge, Pennsylvania Dutch
interior (plank walls, wood stove, Fraktur, Christmas tree with candles), 1827 Philadelphia (State House steeple), emigrant ship.
"""
import sys, os, json, math, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from style import *

ROOT = sys.argv[1]; EP = os.path.join(ROOT, "EP02_belsnickel")
FB = os.path.join(ROOT, "fonts", "Oswald-Bold.ttf"); FR = os.path.join(ROOT, "fonts", "Oswald-Regular.ttf")
SERIF = next((f for f in ("C:/Windows/Fonts/georgiab.ttf",  # Windows: Georgia Bold
                          "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf",
                          "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                          "/Library/Fonts/Georgia Bold.ttf", "/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
              if os.path.exists(f)), "C:/Windows/Fonts/georgiab.ttf")
words = [w for s in json.load(open(os.path.join(EP, "voice_milo_transcript.json"), encoding="utf-8")) for w in s["words"]]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
def T(word, n=1, end=False):
    k = 0
    for w in words:
        if norm(w["w"]) == norm(word):
            k += 1
            if k == n: return w["e"] if end else w["s"]
    raise KeyError((word, n))
VOICE_END = words[-1]["e"]; END = VOICE_END + 0.75

# ---------------- palette (style.json) ----------------
STY = json.load(open(os.path.join(EP, "style.json"), encoding="utf-8"))
tup = lambda k: tuple(STY[k])
FUR_T, FUR_B, FUR_D, FUR_L = tup("fur_top"), tup("fur_bot"), tup("fur_dark"), tup("fur_light")
SOOT, SOOT_D = tup("soot_face"), tup("soot_face_d")
SHIRT, TRIM = tup("child_shirt"), tup("child_trim")
CANDLE, SNOWC, BARN = tup("candle"), tup("snow"), tup("barn_red")
HEXC = [tuple(c) for c in STY["hex_colors"]]
SKIN = (206, 170, 138); SKIN_D = (178, 142, 112)
BEARD, BEARD_D = (84, 76, 66), (56, 50, 44)
NIGHT_T, NIGHT_B = (7, 10, 17), (26, 36, 52)
SN_T, SN_B = (78, 92, 118), (44, 54, 74)          # moonlit snow, kept dim (captions sit at 60-75 % height)
WARM_WIN = (214, 160, 86)
WOOD_T, WOOD_B = (52, 36, 26), (34, 24, 18)
DK = (8, 8, 11)
def dim(c, k): return tuple(int(v * k) for v in c[:3])

# ================= helpers =================
def jag(a, b, n, amp, seed=0):
    """points a->b with every other point pushed down by ~amp (ragged fur hem)."""
    r = random.Random(seed); out = []
    for i in range(n + 1):
        t = i / n; x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
        if i % 2 == 1: y += amp * r.uniform(0.6, 1.3); x += r.uniform(-0.3, 0.3) * amp
        out.append((x, y))
    return out

def tufts(P, cx, cy, rx, ry, n, cols, w, seed=0, ln=1.0):
    r = random.Random(seed)
    for _ in range(n):
        a = r.uniform(0, 2 * math.pi); d = math.sqrt(r.random())
        x = cx + math.cos(a) * rx * d; y = cy + math.sin(a) * ry * d
        L = r.uniform(10, 26) * ln * (w / 4); ang = math.radians(r.uniform(60, 120))
        P.line([(x, y), (x + math.cos(ang) * L * 0.5, y + math.sin(ang) * L)], r.choice(cols), w)

FLAKE = glow_sprite(0, 0, 7, (226, 232, 246), power=1.3, res=2)
def snowfall(n, box, seed):
    """falling snow: flakes wrap vertically inside box."""
    r = random.Random(seed); y0, y1 = box[1], box[3]
    fl = [(r.uniform(box[0], box[2]), r.uniform(y0, y1), r.uniform(0.6, 1.6), r.uniform(0, 6.28)) for _ in range(n)]
    def items(lt, speed=70, op=0.55):
        its = []
        for (x, y, s, ph) in fl:
            yy = y0 + ((y - y0) + lt * speed * s) % (y1 - y0); xx = x + 14 * math.sin(lt * 0.9 + ph)
            its.append(Item(FLAKE, pos=(xx, yy), add=True, opacity=op * min(1.0, s), scale=s, anchor=(xx, yy)))
        return its
    return items

def embers(n, box, seed):
    r = random.Random(seed); y0, y1 = box[1], box[3]
    fl = [(r.uniform(box[0], box[2]), r.uniform(y0, y1), r.uniform(0.5, 1.3), r.uniform(0, 6.28)) for _ in range(n)]
    E = glow_sprite(0, 0, 8, (255, 150, 60), power=1.4, res=2)
    def items(lt):
        its = []
        for (x, y, s, ph) in fl:
            yy = y1 - ((y1 - y) + lt * 60 * s) % (y1 - y0); xx = x + 20 * math.sin(lt * 1.3 + ph)
            its.append(Item(E, pos=(xx, yy), add=True, opacity=0.45 + 0.3 * math.sin(lt * 7 + ph), scale=s, anchor=(xx, yy)))
        return its
    return items

def flick(lt, seed=0.0, depth=0.25):
    v = 1.0
    for a, b in [(1.3, 1.42), (1.5, 1.55), (3.1, 3.2), (4.4, 4.46)]:
        if a + seed < lt < b + seed: v = depth
    return v
def candle_flk(lt, ph=0.0): return 0.82 + 0.10 * math.sin(lt * 9 + ph) + 0.06 * math.sin(lt * 23 + ph * 2)

def hex_sign(P, x, y, r, k=0.78):
    """Pennsylvania Dutch barn star: ring, cream disc, 8-point star in alternating colours."""
    P.circ(x, y, r, dim(HEXC[2], k)); P.circ(x, y, r * 0.86, dim(HEXC[3], k * 0.8))
    for i in range(8):
        a = math.radians(i * 45 - 90); a1 = math.radians(i * 45 - 90 - 16); a2 = math.radians(i * 45 - 90 + 16)
        P.poly([(x, y), (x + math.cos(a1) * r * 0.36, y + math.sin(a1) * r * 0.36), (x + math.cos(a) * r * 0.8, y + math.sin(a) * r * 0.8),
                (x + math.cos(a2) * r * 0.36, y + math.sin(a2) * r * 0.36)], dim(HEXC[i % 2], k))
    P.circ(x, y, r * 0.14, dim(HEXC[2], k))

def stone_wall(P, box, seed, base=(70, 72, 76), k=1.0):
    x0, y0, x1, y1 = box; r = random.Random(seed)
    P.rect(box, dim(base, 0.75 * k))
    y = y0
    while y < y1:
        hh = r.uniform(26, 44); x = x0 - r.uniform(0, 40)
        while x < x1:
            ww = r.uniform(40, 90); c = dim(base, k * r.uniform(0.82, 1.08))
            P.rrect((max(x0, x + 3), y + 3, min(x1, x + ww - 3), min(y1, y + hh - 3)), 6, c); x += ww
        y += hh

def bare_tree(P, x, base, h, col, seed):
    r = random.Random(seed)
    def br(x0, y0, ang, L, w, d):
        x1 = x0 + math.sin(ang) * L; y1 = y0 - math.cos(ang) * L
        P.line([(x0, y0), (x1, y1)], col, w)
        if d > 0:
            for da in (-r.uniform(0.3, 0.6), r.uniform(0.3, 0.6)): br(x1, y1, ang + da, L * r.uniform(0.62, 0.78), w * 0.62, d - 1)
    P.line([(x, base), (x, base - h * 0.35)], col, h * 0.05); br(x, base - h * 0.35, r.uniform(-0.1, 0.1), h * 0.3, h * 0.04, 5)

def window_lit(P, x0, y0, w, h, col=WARM_WIN, frame=(30, 24, 20), candle=True):
    P.rect((x0 - 8, y0 - 8, x0 + w + 8, y0 + h + 8), frame); P.rect((x0, y0, x0 + w, y0 + h), col)
    P.rect((x0 + w / 2 - 3, y0, x0 + w / 2 + 3, y0 + h), frame); P.rect((x0, y0 + h / 2 - 3, x0 + w, y0 + h / 2 + 3), frame)
    if candle:
        cx = x0 + w / 2; P.rect((cx - 7, y0 + h - 36, cx + 7, y0 + h), (236, 220, 180)); P.ell((cx - 6, y0 + h - 56, cx + 6, y0 + h - 34), (255, 236, 170))

# ================= scenery =================
def farmhouse(P, x0, base, w, h, seed, k=1.0):
    stone_wall(P, (x0, base - h, x0 + w, base), seed, (78, 78, 82), 0.85 * k)
    P.poly([(x0 - 30, base - h), (x0 + w + 30, base - h), (x0 + w * 0.5, base - h - h * 0.55)], dim((30, 30, 36), k))     # gable roof
    P.poly([(x0 - 30, base - h), (x0 + w + 30, base - h), (x0 + w + 20, base - h - 12), (x0 - 20, base - h - 12)], dim(SN_T, 1.15 * k))
    P.poly([(x0 + 10, base - h - 14), (x0 + w * 0.5, base - h - h * 0.55), (x0 + w * 0.5, base - h - h * 0.55 + 18), (x0 + 30, base - h - 14)], dim(SN_T, 1.2 * k))
    for cxk in (0.12, 0.88):                                                                       # end chimneys
        cx = x0 + w * cxk; P.rect((cx - 18, base - h - h * 0.55 * (1 - abs(cxk - 0.5) * 2) - 70, cx + 18, base - h), dim((64, 62, 64), k))
    for i in range(4):
        wx = x0 + w * (0.1 + i * 0.22); window_lit(P, wx, base - h * 0.78, w * 0.12, h * 0.26)
        if i != 1: window_lit(P, wx, base - h * 0.4, w * 0.12, h * 0.26, candle=i != 2)
    P.rect((x0 + w * 0.33, base - h * 0.42, x0 + w * 0.43, base), dim((46, 30, 22), k))                  # door

def bank_barn(P, x0, base, w, h, k=1.0):
    stone_wall(P, (x0, base - h * 0.35, x0 + w, base), 77, (74, 74, 78), 0.8 * k)
    P.rect((x0, base - h, x0 + w, base - h * 0.35), dim(BARN, 0.72 * k))
    for xx in np.arange(x0 + 20, x0 + w, 24): P.line([(xx, base - h), (xx, base - h * 0.35)], dim(BARN, 0.58 * k), 2)
    P.poly([(x0 - 26, base - h), (x0 + w + 26, base - h), (x0 + w * 0.5, base - h - h * 0.5)], dim((28, 26, 30), k))
    P.poly([(x0 - 26, base - h), (x0 + w + 26, base - h), (x0 + w + 14, base - h - 12), (x0 - 14, base - h - 12)], dim(SN_T, 1.15 * k))
    for hx in (0.25, 0.75): hex_sign(P, x0 + w * hx, base - h * 0.74, h * 0.13, 0.8 * k)            # hex signs
    dx0, dx1 = x0 + w * 0.38, x0 + w * 0.62; dy0, dy1 = base - h * 0.6, base - h * 0.35
    P.rect((dx0, dy0, dx1, dy1), dim(BARN, 0.55 * k)); P.line([(dx0, dy0), (dx1, dy1)], dim((200, 190, 170), 0.6 * k), 5); P.line([(dx1, dy0), (dx0, dy1)], dim((200, 190, 170), 0.6 * k), 5)
    P.rect((dx0, dy0, dx1, dy1 - (dy1 - dy0) + 6), dim((200, 190, 170), 0.6 * k))

def covered_bridge(P, cx, base, w, h, col):
    P.rect((cx - w / 2, base - h, cx + w / 2, base), col)
    P.poly([(cx - w / 2 - 20, base - h), (cx + w / 2 + 20, base - h), (cx, base - h - h * 0.55)], col)
    P.poly([(cx - w * 0.28, base), (cx - w * 0.28, base - h * 0.62), (cx, base - h * 0.82), (cx + w * 0.28, base - h * 0.62), (cx + w * 0.28, base)], (4, 4, 6))   # dark tunnel mouth
    P.poly([(cx - w / 2 - 20, base - h), (cx + w / 2 + 20, base - h), (cx + w / 2 + 10, base - h - 10), (cx - w / 2 - 10, base - h - 10)], dim(SN_T, 1.1))

def rail_fence(P, x0, x1, y, h, col, seed):
    r = random.Random(seed); x = x0; up = True
    while x < x1:
        nx = x + r.uniform(110, 150)
        for k in (0.25, 0.55, 0.85): P.line([(x, y - h * k + (12 if up else -12)), (nx, y - h * k + (-12 if up else 12))], col, 9)
        P.line([(nx, y), (nx, y - h)], col, 10); up = not up; x = nx

def hills(P, y, amp, col_t, col_b, seed, bottom):
    r = random.Random(seed); ph = r.uniform(0, 6); pts = [(P.x0, bottom)]
    for x in np.linspace(P.x0, P.x1, 40): pts.append((x, y - amp * (0.6 * math.sin(x / 260 + ph) + 0.4 * math.sin(x / 120 + ph * 2))))
    pts.append((P.x1, bottom)); P.gpoly(pts, col_t, col_b, y - amp, bottom)

def pa_farm(seed=1, moon_xy=(880, 300)):
    P = Painter((-160, -120, 1240, 2040), res=1.0)
    P.gfill(NIGHT_T, (32, 42, 60)); stars(P, (-160, -120, 1240, 900), 160, 40 + seed)
    hills(P, 1000, 40, (52, 62, 82), (40, 48, 64), seed, 1200)
    for i in range(14): bare_tree(P, -140 + i * 105 + (seed * 37) % 60, 985, 90 + (i * 29) % 50, (24, 28, 38), i + seed)
    haze(P, 1010, 90, (34, 44, 62), 120)
    hills(P, 1090, 26, SN_T, SN_B, seed + 3, 2040)
    farmhouse(P, -60, 1150, 470, 250, seed)
    bank_barn(P, 600, 1140, 520, 330)
    rail_fence(P, -160, 1240, 1480, 120, (22, 20, 22), seed)
    bare_tree(P, 1100, 1900, 900, (12, 12, 16), 9 + seed)
    P.gpoly([(-160, 1820), (1240, 1820), (1240, 2040), (-160, 2040)], (10, 10, 14, 0), (4, 4, 6, 255))
    bg = P.sprite()
    md, mg, ga = moon(moon_xy[0], moon_xy[1], 82, res=1.4)
    wins = [glow_sprite(-60 + 470 * (0.1 + i * 0.22) + 470 * 0.06, 1150 - 250 * 0.65, 70, WARM_WIN, power=1.6) for i in range(4)]
    return dict(bg=bg, md=md, mg=mg, ga=ga, wins=wins)

def farm_items(A, lt):
    return [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"])] + [Item(g, add=True, opacity=0.45 * candle_flk(lt, i)) for i, g in enumerate(A["wins"])]

def interior(door_open=False, cold=False, tree=False):
    """Pennsylvania Dutch room: plank walls, wood stove, window candle, Fraktur, plank floor."""
    P = Painter((-60, -60, 1140, 1980), res=1.0)
    wt, wb = ((30, 32, 40), (22, 24, 30)) if cold else (WOOD_T, WOOD_B)
    P.gfill(wt, wb)
    for x in range(-60, 1140, 72): P.line([(x, -60), (x, 1160)], dim(wb, 0.7), 3)
    P.rect((-60, 1150, 1140, 1980), dim(wb, 0.9))
    VP = (540, 620)
    for i in range(-10, 11):
        xb = 540 + i * 170; xt = VP[0] + (xb - VP[0]) * (1150 - VP[1]) / (1980 - VP[1])
        P.line([(xt, 1150), (xb, 1980)], dim(wb, 0.6), 3)
    for yy in (1230, 1360, 1560, 1840): P.line([(-60, yy), (1140, yy)], dim(wb, 0.75), 2)
    P.rect((-60, 1140, 1140, 1158), dim(wb, 0.55))
    # window with candle (left)
    P.rect((70, 340, 340, 740), (26, 20, 16))
    P.gpoly([(86, 356), (324, 356), (324, 724), (86, 724)], (18, 26, 42), (44, 54, 74))
    P.rect((86, 640, 324, 724), dim(SN_T, 1.1))
    for (fx, fy) in [(120, 400), (200, 460), (290, 420), (150, 560), (260, 600), (230, 380)]: P.circ(fx, fy, 3, (200, 210, 230))
    P.rect((200, 356, 210, 724), (26, 20, 16)); P.rect((86, 535, 324, 545), (26, 20, 16))
    P.rect((60, 740, 350, 760), (40, 28, 20))
    P.rect((196, 690, 214, 742), (226, 214, 180)); P.ell((198, 664, 212, 692), (255, 230, 160))
    # door (centre)
    P.rect((430, 330, 690, 1150), (20, 14, 10))
    if door_open:
        P.gpoly([(446, 346), (674, 346), (674, 1150), (446, 1150)], (22, 30, 46), (48, 58, 78))
        P.rect((446, 980, 674, 1150), dim(SN_T, 1.0)); stars(P, (446, 346, 674, 700), 12, 5, a=140)
        P.poly([(446, 346), (500, 380), (500, 1110), (446, 1150)], (40, 28, 20))                         # door leaf swung in
    else:
        P.rect((446, 346, 674, 1150), (46, 32, 22))
        for yy in (420, 740, 1060): P.rect((470, yy, 650, yy + 16), (36, 24, 16))
        P.circ(650, 760, 9, (110, 90, 60))
    # Fraktur (decorated birth/house blessing) right of the door
    P.rect((740, 420, 930, 640), (44, 30, 20)); P.rect((752, 432, 918, 628), (140, 124, 94))
    P.circ(835, 520, 32, (150, 50, 42)); P.poly([(803, 528), (867, 528), (835, 586)], (150, 50, 42))      # heart
    for sx in (-1, 1): P.ell((835 + sx * 56 - 14, 470, 835 + sx * 56 + 14, 510), (180, 140, 50)); P.line([(835 + sx * 56, 510), (835 + sx * 56, 600)], (60, 90, 50), 4)
    # wood stove (right)
    P.rect((952, -60, 980, 760), (18, 18, 20)); P.rrect((870, 760, 1080, 1060), 16, (20, 20, 22)); P.rect((880, 1060, 900, 1140), (16, 16, 18)); P.rect((1050, 1060, 1070, 1140), (16, 16, 18))
    P.rect((910, 900, 1040, 930), (230, 110, 40)); P.rect((870, 750, 1080, 770), (30, 30, 34))
    # shelf with crocks
    P.rect((40, 230, 360, 246), (40, 28, 20))
    for i, cx in enumerate((80, 150, 230, 310)): P.rrect((cx - 24, 160 + (i % 2) * 14, cx + 24, 230), 10, (96, 84, 66) if i % 2 else (70, 60, 50))
    P.gpoly([(-60, 1760), (1140, 1760), (1140, 1980), (-60, 1980)], (6, 6, 8, 0), (4, 4, 6, 255))
    bg = P.sprite()
    g_win = glow_sprite(205, 680, 150, CANDLE, power=1.5); g_stove = glow_sprite(975, 915, 260, (230, 110, 40), power=1.6)
    g_door = beam_sprite(560, 700, 560, 1700, 230, 700, (150, 176, 220), 0.30, 0.0, res=0.4, blur=50) if door_open else None
    return dict(bg=bg, gw=g_win, gs=g_stove, gd=g_door)

def int_items(A, lt, door_op=1.0):
    its = [Item(A["bg"]), Item(A["gw"], add=True, opacity=0.6 * candle_flk(lt)), Item(A["gs"], add=True, opacity=0.5 * candle_flk(lt, 2))]
    if A["gd"] is not None: its.append(Item(A["gd"], add=True, opacity=door_op))
    return its

def floor_bg(cold=False):
    P = Painter((-60, -60, 1140, 1980), res=1.0)
    a, b = ((34, 36, 46), (26, 28, 36)) if cold else ((72, 50, 34), (58, 40, 28))
    P.gfill(dim(a, 0.7), b)
    VP = (540, -1400)
    xs = [540 + i * 150 for i in range(-9, 10)]
    for j, (xa, xb) in enumerate(zip(xs[:-1], xs[1:])):
        ta = VP[0] + (xa - VP[0]) * (-60 - VP[1]) / (1980 - VP[1]); tb = VP[0] + (xb - VP[0]) * (-60 - VP[1]) / (1980 - VP[1])
        c = a if j % 2 else b
        P.gpoly([(ta, -60), (tb, -60), (xb, 1980), (xa, 1980)], dim(c, 0.75), c)
        P.line([(ta, -60), (xa, 1980)], dim(b, 0.45), 4)
        r = random.Random(j)
        for _ in range(2):
            yy = r.uniform(0, 1900); fa = (yy - VP[1]) / (1980 - VP[1])
            x0 = VP[0] + (xa - VP[0]) * fa; x1 = VP[0] + (xb - VP[0]) * fa; P.line([(x0, yy), (x1, yy)], dim(b, 0.5), 3)
            P.circ(x0 + 14, yy + 10, 3, dim(b, 0.4))
    P.gpoly([(-60, -60), (1140, -60), (1140, 400), (-60, 400)], (4, 4, 6, 220), (4, 4, 6, 0))
    bg = P.sprite()
    pool = glow_sprite(540, 900, 760, (160, 180, 220) if cold else CANDLE, power=1.4)
    return bg, pool

def snow_road():
    VX, HY = 560, 1000
    P = Painter((-160, -120, 1240, 2040), res=1.0)
    P.gfill(NIGHT_T, (32, 42, 60)); stars(P, (-160, -120, 1240, 900), 150, 61)
    hills(P, HY, 30, (50, 60, 80), (40, 48, 64), 7, 1100)
    haze(P, HY + 10, 90, (34, 44, 62), 120)
    P.gpoly([(-160, HY), (1240, HY), (1240, 2040), (-160, 2040)], SN_T, SN_B)
    P.gpoly([(VX - 40, HY), (VX + 40, HY), (1100, 2040), (20, 2040)], (54, 62, 80), (40, 46, 60))         # road (tracked snow)
    for k in (-1, 1): P.line([(VX + k * 14, HY), (VX + k * 260, 2040)], (36, 42, 56), 10)                  # sleigh ruts
    covered_bridge(P, VX, HY + 8, 150, 70, (22, 22, 28))
    for side in (-1, 1):
        for i in range(7):
            t = (i + 1) / 8; x = VX + side * (70 + 900 * t ** 1.7); y = HY + (2040 - HY) * t ** 1.7; bare_tree(P, x, y, 140 + 1200 * t ** 1.7, (14, 15, 20), i * 3 + side)
    for i in range(10):                                                                                       # fence posts along the right
        t = (i + 1) / 11; x = VX + 60 + 640 * t ** 1.6; y = HY + 10 + (2040 - HY) * t ** 1.6; hh = 12 + 160 * t ** 1.6
        P.line([(x, y), (x, y - hh)], (18, 18, 22), 3 + 12 * t)
    farmhouse(P, 140, 990, 110, 60, 3, 0.8)
    P.gpoly([(-160, 1820), (1240, 1820), (1240, 2040), (-160, 2040)], (10, 10, 14, 0), (4, 4, 6, 255))
    md, mg, ga = moon(300, 330, 76, res=1.4)
    return dict(bg=P.sprite(), md=md, mg=mg, ga=ga, VX=VX, HY=HY)

# ================= characters =================
def belsnickel_side(P, x, feet, h, phase=0.0, switches=True, sack=True, sil=False):
    """hunched side view facing right: ragged fur coat to the shins, sack on the back, fur cap, soot face, beard,
    bundle of switches hanging from the front hand, heavy boots. h = cap top to sole."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    ft, fb, fd, fl = (DK,) * 4 if sil else (FUR_T, FUR_B, FUR_D, FUR_L)
    if not sil: P.ell((X(-230), Y(14), X(230), Y(-16)), (0, 0, 0, 100))
    a = math.sin(phase * 2 * math.pi)
    for s, lx in ((1, -40), (-1, 30)):
        bx = lx + a * s * 60; lift = max(0, a * s) * 34
        P.rect((X(bx - 6), Y(230), X(bx + 44), Y(40 + lift)), DK if sil else (30, 26, 24))
        P.rrect((X(bx - 20), Y(66 + lift), X(bx + 82), Y(lift)), 14 * k, DK if sil else (16, 14, 13))
    if sack:
        P.ell((X(-270), Y(930), X(-50), Y(560)), DK if sil else (92, 78, 56))
        P.poly([(X(-210), Y(920)), (X(-150), Y(1000)), (X(-110), Y(910))], DK if sil else (80, 66, 46))
        if not sil:
            P.line([(X(-120), Y(900)), (X(10), Y(820))], (64, 52, 36), 9 * k)
            for i in range(5): P.line([(X(-250 + i * 40), Y(700 + (i % 2) * 40)), (X(-230 + i * 40), Y(640 + (i % 2) * 40))], (74, 62, 44), 4 * k)
    top = [(X(-120), Y(860)), (X(-30), Y(900)), (X(60), Y(870)), (X(118), Y(790)), (X(140), Y(500)), (X(180), Y(170))]
    hem = jag((X(180), Y(170)), (X(-200), Y(150)), 14, 46 * k, seed=3)
    back = [(X(-200), Y(150)), (X(-180), Y(450)), (X(-160), Y(720))]
    P.gpoly(top + hem + back, ft, fb, Y(900), Y(110))
    if not sil:
        P.gpoly([(X(-120), Y(860)), (X(-60), Y(880)), (X(-110), Y(450)), (X(-140), Y(160)), (X(-200), Y(150)), (X(-180), Y(450)), (X(-160), Y(720))], fd, dim(fd, 0.8), Y(880), Y(150))
        tufts(P, X(-10), Y(520), 150 * k, 320 * k, 55, [dim(fl, 0.85), dim(ft, 1.12), fd], min(4.5 * k, 6), seed=4)
        P.line([(X(-175), Y(540)), (X(145), Y(560))], (64, 52, 36), 10 * k)                             # rope belt
    P.poly([(X(30), Y(850)), (X(118), Y(800)), (X(176), Y(570)), (X(120), Y(540))], fd if not sil else DK)   # sleeve
    if not sil: tufts(P, X(110), Y(680), 40 * k, 120 * k, 18, [fl, fb], 4 * k, seed=5)
    P.ell((X(122), Y(590), X(184), Y(520)), DK if sil else SOOT)                                           # hand
    if switches:
        r = random.Random(2)
        for i in range(11):
            ex = 150 + r.uniform(-50, 70); ey = 120 + r.uniform(-30, 60)
            P.line([(X(152 + r.uniform(-8, 8)), Y(560)), (X(ex), Y(ey))], DK if sil else r.choice([(60, 44, 30), (74, 56, 38), (50, 38, 28)]), r.uniform(3, 6) * k)
        if not sil: P.rect((X(132), Y(500), X(176), Y(476)), (120, 100, 70))
    # head
    P.ell((X(-60), Y(990), X(110), Y(800)), DK if sil else SOOT)
    P.poly([(X(96), Y(900)), (X(140), Y(870)), (X(104), Y(850))], DK if sil else SOOT)                       # nose
    beard = [(X(-10), Y(880)), (X(116), Y(850))] + jag((X(116), Y(850)), (X(20), Y(690)), 6, 30 * k, 7) + [(X(-20), Y(760))]
    P.poly(beard, DK if sil else BEARD)
    if not sil:
        for i in range(6): P.line([(X(20 + i * 16), Y(840)), (X(10 + i * 18), Y(720))], BEARD_D, 3 * k)
        P.circ(X(76), Y(920), 9 * k, (220, 206, 170)); P.circ(X(78), Y(920), 4 * k, (20, 16, 14))             # eye glint
        P.line([(X(52), Y(944)), (X(100), Y(934))], (12, 10, 10), 6 * k)
    P.chord((X(-90), Y(1040), X(130), Y(870)), 180, 360, ft)                                               # fur cap
    P.rect((X(-92), Y(958), X(132), Y(930)), fl if not sil else DK)
    if not sil: tufts(P, X(20), Y(990), 110 * k, 40 * k, 30, [fl, fd], 4 * k, seed=6, ln=0.8)

def belsnickel_front(P, x, feet, h, sil=False, sway=0.0, eyes=True, switches=True):
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    ft, fb, fd, fl = (DK,) * 4 if sil else (FUR_T, FUR_B, FUR_D, FUR_L)
    if not sil: P.ell((X(-280), Y(14), X(280), Y(-18)), (0, 0, 0, 110))
    for lx in (-80, 30):
        P.rect((X(lx), Y(220), X(lx + 50), Y(40)), DK if sil else (30, 26, 24)); P.rrect((X(lx - 14), Y(70), X(lx + 64), Y(0)), 14 * k, DK if sil else (16, 14, 13))
    top = [(X(-170), Y(860)), (X(-70), Y(920)), (X(70), Y(920)), (X(170), Y(860)), (X(230), Y(500)), (X(270 + sway * 0.4), Y(170))]
    hem = jag((X(270 + sway * 0.4), Y(170)), (X(-270 + sway * 0.4), Y(170)), 16, 50 * k, seed=8)
    P.gpoly(top + hem + [(X(-230), Y(500))], ft, fb, Y(920), Y(120))
    if not sil:
        P.line([(X(0), Y(900)), (X(sway * 0.3), Y(180))], fd, 5 * k)
        tufts(P, X(0), Y(540), 210 * k, 330 * k, 70, [dim(fl, 0.85), dim(ft, 1.12), fd], min(5 * k, 6), seed=9)
        P.line([(X(-215), Y(560)), (X(215), Y(560))], (64, 52, 36), 11 * k)
    P.poly([(X(160), Y(850)), (X(230), Y(800)), (X(250), Y(520)), (X(190), Y(500))], fd if not sil else DK)     # right sleeve
    P.ell((X(186), Y(530), X(252), Y(460)), DK if sil else SOOT)
    if switches:
        r = random.Random(4)
        for i in range(11):
            ex = 220 + r.uniform(-50, 60) + sway * 0.5; ey = 80 + r.uniform(-20, 60)
            P.line([(X(218 + r.uniform(-8, 8)), Y(500)), (X(ex), Y(ey))], DK if sil else r.choice([(60, 44, 30), (74, 56, 38), (50, 38, 28)]), r.uniform(3, 6) * k)
        if not sil: P.rect((X(196), Y(450), X(242), Y(426)), (120, 100, 70))
    P.poly([(X(-160), Y(850)), (X(-230), Y(800)), (X(-250), Y(520)), (X(-190), Y(500))], fd if not sil else DK)    # left sleeve
    P.ell((X(-252), Y(530), X(-186), Y(460)), DK if sil else SOOT)
    P.ell((X(-120), Y(1080), X(120), Y(840)), ft)                                                          # fur hood/cap
    P.ell((X(-70), Y(1010), X(70), Y(870)), DK if sil else SOOT)
    beard = [(X(-70), Y(930))] + jag((X(-70), Y(900)), (X(70), Y(900)), 2, 0) + jag((X(70), Y(900)), (X(0), Y(690)), 5, 36 * k, 3) + [(X(-60), Y(800))]
    P.poly(beard, DK if sil else BEARD)
    if not sil:
        for i in range(5): P.line([(X(-40 + i * 20), Y(880)), (X(-30 + i * 16), Y(740))], BEARD_D, 3 * k)
        tufts(P, X(0), Y(1050), 120 * k, 40 * k, 30, [fl, fd], 5 * k, seed=10, ln=0.8)
    if eyes:
        c = (196, 184, 150) if sil else (226, 214, 180)
        for ex in (-26, 26): P.ell((X(ex - 10), Y(960), X(ex + 10), Y(948)), c)

def child_front(P, x, feet, h, kind=0, sil=False, hands="side", fear=False):
    """1800s Pennsylvania Dutch children. kind 0: boy (shirt, suspenders, flat cap); kind 1: girl (dress, apron, bonnet)."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    c = lambda col: DK if sil else col
    if not sil: P.ell((X(-160), Y(14), X(160), Y(-14)), (0, 0, 0, 90))
    if kind == 0:
        for lx in (-70, 14): P.rect((X(lx), Y(420), X(lx + 56), Y(30)), c((40, 36, 42))); P.rrect((X(lx - 6), Y(40), X(lx + 70), Y(0)), 10 * k, c((18, 16, 16)))
        P.rrect((X(-110), Y(720), X(110), Y(400)), 40 * k, c(SHIRT))
        if not sil:
            for sx in (-50, 50): P.line([(X(sx), Y(720)), (X(sx * 0.8), Y(410))], dim(TRIM, 0.7), 8 * k)
            P.rect((X(-110), Y(440), X(110), Y(400)), (40, 36, 42))
    else:
        P.poly([(X(-100), Y(720)), (X(100), Y(720)), (X(170), Y(60)), (X(-170), Y(60))], c((90, 38, 34)))
        if not sil: P.poly([(X(-70), Y(560)), (X(70), Y(560)), (X(100), Y(110)), (X(-100), Y(110))], (128, 120, 104))
        for lx in (-60, 20): P.rrect((X(lx - 6), Y(64), X(lx + 56), Y(0)), 10 * k, c((18, 16, 16)))
    if hands == "side":
        for sx in (-1, 1): P.line([(X(sx * 110), Y(690)), (X(sx * 140), Y(430))], c(SHIRT if kind == 0 else (90, 38, 34)), 46 * k); P.circ(X(sx * 142), Y(410), 26 * k, c(SKIN))
    elif hands == "behind":
        for sx in (-1, 1): P.line([(X(sx * 110), Y(690)), (X(sx * 96), Y(500))], c(SHIRT if kind == 0 else (90, 38, 34)), 46 * k)
    elif hands == "reach":
        P.line([(X(-110), Y(690)), (X(-140), Y(430))], c(SHIRT if kind == 0 else (90, 38, 34)), 46 * k); P.circ(X(-142), Y(410), 26 * k, c(SKIN))
        P.line([(X(110), Y(690)), (X(250), Y(420))], c(SHIRT if kind == 0 else (90, 38, 34)), 46 * k); P.circ(X(262), Y(396), 28 * k, c(SKIN))
    P.rect((X(-30), Y(760), X(30), Y(700)), c(SKIN_D))
    P.ell((X(-100), Y(990), X(100), Y(750)), c(SKIN))
    if kind == 0:
        P.chord((X(-112), Y(1030), X(112), Y(880)), 180, 360, c((54, 48, 44))); P.ell((X(-130), Y(930), X(150), Y(900)), c((44, 40, 36)))
    else:
        P.chord((X(-130), Y(1040), X(130), Y(820)), 180, 360, c((120, 110, 96))); P.rect((X(-130), Y(935), X(-100), Y(800)), c((120, 110, 96))); P.rect((X(100), Y(935), X(130), Y(800)), c((120, 110, 96)))
    if not sil:
        for ex in (-36, 36): P.ell((X(ex - 11), Y(880), X(ex + 11), Y(856)), (240, 232, 220) if fear else (30, 22, 18)); P.circ(X(ex), Y(868), 6 * k, (20, 14, 12))
        if fear: P.ell((X(-16), Y(820), X(16), Y(784)), (60, 30, 26))
        else: P.line([(X(-18), Y(806)), (X(18), Y(806))], (120, 70, 60), 4 * k)

# ---------- portraits ----------
def portrait_bg(warm=True):
    P = Painter((-60, -60, 1140, 1980), res=1.0)
    P.gfill((6, 7, 10), (12, 12, 16)); P.glow(540, 860, 820, (84, 58, 30) if warm else (40, 50, 70), 1.0, 1.4)
    P.rect((930, -60, 958, 1980), (20, 16, 14) if warm else (16, 18, 24))
    return P.sprite()

def bel_portrait(mode="shadow"):
    """front portrait. mode: shadow (hood shadow, only eye glints) | soot (soot-black face visible) | reveal (grin)."""
    D = Painter((-60, 300, 1140, 1980), res=1.2)
    D.ell((40, 1240, 1040, 2260), FUR_D)
    tufts(D, 540, 1330, 470, 90, 110, [FUR_T, dim(FUR_L, 0.85), FUR_B], 6, seed=11, ln=1.3)
    D.ell((250, 400, 830, 1240), FUR_B)                                                                  # hood mass
    tufts(D, 540, 820, 290, 410, 90, [FUR_T, dim(FUR_L, 0.8), FUR_D], 6, seed=12, ln=1.1)
    beard = [(390, 960)] + jag((390, 980), (540, 1440), 6, 50, 13)[1:] + jag((540, 1440), (690, 980), 6, 50, 14)[1:] + [(690, 960)]
    D.poly(beard, BEARD)
    for i in range(10): D.line([(420 + i * 26, 1000), (430 + i * 22 - (i - 5) * 6, 1340 - abs(i - 5) * 20)], BEARD_D, 4)
    D.ell((372, 560, 708, 1050), SOOT)
    D.ell((420, 790, 490, 860), dim(SOOT, 1.45)); D.ell((590, 790, 660, 860), dim(SOOT, 1.45))           # cheek highlights
    D.poly([(518, 760), (562, 760), (590, 900), (540, 914), (490, 900)], dim(SOOT, 1.6))                  # nose
    D.ell((508, 892, 532, 906), SOOT_D); D.ell((548, 892, 572, 906), SOOT_D)
    for (sx, sy, sr) in [(450, 640, 40), (640, 690, 34), (470, 960, 30), (620, 950, 36)]: D.glow(sx, sy, sr, SOOT_D, 0.9, 1.0)   # soot smudges
    D.line([(426, 720), (508, 750)], (12, 10, 10), 12); D.line([(572, 750), (654, 720)], (12, 10, 10), 12)  # heavy brows, angled
    D.chord((300, 450, 780, 760), 180, 360, FUR_B); tufts(D, 540, 640, 230, 30, 60, [FUR_L, FUR_T], 6, seed=15, ln=1.2)   # cap rim
    if mode == "shadow":
        sh = Image.new("RGBA", D.img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        sd.ellipse(D.box((330, 520, 750, 1000)), fill=(4, 4, 6, 200)); sh = sh.filter(ImageFilter.GaussianBlur(40 * D.k))
        D.img = Image.alpha_composite(D.img, sh); D.d = ImageDraw.Draw(D.img)
    if mode == "reveal":
        top = [(420, 950), (470, 976), (540, 986), (610, 976), (660, 950)]
        bot = [(660, 950), (620, 1030), (540, 1052), (460, 1030), (420, 950)]
        D.poly(top + bot, (26, 10, 10))
        for i in range(8):
            tx = 446 + i * 25; dy = abs(i - 3.5) * 3
            D.rect((tx, 966 + dy * 0.6, tx + 20, 994 + dy * 0.2), (198, 184, 140)); D.rect((tx + 2, 1012 - dy, tx + 20, 1030 - dy * 1.2), (180, 166, 124))
        D.line(top, (14, 8, 8), 6); D.line(bot, (14, 8, 8), 6)
    else:
        D.line([(490, 960), (540, 968), (590, 960)], (16, 10, 10), 6)
    return D.sprite()

def bel_eyes(mode="calm", look=0.0):
    E = Painter((400, 740, 690, 840), res=2.0)
    for ex in (466, 614):
        cy = 790
        if mode == "glint":
            E.ell((ex - 30, cy - 10, ex + 30, cy + 10), (120, 110, 92)); E.circ(ex + 8 * look, cy, 9, (10, 8, 6)); E.circ(ex + 8 * look - 3, cy - 3, 4, (240, 230, 200))
        elif mode == "dead":
            E.ell((ex - 44, cy - 24, ex + 44, cy + 22), (20, 16, 16)); E.ell((ex - 34, cy - 16, ex + 34, cy + 16), (236, 232, 222)); E.circ(ex, cy, 6, (8, 4, 4))
        else:
            E.ell((ex - 40, cy - 15, ex + 40, cy + 15), (198, 186, 160)); E.circ(ex + 12 * look, cy + 1, 14, (40, 26, 16)); E.circ(ex + 12 * look, cy + 1, 6, (6, 4, 4))
            E.circ(ex + 12 * look - 5, cy - 4, 3, (240, 230, 210))
            E.line([(ex - 44, cy - 10), (ex, cy - 20), (ex + 44, cy - 10)], (10, 8, 8), 8)
    return E.sprite()

def child_portrait():
    D = Painter((0, 400, 1080, 1980), res=1.2)
    D.chord((90, 1340, 990, 2240), 180, 360, SHIRT); D.rect((90, 1790, 990, 1980), SHIRT)
    for sx in (-1, 1): D.line([(540 + sx * 190, 1380), (540 + sx * 230, 1980)], dim(TRIM, 0.7), 22)
    D.poly([(450, 1350), (630, 1350), (540, 1430)], (170, 160, 140))
    D.rect((480, 1180, 600, 1370), SKIN_D)
    D.ell((316, 700, 360, 860), SKIN_D); D.ell((720, 700, 764, 860), SKIN_D)
    D.ell((340, 560, 740, 1230), SKIN); D.pie((340, 560, 740, 1230), -90, 90, SKIN_D)
    D.rect((340, 640, 740, 700), (46, 30, 20))
    D.chord((310, 420, 770, 1000), 180, 360, (54, 48, 44)); D.ell((290, 680, 800, 760), (44, 40, 36))
    D.arc((410, 790, 500, 830), 200, 340, (40, 26, 18), 9); D.arc((580, 790, 670, 830), 200, 340, (40, 26, 18), 9)   # raised brows
    D.line([(546, 900), (530, 1000)], (150, 110, 84), 5); D.arc((520, 990, 560, 1012), 10, 170, (150, 110, 84), 5)
    D.ell((508, 1060, 572, 1120), (64, 30, 26))
    face = D.sprite()
    E = Painter((400, 830, 700, 930), res=2)
    for ex in (456, 624):
        cy = 880; E.ell((ex - 40, cy - 22, ex + 40, cy + 22), (238, 230, 218)); E.circ(ex, cy, 11, (40, 26, 16)); E.circ(ex, cy, 5, (6, 4, 4)); E.circ(ex - 4, cy - 4, 3, (255, 255, 255))
        E.arc((ex - 42, cy - 26, ex + 42, cy + 20), 195, 345, (24, 16, 12), 6)
    return face, E.sprite()

# ---------- props ----------
def arm_sprite(length=560, sleeve=SHIRT, skin=SKIN, w=110):
    P = Painter((-20, -w, length + 200, w), res=1.1)
    P.rrect((0, -w * 0.55, length, w * 0.55), w * 0.3, sleeve); P.rect((length - 30, -w * 0.58, length + 4, w * 0.58), dim(sleeve, 0.7))
    P.ell((length - 10, -w * 0.45, length + 110, w * 0.45), skin)
    for i, dy in enumerate((-0.30, -0.10, 0.10, 0.28)):
        L = (60, 70, 66, 52)[i]; P.rrect((length + 70, w * dy - 11, length + 90 + L, w * dy + 11), 10, skin)
    P.rrect((length + 20, -w * 0.62, length + 90, -w * 0.40), 10, SKIN_D)
    return P.sprite()

def candy_sprites():
    out = []
    P = Painter((-24, -24, 24, 24), res=2); P.circ(0, 0, 21, (190, 40, 38))
    for a in range(0, 360, 60): P.pie((-21, -21, 21, 21), a, a + 30, (226, 216, 200))
    P.circ(0, 0, 7, (190, 40, 38)); out.append(P.sprite())
    for col in ((214, 166, 50), (60, 130, 70), (176, 60, 110)):
        P = Painter((-44, -20, 44, 20), res=2); P.ell((-22, -16, 22, 16), col); P.poly([(-20, 0), (-42, -16), (-42, 16)], dim(col, 0.8)); P.poly([(20, 0), (42, -16), (42, 16)], dim(col, 0.8))
        P.line([(-8, -14), (-12, 14)], dim(col, 1.25), 3); out.append(P.sprite())
    P = Painter((-22, -18, 22, 18), res=2); P.ell((-20, -16, 20, 16), (104, 72, 44)); P.line([(-18, 0), (18, 0)], (70, 46, 28), 3); P.arc((-14, -12, 14, 12), 200, 340, (130, 92, 58), 2); out.append(P.sprite())
    P = Painter((-16, -16, 16, 16), res=2); P.circ(0, 0, 14, (220, 150, 60)); P.circ(-4, -4, 4, (250, 220, 170)); out.append(P.sprite())
    return out
CANDY = None

def scatter(n, src, area, t0, seed, dur=(0.35, 0.7), arc=(80, 220), drop=False):
    r = random.Random(seed); cs = []
    for i in range(n):
        x1 = r.uniform(area[0], area[2]); y1 = r.uniform(area[1], area[3])
        sx = src[0] + r.uniform(-40, 40) if not drop else x1 + r.uniform(-20, 20); sy = src[1] + r.uniform(-30, 30)
        cs.append(dict(x0=sx, y0=sy, x1=x1, y1=y1, t0=t0 + r.uniform(0, 0.25) + (i * 0.08 if drop else 0), d=r.uniform(*dur), h=0 if drop else r.uniform(*arc),
                       spr=r.randrange(6), rot=r.uniform(0, 360), spin=r.uniform(-500, 500), slide=r.uniform(10, 40) * r.choice((-1, 1)), sc=r.uniform(0.9, 1.3)))
    return cs

def candy_items(cs, lt, scale=1.0, persp=None):
    its = []
    for c in cs:
        if lt < c["t0"]: continue
        p = (lt - c["t0"]) / c["d"]
        if p < 1:
            pe = p * p if c["h"] == 0 else p
            x = c["x0"] + (c["x1"] - c["x0"]) * pe; y = c["y0"] + (c["y1"] - c["y0"]) * pe - c["h"] * math.sin(math.pi * p); rot = c["rot"] + c["spin"] * (lt - c["t0"])
        else:
            dt = lt - c["t0"] - c["d"]; b = 34 * math.exp(-dt * 5) * abs(math.sin(dt * 13))
            x = c["x1"] + c["slide"] * (1 - math.exp(-dt * 4)); y = c["y1"] - b; rot = c["rot"] + c["spin"] * c["d"] + c["spin"] * 0.15 * (1 - math.exp(-dt * 4))
        s = c["sc"] * scale * (persp(y) if persp else 1.0)
        its.append(Item(CANDY[c["spr"]], pos=(x, y), rot=rot, scale=s, anchor=(x, y)))
    return its

def switch_bundle(L=900):
    P = Painter((-40, -60, L + 60, 60), res=1.1); r = random.Random(3)
    for i in range(13):
        ey = r.uniform(-50, 50); P.line([(0, r.uniform(-8, 8)), (L * r.uniform(0.75, 1.0), ey)], r.choice([(118, 92, 62), (136, 108, 72), (100, 78, 54)]), r.uniform(5, 9))
        for _ in range(2):
            t = r.uniform(0.3, 0.9); P.line([(L * t, ey * t), (L * t + 40, ey * t + r.uniform(-24, 24))], (60, 44, 30), 3)
    P.rect((40, -18, 110, 18), (120, 100, 70)); P.rrect((-30, -34, 70, 34), 20, SOOT)
    return P.sprite()

# ================= SHOT BUILDERS =================
def mk(t0, t1, fn, dissolve=0.0): return dict(t0=t0, t1=t1, fn=fn, dz=dissolve)

def build_all():
    global CANDY
    CANDY = candy_sprites()
    S = []
    farm = pa_farm(1)
    sf_wide = snowfall(70, (-160, -200, 1240, 2040), 1)
    # S0 — "In Pennsylvania": snowy farm at night, stone farmhouse + hex-sign barn, snow, push in
    def s0(t):
        lt = t; p = lt / max(0.5, T("man"))
        return farm_items(farm, lt) + sf_wide(lt), (560, 1000 - 30 * p, 1.0 + 0.07 * EASE["sine"](p))
    S.append(mk(0, T("man"), s0))
    # S1 — "a man in a ragged fur coat": side view walking through the snow toward the house (camera tracks)
    SB = Painter((-160, -120, 1240, 2040), res=1.0); SB.gfill(NIGHT_T, (32, 42, 60)); stars(SB, (-160, -120, 1240, 900), 140, 71)
    hills(SB, 1150, 50, (50, 60, 80), (40, 48, 64), 2, 1300); farmhouse(SB, 700, 1260, 520, 300, 4)
    for i in range(6): bare_tree(SB, -100 + i * 140, 1190, 160 + (i * 41) % 80, (22, 26, 36), 30 + i)
    haze(SB, 1260, 100, (34, 44, 62), 110)
    SB.gpoly([(-160, 1300), (1240, 1300), (1240, 2040), (-160, 2040)], SN_T, SN_B)
    rail_fence(SB, -160, 1240, 1380, 110, (20, 20, 24), 5)
    SB.gpoly([(-160, 1840), (1240, 1840), (1240, 2040), (-160, 2040)], (10, 10, 14, 0), (4, 4, 6, 255)); side_bg = SB.sprite()
    s1md, s1mg, s1ga = moon(260, 360, 74, res=1.4)
    WALK = []
    for i in range(8):
        WP = Painter((-60, 640, 760, 1720), res=1.25); belsnickel_side(WP, 340, 1680, 1000, i / 8); WALK.append(WP.sprite())
    s1win = glow_sprite(700 + 520 * 0.32, 1260 - 300 * 0.65, 90, WARM_WIN, power=1.6)
    t1a, t1b = T("man"), T("walks")
    def s1(t):
        lt = t - t1a; x = -260 + lt * 120
        return [Item(side_bg), Item(s1mg, add=True, opacity=s1ga), Item(s1md), Item(s1win, add=True, opacity=0.5 * candle_flk(lt)),
                Item(WALK[int(lt * 6) % 8], pos=(x, 3 * abs(math.sin(lt * 6 * math.pi / 4))))] + sf_wide(lt), (440 + lt * 70, 1180, 1.05)
    S.append(mk(t1a, t1b, s1))
    # S2 — "walks into your house a few nights before Christmas": inside, the door, cold light, his silhouette fills the doorway
    room_open = interior(door_open=True)
    DS = Painter((300, 280, 820, 1170), res=1.4); belsnickel_front(DS, 560, 1150, 800, sil=True); door_sil = DS.sprite()
    sf_door = snowfall(26, (446, 346, 674, 1150), 3)
    t2a, t2b = T("walks"), T("and", 1)
    def s2(t):
        lt = t - t2a; p = lt / (t2b - t2a); op = ease_io(min(1, lt / 0.8))
        return int_items(room_open, lt, op) + sf_door(lt, 40, 0.45) + [Item(door_sil, opacity=op, scale=0.9 + 0.1 * ease_out(min(1, lt / 1.6)), anchor=(560, 1150))], (560, 900, 1.0 + 0.10 * EASE["sine"](p))
    S.append(mk(t2a, t2b, s2))
    # S3 — "and throws candy across the floor": plank floor, candies fly in, bounce, roll (camera low over the floor)
    fl_bg, fl_pool = floor_bg(False)
    t3a, t3b = T("and", 1), T("dont", 1)
    cs3 = scatter(18, (540, -200), (60, 900, 1020, 1500), T("throws") - t3a + 0.15, 3)
    persp = lambda y: 0.7 + 0.6 * (y - 400) / 1200
    def s3(t):
        lt = t - t3a; p = lt / (t3b - t3a)
        return [Item(fl_bg), Item(fl_pool, add=True, opacity=0.32 * candle_flk(lt))] + candy_items(cs3, lt, 1.4, persp), (540, 1060, 1.0 + 0.08 * p)
    S.append(mk(t3a, t3b, s3))
    # S4 — hook card
    f = ImageFont.truetype(FB, 160); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    hk = "DON'T GRAB IT."; fs = 160
    while d.textlength(hk, font=f) > 980: fs -= 4; f = ImageFont.truetype(FB, fs)
    d.text(((W - d.textlength(hk, font=f)) / 2, 780), hk, font=f, fill=(198, 38, 38, 255))
    hook = Sprite(np.asarray(lay).copy(), 1, 0, 0); g = np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).copy(); hookg = Sprite(g, 1, 0, 0)
    t4a, t4b = T("dont", 1), T("because", 1) - 0.05
    def s4(t):
        lt = t - t4a; dd = t4b - t4a; op = 1.0 if lt < dd - 0.3 else max(0, (dd - lt) / 0.3); s_ = 1 + 0.035 * lt / dd
        return [Item(hookg, add=True, opacity=0.8 * op, scale=s_, anchor=(540, 860)), Item(hook, opacity=op, scale=s_, anchor=(540, 860))], (540, 960, 1.0)
    S.append(mk(t4a, t4b, s4))
    # S5 — "Because he isn't giving you a gift. He's testing you." hooded portrait in shadow, only the eyes catch the light
    pbg = portrait_bg(True); bp_sh = bel_portrait("shadow"); e_gl = bel_eyes("glint"); e_gl2 = bel_eyes("glint", -0.8)
    emb = embers(24, (100, 600, 980, 1900), 5)
    t5a, t5b = T("because", 1), T("they", 1)
    def s5(t):
        lt = t - t5a; p = lt / (t5b - t5a)
        e = e_gl if lt < 1.6 else e_gl2
        return [Item(pbg, opacity=candle_flk(lt))] + emb(lt) + [Item(bp_sh), Item(e, opacity=0 if abs(lt - 1.0) < 0.06 else 1)], (540, 920, 1.0 + 0.08 * p)
    S.append(mk(t5a, t5b, s5))
    # S6 — title card (dissolve in): moon, covered bridge + barn silhouettes, Belsnickel silhouette walking with switches
    TP = Painter((-80, -80, 1160, 2000), res=1.1); TP.gfill((6, 8, 12), (22, 24, 30)); stars(TP, (-80, -80, 1160, 1100), 90, 31, a=90); tbg = TP.sprite()
    t_md, t_mg, t_ga = moon(540, 1090, 330, res=1.2, glow_r=2.0, glow_a=0.75)
    TF = Painter((-80, 900, 1160, 2000), res=1.1)
    TF.poly([(-80, 1600), (200, 1540), (420, 1430), (540, 1400), (660, 1430), (880, 1540), (1160, 1600), (1160, 2000), (-80, 2000)], (8, 9, 12))
    covered_bridge(TF, 120, 1560, 300, 120, (8, 9, 12))
    bx0, bb = 820, 1560; TF.rect((bx0, bb - 200, bx0 + 260, bb), (8, 9, 12)); TF.poly([(bx0 - 16, bb - 200), (bx0 + 276, bb - 200), (bx0 + 130, bb - 300)], (8, 9, 12))
    TF.circ(bx0 + 130, bb - 130, 40, (14, 15, 19)); TF.circ(bx0 + 130, bb - 130, 34, (8, 9, 12))                    # hex sign silhouette
    for i in range(8):
        a = math.radians(i * 45); TF.line([(bx0 + 130, bb - 130), (bx0 + 130 + math.cos(a) * 30, bb - 130 + math.sin(a) * 30)], (14, 15, 19), 4)
    bare_tree(TF, 660, 1440, 380, (8, 9, 12), 21)
    TF.gpoly([(-80, 1700), (1160, 1700), (1160, 2000), (-80, 2000)], (8, 9, 12, 0), (4, 4, 6, 255)); tfg = TF.sprite()
    lab = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    fr = ImageFont.truetype(FR, 30); fb = ImageFont.truetype(FB, 140)
    s_ = "P E N N S Y L V A N I A   ·   L E G E N D"
    d.rectangle([W / 2 - 22, 110, W / 2 + 22, 115], fill=(190, 46, 40, 255))
    d.text(((W - d.textlength(s_, font=fr)) / 2, 135), s_, font=fr, fill=(178, 172, 158, 255))
    d.text(((W - d.textlength("BELSNICKEL", font=fb)) / 2, 175), "BELSNICKEL", font=fb, fill=(228, 216, 194, 255))
    title = Sprite(np.asarray(lab).copy(), 1, 0, 0)
    sils = []
    for kk in range(8):
        SP = Painter((300, 880, 820, 1420), res=1.6); belsnickel_front(SP, 540, 1400, 470, sil=True, sway=14 * math.sin(kk / 8 * 2 * math.pi)); sils.append(SP.sprite())
    tb = beam_sprite(540, -100, 540, 1400, 300, 700, (200, 196, 180), 0.16, 0.0, res=0.4, blur=60)
    sf_title = snowfall(40, (-80, -80, 1160, 2000), 6)
    t6a, t6b = T("they", 1), T("german")
    def s6(t):
        lt = t - t6a; p = lt / (t6b - t6a); ta = min(1, max(0, (lt - 0.35) / 0.55))
        return [Item(tbg), Item(tb, add=True, opacity=0.9), Item(t_mg, add=True, opacity=t_ga), Item(t_md), Item(tfg), Item(sils[int(lt * 8) % 8], pos=(0, -3 * abs(math.sin(lt * 4))))] + sf_title(lt, 50, 0.4) + \
               [Item(title, opacity=ta, par=0.0, scale=1.03 - 0.03 * ta, anchor=(540, 260))], (540, 1000, 1.0 + 0.06 * EASE["sine"](p))
    S.append(mk(t6a, t6b, s6, dissolve=0.27))
    # S7a — "German families brought him": emigrant sailing ship at night on the Atlantic, bobbing
    SH_ = Painter((-160, -120, 1240, 2040), res=1.0); SH_.gfill(NIGHT_T, (30, 40, 58)); stars(SH_, (-160, -120, 1240, 1000), 170, 81)
    SH_.gpoly([(-160, 1100), (1240, 1100), (1240, 2040), (-160, 2040)], (24, 34, 50), (8, 12, 20)); haze(SH_, 1110, 80, (40, 52, 70), 110)
    sea_bg = SH_.sprite(); smd, smg, sga = moon(760, 420, 80, res=1.4)
    shine = beam_sprite(760, 1110, 760, 2000, 60, 300, (190, 180, 150), 0.35, 0.0, res=0.4, blur=30)
    SP_ = Painter((140, 520, 980, 1260), res=1.2)
    SP_.poly([(200, 1100), (940, 1100), (880, 1210), (270, 1210)], (14, 14, 18)); SP_.rect((200, 1080, 940, 1104), (22, 20, 22))
    for i, mx in enumerate((360, 560, 760)):
        hh = (420, 500, 400)[i]; SP_.rect((mx - 6, 1100 - hh, mx + 6, 1100), (14, 14, 18))
        for j in range(3):
            y0 = 1100 - hh + 30 + j * hh * 0.29; SP_.poly([(mx - 90 + j * 6, y0), (mx + 90 - j * 6, y0), (mx + 100 - j * 4, y0 + hh * 0.25), (mx - 100 + j * 4, y0 + hh * 0.25)], (70, 80, 98) if j % 2 == 0 else (60, 70, 88))
    SP_.line([(360, 700), (180, 1090)], (14, 14, 18), 3); SP_.line([(760, 720), (960, 1090)], (14, 14, 18), 3)
    for wx in (420, 520, 640): SP_.rect((wx, 1130, wx + 16, 1146), WARM_WIN)
    ship = SP_.sprite()
    FLAG = []                                                                                      # German black-red-gold flag on the mainmast, waving
    for i in range(8):
        FP = Painter((540, 560, 780, 740), res=2.0); x0, y0, fw, fh = 566, 604, 190, 114
        def fy(x, base, i=i): return base + 9 * math.sin((x - x0) / 46 - i / 8 * 2 * math.pi) * (x - x0) / fw
        xs = np.linspace(x0, x0 + fw, 24)
        for j, col in enumerate(((26, 26, 30), (196, 40, 36), (226, 184, 40))):
            ya, yb = y0 + fh * j / 3, y0 + fh * (j + 1) / 3
            FP.poly([(x, fy(x, ya)) for x in xs] + [(x, fy(x, yb)) for x in xs[::-1]], col)
        FP.line([(x, fy(x, y0)) for x in xs] + [(x0 + fw, fy(x0 + fw, y0 + fh))] + [(x, fy(x, y0 + fh)) for x in xs[::-1]], (150, 156, 176), 2.2)   # moonlit rim so the black band reads at night
        FP.rect((x0 - 6, 586, x0, 744), (14, 14, 18)); FP.circ(x0 - 3, 584, 6, (120, 110, 80))
        FLAG.append(FP.sprite())
    WV = []
    for j in range(3):
        WP_ = Painter((-400, 1100, 1640, 2040), res=0.8); r = random.Random(j)
        yb = 1180 + j * 260; pts = [(-400, 2040)]
        for x in np.linspace(-400, 1640, 60): pts.append((x, yb - 22 * math.sin(x / (90 + j * 40) + j) - 10 * math.sin(x / 37 + j)))
        pts.append((1640, 2040)); WP_.gpoly(pts, dim((26, 38, 56), 1 - j * 0.25), (6, 8, 14), yb - 30, 2040); WV.append(WP_.sprite())
    t7a, t7b = T("german"), T("pennsylvania", 2)
    def s7(t):
        lt = t - t7a; p = lt / (t7b - t7a)
        its = [Item(sea_bg), Item(smg, add=True, opacity=sga), Item(smd), Item(shine, add=True, opacity=0.6), Item(WV[0], pos=(-40 * lt % 200 - 100, 0)),
               Item(ship, pos=(-30 + 40 * lt, 6 * math.sin(lt * 1.8)), rot=2.2 * math.sin(lt * 1.5), anchor=(560 + 40 * lt, 1150)),
               Item(FLAG[int(lt * 10) % 8], pos=(-30 + 40 * lt, 6 * math.sin(lt * 1.8)), rot=2.2 * math.sin(lt * 1.5), anchor=(560 + 40 * lt, 1150))]
        its += [Item(WV[1], pos=(60 * lt % 300 - 150, 0)), Item(WV[2], pos=(-90 * lt % 400 - 200, 0))]
        return its, (560 + 40 * ease_io(p), 1020 - 120 * ease_io(p), 1.04 + 0.14 * ease_io(p))   # drift up toward the flag
    S.append(mk(t7a, t7b, s7))
    # S7b — "to Pennsylvania 200 years ago": the farm settlement (different framing), windows lighting up
    farm2 = pa_farm(2, moon_xy=(240, 330))
    t7c, t7d = T("pennsylvania", 2), T("by")
    def s7b(t):
        lt = t - t7c; p = lt / (t7d - t7c)
        return farm_items(farm2, lt) + sf_wide(lt + 3), (760 - 120 * p, 1020, 1.25 - 0.08 * p)
    S.append(mk(t7c, t7d, s7b))
    # S8a — "By 1827, a Philadelphia...": 1827 Philadelphia street, brick rowhouses, State House steeple, snow
    PH = Painter((-160, -80, 1240, 2000), res=1.0); PH.gfill(NIGHT_T, (30, 40, 56)); stars(PH, (-160, -80, 1240, 900), 140, 91)
    sx_ = 560                                                                                      # State House (Independence Hall) steeple
    PH.rect((sx_ - 70, 620, sx_ + 70, 1200), (26, 22, 26)); PH.rect((sx_ - 52, 520, sx_ + 52, 620), (40, 38, 42)); PH.circ(sx_, 570, 30, (150, 140, 110)); PH.circ(sx_, 570, 24, (40, 38, 42))
    PH.rect((sx_ - 40, 420, sx_ + 40, 520), (36, 34, 40)); PH.rect((sx_ - 26, 330, sx_ + 26, 420), (32, 30, 36)); PH.poly([(sx_ - 20, 330), (sx_ + 20, 330), (sx_, 180)], (30, 28, 34))
    r = random.Random(4); x = -160
    while x < 1240:
        bw = r.uniform(150, 210); hh = r.uniform(380, 480); col = (r.randint(60, 74), r.randint(30, 36), r.randint(28, 32))
        PH.rect((x, 1420 - hh, x + bw - 6, 1420), col); PH.rect((x - 4, 1420 - hh - 16, x + bw - 2, 1420 - hh), (26, 22, 24)); PH.rect((x, 1420 - hh - 22, x + bw - 6, 1420 - hh - 14), dim(SN_T, 1.1))
        for row in range(3):
            for c in range(3):
                wx = x + 22 + c * (bw - 50) / 3; wy = 1420 - hh + 40 + row * 120
                lit = r.random() < 0.45; PH.rect((wx, wy, wx + 34, wy + 64), WARM_WIN if lit else (24, 26, 34)); PH.rect((wx - 10, wy, wx - 3, wy + 64), (40, 34, 30)); PH.rect((wx + 37, wy, wx + 44, wy + 64), (40, 34, 30))
        x += bw
    PH.gpoly([(-160, 1420), (1240, 1420), (1240, 2000), (-160, 2000)], dim(SN_T, 0.9), SN_B)
    for i in range(80): PH.circ(r.uniform(-160, 1240), r.uniform(1450, 2000), r.uniform(4, 9), dim(SN_B, 0.8))
    for lx_ in (60, 1000): PH.rect((lx_ - 6, 1160, lx_ + 6, 1500), (14, 14, 18)); PH.rect((lx_ - 22, 1120, lx_ + 22, 1170), (20, 20, 24)); PH.rect((lx_ - 14, 1128, lx_ + 14, 1162), (255, 220, 150))
    PH.gpoly([(-160, 1820), (1240, 1820), (1240, 2000), (-160, 2000)], (10, 10, 14, 0), (4, 4, 6, 255)); phl = PH.sprite()
    lgl = [glow_sprite(lx_, 1145, 110, (255, 210, 140), power=1.6) for lx_ in (60, 1000)]
    pmd, pmg, pga = moon(880, 260, 66, res=1.4)
    t8a, t8b = T("by"), T("newspaper")
    def s8(t):
        lt = t - t8a; p = lt / (t8b - t8a)
        return [Item(phl), Item(pmg, add=True, opacity=pga), Item(pmd)] + [Item(g_, add=True, opacity=0.6 * candle_flk(lt, i)) for i, g_ in enumerate(lgl)] + sf_wide(lt + 5), (540, 900 + 60 * p, 1.12 - 0.08 * p)
    S.append(mk(t8a, t8b, s8))
    # S8b — "newspaper was already describing him": an old broadsheet by candlelight, woodcut of the fur figure
    NB = Painter((-60, -60, 1140, 1980), res=1.0); NB.gfill((14, 10, 8), (26, 18, 14)); nbg = NB.sprite()
    NP = Painter((120, 180, 960, 1200), res=1.2)
    NP.rect((150, 220, 930, 1170), (128, 112, 84)); NP.glow(540, 600, 600, (150, 134, 100), 0.8, 1.4)
    fsm = ImageFont.truetype(SERIF, int(64 * NP.k)); fss = ImageFont.truetype(SERIF, int(22 * NP.k))
    NP.d.text(NP.P(540, 300), "PHILADELPHIA", font=fsm, fill=(36, 28, 20, 255), anchor="mm")
    NP.line([(180, 350), (900, 350)], (50, 40, 30), 3); NP.line([(180, 392), (900, 392)], (50, 40, 30), 2)
    NP.d.text(NP.P(540, 372), "DECEMBER  ·  1827", font=fss, fill=(46, 36, 26, 255), anchor="mm")
    r = random.Random(8)
    for col in range(3):
        cx0 = 190 + col * 245
        for ln in range(26):
            yy = 420 + ln * 28
            if col == 1 and 520 < yy < 860: continue
            NP.rect((cx0, yy, cx0 + 215 * r.uniform(0.7, 1.0), yy + 9), (78, 66, 50))
        if col < 2: NP.line([(cx0 + 230, 410), (cx0 + 230, 1150)], (90, 78, 60), 2)
    NP.rect((440, 520, 650, 860), (110, 96, 72)); NP.rect((440, 520, 650, 860), (110, 96, 72))
    belsnickel_front(NP, 545, 850, 300, sil=True, eyes=False)
    for i in range(18): NP.line([(445, 525 + i * 18), (645, 525 + i * 18)], (100, 86, 64), 1)
    paper = NP.sprite()
    cg = glow_sprite(900, 200, 500, CANDLE, power=1.5)
    t8c, t8d = T("newspaper"), T("according")
    def s8b(t):
        lt = t - t8c; p = lt / (t8d - t8c)
        return [Item(nbg), Item(paper, rot=-3 + 1.0 * p, anchor=(540, 700)), Item(cg, add=True, opacity=0.35 * candle_flk(lt))], (560, 760 + 40 * p, 1.05 + 0.10 * EASE["sine"](p))
    S.append(mk(t8c, t8d, s8b))
    # S9 — "According to the legend, he comes before Santa": snowy road, he emerges from the covered bridge with a lantern (dissolve)
    road = snow_road()
    RW = []
    for i in range(8):
        RP = Painter((440, 820, 700, 1060), res=3); belsnickel_front(RP, 570, 1040, 200, sway=10 * math.sin(i / 8 * 2 * math.pi)); RW.append(RP.sprite())
    lant = glow_sprite(0, 0, 90, CANDLE, power=1.5)
    sf_road = snowfall(70, (-160, -200, 1240, 2040), 9)
    t9a, t9b = T("according"), T("his", 1)
    def s9(t):
        lt = t - t9a; p = lt / (t9b - t9a); sc = 0.25 + 0.9 * ease_io(p)
        y = road["HY"] + 20 + 160 * ease_io(p)
        return [Item(road["bg"]), Item(road["mg"], add=True, opacity=road["ga"]), Item(road["md"]),
                Item(lant, pos=(570 + 46 * sc, y - 100 * sc), add=True, opacity=0.6 * candle_flk(lt), scale=0.6 + sc, anchor=(570 + 46 * sc, y - 100 * sc)),
                Item(RW[int(lt * 6) % 8], scale=sc, anchor=(570, 1040), pos=(0, y - 1040))] + sf_road(lt), (560, 1060, 1.0 + 0.08 * p)
    S.append(mk(t9a, t9b, s9, dissolve=0.27))
    # S10 — "his face dark with soot": the soot-black face, embers drifting, push-in
    bp_soot = bel_portrait("soot"); e_calm = bel_eyes("calm"); e_calm_l = bel_eyes("calm", 0.6)
    t10a, t10b = T("his", 1), T("bundle") - 0.5
    def s10(t):
        lt = t - t10a; p = lt / (t10b - t10a)
        return [Item(pbg, opacity=candle_flk(lt))] + emb(lt + 2) + [Item(bp_soot), Item(e_calm if lt < 1.1 else e_calm_l, opacity=0 if abs(lt - 0.6) < 0.06 else 1)], (540, 860, 1.10 + 0.10 * EASE["sine"](p))
    S.append(mk(t10a, t10b, s10))
    # S11 — "a bundle of switches in his hand": fur sleeve, sooty hand gripping the switches, tilt down the bundle
    HB = Painter((-60, -60, 1140, 1980), res=1.0); HB.gfill((12, 9, 8), (22, 16, 12)); HB.glow(700, 600, 700, (90, 60, 30), 1.0, 1.5)
    HB.poly([(-60, -60), (520, -60), (620, 380), (440, 520), (-60, 300)], FUR_D); tufts(HB, 300, 160, 300, 220, 90, [FUR_T, dim(FUR_L, 0.85), FUR_B], 6, seed=31, ln=1.3)
    HB.ell((430, 300, 660, 520), SOOT); HB.ell((470, 330, 560, 400), dim(SOOT, 1.5))
    for i in range(4): HB.rrect((600, 320 + i * 44, 690, 360 + i * 44), 18, dim(SOOT, 1.2 + 0.1 * i))
    r = random.Random(7)
    for i in range(15):
        x0 = 560 + r.uniform(-30, 30); HB.line([(x0, 380), (x0 + r.uniform(-160, 160), 1980)], r.choice([(70, 52, 36), (86, 66, 44), (54, 40, 28)]), r.uniform(5, 10))
        for _ in range(3):
            tt = r.uniform(0.3, 0.95); yy = 380 + 1600 * tt; HB.line([(x0, yy), (x0 + r.uniform(-50, 50), yy + 50)], (64, 48, 32), 4)
    for yy in (560, 590, 620): HB.line([(500, yy), (630, yy + 6)], (130, 108, 74), 8)
    hb = HB.sprite()
    t11a, t11b = t10b, T("asks") - 0.3
    def s11(t):
        lt = t - t11a; p = lt / (t11b - t11a)
        cam = kf([(0, (560, 520, 1.5)), (0.4, (560, 540, 1.5), "lin"), (1.9, (560, 1250, 1.1), "io"), (t11b - t11a, (560, 1290, 1.12), "lin")], lt)
        return [Item(hb, rot=1.5 * math.sin(lt * 2.0), anchor=(560, 380))], cam
    S.append(mk(t11a, t11b, s11))
    # S12 — "He asks the children if they've been good": the children in a row, the fur figure looming at right
    room = interior()
    BF = Painter((480, 120, 1240, 1600), res=1.0); belsnickel_front(BF, 880, 1580, 1300); bfront = BF.sprite()
    KID = []
    for kind in (0, 1, 0):
        KP = Painter((-200, 700, 200, 1620), res=1.4); child_front(KP, 0, 1600, 760 if kind else 700, kind, fear=True); KID.append(KP.sprite())
    t12a, t12b = T("asks") - 0.3, T("then")
    def s12(t):
        lt = t - t12a; p = lt / (t12b - t12a)
        its = int_items(room, lt)
        for i, kx in enumerate((160, 360, 560)): its.append(Item(KID[i], pos=(kx, 2 * math.sin(lt * 3 + i)), scale=0.62 + i * 0.03, anchor=(kx, 1600)))
        its.append(Item(bfront, rot=1.2 * math.sin(lt * 1.2), anchor=(880, 1580)))
        return its, (560 - 40 * p, 1060, 1.0 + 0.10 * p)
    S.append(mk(t12a, t12b, s12))
    # S13a — "Then he scatters the candy": his arm sweeps at the top, candy rains across the planks
    t13a, t13b = T("then"), T("waits")
    cs13 = scatter(24, (300, -150), (40, 800, 1040, 1700), T("scatters") - t13a, 13, dur=(0.4, 0.8), arc=(120, 280))
    FA = arm_sprite(700, FUR_D, SOOT, 150)
    def s13(t):
        lt = t - t13a; ts = T("scatters") - t13a; sw = ease_io(min(1, max(0, (lt - ts + 0.4) / 0.6)))
        its = [Item(fl_bg), Item(fl_pool, add=True, opacity=0.32 * candle_flk(lt))] + candy_items(cs13, lt, 1.3, persp)
        its.append(Item(FA, pos=(-120, -200), rot=20 + 40 * sw, anchor=(-120, -200)))
        return its, (540, 1100, 1.0 + 0.06 * lt / (t13b - t13a))
    S.append(mk(t13a, t13b, s13))
    # S13b — "and waits": low angle, the figure stands still in the candle light, only the fur stirs
    BL = Painter((-60, -60, 1140, 2000), res=0.9); belsnickel_front(BL, 570, 1960, 1800); blow = BL.sprite()
    t13c, t13d = T("waits"), T("but")
    def s13b(t):
        lt = t - t13c
        return int_items(room, lt) + [Item(blow, scale=1.0 + 0.004 * math.sin(lt * 2), anchor=(570, 1960))], (560, 860, 1.0 + 0.05 * lt)
    S.append(mk(t13c, t13d, s13b))
    # S14 — "But here's the terrifying part": a child's face, frozen, trembling
    cface, ceyes = child_portrait()
    CB = Painter((-60, -60, 1140, 1980), res=1.0); CB.gfill((8, 7, 8), (18, 14, 12)); CB.glow(300, 600, 600, (90, 60, 30), 1.0, 1.5); CB.rect((880, -60, 910, 1980), (22, 16, 14)); cbg = CB.sprite()
    t14a, t14b = T("but"), T("never") - 0.45
    def s14(t):
        lt = t - t14a; p = lt / (t14b - t14a); sh = 2 * math.sin(lt * 31)
        return [Item(cbg, opacity=candle_flk(lt)), Item(cface, pos=(sh, 0)), Item(ceyes, pos=(sh, 0), opacity=0 if abs(lt - 1.3) < 0.06 else 1)], (540, 960, 1.0 + 0.08 * p)
    S.append(mk(t14a, t14b, s14))
    # S15 — "He never tells you what good means": hooded portrait, eyes in the shadow, candle flicker, slow push
    t15a, t15b = T("never") - 0.45, T("watches") - 0.6
    def s15(t):
        lt = t - t15a; p = lt / (t15b - t15a)
        return [Item(pbg, opacity=flick(lt, -0.4, 0.5) * candle_flk(lt))] + emb(lt + 5) + [Item(bp_sh), Item(e_gl, opacity=0 if abs(lt - 1.8) < 0.06 else 1)], (540, 880, 1.15 + 0.18 * EASE["sine"](p))
    S.append(mk(t15a, t15b, s15))
    # S16 — "He only watches who moves first and who reaches the fastest": candy on the floor, hands creep in from the edges
    cs16 = [dict(c, t0=-5) for c in scatter(16, (540, -200), (100, 820, 980, 1500), 0, 16)]
    ARM = arm_sprite(620, SHIRT, SKIN, 110); ARM2 = arm_sprite(620, (90, 38, 34), SKIN, 100)
    t16a, t16b = T("watches") - 0.6, T("they", 2)
    def s16(t):
        lt = t - t16a; tm = T("moves") - t16a; tr = T("reaches") - t16a
        a1 = ease_io(min(1, max(0, (lt - tm + 0.3) / 1.2))); a2 = ease_out(min(1, max(0, (lt - tr) / 0.35)))
        its = [Item(fl_bg), Item(fl_pool, add=True, opacity=0.32 * candle_flk(lt))] + candy_items(cs16, lt, 1.3, persp)
        its.append(Item(ARM, pos=(-180 + 200 * a1, 2050 - 60 * a1), rot=-50, anchor=(-180 + 200 * a1, 2050 - 60 * a1)))
        its.append(Item(ARM2, pos=(1300 - 420 * a2, 1950 - 260 * a2), rot=-140, anchor=(1300 - 420 * a2, 1950 - 260 * a2)))
        return its, (540, 1120, 1.0 + 0.05 * lt / (t16b - t16a))
    S.append(mk(t16a, t16b, s16))
    # S17 — "They say the only safe thing is to wait until he tells you to take it": a girl stands still, hands behind her back,
    #        his shadow grows across the wall
    GIRL = Painter((-220, 300, 220, 1640), res=1.3); child_front(GIRL, 0, 1620, 1150, 1, hands="behind"); girl = GIRL.sprite()
    SHD = Painter((100, -200, 1200, 1800), res=0.5); belsnickel_front(SHD, 700, 1700, 1700, sil=True, eyes=False); SHD.blur(10); shadow = SHD.sprite()
    cs17 = [dict(c, t0=-5) for c in scatter(9, (540, -200), (200, 1640, 900, 1760), 0, 17)]
    t17a, t17b = T("they", 2), T("children", 2) - 0.3
    def s17(t):
        lt = t - t17a; p = lt / (t17b - t17a); g_ = ease_io(min(1, lt / 3.0))
        its = int_items(room, lt) + [Item(shadow, opacity=0.65 * g_, scale=0.8 + 0.25 * g_, anchor=(700, 1700))]
        its += candy_items(cs17, lt, 1.0) + [Item(girl, pos=(420, 2 * math.sin(lt * 2.4)), scale=1.0, anchor=(420, 1620))]
        return its, (520, 1080, 1.0 + 0.06 * p)
    S.append(mk(t17a, t17b, s17))
    # S18 — "The children who rush feel the switch": a hand darts for candy, the switches whip down onto the planks
    SW = switch_bundle(1000)
    flash = Sprite(np.full((8, 8, 4), 255, np.uint8), 8 / W, 0, 0)
    t18a, t18b = T("children", 2) - 0.3, T("so")
    cs18 = [dict(c, t0=-5) for c in scatter(10, (540, -200), (200, 900, 900, 1400), 0, 18)]
    def s18(t):
        lt = t - t18a; tr = T("rush") - t18a; ts = T("switch") - t18a
        a1 = ease_out(min(1, max(0, (lt - tr + 0.2) / 0.35)))
        back = ease_out(min(1, max(0, (lt - ts - 0.05) / 0.25)))
        reach = a1 * (1 - back)
        sw = ease_io(min(1, max(0, (lt - ts + 0.35) / 0.35)))
        its = [Item(fl_bg), Item(fl_pool, add=True, opacity=0.32 * candle_flk(lt))] + candy_items(cs18, lt, 1.3, persp)
        its.append(Item(ARM, pos=(-200 + 330 * reach, 1900 - 420 * reach), rot=-40, anchor=(-200 + 330 * reach, 1900 - 420 * reach)))
        its.append(Item(SW, pos=(1100, 500), rot=200 - 73 * sw, anchor=(1100, 500)))
        fo = max(0, 1 - abs(lt - ts) / 0.12) * 0.35
        if fo > 0: its.append(Item(flash, opacity=fo, par=0.0))
        return its, (540 + 6 * math.sin(lt * 40) * max(0, 1 - abs(lt - ts) / 0.3), 1100, 1.05)
    S.append(mk(t18a, t18b, s18))
    # S19 — "if you hear heavy boots on the porch this December": porch at night, heavy boots and fur hem step across the boards
    PO = Painter((-160, -120, 1240, 2040), res=1.0)
    stone_wall(PO, (-160, -120, 1240, 1250), 51, (78, 78, 82), 0.75)
    window_lit(PO, 60, 300, 260, 400); PO.rect((40, 720, 340, 740), (40, 30, 24))
    PO.rect((640, 240, 960, 1250), (24, 16, 12)); PO.rect((660, 260, 940, 1250), (50, 34, 24))
    for yy in (330, 700, 1080): PO.rect((690, yy, 910, yy + 20), (40, 26, 18))
    PO.circ(800, 480, 92, (30, 52, 34)); PO.circ(800, 480, 56, (50, 34, 24))                         # evergreen wreath
    for a in range(0, 360, 30): PO.circ(800 + 74 * math.cos(math.radians(a)), 480 + 74 * math.sin(math.radians(a)), 22, (36, 62, 40))
    PO.poly([(780, 560), (820, 560), (840, 620), (800, 590), (760, 620)], (150, 36, 34))                   # red bow
    PO.gpoly([(-160, 1250), (1240, 1250), (1240, 2040), (-160, 2040)], (62, 50, 40), (40, 32, 26))
    for yy in np.linspace(1270, 2040, 9): PO.line([(-160, yy), (1240, yy)], (30, 24, 20), 3)
    for x_ in (-120, 1180): PO.rect((x_ - 30, -120, x_ + 30, 2040), (34, 26, 20))
    PO.gpoly([(-160, 1240), (1240, 1240), (1240, 1300), (-160, 1300)], (90, 104, 128, 120), (90, 104, 128, 0))
    PO.gpoly([(-160, 1840), (1240, 1840), (1240, 2040), (-160, 2040)], (10, 10, 14, 0), (4, 4, 6, 255)); porch = PO.sprite()
    pwin = glow_sprite(190, 520, 260, CANDLE, power=1.5)
    BOOT = []
    for i in range(8):
        BP = Painter((-520, 400, 520, 1860), res=0.8); belsnickel_side(BP, 0, 1800, 2400, i / 8, switches=False, sack=False); BOOT.append(BP.sprite())
    sf_porch = snowfall(30, (-160, -120, 1240, 2040), 19)
    t19a, t19b = T("so"), T("and", 4)
    def s19(t):
        lt = t - t19a; x = 1000 - lt * 230
        its = [Item(porch), Item(pwin, add=True, opacity=0.6 * candle_flk(lt))] + sf_porch(lt, 50, 0.3)
        if lt < T("porch") - t19a: its.append(Item(BOOT[int(lt * 5) % 8], pos=(x, 2 * abs(math.sin(lt * 5 * math.pi / 4)))))
        return its, (600 - 40 * lt, 1520, 1.45 + 0.03 * lt)
    S.append(mk(t19a, t19b, s19))
    # S20 — "and something hits your floor like falling sweets": dark room in cold moonlight, candy drops and bounces
    fl_cold, pool_cold = floor_bg(True)
    t20a, t20b = T("and", 4), T("dont", 2)
    cs20 = scatter(14, (540, -300), (120, 800, 960, 1600), T("hits") - t20a - 0.35, 20, dur=(0.45, 0.6), drop=True)
    mbeam = beam_sprite(900, -100, 500, 1900, 200, 700, (150, 176, 220), 0.30, 0.05, res=0.4, blur=60)
    def s20(t):
        lt = t - t20a
        return [Item(fl_cold), Item(mbeam, add=True, opacity=0.8)] + candy_items(cs20, lt, 1.3, persp), (540, 1100, 1.0 + 0.05 * lt / (t20b - t20a))
    S.append(mk(t20a, t20b, s20))
    # S21 — "don't reach for it": a small hand hovers over the candy and pulls back
    t21a, t21b = T("dont", 2), T("because", 2)
    cs21 = [dict(c, t0=-5) for c in scatter(8, (540, -200), (300, 1000, 800, 1300), 0, 21)]
    def s21(t):
        lt = t - t21a; a1 = ease_io(min(1, lt / 0.45)); b = ease_io(min(1, max(0, (lt - 0.55) / 0.4)))
        r_ = a1 * (1 - 0.7 * b)
        return [Item(fl_cold), Item(mbeam, add=True, opacity=0.8)] + candy_items(cs21, lt, 1.6, persp) + \
               [Item(ARM, pos=(-160 + 300 * r_, 1950 - 520 * r_), rot=-55, anchor=(-160 + 300 * r_, 1950 - 520 * r_))], (540, 1180, 1.25)
    S.append(mk(t21a, t21b, s21))
    # S22 — "Because the Belsnickel isn't counting your presents": candle-lit Christmas tree, wrapped gifts, he waits in the doorway
    TR = Painter((40, 600, 520, 1500), res=1.2)
    TR.rect((60, 1300, 500, 1340), (46, 32, 22)); TR.rect((100, 1340, 120, 1500), (40, 28, 20)); TR.rect((440, 1340, 460, 1500), (40, 28, 20))   # table
    for k in range(5):
        y1 = 700 + k * 110; wdt = 60 + k * 45; TR.poly([(280 - wdt, y1 + 140), (280, y1), (280 + wdt, y1 + 140)], (20, 44, 30) if k % 2 else (26, 54, 36))
    TR.rect((272, 1250, 288, 1300), (40, 28, 20))
    tpos = [(230, 790), (330, 830), (190, 920), (370, 960), (160, 1060), (400, 1100), (250, 1000)]
    for (cx, cy) in tpos: TR.rect((cx - 4, cy - 22, cx + 4, cy), (230, 220, 190)); TR.ell((cx - 4, cy - 34, cx + 4, cy - 20), (255, 220, 140))
    for (x0, w_, h_, col) in [(110, 120, 90, (120, 50, 40)), (250, 90, 70, (60, 80, 60)), (360, 110, 100, (130, 110, 70))]:
        TR.rect((x0, 1300 - h_, x0 + w_, 1300), col); TR.rect((x0 + w_ / 2 - 4, 1300 - h_, x0 + w_ / 2 + 4, 1300), (190, 170, 120)); TR.rect((x0, 1300 - h_ / 2 - 4, x0 + w_, 1300 - h_ / 2 + 4), (190, 170, 120))
    tree = TR.sprite()
    tglows = [glow_sprite(cx, cy - 28, 50, CANDLE, power=1.4) for (cx, cy) in tpos]
    DW = Painter((300, 280, 820, 1170), res=1.4); belsnickel_front(DW, 560, 1150, 800, sil=True); dsil = DW.sprite()
    t22a, t22b = T("because", 2), T("hes", 2)
    def s22(t):
        lt = t - t22a; p = lt / (t22b - t22a); tc = T("counting", 1) - t22a
        op = ease_io(min(1, max(0, (lt - tc + 0.3) / 0.8)))
        its = int_items(room_open, lt, 0.8) + sf_door(lt, 40, 0.45) + [Item(dsil, opacity=op)]
        its += [Item(tree)] + [Item(g_, add=True, opacity=0.7 * candle_flk(lt, i)) for i, g_ in enumerate(tglows)]
        return its, kf([(0, (330, 1080, 1.35)), (tc - 0.2, (350, 1080, 1.38), "lin"), (tc + 0.8, (540, 860, 1.15), "io"), (t22b - t22a, (545, 850, 1.17), "lin")], lt)
    S.append(mk(t22a, t22b, s22))
    # S23 — "He's counting your hands." the reveal: soot face, dead white eyes, a grin of yellow teeth; flash, final hold
    bp_rev = bel_portrait("reveal"); e_dead = bel_eyes("dead"); cbg2 = portrait_bg(False)
    t23a = T("hes", 2)
    def s23(t):
        lt = t - t23a
        fl = 1.0 if (lt % 0.9) > 0.06 else 0.2
        return [Item(cbg2, opacity=fl)] + emb(lt + 7) + [Item(bp_rev), Item(e_dead)], (540, 900, 1.12 + 0.20 * EASE["sine"](min(1, lt / 2.6)))
    S.append(mk(t23a, END, s23))
    # ---- extra cuts on long shots (punch-in / reframe), as in EP01 ----
    def split(idx_fn, t_cut, cam_fn):
        i = next(k for k, s_ in enumerate(S) if s_["fn"].__name__ == idx_fn)
        a = S[i]; f0 = a["fn"]
        def f2(t, f0=f0, t_cut=t_cut):
            its, cam = f0(t); return its, cam_fn(t - t_cut, cam)
        f2.__name__ = idx_fn + "b"
        S[i] = mk(a["t0"], t_cut, f0, a["dz"]); S.insert(i + 1, mk(t_cut, a["t1"], f2))
    split("s5", T("hes", 1), lambda lt, c: (540, 800, 1.55 + 0.05 * lt))
    split("s9", T("comes"), lambda lt, c: (565, 1120, 1.9 + 0.05 * lt))
    split("s16", T("who", 2), lambda lt, c: (620, 1260, 1.45 + 0.05 * lt))
    split("s17", T("until"), lambda lt, c: (420, 900, 1.6 + 0.05 * lt))
    split("s19", T("porch"), lambda lt, c: (560, 860, 1.0 + 0.04 * lt))
    split("s20", T("like"), lambda lt, c: (520, 1260, 1.5 + 0.05 * lt))
    return S

# ================= captions =================
CHUNKS = ["In Pennsylvania,", "if a man", "in a ragged fur coat", "walks into your house", "a few nights", "before Christmas,", "and throws candy", "across the floor,",
          "#don't grab it.", "Because he isn't", "giving you a gift.", "He's testing you.", "They call him", "the Belsnickel.", "German families", "brought him",
          "to Pennsylvania", "200 years ago.", "By 1827,", "a Philadelphia newspaper", "was already", "describing him.", "According to the legend,", "he comes",
          "before Santa,", "his face", "dark with soot,", "a bundle of switches", "in his hand.", "He asks the children", "if they've been good.", "Then he scatters",
          "the candy", "and waits.", "But here's the", "terrifying part.", "He never tells you", "what good means.", "He only watches", "who moves first,",
          "and who reaches", "the fastest.", "They say the only", "safe thing", "is to wait", "until he tells you", "to take it.", "The children", "who rush",
          "feel the switch.", "So, if you hear", "heavy boots", "on the porch", "this December,", "and something", "hits your floor", "like falling sweets,",
          "don't reach for it.", "Because the Belsnickel", "isn't counting", "your presents.", "He's counting", "your hands."]
RED = {"GERMAN", "PENNSYLVANIA,", "PENNSYLVANIA", "RAGGED", "FUR", "CHRISTMAS,", "CANDY", "GIFT.", "TESTING", "BELSNICKEL.", "BELSNICKEL", "200", "1827,", "PHILADELPHIA",
       "LEGEND,", "SANTA,", "SOOT,", "SWITCHES", "GOOD.", "TERRIFYING", "FIRST,", "FASTEST.", "WAIT", "SWITCH.", "BOOTS", "DECEMBER,", "SWEETS,", "REACH",
       "PRESENTS.", "HANDS."}
def build_chunks():
    out = []; k = 0
    ws_all = list(words)
    for c in CHUNKS:
        hidden = c.startswith("#"); toks = c.lstrip("#").split()
        ws = []
        for tok in toks:
            m = ws_all[k]; k += 1
            txt = tok.upper()
            ws.append(dict(txt=txt, s=m["s"], e=m["e"], red=txt in RED and not (txt == "CANDY" and "THE CANDY" in c.upper())))
        out.append(dict(words=ws, hidden=hidden))
    assert k == len(ws_all), (k, len(ws_all))
    return out

def main():
    print("building shots...", flush=True)
    SH = build_all(); chunks = build_chunks(); cap = Captioner(FB, size=84)
    for a, b in zip(SH[:-1], SH[1:]): assert b["t0"] >= a["t1"] - 1e-6 and b["t0"] - a["t1"] < 0.1, (a["fn"].__name__, a["t1"], b["fn"].__name__, b["t0"])
    print("shots", len(SH), [(s_["fn"].__name__, round(s_["t1"] - s_["t0"], 2)) for s_ in SH], flush=True)
    def shot_at(t):
        for i, s_ in enumerate(SH):
            if t < s_["t1"]: return i
        return len(SH) - 1
    def rend(i, t): return render_frame(SH[i]["fn"], t)
    def frame(n):
        t = n / FPS; i = shot_at(t); img = rend(i, t)
        dz = SH[i]["dz"]
        if dz and t - SH[i]["t0"] < dz and i > 0:
            a = (t - SH[i]["t0"]) / dz; a = a * a * (3 - 2 * a); img = rend(i - 1, t) * (1 - a) + img * a
        hook = SH[i]["fn"].__name__ == "s4"
        if not hook: img = vignette(img, 0.6)
        img = grain(img, 0, 2.0)
        act = None
        for c in chunks:
            if c["words"][0]["s"] <= t + 0.03: act = c
        if act and not act["hidden"] and not hook and t < VOICE_END + 0.3:
            img = cap.apply(img, act["words"], sum(1 for w in act["words"] if w["s"] <= t + 0.03))
        return np.clip(img, 0, 255).astype(np.uint8)
    if len(sys.argv) > 2:
        ts = [float(x) for x in sys.argv[2].split(",")]; ims = [Image.fromarray(frame(int(t * FPS))).resize((270, 480), Image.LANCZOS) for t in ts]
        cols = min(8, len(ims)); sheet = Image.new("RGB", (270 * cols, 480 * ((len(ims) + cols - 1) // cols)))
        for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 270, (k // cols) * 480))
        out = os.path.join(EP, sys.argv[3] if len(sys.argv) > 3 else "stills.jpg"); sheet.save(out, quality=90); print("stills", out); return
    out = os.path.join(EP, "ep02_noaudio.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    nf = int(math.ceil(END * FPS))
    for n in range(nf):
        pr.stdin.write(frame(n).tobytes())
        if n % 150 == 0: print("frame", n, "/", nf, flush=True)
    pr.stdin.close(); pr.wait(); print("wrote", out, "%.2f s" % (nf / FPS))

if __name__ == "__main__":
    main()
