"""render_ep04.py — EP04 "Kushtaka" (Alaska, Tlingit legend) in the Dark Atlas Tales style, Milo narration.
Usage: python -I render_ep04.py <dark_atlas_dir> [stills "t1,t2,..." [out.jpg]]
Same engine/style/captions/cut rhythm as render_ep02.py (approved). New scenes: Southeast Alaska coast, Tlingit village,
1900s steamer wharf, notebook, beach/waves/fog, the land otter man.
"""
import sys, os, json, math, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from style import *

ROOT = sys.argv[1]; EP = os.path.join(ROOT, "EP04_kushtaka")
FB = os.path.join(ROOT, "fonts", "Oswald-Bold.ttf"); FR = os.path.join(ROOT, "fonts", "Oswald-Regular.ttf")
HAND = next((f for f in ("C:/Windows/Fonts/segoesc.ttf", "C:/Windows/Fonts/georgiai.ttf",  # Windows: Segoe Script / Georgia Italic
                         "/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf",
                         "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                         "/System/Library/Fonts/Supplemental/Georgia Italic.ttf")
             if os.path.exists(f)), "C:/Windows/Fonts/georgiai.ttf")
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

STY = json.load(open(os.path.join(EP, "style.json"), encoding="utf-8"))
tup = lambda k: tuple(STY[k])
FUR, FUR_D, SHEEN, EYE = tup("fur"), tup("fur_d"), tup("fur_sheen"), tup("eye_glow")
SLK, SLK_D = tup("slicker"), tup("slicker_d")
CED, CED_D, FRED, FBLK = tup("cedar"), tup("cedar_d"), tup("formline_red"), tup("formline_black")
WAT_T, WAT_B, FOG = tup("water_t"), tup("water_b"), tup("fog")
NIGHT_T, NIGHT_B = (6, 9, 15), (24, 34, 48)
SKIN = (204, 168, 136); SKIN_D = (176, 140, 110)
WARM = (214, 160, 86); DK = (7, 8, 11)
def dim(c, k): return tuple(int(min(255, v * k)) for v in c[:3])

# ================= helpers =================
def flick(lt, seed=0.0, depth=0.25):
    v = 1.0
    for a, b in [(1.3, 1.42), (1.5, 1.55), (3.1, 3.2), (4.4, 4.46)]:
        if a + seed < lt < b + seed: v = depth
    return v
def fire_flk(lt, ph=0.0): return 0.80 + 0.12 * math.sin(lt * 9 + ph) + 0.08 * math.sin(lt * 23 + ph * 2)

R = Painter((-400, -400, 400, 400), res=1.2)
for r_ in (120, 220, 330): R.arc((-r_, -r_, r_, r_), 0, 360, (200, 220, 230, 110), 2.5)
RINGS = R.sprite()
def ring_items(lt, x, y, speed=0.7, n=3, s0=0.3, s1=1.0, op=0.6):
    out = []
    for k in range(n):
        ph = (lt * speed + k / n) % 1
        out.append(Item(RINGS, pos=(x, y), scale=s0 + ph * s1, anchor=(x, y), opacity=(1 - ph) * op))
    return out

def fog_layers(y, n=3, seed=0, a=110):
    out = []
    for j in range(n):
        F = Painter((-700, y - 220, 1800, y + 220), res=0.25, ss=1); r = random.Random(seed + j)
        for _ in range(9): F.glow(r.uniform(-600, 1700), y + r.uniform(-60, 60), r.uniform(200, 380), FOG, a * 0.42 / 255, 1.4)
        out.append(F.sprite())
    def items(lt, speed=14):
        return [Item(f, pos=(speed * 9 * math.sin(lt * 0.09 * (j + 1) + j * 2.1), 0)) for j, f in enumerate(out)]
    return items

def wave_bands(y0, n, x0=-500, x1=1600, seed=0, dark=1.0):
    WV = []
    for j in range(n):
        P = Painter((x0, y0 - 40, x1, y0 + 260 + j * 150), res=0.7); yb = y0 + j * 130
        pts = [(x0, y0 + 260 + j * 150)] + [(x, yb - 12 * math.sin(x / (70 + j * 30) + j) - 6 * math.sin(x / 29 + j)) for x in np.linspace(x0, x1, 70)] + [(x1, y0 + 260 + j * 150)]
        P.gpoly(pts, dim(WAT_T, (1.3 - j * 0.2) * dark), WAT_B, yb - 20, y0 + 260 + j * 150)
        P.line([(x, yb - 12 * math.sin(x / (70 + j * 30) + j) - 6 * math.sin(x / 29 + j)) for x in np.linspace(x0, x1, 70)], (120, 140, 160, 90), 2)
        WV.append(P.sprite())
    def items(lt):
        return [Item(w, pos=(70 * math.sin(lt * 0.5 * (j + 1) + j), 4 * math.sin(lt * 1.6 + j))) for j, w in enumerate(WV)]
    return items

def spruce(P, x, base, h, col):
    w = h * 0.22
    P.rect((x - h * 0.012, base - h, x + h * 0.012, base), col)
    for k in range(9):
        t = k / 9; y = base - h * (0.12 + t * 0.86); ww = w * (1 - t * 0.85)
        P.poly([(x - ww, y + h * 0.07), (x, y - h * 0.06), (x + ww, y + h * 0.07)], col)

def forest(P, x0, x1, base, hmin, hmax, col, seed, step=(26, 50)):
    r = random.Random(seed); x = x0
    while x < x1:
        spruce(P, x, base + r.uniform(0, 12), r.uniform(hmin, hmax), col); x += r.uniform(*step)

def rocks(P, x0, x1, y, seed, col=(20, 22, 28), hi=(52, 58, 70), size=(40, 120)):
    r = random.Random(seed); x = x0
    while x < x1:
        w = r.uniform(*size); h = w * r.uniform(0.35, 0.6)
        P.ell((x, y - h, x + w, y + h * 0.4), col); P.arc((x + w * 0.1, y - h, x + w * 0.9, y), 200, 300, hi, 3)
        x += w * r.uniform(0.6, 0.95)

def onion_church(P, x, base, s, col, gold=(150, 130, 80)):
    P.rect((x - 60 * s, base - 120 * s, x + 60 * s, base), col)
    P.poly([(x - 70 * s, base - 120 * s), (x + 70 * s, base - 120 * s), (x, base - 170 * s)], col)
    P.rect((x - 22 * s, base - 230 * s, x + 22 * s, base - 150 * s), col)
    P.ell((x - 30 * s, base - 290 * s, x + 30 * s, base - 222 * s), col); P.poly([(x - 10 * s, base - 280 * s), (x + 10 * s, base - 280 * s), (x, base - 316 * s)], col)
    P.line([(x, base - 316 * s), (x, base - 350 * s)], gold, 3 * s); P.line([(x - 10 * s, base - 336 * s), (x + 10 * s, base - 336 * s)], gold, 3 * s)
    P.rect((x - 12 * s, base - 70 * s, x + 12 * s, base - 30 * s), WARM)

def stilt_houses(P, x0, x1, base, seed, col=(18, 20, 26)):
    r = random.Random(seed); x = x0
    while x < x1:
        w = r.uniform(60, 110); h = r.uniform(40, 70)
        for px in np.arange(x + 6, x + w, 22): P.line([(px, base), (px, base + 40)], col, 3)
        P.rect((x, base - h, x + w, base), col); P.poly([(x - 6, base - h), (x + w + 6, base - h), (x + w / 2, base - h - h * 0.5)], col)
        if r.random() < 0.6: P.rect((x + w * 0.3, base - h * 0.6, x + w * 0.45, base - h * 0.3), WARM)
        x += w + r.uniform(10, 50)

def ovoid(P, x, y, w, h, col, inner=None):
    P.rrect((x - w / 2, y - h / 2, x + w / 2, y + h / 2), h * 0.45, col)
    if inner: P.rrect((x - w * 0.3, y - h * 0.28, x + w * 0.3, y + h * 0.28), h * 0.25, inner)

def clan_house(P, x, base, w, h, k=1.0):
    """Tlingit plank house: low gable, vertical cedar planks, painted formline front (stylised ovoids/eyes), round door."""
    P.rect((x - w / 2, base - h, x + w / 2, base), dim(CED, k))
    for px in np.arange(x - w / 2 + 14, x + w / 2, 28): P.line([(px, base - h), (px, base)], dim(CED_D, k), 3)
    P.poly([(x - w / 2 - 20, base - h), (x + w / 2 + 20, base - h), (x, base - h - h * 0.32)], dim(CED_D, k * 0.9))
    cy = base - h * 0.55
    ovoid(P, x, cy, w * 0.62, h * 0.42, dim(FBLK, 1), dim(CED, k))
    for sx in (-1, 1):
        ovoid(P, x + sx * w * 0.18, cy - h * 0.04, w * 0.16, h * 0.14, dim(FBLK, 1), dim(FRED, k))
        P.circ(x + sx * w * 0.18, cy - h * 0.04, h * 0.03, dim(FBLK, 1))
    P.poly([(x - w * 0.12, cy + h * 0.1), (x + w * 0.12, cy + h * 0.1), (x, cy + h * 0.18)], dim(FRED, k))
    P.ell((x - w * 0.07, base - h * 0.3, x + w * 0.07, base), (8, 6, 6))

def totem(P, x, base, h, w, k=1.0, sil=False):
    c = (lambda col: DK) if sil else (lambda col: dim(col, k))
    P.rect((x - w / 2, base - h, x + w / 2, base), c(CED))
    n = 4
    for i in range(n):
        yc = base - h * (i + 0.5) / n
        ovoid(P, x - w * 0.22, yc - h * 0.04, w * 0.34, h * 0.08, c(FBLK), c(FRED if i % 2 else CED))
        ovoid(P, x + w * 0.22, yc - h * 0.04, w * 0.34, h * 0.08, c(FBLK), c(FRED if i % 2 else CED))
        P.rect((x - w * 0.3, yc + h * 0.05, x + w * 0.3, yc + h * 0.08), c(FBLK))
    P.poly([(x - w * 0.9, base - h * 0.78), (x - w / 2, base - h * 0.74), (x - w / 2, base - h * 0.70)], c(CED_D)); P.poly([(x + w * 0.9, base - h * 0.78), (x + w / 2, base - h * 0.74), (x + w / 2, base - h * 0.70)], c(CED_D))

def canoe(P, x, base, L, col):
    P.poly([(x - L / 2, base - L * 0.09), (x - L * 0.4, base), (x + L * 0.4, base), (x + L / 2, base - L * 0.12), (x + L * 0.36, base - L * 0.05), (x - L * 0.36, base - L * 0.05)], col)
    P.poly([(x + L * 0.42, base - L * 0.05), (x + L * 0.52, base - L * 0.16), (x + L * 0.47, base - L * 0.05)], col)

# ================= scenery =================
def sky(P, seed, n=160):
    P.gfill(NIGHT_T, NIGHT_B); stars(P, (P.x0, P.y0, P.x1, P.y0 + (P.y1 - P.y0) * 0.5), n, seed)

def coast_wide(seed=1, moon_xy=(800, 330), church=True):
    P = Painter((-160, -120, 1240, 2040), res=1.0); sky(P, seed)
    mountains(P, 1000, range_peaks(-300, 1400, 1000, 300, 520, 140, 220, seed), fill_below=None)
    haze(P, 1000, 160, (30, 40, 56), 150)
    forest(P, -200, 1300, 1060, 60, 130, (14, 18, 22), seed + 2)
    P.gpoly([(-160, 1060), (1240, 1060), (1240, 2040), (-160, 2040)], WAT_T, WAT_B)
    stilt_houses(P, -140, 520, 1056, seed + 4)
    if church: onion_church(P, 700, 1060, 0.7, (18, 20, 26))
    stilt_houses(P, 780, 1240, 1056, seed + 5)
    P.gpoly([(-160, 1840), (1240, 1840), (1240, 2040), (-160, 2040)], (6, 8, 12, 0), (3, 4, 6, 255))
    md, mg, ga = moon(moon_xy[0], moon_xy[1], 80, res=1.4)
    shine = beam_sprite(moon_xy[0], 1070, moon_xy[0] - 40, 2000, 50, 340, (190, 196, 200), 0.40, 0.0, res=0.4, blur=34)
    return dict(bg=P.sprite(), md=md, mg=mg, ga=ga, shine=shine)

def beach_scene(seed=1, moon_xy=(260, 360), forest_line=True):
    """low beach: black water band, rocky shore in the foreground."""
    P = Painter((-160, -120, 1240, 2040), res=1.0); sky(P, seed + 20, 140)
    mountains(P, 900, range_peaks(-300, 1400, 900, 200, 380, 120, 200, seed + 3))
    haze(P, 900, 140, (30, 40, 56), 150)
    if forest_line: forest(P, -200, 1300, 940, 40, 90, (14, 18, 22), seed + 6, (18, 36))
    P.gpoly([(-160, 940), (1240, 940), (1240, 1500), (-160, 1500)], WAT_T, WAT_B)
    P.gpoly([(-160, 1480), (1240, 1440), (1240, 2040), (-160, 2040)], (30, 30, 34), (14, 14, 18))
    rocks(P, -200, 1300, 1500, seed + 7, size=(60, 160)); rocks(P, -200, 1300, 1760, seed + 8, (14, 15, 19), (44, 48, 58), (120, 260))
    P.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 8, 12, 0), (3, 4, 6, 255))
    md, mg, ga = moon(moon_xy[0], moon_xy[1], 72, res=1.4)
    shine = beam_sprite(moon_xy[0], 950, moon_xy[0] + 30, 1480, 40, 220, (190, 196, 200), 0.35, 0.0, res=0.4, blur=30)
    return dict(bg=P.sprite(), md=md, mg=mg, ga=ga, shine=shine)

def sc_items(A, lt):
    return [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"]), Item(A["shine"], add=True, opacity=0.55 + 0.1 * math.sin(lt * 2.2))]

# ================= characters =================
def kushtaka(P, x, feet, h, sil=False, arm=0.0, eyes=True, tail=0.0):
    """land otter man standing upright, hunched: small round head, tiny ears, long sleek body, short legs, long tail,
    long arms with webbed claws, wet sheen. h = head top to feet."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    f, fd, sh = (DK, DK, DK) if sil else (FUR, FUR_D, SHEEN)
    if not sil: P.ell((X(-200), Y(14), X(200), Y(-16)), (0, 0, 0, 100))
    P.poly([(X(-60), Y(260)), (X(-200 - 60 * tail), Y(120)), (X(-330 - 80 * tail), Y(40)), (X(-300 - 80 * tail), Y(20)), (X(-170), Y(80)), (X(-40), Y(200))], fd)   # tail
    for lx in (-70, 20):
        P.rrect((X(lx), Y(330), X(lx + 60), Y(30)), 26 * k, fd); P.ell((X(lx - 20), Y(50), X(lx + 90), Y(0)), fd)
    body = [(X(-90), Y(820)), (X(30), Y(860)), (X(110), Y(780)), (X(140), Y(560)), (X(120), Y(300)), (X(-110), Y(280)), (X(-150), Y(520))]
    P.gpoly(body, f, fd, Y(860), Y(280))
    if not sil:
        P.line([(X(100), Y(760)), (X(124), Y(560)), (X(104), Y(360))], sh, 6 * k)                  # wet sheen
        P.ell((X(-40), Y(700), X(90), Y(420)), dim(FUR, 1.25))                                      # lighter belly
    for s in (-1, 1):                                                                                # arms
        ax = 90 if s > 0 else -110; ang = math.radians(10 + 30 * arm * (1 if s > 0 else 0.4))
        ex = ax + s * math.sin(ang) * 420; ey = 780 - math.cos(ang) * 420
        P.line([(X(ax), Y(780)), (X(ex), Y(ey))], fd, 52 * k)
        for i in range(4):
            a2 = math.radians(-30 + i * 20); P.line([(X(ex), Y(ey)), (X(ex + math.sin(a2) * 70), Y(ey - math.cos(a2) * 80))], fd, 10 * k)
        if not sil: P.chord((X(ex - 50), Y(ey + 10), X(ex + 50), Y(ey - 90)), 0, 180, dim(FUR_D, 1.3))
    P.ell((X(-110), Y(980), X(130), Y(830)), f)                                                     # flat wide head
    P.ell((X(20), Y(930), X(170), Y(846)), f)                                                       # muzzle
    for ex_ in (-100, 116): P.ell((X(ex_ - 11), Y(968), X(ex_ + 11), Y(944)), fd)                  # tiny ears, low on the sides
    if not sil:
        P.ell((X(120), Y(912), X(160), Y(884)), (10, 8, 8))                                         # nose
        for i in range(3): P.line([(X(120), Y(880 - i * 10)), (X(200), Y(890 - i * 18))], (150, 150, 150), 2 * k)
        P.arc((X(-40), Y(1000), X(100), Y(850)), 200, 300, sh, 4 * k)
    if eyes: P.circ(X(50), Y(935), 12 * k, EYE if not sil else (150, 180, 150))

def otter_head_water(P, x, y, s):
    P.ell((x - 70 * s, y - 80 * s, x + 70 * s, y + 30 * s), FUR); P.ell((x - 40 * s, y - 20 * s, x + 40 * s, y + 30 * s), dim(FUR, 1.3))
    for ex in (-48, 48): P.ell((x + ex * s - 14 * s, y - 92 * s, x + ex * s + 14 * s, y - 62 * s), FUR_D)
    P.ell((x - 16 * s, y - 6 * s, x + 16 * s, y + 14 * s), (10, 8, 8))
    for sx in (-1, 1):
        for i in range(3): P.line([(x + sx * 24 * s, y + 6 * s + i * 6 * s), (x + sx * 110 * s, y - 4 * s + i * 14 * s)], (150, 150, 150), 2)
    P.arc((x - 60 * s, y - 76 * s, x + 30 * s, y + 10 * s), 200, 280, SHEEN, 4)

def traveler(P, x, feet, h, back=False, lantern_side=1, step=0.0):
    """person in a yellow fisherman's slicker with hood (front or back view)."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-150), Y(12), X(150), Y(-14)), (0, 0, 0, 90))
    o = 30 * math.sin(step * 2 * math.pi)
    for lx, oo in ((-60, o), (14, -o)):
        P.rect((X(lx), Y(420), X(lx + 48), Y(30 + max(0, oo))), (30, 32, 40)); P.rrect((X(lx - 8), Y(50 + max(0, oo)), X(lx + 66), Y(max(0, oo))), 12 * k, (16, 16, 18))
    P.gpoly([(X(-120), Y(830)), (X(120), Y(830)), (X(150), Y(380)), (X(-150), Y(380))], SLK, SLK_D, Y(830), Y(380))
    for s in (-1, 1): P.line([(X(s * 112), Y(800)), (X(s * 150), Y(470))], SLK_D, 50 * k)
    if lantern_side:
        hx = 150 * lantern_side; P.line([(X(hx), Y(470)), (X(hx), Y(420))], (30, 30, 30), 4 * k)
        P.rrect((X(hx - 26), Y(420), X(hx + 26), Y(330)), 8 * k, (40, 36, 30)); P.rect((X(hx - 18), Y(410), X(hx + 18), Y(342)), (255, 220, 150))
    P.ell((X(-100), Y(1010), X(100), Y(800)), SLK)
    if not back:
        P.ell((X(-62), Y(960), X(62), Y(820)), SKIN); P.chord((X(-100), Y(1010), X(100), Y(880)), 180, 360, SLK)
        for ex in (-24, 24): P.circ(X(ex), Y(900), 7 * k, (24, 16, 12))
    else:
        P.chord((X(-90), Y(1000), X(90), Y(840)), 0, 360, SLK_D)

def figure_sil(P, x, feet, h, kind="man", col=(10, 12, 16), wet=False, arm_up=0.0):
    """dark silhouettes for the shapes it takes: man (drowned friend), child, woman (mother, long coat + long hair)."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    if kind == "child":
        P.rect((X(-50), Y(400), X(-8), Y(0)), col); P.rect((X(8), Y(400), X(50), Y(0)), col)
        P.rrect((X(-100), Y(760), X(100), Y(380)), 50 * k, col); P.ell((X(-90), Y(1000), X(90), Y(760)), col)
        for s in (-1, 1): P.line([(X(s * 96), Y(720)), (X(s * 120), Y(440))], col, 40 * k)
        return
    if kind == "woman":
        P.poly([(X(-90), Y(940)), (X(90), Y(940)), (X(110), Y(560)), (X(-110), Y(560))], col)
        P.poly([(X(-110), Y(820)), (X(110), Y(820)), (X(190), Y(20)), (X(-190), Y(20))], col)
        P.line([(X(100), Y(800)), (X(100 + 150 * arm_up), Y(560 + 300 * arm_up))], col, 46 * k)
        P.line([(X(-100), Y(800)), (X(-130), Y(470))], col, 46 * k)
        P.ell((X(-80), Y(1000), X(80), Y(830)), col); return
    for lx in (-70, 14): P.rect((X(lx), Y(470), X(lx + 56), Y(0)), col)
    P.poly([(X(-130), Y(840)), (X(130), Y(840)), (X(110), Y(440)), (X(-110), Y(440))], col)
    for s in (-1, 1): P.line([(X(s * 124), Y(810)), (X(s * 150), Y(420))], col, 50 * k)
    P.ell((X(-80), Y(1000), X(80), Y(830)), col)
    if wet:
        r = random.Random(3)
        for _ in range(16): xx = r.uniform(-130, 130); yy = r.uniform(300, 900); P.line([(X(xx), Y(yy)), (X(xx), Y(yy - 40))], (90, 110, 130), 3 * k)

def kush_portrait(mode="calm"):
    """front portrait of the land otter man. mode: calm | reveal (mouth open, needle teeth)."""
    D = Painter((-60, 300, 1140, 1980), res=1.2)
    D.ell((20, 1300, 1060, 2300), FUR_D)
    D.ell((170, 540, 910, 1240), FUR)                                                     # broad flat head
    D.ell((330, 860, 750, 1260), dim(FUR, 1.35))                                          # muzzle (lighter)
    D.rrect((470, 880, 610, 960), 30, (10, 8, 8))                                         # nose pad
    D.line([(540, 960), (540, 1010)], (10, 8, 8), 6)
    for sx in (-1, 1):
        for i in range(4): D.line([(540 + sx * 120, 1000 + i * 22), (540 + sx * (420 + i * 30), 960 + i * 50)], (170, 170, 170), 3)
        for i in range(3): D.circ(540 + sx * (100 + i * 22), 990 + (i % 2) * 18, 4, (20, 16, 14))
    if mode == "reveal":
        D.chord((380, 980, 700, 1200), 0, 180, (20, 6, 8))
        for i in range(13): tx = 400 + i * 22; D.poly([(tx, 1090), (tx + 18, 1090), (tx + 9, 1124)], (220, 214, 196))
        for i in range(11): tx = 420 + i * 22; D.poly([(tx, 1176), (tx + 18, 1176), (tx + 9, 1146)], (204, 198, 180))
    else:
        D.arc((480, 1000, 600, 1060), 20, 160, (10, 8, 8), 6)
    return D.sprite()

def kush_eyes(mode="calm"):
    E = Painter((360, 700, 720, 840), res=2.0)
    for ex in (440, 640):
        cy = 770
        if mode == "glow":
            E.ell((ex - 40, cy - 30, ex + 40, cy + 30), (6, 6, 8)); E.ell((ex - 26, cy - 22, ex + 26, cy + 22), EYE); E.ell((ex - 6, cy - 18, ex + 6, cy + 18), (10, 20, 12))
        else:
            E.ell((ex - 36, cy - 30, ex + 36, cy + 30), (6, 6, 8)); E.circ(ex + 8, cy - 8, 8, (220, 230, 220))
    return E.sprite()
KGLOW = None

def trav_portrait():
    D = Painter((-60, 300, 1140, 1980), res=1.2)
    D.chord((60, 1300, 1020, 2300), 180, 360, SLK_D); D.rect((60, 1800, 1020, 1980), SLK_D)
    D.ell((230, 460, 850, 1280), SLK); D.line([(300, 760), (330, 1240)], SLK_D, 10); D.line([(780, 760), (750, 1240)], SLK_D, 10)
    D.ell((340, 600, 740, 1180), SKIN); D.pie((340, 600, 740, 1180), -90, 90, SKIN_D)
    D.chord((300, 520, 780, 860), 180, 360, SLK)
    D.arc((400, 760, 500, 800), 200, 340, (50, 34, 24), 9); D.arc((580, 760, 680, 800), 200, 340, (50, 34, 24), 9)
    D.line([(546, 860), (530, 960)], (150, 110, 84), 5); D.arc((520, 950, 560, 972), 10, 170, (150, 110, 84), 5)
    D.ell((508, 1030, 572, 1080), (70, 34, 28))
    for i in range(10):                                                                     # rain drops on the hood
        r = random.Random(i); x = r.uniform(250, 830); y = r.uniform(480, 1250); D.line([(x, y), (x - 4, y + 30)], (230, 220, 160), 3)
    face = D.sprite()
    E = Painter((400, 800, 700, 880), res=2)
    for ex in (456, 624):
        cy = 840; E.ell((ex - 38, cy - 20, ex + 38, cy + 20), (238, 230, 218)); E.circ(ex - 10, cy, 11, (40, 26, 16)); E.circ(ex - 10, cy, 5, (6, 4, 4)); E.circ(ex - 14, cy - 4, 3, (255, 255, 255))
        E.arc((ex - 40, cy - 24, ex + 40, cy + 18), 195, 345, (24, 16, 12), 6)
    return face, E.sprite()

def hand_sprite(kind="human", L=620):
    P = Painter((-20, -110, L + 220, 110), res=1.1)
    if kind == "human":
        P.rrect((0, -62, L, 62), 30, SLK); P.rect((L - 30, -64, L + 4, 64), SLK_D)
        P.ell((L - 10, -50, L + 110, 50), SKIN)
        for i, dy in enumerate((-0.30, -0.10, 0.10, 0.28)):
            l_ = (60, 70, 66, 52)[i]; P.rrect((L + 70, 110 * dy - 11, L + 90 + l_, 110 * dy + 11), 10, SKIN)
        P.rrect((L + 20, -68, L + 90, -44), 10, SKIN_D)
    else:
        P.rrect((0, -56, L, 56), 40, FUR_D); P.ell((L - 20, -60, L + 110, 60), FUR)
        for i, dy in enumerate((-0.34, -0.12, 0.10, 0.32)):
            P.line([(L + 60, 110 * dy), (L + 170, 110 * dy * 1.4)], FUR, 22); P.poly([(L + 166, 110 * dy * 1.4 - 8), (L + 210, 110 * dy * 1.5), (L + 166, 110 * dy * 1.4 + 8)], (200, 196, 180))
        P.poly([(L + 60, -40), (L + 170, -48), (L + 170, 48), (L + 60, 40)], (60, 52, 46, 160))
        P.line([(40, -50), (L - 40, -44)], SHEEN, 4)
    return P.sprite()

# ================= SHOT BUILDERS =================
def mk(t0, t1, fn, dissolve=0.0): return dict(t0=t0, t1=t1, fn=fn, dz=dissolve)

def build_all():
    S = []
    cw = coast_wide(1); fogA = fog_layers(1030, 3, 1, 120); wavA = wave_bands(1120, 3, seed=1)
    # S0 — "In Alaska": fjord, snowy peaks, spruce, stilt houses + onion-dome church, moon path on black water
    def s0(t):
        lt = t; p = lt / T("baby")
        return sc_items(cw, lt) + wavA(lt) + fogA(lt), (560, 1000 - 20 * p, 1.0 + 0.06 * EASE["sine"](p))
    S.append(mk(0, 1.25, s0))
    # S0b — cold-open glimpse (0.5 s): the land otter man's face in the dark, only the eyes lit, water dripping
    kp_calm = kush_portrait("reveal"); e_g0 = kush_eyes("glow"); eg0 = glow_sprite(540, 770, 300, EYE, power=1.8)
    DKB = Painter((-60, -60, 1140, 1980), res=0.5, ss=1); DKB.gfill((2, 3, 5), (6, 8, 12)); dkb = DKB.sprite()
    SHD0 = Painter((-60, -60, 1140, 1980), res=0.5, ss=1); SHD0.gfill((0, 0, 0, 120), (0, 0, 0, 120)); SHD0.glow(540, 820, 600, (0, 0, 0), -0.0, 1.0); shd0 = SHD0.sprite()
    drip0 = glow_sprite(0, 0, 6, (150, 170, 190), power=1.2, res=2)
    t0b = T("baby")
    def s0b(t):
        lt = t - 1.25; p = lt / (t0b - 1.25)
        its = [Item(dkb), Item(kp_calm, opacity=0.42), Item(shd0), Item(eg0, add=True, opacity=0.7), Item(e_g0)]
        for i, dx in enumerate((380, 700)):
            q = (lt * 1.4 + i * 0.5) % 1; its.append(Item(drip0, pos=(dx, 1180 + q * 400), add=True, opacity=(1 - q) * 0.9, anchor=(dx, 1180 + q * 400)))
        return its, (540, 820, 1.55 + 0.25 * p)
    S.append(mk(1.25, t0b, s0b))
    # S1 — "a baby crying down by the water at night": the shoreline rocks, sound rings spreading from the waterline
    bs = beach_scene(2); wavB = wave_bands(1000, 3, seed=2); fogB = fog_layers(960, 2, 5, 110)
    t1a, t1b = T("baby"), T("far")
    def s1(t):
        lt = t - t1a; p = lt / (t1b - t1a)
        return sc_items(bs, lt) + wavB(lt) + fogB(lt) + ring_items(lt, 700, 1470, 0.6, 3, 0.2, 1.1, 0.7), (620, 1300, 1.25 + 0.08 * p)
    S.append(mk(t1a, t1b, s1))
    # S2 — "far from any house": lone traveler in a yellow slicker with a lantern, the town's lights far behind
    TR_ = Painter((-200, 600, 260, 1660), res=1.3); traveler(TR_, 0, 1640, 1000, back=False, lantern_side=1); trv = TR_.sprite()
    lglow = glow_sprite(0, 0, 160, (255, 210, 140), power=1.5)
    t2a, t2b = T("far"), T("dont", 1)
    def s2(t):
        lt = t - t2a; p = lt / (t2b - t2a); turn = ease_io(min(1, max(0, (lt - 0.8) / 0.6)))
        x = 440
        return sc_items(bs, lt) + wavB(lt) + fogB(lt) + [Item(lglow, pos=(x + 150, 1640 - 380), add=True, opacity=0.7 * fire_flk(lt), anchor=(x + 150, 1260)),
                Item(trv, pos=(x, 0), rot=-2 * turn)], (500 + 40 * p, 1250, 1.15 + 0.05 * p)
    S.append(mk(t2a, t2b, s2))
    # S3 — hook card
    f = ImageFont.truetype(FB, 160); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    hk = "DON'T GO LOOKING."; fs = 160
    while d.textlength(hk, font=f) > 980: fs -= 4; f = ImageFont.truetype(FB, fs)
    d.text(((W - d.textlength(hk, font=f)) / 2, 780), hk, font=f, fill=(198, 38, 38, 255))
    hook = Sprite(np.asarray(lay).copy(), 1, 0, 0); g = np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).copy(); hookg = Sprite(g, 1, 0, 0)
    t3a, t3b = T("dont", 1), T("because", 1) - 0.05
    def s3(t):
        lt = t - t3a; dd = t3b - t3a; op = 1.0 if lt < dd - 0.3 else max(0, (dd - lt) / 0.3); s_ = 1 + 0.035 * lt / dd
        return ring_items(lt, 540, 860, 0.55, 3, 0.4, 2.2, 0.22 * op) + [Item(hookg, add=True, opacity=0.8 * op, scale=s_, anchor=(540, 860)), Item(hook, opacity=op, scale=s_, anchor=(540, 860))], (540, 960, 1.0)
    S.append(mk(t3a, t3b, s3))
    # S4 — "Because there is no baby": close on the tide-pool rocks, nothing there, the crying rings stop; two eyes open in the water
    t4a, t4b = T("because", 1), T("something")
    eyesW = Painter((640, 1380, 780, 1430), res=2); [eyesW.circ(ex, 1405, 9, EYE) for ex in (680, 740)]; eyw = eyesW.sprite()
    eyg = glow_sprite(710, 1405, 70, EYE, power=1.6)
    def s4(t):
        lt = t - t4a; p = lt / (t4b - t4a); eo = ease_io(min(1, max(0, (lt - 1.4) / 0.4)))
        return sc_items(bs, lt) + wavB(lt) + fogB(lt) + [Item(eyg, add=True, opacity=0.5 * eo), Item(eyw, opacity=eo)], (700, 1420, 2.0 + 0.15 * p)
    S.append(mk(t4a, t4b, s4))
    # S5 — "Something out there is using its voice": an otter head surfaces in the black water, ripples
    WH = Painter((-160, -120, 1240, 2040), res=1.0); WH.gfill((4, 6, 10), (10, 16, 24)); WH.glow(540, 700, 700, (40, 56, 74), 0.9, 1.4); wh_bg = WH.sprite()
    wavC = wave_bands(1020, 4, seed=3, dark=0.9)
    OH = Painter((300, 800, 780, 1120), res=1.4); otter_head_water(OH, 540, 1040, 2.2); ohead = OH.sprite()
    t5a, t5b = T("something"), T("they", 1)
    def s5(t):
        lt = t - t5a; p = lt / (t5b - t5a); up = ease_out(min(1, lt / 1.4))
        its = [Item(wh_bg)] + wavC(lt)[:1] + ring_items(lt, 540, 1060, 0.5, 3, 0.4, 1.4, 0.5) + [Item(ohead, pos=(0, 120 * (1 - up) + 6 * math.sin(lt * 2)))] + wavC(lt)[1:]
        return its, (540, 1000, 1.05 + 0.10 * p)
    S.append(mk(t5a, t5b, s5))
    # S6 — title card (fog dissolve): no moon disc this time. The land otter man stands on a rock at the waterline;
    #        his upside-down reflection wobbles in the black water, the title rises out of the water.
    TP = Painter((-80, -80, 1160, 2000), res=1.0); TP.gfill((4, 6, 10), (16, 22, 30)); stars(TP, (-80, -80, 1160, 900), 70, 31, a=80)
    TP.glow(540, 980, 700, (50, 62, 78), 0.9, 1.6)
    for (sx, h_) in [(-60, 520), (40, 380), (140, 300), (900, 340), (1000, 460), (1100, 560)]: spruce(TP, sx, 1000, h_, (6, 8, 11))
    TP.gpoly([(-80, 1000), (1160, 1000), (1160, 2000), (-80, 2000)], (12, 18, 26), (2, 4, 8)); TP.glow(560, 1230, 560, (84, 104, 128), 0.85, 1.2)
    for yy in range(1020, 1700, 26): TP.line([(560 - 300 + (yy % 52), yy), (560 + 300 - (yy % 52), yy)], (110, 130, 150, 60), 2)
    tbg = TP.sprite()
    RK = Painter((380, 860, 760, 1020), res=1.6); RK.ell((400, 940, 740, 1060), (10, 12, 16)); RK.arc((420, 940, 720, 1040), 200, 330, (60, 70, 84), 3); rock = RK.sprite()
    KT = Painter((300, 520, 820, 980), res=1.6); kushtaka(KT, 560, 960, 440, sil=True); kt = KT.sprite()
    base_ref = np.flipud(kt.a).copy(); hh_, ww_ = base_ref.shape[:2]
    REF = []
    for kk in range(8):
        yy_, xx_ = np.mgrid[0:hh_, 0:ww_].astype(np.float32)
        mx = xx_ + 6 * kt.res * np.sin(yy_ / (14 * kt.res) + kk / 8 * 2 * np.pi) * (yy_ / hh_)
        rf = cv2.remap(base_ref, mx, yy_, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        rf[..., :3] = (rf[..., :3] * 0.8 + np.array([6, 8, 12]) * 0.2).astype(np.uint8); rf[..., 3] = (rf[..., 3] * np.linspace(0.75, 0.05, hh_)[:, None]).astype(np.uint8)
        REF.append(Sprite(rf, kt.res, kt.ox, 960 + (960 - kt.oy - hh_ / kt.res)))
    lineg = beam_sprite(-80, 1000, 1160, 1000, 6, 6, (120, 140, 160), 0.6, 0.6, res=0.5, blur=6)
    lab = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    fr = ImageFont.truetype(FR, 30); fb = ImageFont.truetype(FB, 140)
    s_ = "A L A S K A   ·   T L I N G I T   L E G E N D"
    d.rectangle([W / 2 - 22, 110, W / 2 + 22, 115], fill=(190, 46, 40, 255))
    d.text(((W - d.textlength(s_, font=fr)) / 2, 135), s_, font=fr, fill=(178, 172, 158, 255))
    d.text(((W - d.textlength("KUSHTAKA", font=fb)) / 2, 175), "KUSHTAKA", font=fb, fill=(214, 222, 226, 255))
    title = Sprite(np.asarray(lab).copy(), 1, 0, 0)
    fogT = fog_layers(1000, 2, 9, 110)
    t6a, t6b = T("they", 1), T("for", 2)
    def s6(t):
        lt = t - t6a; p = lt / (t6b - t6a); ta = ease_out(min(1, max(0, (lt - 0.3) / 0.9)))
        its = [Item(tbg), Item(lineg, add=True, opacity=0.5), Item(REF[int(lt * 7) % 8])] + ring_items(lt, 570, 1010, 0.35, 3, 0.3, 1.6, 0.35) + [Item(rock), Item(kt)] + fogT(lt)
        its.append(Item(title, opacity=ta, par=0.0, pos=(0, 40 * (1 - ta))))
        return its, (560, 980 - 40 * p, 1.05 + 0.10 * EASE["sine"](p))
    S.append(mk(t6a, t6b, s6, dissolve=0.27))
    # S7 — "For generations, the Tlingit people of Southeast Alaska...": village of plank clan houses, totem poles, canoes, fire smoke
    VI = Painter((-160, -120, 1240, 2040), res=1.0); sky(VI, 41)
    mountains(VI, 1000, range_peaks(-300, 1400, 1000, 260, 480, 140, 220, 42)); haze(VI, 1000, 150, (30, 40, 56), 150)
    forest(VI, -200, 1300, 1080, 120, 260, (14, 18, 22), 43)
    VI.gpoly([(-160, 1300), (1240, 1300), (1240, 2040), (-160, 2040)], (34, 34, 36), (18, 18, 22))
    for (hx, hw, hh) in [(140, 300, 180), (520, 340, 200), (900, 300, 170)]: clan_house(VI, hx, 1300, hw, hh, 0.8)
    for tx_ in (330, 720): totem(VI, tx_, 1310, 420, 46, 0.8)
    VI.gpoly([(-160, 1520), (1240, 1500), (1240, 2040), (-160, 2040)], WAT_T, WAT_B)
    for (cx, L_) in [(200, 360), (620, 420)]: canoe(VI, cx, 1490, L_, (40, 26, 20))
    VI.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 8, 12, 0), (3, 4, 6, 255)); vil = VI.sprite()
    vmd, vmg, vga = moon(880, 300, 70, res=1.4)
    fire = glow_sprite(520, 1300, 200, (240, 140, 60), power=1.5)
    SM = Painter((-80, -260, 80, 10), res=0.6, ss=1); SM.glow(0, -120, 80, (70, 74, 82), 0.6, 1.2); smoke = SM.sprite()
    wavV = wave_bands(1510, 2, seed=7)
    t7a, t7b = T("for", 2), T("over")
    def s7(t):
        lt = t - t7a; p = lt / (t7b - t7a)
        its = [Item(vil), Item(vmg, add=True, opacity=vga), Item(vmd), Item(fire, add=True, opacity=0.5 * fire_flk(lt))] + wavV(lt)
        for i in range(5):
            ph = (lt * 0.25 + i / 5) % 1; its.append(Item(smoke, pos=(520 + 30 * math.sin(ph * 6 + i), 1120 - ph * 600), scale=0.8 + ph * 1.5, anchor=(520, 1120 - ph * 600), opacity=(1 - ph) * 0.6))
        return its, (540 + 40 * p, 1180, 1.12 - 0.06 * p)
    S.append(mk(t7a, t7b, s7))
    # S8a — "Over a century ago, an ethnologist traveled there": early-1900s steamer at a wooden wharf (dissolve)
    SW = Painter((-160, -120, 1240, 2040), res=1.0); sky(SW, 51)
    mountains(SW, 1000, range_peaks(-300, 1400, 1000, 300, 520, 140, 220, 52)); haze(SW, 1000, 150, (30, 40, 56), 150)
    forest(SW, -200, 1300, 1060, 60, 130, (14, 18, 22), 53)
    SW.gpoly([(-160, 1060), (1240, 1060), (1240, 2040), (-160, 2040)], WAT_T, WAT_B)
    onion_church(SW, 160, 1060, 0.6, (18, 20, 26))
    SW.rect((560, 1250, 1240, 1290), (40, 32, 26))                                                                  # wharf
    for px in range(580, 1240, 60): SW.rect((px, 1290, px + 12, 1500), (30, 24, 20))
    SW.rect((860, 1060, 1180, 1250), (36, 30, 26)); SW.poly([(840, 1060), (1200, 1060), (1020, 990)], (26, 22, 20)); SW.rect((900, 1120, 940, 1180), WARM)
    SW.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 8, 12, 0), (3, 4, 6, 255)); wharf = SW.sprite()
    ST = Painter((-60, 820, 640, 1340), res=1.2)
    ST.poly([(-40, 1220), (600, 1220), (560, 1320), (0, 1320)], (16, 16, 20)); ST.rect((60, 1150, 500, 1222), (150, 146, 136))
    for wx in range(90, 480, 40): ST.rect((wx, 1170, wx + 18, 1190), WARM)
    ST.rect((240, 960, 290, 1150), (24, 20, 20)); ST.rect((240, 960, 290, 980), (150, 40, 34))
    for mx in (100, 440): ST.rect((mx - 4, 860, mx + 4, 1150), (16, 16, 20))
    steamer = ST.sprite()
    SMK = Painter((-120, -400, 120, 20), res=0.6, ss=1); SMK.glow(0, -200, 120, (60, 62, 68), 0.7, 1.2); smk = SMK.sprite()
    wavS = wave_bands(1280, 2, seed=9)
    t8a, t8b = T("over"), T("wrote")
    def s8(t):
        lt = t - t8a; p = lt / (t8b - t8a)
        its = [Item(wharf)] + wavS(lt)[:1] + [Item(steamer, pos=(-80 + 60 * ease_out(min(1, lt / 3)), 4 * math.sin(lt * 1.6)))] + wavS(lt)[1:]
        for i in range(4):
            ph = (lt * 0.3 + i / 4) % 1; its.append(Item(smk, pos=(185 + 60 * ease_out(min(1, lt / 3)) + 40 * ph, 960 - ph * 500), scale=0.6 + ph * 1.6, anchor=(185, 960 - ph * 500), opacity=(1 - ph) * 0.6))
        return its, (560 - 40 * p, 1120, 1.08 + 0.05 * p)
    S.append(mk(t8a, t8b, s8, dissolve=0.27))
    # S8b — "wrote those stories down": a field notebook by lamplight, a pencil sketch of the land otter man
    NB = Painter((-60, -60, 1140, 1980), res=1.0); NB.gfill((16, 12, 10), (28, 20, 14)); nbg = NB.sprite()
    NP = Painter((100, 200, 980, 1200), res=1.2)
    NP.rect((130, 240, 950, 1160), (120, 108, 86)); NP.line([(540, 240), (540, 1160)], (80, 70, 56), 4); NP.glow(540, 600, 600, (140, 126, 98), 0.7, 1.4)
    fh = ImageFont.truetype(HAND, int(40 * NP.k)); fh2 = ImageFont.truetype(HAND, int(26 * NP.k))
    NP.d.text(NP.P(170, 280), "Land Otter People", font=fh, fill=(40, 32, 24, 255))
    NP.d.text(NP.P(170, 340), "Kóoshdaa Káa", font=fh2, fill=(60, 48, 36, 255))
    r = random.Random(4)
    for ln in range(18):
        yy = 410 + ln * 38; NP.line([(170, yy), (170 + 330 * r.uniform(0.6, 1.0), yy + r.uniform(-3, 3))], (70, 58, 44), 3)
    kushtaka(NP, 740, 1080, 560, sil=True, eyes=False)
    for i in range(10): NP.line([(600 + i * 30, 1090), (620 + i * 30, 1100)], (90, 78, 60), 2)
    paper = NP.sprite()
    lamp = glow_sprite(920, 220, 520, (240, 170, 80), power=1.5)
    t8c, t8d = T("wrote"), T("according")
    def s8b(t):
        lt = t - t8c; p = lt / (t8d - t8c)
        return [Item(nbg), Item(paper, rot=-2 + 1.0 * p, anchor=(540, 700)), Item(lamp, add=True, opacity=0.35 * fire_flk(lt))], (600, 700 + 60 * p, 1.10 + 0.08 * p)
    S.append(mk(t8c, t8d, s8b))
    # S9 — "According to the legend, the kushtaka can take any shape": on the beach, its silhouette melts between otter and man (dissolve)
    HALO = glow_sprite(540, 1150, 460, (78, 94, 116), power=1.3)
    bs2 = beach_scene(5, moon_xy=(820, 330)); wavD = wave_bands(1000, 3, seed=5); fogD = fog_layers(960, 2, 15, 110)
    KS = Painter((260, 820, 820, 1560), res=1.3); kushtaka(KS, 540, 1540, 700); ksp = KS.sprite()
    MS = Painter((260, 820, 820, 1560), res=1.3); figure_sil(MS, 540, 1540, 680, "man", (18, 20, 26)); msp = MS.sprite()
    t9a, t9b = T("according"), T("a", 4) if False else T("drowned") - 0.34
    def s9(t):
        lt = t - t9a; p = lt / (t9b - t9a); m = 0.5 + 0.5 * math.sin(lt * 2.2)
        mo = m if lt > T("take") - t9a - 0.4 else 0.0
        return sc_items(bs2, lt) + wavD(lt) + [Item(HALO, pos=(10, -60), add=True, opacity=0.6), Item(ksp, opacity=1 - mo), Item(msp, opacity=mo)] + fogD(lt), (560, 1240, 1.15 + 0.08 * p)
    S.append(mk(t9a, t9b, s9, dissolve=0.27))
    # S10 — "A drowned friend": a man standing in the shallows, dripping, backlit by the moon
    DF = Painter((260, 760, 820, 1560), res=1.3); figure_sil(DF, 540, 1540, 760, "man", (14, 16, 22), wet=True); dfr = DF.sprite()
    t10a, t10b = T("drowned") - 0.34, T("lost") - 0.34
    def s10(t):
        lt = t - t10a
        return sc_items(bs2, lt) + [Item(HALO, add=True, opacity=0.7), Item(dfr, pos=(0, 2 * math.sin(lt * 1.5)))] + wavD(lt) + fogD(lt), (540, 1180, 1.3 + 0.06 * lt)
    S.append(mk(t10a, t10b, s10))
    # S11 — "A lost child": a small figure at the edge of the spruce forest in the fog
    FS = Painter((-160, -120, 1240, 2040), res=1.0); sky(FS, 61, 80)
    forest(FS, -200, 1300, 1500, 600, 1100, (12, 16, 20), 62, (60, 120)); FS.gpoly([(-160, 1500), (1240, 1500), (1240, 2040), (-160, 2040)], (26, 28, 32), (12, 12, 16))
    forest(FS, -200, 1300, 1700, 900, 1500, (6, 8, 10), 63, (200, 320)); FS.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 8, 12, 0), (3, 4, 6, 255)); fst = FS.sprite()
    CH = Painter((480, 1180, 640, 1520), res=2); figure_sil(CH, 560, 1510, 320, "child", (10, 12, 16)); chs = CH.sprite()
    fogF = fog_layers(1440, 3, 21, 130)
    t11a, t11b = T("lost") - 0.34, T("even")
    def s11(t):
        lt = t - t11a
        return [Item(fst), Item(HALO, pos=(20, 200), add=True, opacity=0.5), Item(chs, pos=(0, 0))] + fogF(lt, 20) + ring_items(lt, 560, 1330, 0.6, 2, 0.2, 0.7, 0.4), (560, 1300, 1.3 + 0.08 * lt)
    S.append(mk(t11a, t11b, s11))
    # S12 — "Even your own mother, calling your name from the beach": a woman at the waterline, calling (rings)
    WM = Painter((280, 700, 900, 1560), res=1.3); figure_sil(WM, 560, 1540, 800, "woman", (14, 16, 22), arm_up=0.6); wom = WM.sprite()
    t12a, t12b = T("even"), T("but")
    def s12(t):
        lt = t - t12a; p = lt / (t12b - t12a)
        return sc_items(bs2, lt) + wavD(lt) + [Item(HALO, pos=(20, -80), add=True, opacity=0.7), Item(wom, pos=(0, 0))] + ring_items(lt, 560, 830, 0.7, 3, 0.2, 1.1, 0.6) + fogD(lt), (560, 1150, 1.1 + 0.08 * p)
    S.append(mk(t12a, t12b, s12))
    # S13 — "But here's the terrifying part": the traveler's face under the yellow hood, rain, trembling
    tface, teyes = trav_portrait()
    PB = Painter((-60, -60, 1140, 1980), res=1.0); PB.gfill((5, 7, 10), (12, 16, 22)); PB.glow(760, 500, 600, (60, 74, 90), 1.0, 1.5); pbg = PB.sprite()
    rain = []
    rr = random.Random(9)
    RN = Painter((-60, -60, 1140, 1980), res=0.6, ss=1)
    for _ in range(140): x = rr.uniform(-60, 1140); y = rr.uniform(-60, 1980); RN.line([(x, y), (x - 8, y + 50)], (140, 160, 180, 90), 2)
    rains = RN.sprite()
    t13a, t13b = T("but"), T("if", 2)
    def s13(t):
        lt = t - t13a; p = lt / (t13b - t13a); sh = 2 * math.sin(lt * 31)
        return [Item(pbg), Item(rains, pos=(-(lt * 120) % 200, (lt * 900) % 400 - 400)), Item(tface, pos=(sh, 0)), Item(teyes, pos=(sh, 0), opacity=0 if abs(lt - 1.1) < 0.06 else 1)], (540, 900, 1.0 + 0.08 * p)
    S.append(mk(t13a, t13b, s13))
    # S14 — "If it catches you, it doesn't kill you": a webbed claw rises from the water and seizes the yellow sleeve
    HU = hand_sprite("human"); HC = hand_sprite("claw")
    wavE = wave_bands(1150, 3, seed=11)
    t14a, t14b = T("if", 2), T("it", 6)
    def s14(t):
        lt = t - t14a; tc = T("catches") - t14a; a = ease_out(min(1, max(0, (lt - tc + 0.2) / 0.35)))
        pull = 30 * ease_io(min(1, max(0, (lt - tc - 0.3) / 0.8)))
        its = [Item(wh_bg)] + wavE(lt)[:1]
        its.append(Item(HU, pos=(-120, 700 + pull), rot=20, anchor=(-120, 700 + pull)))
        its.append(Item(HC, pos=(960, 1720 + 520 * (1 - a) + pull), rot=-114, anchor=(960, 1720 + 520 * (1 - a) + pull)))
        its += wavE(lt)[1:] + ring_items(lt, 600, 1200, 0.8, 2, 0.4, 1.2, 0.4)
        return its, (560, 1060, 1.05 + 0.04 * lt)
    S.append(mk(t14a, t14b, s14))
    # S15 — "It slowly turns you into one of them": the human hand darkens, fur and webbing spread, claws grow
    t15a, t15b = T("it", 6), T("they", 2)
    def s15(t):
        lt = t - t15a; m = ease_io(min(1, max(0, (lt - 0.4) / (t15b - t15a - 0.8))))
        its = [Item(pbg)]
        its += [Item(HU, pos=(-60, 1100), rot=-20, anchor=(-60, 1100), opacity=1 - m), Item(HC, pos=(-60, 1100), rot=-20, anchor=(-60, 1100), opacity=m)]
        return its, (520, 900, 1.25 + 0.10 * lt / (t15b - t15a))
    S.append(mk(t15a, t15b, s15))
    # S16 — "They say only a shaman could bring a person back": firelight inside a clan house, a figure with a drum, sparks
    CI = Painter((-60, -60, 1140, 1980), res=1.0); CI.gfill((16, 10, 8), (30, 18, 12))
    for x in range(-60, 1140, 54): CI.line([(x, -60), (x, 1300)], (22, 14, 10), 4)
    ovoid(CI, 540, 560, 760, 420, (12, 8, 8), (60, 30, 22))
    for sx in (-1, 1): ovoid(CI, 540 + sx * 200, 520, 200, 140, (12, 8, 8), (110, 36, 28)); CI.circ(540 + sx * 200, 520, 30, (12, 8, 8))
    CI.rect((-60, 1300, 1140, 1980), (24, 16, 12)); ci = CI.sprite()
    SHM = Painter((300, 700, 800, 1560), res=1.2)
    SHM.poly([(420, 900), (660, 900), (760, 1540), (320, 1540)], (10, 8, 8)); SHM.ell((470, 740, 610, 900), (10, 8, 8))
    SHM.ell((620, 860, 800, 1040), (10, 8, 8)); SHM.ell((634, 874, 786, 1026), (40, 20, 16)); SHM.line([(700, 950), (600, 1000)], (10, 8, 8), 10)
    for i in range(6): SHM.line([(330 + i * 70, 1520), (350 + i * 70, 1420)], (40, 20, 16), 6)
    shm = SHM.sprite()
    fireC = glow_sprite(540, 1500, 520, (255, 140, 50), power=1.4)
    sparks_spr = glow_sprite(0, 0, 8, (255, 170, 80), power=1.4, res=2)
    sp_r = random.Random(16); sparks = [(sp_r.uniform(380, 700), sp_r.uniform(0, 1), sp_r.uniform(0.6, 1.4)) for _ in range(26)]
    t16a, t16b = T("they", 2), T("without")
    def s16(t):
        lt = t - t16a; p = lt / (t16b - t16a); beat = 1 + 0.04 * max(0, math.sin(lt * 6))
        its = [Item(ci), Item(fireC, add=True, opacity=0.7 * fire_flk(lt)), Item(shm, scale=beat, anchor=(540, 1540))]
        for (x, ph, s) in sparks:
            q = (lt * 0.4 * s + ph) % 1; its.append(Item(sparks_spr, pos=(x + 30 * math.sin(q * 8), 1500 - q * 1100), add=True, opacity=(1 - q) * 0.8, scale=s, anchor=(x, 1500 - q * 1100)))
        return its, (540, 1080, 1.0 + 0.06 * p)
    S.append(mk(t16a, t16b, s16))
    # S17 — "Without one, you stay on that shore forever, crying for the next traveler": lonely shore, small otter shapes on the rocks
    bs3 = beach_scene(8, moon_xy=(540, 320), forest_line=True); wavF = wave_bands(1000, 3, seed=8); fogG = fog_layers(980, 3, 31, 120)
    OT = []
    for i, (ox, oy, sc) in enumerate([(220, 1500, 160), (460, 1470, 120), (760, 1510, 180), (930, 1480, 110)]):
        Pq = Painter((ox - 140 * sc / 100, oy - 190 * sc / 100, ox + 140 * sc / 100, oy + 20), res=1.5); kushtaka(Pq, ox, oy, sc, sil=True); OT.append(Pq.sprite())
    t17a, t17b = T("without"), T("so")
    def s17(t):
        lt = t - t17a; p = lt / (t17b - t17a)
        its = sc_items(bs3, lt) + wavF(lt) + [Item(o, pos=(0, 2 * math.sin(lt * 1.3 + i))) for i, o in enumerate(OT)] + fogG(lt)
        if lt > T("crying", 2) - t17a: its += ring_items(lt, 760, 1360, 0.6, 3, 0.2, 1.0, 0.5)
        return its, (560, 1200 - 40 * p, 1.08 + 0.06 * p)
    S.append(mk(t17a, t17b, s17))
    # S18 — "So if you're ever alone on that coast tonight": the traveler from behind, walking the shore, lantern swinging
    TB = []
    for i in range(8):
        TP_ = Painter((-200, 600, 260, 1660), res=1.3); traveler(TP_, 0, 1640, 1000, back=True, lantern_side=1, step=i / 8); TB.append(TP_.sprite())
    t18a, t18b = T("so"), T("and", 2)
    def s18(t):
        lt = t - t18a; p = lt / (t18b - t18a); x = 520 + 20 * lt
        return sc_items(bs3, lt) + wavF(lt) + [Item(lglow, pos=(x + 150, 1260), add=True, opacity=0.7 * fire_flk(lt), anchor=(x + 150, 1260)),
                Item(TB[int(lt * 5) % 8], pos=(x, 2 * abs(math.sin(lt * 5 * math.pi / 4))), scale=1.0 - 0.1 * p, anchor=(x, 1640))] + fogG(lt), (560, 1240, 1.12 + 0.04 * p)
    S.append(mk(t18a, t18b, s18))
    # S19 — "and the crying moves closer to the waves": the rings slide along the shore toward the breaking waves
    t19a, t19b = T("and", 2), T("dont", 2)
    def s19(t):
        lt = t - t19a; p = lt / (t19b - t19a); rx = 300 + 500 * ease_io(p); ry = 1440 - 140 * ease_io(p)
        return sc_items(bs, lt) + wavB(lt) + ring_items(lt, rx, ry, 0.8, 3, 0.2, 1.2, 0.7) + fogB(lt), (500 + 200 * ease_io(p), 1300, 1.25)
    S.append(mk(t19a, t19b, s19))
    # S20 — "don't answer it.": the traveler's face, lips pressed shut, eyes sliding toward the sound
    t20a, t20b = T("dont", 2), T("dont", 3)
    def s20(t):
        lt = t - t20a
        return [Item(pbg), Item(rains, pos=(-(lt * 120) % 200, (lt * 900) % 400 - 400)), Item(tface), Item(teyes)], (540, 860, 1.4 + 0.1 * lt)
    S.append(mk(t20a, t20b, s20))
    # S21 — "Don't follow it.": footprints in the wet sand leading into the water, a wave washes them away
    FP = Painter((-160, -120, 1240, 2040), res=1.0); FP.gfill((58, 58, 62), (34, 34, 38)); r = random.Random(21)
    for i in range(10):
        y = 1900 - i * 120; x = 540 + (36 if i % 2 else -36) + 6 * math.sin(i)
        FP.ell((x - 26, y - 46, x + 26, y + 46), (16, 16, 20)); FP.ell((x - 18, y - 70, x + 18, y - 44), (16, 16, 20)); FP.arc((x - 28, y - 48, x + 28, y + 48), 200, 340, (96, 104, 118), 3)
    FP.gpoly([(-160, -120), (1240, -120), (1240, 700), (-160, 700)], WAT_B, WAT_T); fpr = FP.sprite()
    wavG = wave_bands(500, 2, seed=21)
    t21a, t21b = T("dont", 3), T("because", 2)
    def s21(t):
        lt = t - t21a; surge = 180 * ease_io(min(1, lt / 1.2))
        return [Item(fpr)] + [Item(w.s, pos=(w.pos[0], w.pos[1] + surge)) for w in wavG(lt)], (540, 1100 - 200 * lt, 1.15)
    S.append(mk(t21a, t21b, s21))
    # S22 — "Because it isn't lost.": the 'mother' at the waterline turns; her outline becomes the otter man
    t22a, t22b = T("because", 2), T("its", 2)
    def s22(t):
        lt = t - t22a; m = ease_io(min(1, max(0, (lt - 0.5) / 0.7)))
        return sc_items(bs2, lt) + wavD(lt) + [Item(HALO, pos=(10, -60), add=True, opacity=0.7), Item(wom, opacity=1 - m), Item(ksp, opacity=m, scale=1.1, anchor=(540, 1540))] + fogD(lt), (550, 1160, 1.3 + 0.05 * lt)
    S.append(mk(t22a, t22b, s22))
    # S23 — "It's waiting for you to come find it." the reveal: first two glowing eyes at the waterline, then the otter face
    #        rises out of the black water, needle teeth, water streaming off; slow push, no flicker (EP01/EP02 used flicker)
    kp_rev = kush_portrait("reveal"); e_glow = kush_eyes("glow")
    eglow = glow_sprite(540, 770, 260, EYE, power=1.8)
    PB2 = Painter((-60, -60, 1140, 1980), res=1.0); PB2.gfill((4, 6, 8), (10, 14, 18)); PB2.glow(540, 860, 820, (40, 56, 70), 1.0, 1.4); pbg2 = PB2.sprite()
    drip = glow_sprite(0, 0, 6, (150, 170, 190), power=1.2, res=2)
    wavR = wave_bands(1180, 3, seed=23, dark=1.2)
    t23a = T("its", 2)
    def s23(t):
        lt = t - t23a; rise = ease_out(min(1, max(0, (lt - 0.35) / 1.3)))
        dy = 700 * (1 - rise); wl = 1180 + 520 * rise                                  # waterline sinks below the face as it rises
        its = [Item(pbg2), Item(kp_rev, pos=(0, dy)), Item(eglow, add=True, opacity=0.4 + 0.3 * (1 - rise), pos=(0, dy)), Item(e_glow, pos=(0, dy))]
        its += [Item(w.s, pos=(w.pos[0], w.pos[1] + wl - 1180)) for w in wavR(lt)]
        for i, dx in enumerate((300, 420, 690, 780)):
            q = (lt * 0.6 + i * 0.27) % 1; its.append(Item(drip, pos=(dx, 1200 + dy + q * 500), add=True, opacity=(1 - q) * 0.8 * rise, anchor=(dx, 1200 + q * 500)))
        return its, (540, 960, 1.05 + 0.22 * EASE["sine"](min(1, lt / 3.0)))
    S.append(mk(t23a, END, s23))
    WATER = {"s0", "s1", "s2", "s4", "s5", "s7", "s9", "s10", "s12", "s14", "s17", "s18", "s19", "s22"}
    for s_ in S:
        if s_["fn"].__name__ in WATER:
            f0 = s_["fn"]
            def fb_(t, f0=f0):
                its, (cx, cy, z) = f0(t); return its, (cx + 6 * math.sin(t * 0.7), cy + 9 * math.sin(t * 1.15), z)
            fb_.__name__ = f0.__name__; s_["fn"] = fb_
    # ---- extra cuts on long shots ----
    def split(idx_fn, t_cut, cam_fn):
        i = next(k for k, s_ in enumerate(S) if s_["fn"].__name__ == idx_fn)
        a = S[i]; f0 = a["fn"]
        def f2(t, f0=f0, t_cut=t_cut):
            its, cam = f0(t); return its, cam_fn(t - t_cut, cam)
        f2.__name__ = idx_fn + "b"
        S[i] = mk(a["t0"], t_cut, f0, a["dz"]); S.insert(i + 1, mk(t_cut, a["t1"], f2))
    split("s5", T("using"), lambda lt, c: (540, 1000, 1.6 + 0.05 * lt))
    split("s7", T("southeast"), lambda lt, c: (520, 1180, 1.6 + 0.04 * lt))
    split("s9", T("take"), lambda lt, c: (560, 1200, 1.7 + 0.05 * lt))
    split("s12", T("name"), lambda lt, c: (580, 900, 1.9 + 0.05 * lt))
    split("s15", T("into"), lambda lt, c: (700, 980, 1.7 + 0.05 * lt))
    split("s17", T("crying", 2), lambda lt, c: (760, 1420, 1.8 + 0.05 * lt))
    return S

# ================= captions =================
CHUNKS = ["In Alaska,", "if you hear", "a baby crying", "down by the water", "at night,", "far from any house,", "#don't go looking for it.",
          "Because there", "is no baby.", "Something out there", "is using its voice.", "They call it", "the Kushtaka,", "the land otter man.",
          "For generations,", "the Tlingit people", "of Southeast Alaska", "have told stories", "about it.", "Over a century ago,", "an ethnologist",
          "traveled there", "and wrote", "those stories down.", "According to the legend,", "the Kushtaka", "can take any shape.", "A drowned friend.",
          "A lost child.", "Even your own mother,", "calling your name", "from the beach.", "But here's the", "terrifying part.", "If it catches you,",
          "it doesn't kill you.", "It slowly turns you", "into one of them.", "They say only", "a shaman", "could bring", "a person back.",
          "Without one,", "you stay", "on that shore", "forever,", "crying for", "the next traveler.", "So, if you're ever", "alone",
          "on that coast", "tonight,", "and the crying", "moves closer", "to the waves,", "don't answer it.", "Don't follow it.", "Because it isn't lost.",
          "It's waiting", "for you", "to come find it."]
RED = {"ALASKA,", "ALASKA", "BABY", "CRYING", "WATER", "LOOKING", "BABY.", "VOICE.", "KUSHTAKA,", "OTTER", "TLINGIT", "LEGEND,", "SHAPE.", "DROWNED",
       "CHILD.", "MOTHER,", "TERRIFYING", "CATCHES", "ONE", "THEM.", "SHAMAN", "FOREVER,", "TRAVELER.", "ALONE", "WAVES,", "ANSWER", "FOLLOW", "LOST.", "FIND"}
def build_chunks():
    out = []; k = 0
    for c in CHUNKS:
        hidden = c.startswith("#"); ws = []
        for tok in c.lstrip("#").split():
            m = words[k]; k += 1; txt = tok.upper()
            red = txt in RED and not (txt == "ONE" and "THEM" not in c.upper()) and not (txt == "CRYING" and "BABY" not in c.upper() and "MOVES" not in c.upper() and "THE CRYING" not in c.upper())
            ws.append(dict(txt=txt, s=m["s"], e=m["e"], red=red))
        out.append(dict(words=ws, hidden=hidden))
    assert k == len(words), (k, len(words))
    return out

def main():
    print("building shots...", flush=True)
    SH = build_all(); chunks = build_chunks(); cap = Captioner(FB, size=84)
    for a, b in zip(SH[:-1], SH[1:]): assert b["t1"] > b["t0"] and b["t0"] >= a["t1"] - 1e-6 and b["t0"] - a["t1"] < 0.1, (a["fn"].__name__, a["t1"], b["fn"].__name__, b["t0"])
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
            img = img + np.array([84, 96, 112], np.float32) * 0.45 * math.sin(math.pi * a)          # pass through a bank of fog
        hook = SH[i]["fn"].__name__ == "s3"
        if not hook: img = vignette(img, 0.6)
        if not hook:                                                                                  # EP04 grade: cold, slightly desaturated, moss/teal shadows
            lum = img.mean(axis=2, keepdims=True); img = img * 0.88 + lum * 0.12
            img = img * np.array([0.93, 1.0, 1.04], np.float32) + np.array([0, 3, 4], np.float32)
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
    out = os.path.join(EP, "ep04_noaudio.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    nf = int(math.ceil(END * FPS))
    for n in range(nf):
        pr.stdin.write(frame(n).tobytes())
        if n % 150 == 0: print("frame", n, "/", nf, flush=True)
    pr.stdin.close(); pr.wait(); print("wrote", out, "%.2f s" % (nf / FPS))

if __name__ == "__main__":
    main()
