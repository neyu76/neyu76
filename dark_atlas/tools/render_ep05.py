"""render_ep05.py — EP05 "Nimerigar" (Wyoming, Shoshone legend) in the Dark Atlas Tales style, Milo narration.
Usage: python -I render_ep05.py <dark_atlas_dir> [stills "t1,t2,..." [out.jpg]]
Per-episode variations (see skill: bảng biến thể): title = rock blast + dust clearing; soft transitions = arrow WHIP-PAN;
camera = LOW, ground level with fast-parallax sagebrush foreground; grade = warm red rock/ochre; reveal = lantern beam sweeps a cave
mouth full of eyes, then one face; hook accent = an arrow thunks into the frame; cold open = small shape darting between rocks.
"""
import sys, os, json, math, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from style import *

ROOT = sys.argv[1]; EP = os.path.join(ROOT, "EP05_nimerigar")
FB = os.path.join(ROOT, "fonts", "Oswald-Bold.ttf"); FR = os.path.join(ROOT, "fonts", "Oswald-Regular.ttf")
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
ROCK, ROCK_D, ROCK_L, DUST, SAGE, SAGE_D = tup("rock"), tup("rock_d"), tup("rock_l"), tup("dust"), tup("sage"), tup("sage_d")
NSK, NSK_D, NHAIR, MUM, MUM_D = tup("nim_skin"), tup("nim_skin_d"), tup("nim_hair"), tup("mummy"), tup("mummy_d")
FLN, FLN_D, BEAN, LANT, POIS = tup("flannel"), tup("flannel_d"), tup("beanie"), tup("lantern"), tup("poison")
NIGHT_T, NIGHT_B = (6, 8, 16), (34, 30, 44)
SKIN = (206, 166, 132); SKIN_D = (176, 138, 108); DK = (8, 7, 8); EYEW = (230, 226, 210)
def dim(c, k): return tuple(int(min(255, v * k)) for v in c[:3])
def fire_flk(lt, ph=0.0): return 0.80 + 0.12 * math.sin(lt * 9 + ph) + 0.08 * math.sin(lt * 23 + ph * 2)

# ================= scenery helpers =================
def milky_way(P, seed):
    r = random.Random(seed)
    for i in range(46):
        t = i / 45; x = -100 + 1300 * t; y = 900 - 760 * t + r.uniform(-40, 40)
        P.glow(x, y, r.uniform(90, 170), (70, 64, 84), 0.32, 1.3)
    for _ in range(700):
        t = r.random(); x = -100 + 1300 * t + r.gauss(0, 70); y = 900 - 760 * t + r.gauss(0, 70)
        P.circ(x, y, r.uniform(0.6, 1.5), (220, 216, 230, r.randint(60, 200)))

def desert_sky(P, seed):
    P.gfill(NIGHT_T, NIGHT_B); stars(P, (P.x0, P.y0, P.x1, P.y0 + (P.y1 - P.y0) * 0.55), 220, seed, a=170); milky_way(P, seed)

def butte(P, x0, x1, base, top, col, cap=None):
    w = x1 - x0
    pts = [(x0 - w * 0.25, base), (x0, top + (base - top) * 0.25), (x0 + w * 0.06, top), (x1 - w * 0.06, top), (x1, top + (base - top) * 0.22), (x1 + w * 0.3, base)]
    P.gpoly(pts, col, dim(col, 0.65), top, base)
    for k in range(1, 5): P.line([(x0 + w * 0.02, top + (base - top) * k * 0.18), (x1 - w * 0.02, top + (base - top) * k * 0.18 + 6)], dim(col, 0.82), 3)
    if cap: P.rect((x0 + w * 0.06, top - 6, x1 - w * 0.06, top + 8), cap)

def sage_clump(P, x, y, s, col, seed):
    r = random.Random(seed)
    for _ in range(9): P.ell((x + r.uniform(-60, 60) * s, y - r.uniform(0, 70) * s - 30 * s, x + r.uniform(-60, 60) * s + 60 * s, y - r.uniform(0, 30) * s + 10 * s), dim(col, r.uniform(0.8, 1.1)))
    for _ in range(6): P.line([(x + 30 * s, y), (x + r.uniform(-10, 70) * s, y - r.uniform(30, 70) * s)], dim(col, 0.6), 3 * s)

def boulder(P, x, y, w, h, col, seed):
    r = random.Random(seed)
    pts = [(x + w * (0.5 + 0.5 * math.cos(a)) + r.uniform(-w, w) * 0.06, y - h * (0.5 + 0.5 * math.sin(a)) * (1 if math.sin(a) > -0.2 else 0.15)) for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
    P.poly(pts, col); P.arc((x + w * 0.1, y - h, x + w * 0.85, y - h * 0.1), 200, 290, dim(col, 1.45), 4)
    for _ in range(3): xx = x + r.uniform(0.2, 0.8) * w; P.line([(xx, y - h * r.uniform(0.3, 0.8)), (xx + r.uniform(-20, 20), y - h * 0.1)], dim(col, 0.7), 2)

def fg_layer(seed, y=1880, n=5, col=(18, 16, 14)):
    """big dark sagebrush/rocks right in front of the low camera (drawn with par>1 so they slide faster)."""
    P = Painter((-500, 1300, 1600, 2100), res=0.5, ss=1); r = random.Random(seed)
    for i in range(n): sage_clump(P, -400 + i * 450 + r.uniform(-60, 60), y + r.uniform(0, 60), r.uniform(2.4, 3.4), col, seed + i)
    P.blur(5); return P.sprite()

def dust_items_factory(n, box, seed, col=DUST):
    r = random.Random(seed); D = glow_sprite(0, 0, 10, col, power=1.3, res=1.5)
    pts = [(r.uniform(box[0], box[2]), r.uniform(box[1], box[3]), r.uniform(0.5, 1.6), r.uniform(0, 6.28)) for _ in range(n)]
    def items(lt, op=0.35, wind=24):
        out = []
        for (x, y, s, ph) in pts:
            xx = box[0] + ((x - box[0]) + lt * wind * s) % (box[2] - box[0]); yy = y + 12 * math.sin(lt * 0.8 + ph)
            out.append(Item(D, pos=(xx, yy), add=True, opacity=op * min(1, s), scale=s, anchor=(xx, yy)))
        return out
    return items

def wyoming_wide(seed=1, peaks=True):
    P = Painter((-160, -120, 1240, 2040), res=1.0); desert_sky(P, seed)
    if peaks: mountains(P, 1060, range_peaks(-300, 1400, 1060, 260, 420, 120, 200, seed), haze=(40, 34, 48))
    haze(P, 1060, 120, (46, 38, 52), 140)
    butte(P, 520, 960, 1180, 930, ROCK, dim(ROCK_L, 0.9)); butte(P, -120, 200, 1190, 1010, dim(ROCK, 0.85))
    P.gpoly([(-160, 1170), (1240, 1170), (1240, 2040), (-160, 2040)], (70, 56, 50), (30, 24, 22))
    r = random.Random(seed + 5)
    for i in range(46):
        y = 1200 + (i / 46) ** 1.4 * 700; s = 0.25 + (y - 1200) / 700 * 1.2; sage_clump(P, r.uniform(-160, 1240), y, s, SAGE_D, i)
    P.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 6, 8, 0), (3, 3, 4, 255))
    return P.sprite()

def rocks_close(seed=2):
    P = Painter((-160, -120, 1240, 2040), res=1.0); desert_sky(P, seed)
    haze(P, 1100, 160, (46, 38, 52), 150)
    P.gpoly([(-160, 1100), (1240, 1100), (1240, 2040), (-160, 2040)], (62, 48, 44), (24, 20, 18))
    boulder(P, -160, 1500, 640, 560, ROCK_D, seed); boulder(P, 620, 1520, 620, 640, dim(ROCK_D, 0.9), seed + 1); boulder(P, 360, 1560, 300, 200, dim(ROCK_D, 0.75), seed + 2)
    for i in range(140): P.circ(random.Random(i).uniform(-160, 1240), random.Random(i + 900).uniform(1520, 2000), random.Random(i + 7).uniform(2, 6), (40, 32, 28))
    P.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 6, 8, 0), (3, 3, 4, 255))
    return P.sprite()

def cave_wall(lit=1.0, hole=False, seed=4):
    """layered sandstone strata with jagged seams and cracks (no blotches)."""
    P = Painter((-160, -120, 1240, 2040), res=1.0); r = random.Random(seed)
    P.gfill(dim(ROCK_D, 0.55 * lit), dim(ROCK_D, 0.32 * lit))
    y = -140; xs = np.linspace(-160, 1240, 28)
    while y < 2040:
        h = r.uniform(70, 170); tilt = r.uniform(-0.06, 0.06)
        top = [(x, y + tilt * (x - 540) + r.uniform(-14, 14)) for x in xs]; bot = [(x, y + h + tilt * (x - 540) + r.uniform(-14, 14)) for x in xs[::-1]]
        P.gpoly(top + bot, dim(ROCK, r.uniform(0.42, 0.62) * lit), dim(ROCK, r.uniform(0.30, 0.45) * lit), y, y + h)
        P.line(top, dim(ROCK_L, 0.45 * lit), 2); y += h
    for _ in range(9):
        x = r.uniform(-100, 1180); y = r.uniform(-100, 1900); pts = [(x, y)]
        for _ in range(7): x += r.uniform(-40, 40); y += r.uniform(40, 110); pts.append((x, y))
        P.line(pts, dim(ROCK_D, 0.18 * lit), r.uniform(3, 6))
    for _ in range(500): P.circ(r.uniform(-160, 1240), r.uniform(-120, 2040), r.uniform(1, 2.5), dim(ROCK, r.uniform(0.25, 0.7) * lit))
    if hole: P.ell((300, 640, 800, 1240), (4, 3, 3)); P.ell((330, 680, 770, 1210), (2, 2, 2))
    return P.sprite()

# ================= characters / props =================
def nimerigar(P, x, feet, h, sil=False, bow=True, stoop=0.0, eyes=True, club=False):
    """small fierce hunter: big head with matted hair, thin long limbs, hide wrap, small bow. h = head top to feet."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    sk, skd, hr = (DK, DK, DK) if sil else (NSK, NSK_D, NHAIR)
    wrap = DK if sil else (70, 54, 40)
    for lx in (-60, 24): P.line([(X(lx), Y(420)), (X(lx + (10 if lx < 0 else 18)), Y(20))], skd, 44 * k)
    P.poly([(X(-80), Y(700 - stoop * 60)), (X(80), Y(690 - stoop * 60)), (X(118), Y(430)), (X(70), Y(370)), (X(-70), Y(370)), (X(-118), Y(430))], wrap)
    P.line([(X(100), Y(660 - stoop * 60)), (X(190), Y(420))], skd, 34 * k)
    P.line([(X(-100), Y(660 - stoop * 60)), (X(-170 + 80 * stoop), Y(440 - 60 * stoop))], skd, 34 * k)
    if bow and not club:
        P.arc((X(150), Y(760), X(260), Y(300)), 290, 70, DK if sil else (60, 40, 26), 9 * k); P.line([(X(222), Y(740)), (X(222), Y(320))], (160, 150, 130) if not sil else DK, 2 * k)
    if club:
        P.line([(X(190), Y(420)), (X(300), Y(980))], DK if sil else (60, 40, 26), 24 * k); P.ell((X(260), Y(1060), X(350), Y(940)), DK if sil else (70, 50, 34))
    hx = 40 * stoop
    P.ell((X(-150 + hx), Y(1000 - stoop * 120), X(150 + hx), Y(660 - stoop * 120)), sk)
    for i in range(9):
        a = math.radians(200 + i * 18); P.line([(X(hx + math.cos(a) * 130), Y(840 - stoop * 120 - math.sin(a) * 150)), (X(hx + math.cos(a) * 165), Y(800 - stoop * 120 - math.sin(a) * 175))], hr, 22 * k)
    P.chord((X(-150 + hx), Y(1010 - stoop * 120), X(150 + hx), Y(760 - stoop * 120)), 180, 360, hr)
    if eyes:
        for ex in (-55, 55):
            P.ell((X(ex - 36 + hx), Y(860 - stoop * 120), X(ex + 36 + hx), Y(800 - stoop * 120)), (4, 4, 4))
            P.circ(X(ex + 10 + hx), Y(838 - stoop * 120), 7 * k, (240, 236, 220) if not sil else (200, 190, 160))

def nim_portrait(mode="dark"):
    """close portrait: leathery wrinkled face, huge black eyes with pinpoint glints, matted hair, needle grin (mode reveal)."""
    D = Painter((-60, 300, 1140, 1980), res=1.2)
    D.ell((80, 1340, 1000, 2300), (54, 42, 32))
    for i in range(30):
        a = math.radians(160 + i * 7.5); D.line([(540 + math.cos(a) * 300, 860 - math.sin(a) * 360), (540 + math.cos(a) * 470, 860 - math.sin(a) * 520)], NHAIR, 26)
    D.ell((210, 470, 870, 1330), NSK); D.pie((210, 470, 870, 1330), -90, 90, NSK_D)
    for i in range(7): D.arc((300 + i * 6, 560 + i * 22, 780 - i * 6, 760 + i * 22), 200, 340, NSK_D, 4)       # forehead wrinkles
    D.chord((200, 440, 880, 900), 180, 360, NHAIR)
    for sx in (-1, 1):
        cx = 540 + sx * 150; D.ell((cx - 115, 790, cx + 115, 960), (4, 4, 4))                                    # huge black eyes
        D.arc((cx - 130, 770, cx + 130, 980), 200, 340, NSK_D, 10)
        for i in range(3): D.arc((cx - 120 - i * 10, 940 + i * 16, cx + 120 + i * 10, 1010 + i * 16), 20, 160, NSK_D, 4)
    D.poly([(520, 980), (560, 980), (600, 1100), (480, 1100)], NSK_D); D.ell((500, 1086, 530, 1106), (20, 14, 12)); D.ell((550, 1086, 580, 1106), (20, 14, 12))
    if mode == "reveal":
        D.chord((360, 1080, 720, 1290), 0, 180, (18, 6, 6))
        for i in range(14): tx = 380 + i * 23; D.poly([(tx, 1186), (tx + 20, 1186), (tx + 10, 1224)], (214, 204, 170))
        for i in range(12): tx = 392 + i * 25; D.poly([(tx, 1270), (tx + 20, 1270), (tx + 10, 1236)], (196, 186, 150))
    else:
        D.line([(440, 1190), (540, 1210), (640, 1190)], (30, 18, 14), 8)
    return D.sprite()

def nim_glints(spread=1.0):
    E = Painter((360, 840, 720, 920), res=2)
    for sx in (-1, 1): cx = 540 + sx * 150; E.circ(cx + 30, 856, 12, (250, 246, 232)); E.circ(cx - 30, 890, 5, (200, 196, 186))
    return E.sprite()

def mummy(P, x, base, s, col=None):
    """small seated mummified figure: legs crossed, arms folded over the lap, hunched, oversized flattened head with
    sunken eye sockets and a gaping mouth (stylised, no gore)."""
    c = MUM; d = MUM_D; hi = dim(MUM, 1.3)
    P.ell((x - 150 * s, base - 80 * s, x + 150 * s, base + 10 * s), d)                                  # crossed legs
    P.ell((x - 120 * s, base - 110 * s, x - 10 * s, base - 40 * s), c); P.ell((x + 10 * s, base - 110 * s, x + 120 * s, base - 40 * s), c)
    P.poly([(x - 70 * s, base - 300 * s), (x + 60 * s, base - 310 * s), (x + 90 * s, base - 90 * s), (x - 90 * s, base - 90 * s)], c)   # hunched torso
    for i in range(5): P.arc((x - 70 * s, base - 290 * s + i * 34 * s, x + 70 * s, base - 250 * s + i * 34 * s), 20, 160, d, 3 * s)  # ribs
    for sx in (-1, 1):                                                                                 # thin arms folded over the lap
        P.line([(x + sx * 70 * s, base - 280 * s), (x + sx * 100 * s, base - 170 * s), (x - sx * 30 * s, base - 110 * s)], d, 26 * s)
        P.line([(x + sx * 70 * s, base - 280 * s), (x + sx * 100 * s, base - 170 * s), (x - sx * 30 * s, base - 110 * s)], c, 18 * s)
    hx = x + 16 * s
    P.ell((hx - 100 * s, base - 470 * s, hx + 100 * s, base - 290 * s), c); P.chord((hx - 104 * s, base - 480 * s, hx + 104 * s, base - 380 * s), 180, 360, d)   # flat skull top
    for ex in (-40, 40): P.ell((hx + ex * s - 28 * s, base - 410 * s, hx + ex * s + 28 * s, base - 362 * s), (12, 8, 6)); P.arc((hx + ex * s - 34 * s, base - 418 * s, hx + ex * s + 34 * s, base - 356 * s), 200, 340, hi, 3 * s)
    P.poly([(hx - 8 * s, base - 360 * s), (hx + 8 * s, base - 360 * s), (hx, base - 336 * s)], (20, 14, 10))
    P.ell((hx - 26 * s, base - 330 * s, hx + 26 * s, base - 300 * s), (12, 8, 6))
    for i in range(4): P.line([(hx - 80 * s + i * 8 * s, base - 440 * s + i * 30 * s), (hx - 50 * s + i * 8 * s, base - 446 * s + i * 30 * s)], d, 2 * s)

def prospector(P, x, feet, h, pick=False, plunger=False):
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    for lx in (-60, 14): P.rect((X(lx), Y(460), X(lx + 50), Y(0)), DK)
    P.poly([(X(-120), Y(820)), (X(120), Y(820)), (X(110), Y(440)), (X(-110), Y(440))], DK)
    P.ell((X(-70), Y(990), X(70), Y(830)), DK); P.ell((X(-150), Y(950), X(150), Y(910)), DK); P.rrect((X(-80), Y(1050), X(80), Y(930)), 20 * k, DK)
    if pick:
        P.line([(X(120), Y(780)), (X(300), Y(1000))], DK, 14 * k); P.poly([(X(220), Y(1060)), (X(400), Y(930)), (X(390), Y(910)), (X(210), Y(1030))], DK)
        P.line([(X(-110), Y(780)), (X(-160), Y(460))], DK, 40 * k)
    elif plunger:
        P.rect((X(150), Y(300), X(330), Y(0)), DK); P.line([(X(240), Y(300)), (X(240), Y(520))], DK, 16 * k); P.rect((X(160), Y(540), X(320), Y(500)), DK)
        P.line([(X(110), Y(780)), (X(200), Y(540))], DK, 40 * k); P.line([(X(-110), Y(780)), (X(190), Y(560))], DK, 40 * k)
    else:
        for s in (-1, 1): P.line([(X(s * 110), Y(780)), (X(s * 150), Y(460))], DK, 40 * k)

def model_a_truck(P, x, base, s, col=DK):
    P.rect((x - 260 * s, base - 120 * s, x + 160 * s, base - 40 * s), col); P.rect((x - 60 * s, base - 230 * s, x + 110 * s, base - 110 * s), col)
    P.poly([(x + 110 * s, base - 120 * s), (x + 280 * s, base - 100 * s), (x + 280 * s, base - 40 * s), (x + 160 * s, base - 40 * s)], col)
    for wx in (-180, 190): P.circ(x + wx * s, base - 30 * s, 52 * s, col); P.circ(x + wx * s, base - 30 * s, 20 * s, (30, 26, 24))
    P.rect((x - 40 * s, base - 210 * s, x + 90 * s, base - 150 * s), (40, 46, 60))

def camper_portrait():
    D = Painter((-60, 300, 1140, 1980), res=1.2)
    D.chord((60, 1320, 1020, 2300), 180, 360, FLN); D.rect((60, 1800, 1020, 1980), FLN)
    for x in range(100, 1000, 90):
        u = (x - 540) / 480; D.line([(x, 1810 - 490 * math.sqrt(max(0, 1 - u * u)) + 8), (x, 1980)], FLN_D, 14)
    for y in range(1400, 1980, 90):
        v = (1810 - y) / 490; hw = 480 * math.sqrt(max(0, 1 - v * v)) if y < 1810 else 480; D.line([(540 - hw + 8, y), (540 + hw - 8, y)], FLN_D, 14)
    D.rect((470, 1170, 610, 1360), SKIN_D)
    D.ell((330, 590, 750, 1220), SKIN); D.pie((330, 590, 750, 1220), -90, 90, SKIN_D)
    D.chord((300, 430, 780, 860), 180, 360, BEAN); D.rect((300, 640, 780, 720), dim(BEAN, 0.8))
    D.rrect((500, 650, 580, 700), 10, (30, 30, 34)); D.circ(540, 676, 14, (255, 250, 220))                    # headlamp
    D.poly([(320, 720), (360, 720), (350, 1000), (310, 960)], (70, 44, 30)); D.poly([(760, 720), (720, 720), (730, 1000), (770, 960)], (70, 44, 30))
    D.arc((400, 790, 500, 830), 200, 340, (60, 40, 28), 9); D.arc((580, 790, 680, 830), 200, 340, (60, 40, 28), 9)
    D.line([(546, 890), (530, 990)], (150, 110, 84), 5); D.arc((520, 980, 560, 1002), 10, 170, (150, 110, 84), 5)
    D.ell((508, 1060, 572, 1110), (70, 34, 28))
    face = D.sprite()
    E = Painter((400, 840, 700, 910), res=2)
    for ex in (456, 624):
        cy = 870; E.ell((ex - 38, cy - 20, ex + 38, cy + 20), (238, 230, 218)); E.circ(ex + 10, cy, 11, (40, 26, 16)); E.circ(ex + 10, cy, 5, (6, 4, 4)); E.circ(ex + 6, cy - 4, 3, (255, 255, 255))
        E.arc((ex - 40, cy - 24, ex + 40, cy + 18), 195, 345, (24, 16, 12), 6)
    return face, E.sprite()

def arrow_sprite(L=420):
    P = Painter((-30, -30, L + 70, 30), res=1.5)
    P.line([(0, 0), (L, 0)], (120, 92, 60), 7)
    for dy in (-1, 1): P.poly([(0, 0), (60, 0), (30, dy * 24), (-20, dy * 22)], (170, 160, 140))
    P.poly([(L - 6, -14), (L + 60, 0), (L - 6, 14)], (70, 66, 60)); P.poly([(L + 10, -8), (L + 56, 0), (L + 10, 8)], POIS)
    return P.sprite()

def tent_scene(inside=False):
    P = Painter((-160, -120, 1240, 2040), res=1.0)
    if inside:
        P.gfill((60, 46, 30), (36, 26, 18)); P.glow(540, 1300, 900, (190, 140, 80), 0.9, 1.3)
        P.poly([(-160, -120), (540, -120), (-160, 1400)], (40, 30, 20)); P.poly([(1240, -120), (540, -120), (1240, 1400)], (40, 30, 20))
        P.line([(540, -120), (540, 2040)], (30, 22, 14), 10)
        for x in range(-160, 1240, 140): P.line([(x, 1450), (540, -120)], (54, 40, 26), 2)
        P.rect((-160, 1450, 1240, 2040), (30, 24, 18)); P.rrect((380, 1500, 700, 1700), 40, (80, 30, 26))      # sleeping bag
        return P.sprite()
    desert_sky(P, 77); mountains(P, 1060, range_peaks(-300, 1400, 1060, 220, 380, 120, 200, 78), haze=(40, 34, 48)); haze(P, 1060, 120, (46, 38, 52), 140)
    P.gpoly([(-160, 1120), (1240, 1040), (1240, 2040), (-160, 2040)], (66, 52, 46), (26, 22, 20))
    P.poly([(300, 1460), (540, 1160), (780, 1460)], (110, 96, 70)); P.poly([(540, 1160), (780, 1460), (880, 1430), (640, 1150)], (80, 70, 52))
    P.poly([(470, 1460), (540, 1300), (610, 1460)], (60, 50, 36))
    for i in range(26): sage_clump(P, random.Random(i).uniform(-160, 1240), 1180 + random.Random(i + 50).uniform(0, 680), 0.6 + random.Random(i + 9).uniform(0, 0.8), SAGE_D, i)
    P.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 6, 8, 0), (3, 3, 4, 255))
    return P.sprite()

# ================= SHOTS =================
def mk(t0, t1, fn, whip=False): return dict(t0=t0, t1=t1, fn=fn, whip=whip)

def build_all():
    S = []
    wide = wyoming_wide(1); fgA = fg_layer(3); dustA = dust_items_factory(40, (-160, 900, 1240, 1900), 1)
    md, mg, ga = moon(820, 300, 60, res=1.4)
    # S0 — "In Wyoming, if you hear": high desert, red butte, Wind River peaks, Milky Way; low camera, sage slides past
    def s0(t):
        lt = t; p = lt / T("something")
        return [Item(wide), Item(mg, add=True, opacity=ga), Item(md)] + dustA(lt) + [Item(fgA, pos=(-120 * lt, 0), par=1.35)], (560 + 30 * p, 1180, 1.05 + 0.05 * p)
    S.append(mk(0, 0.85, s0))
    # S0J — JUMP SCARE (0.85 s → "something"): the face lunges at the lens, full frame, red flash + hard shake
    np_j = nim_portrait("reveal"); gl_j = nim_glints()
    JB = Painter((-60, -60, 1140, 1980), res=0.5, ss=1); JB.gfill((10, 2, 2), (4, 0, 0)); JB.glow(540, 1000, 900, (120, 20, 14), 0.9, 1.2); jbg = JB.sprite()
    RIM = glow_sprite(540, 1000, 700, (200, 60, 40), power=1.6)
    SHD = Painter((-60, 300, 1140, 1980), res=0.5, ss=1); SHD.gpoly([(-60, 300), (1140, 300), (1140, 1000), (-60, 1000)], (0, 0, 0, 215), (0, 0, 0, 0))
    SHD.glow(540, 1700, 520, (170, 30, 20), 0.55, 1.3); jshade = SHD.sprite()                      # dark from above, red under-light
    redf = Sprite(np.dstack([np.full((8, 8), 200, np.uint8), np.full((8, 8), 20, np.uint8), np.full((8, 8), 16, np.uint8), np.full((8, 8), 255, np.uint8)]), 8 / W, 0, 0)
    tj1 = T("something")
    def s0j(t):
        lt = t - 0.85; lunge = ease_out(min(1, lt / 0.16))
        z = 3.2 - 1.75 * lunge + 0.08 * lt                                            # rushes from extreme close to full face
        sh = 26 * math.exp(-lt * 6) * math.sin(lt * 95); sv = 18 * math.exp(-lt * 6) * math.cos(lt * 83)
        its = [Item(jbg), Item(RIM, add=True, opacity=0.55), Item(np_j), Item(jshade), Item(gl_j)]
        fo = 0.75 if lt < 0.07 else max(0, 0.35 - (lt - 0.07) * 1.2)
        if fo > 0: its.append(Item(redf, opacity=fo, par=0.0))
        return its, (540 + sh, 1060 + sv, z)
    S.append(mk(0.85, tj1, s0j))
    # S1 — "something small moving between the rocks at night": a small shape darts across the gap between boulders
    rc = rocks_close(2); fgB = fg_layer(5, 1900, 4)
    RUN = []
    for i in range(6):
        RP = Painter((-140, 700, 160, 1010), res=2); nimerigar(RP, 0, 1000, 300, sil=True, bow=False, stoop=0.6 + 0.1 * math.sin(i)); RUN.append(RP.sprite())
    GL = Painter((-30, -10, 30, 10), res=3); GL.circ(-14, 0, 5, (250, 240, 200)); GL.circ(14, 0, 5, (250, 240, 200)); glint = GL.sprite()
    glg = glow_sprite(0, 0, 40, (250, 230, 170), power=1.6)
    t1a, t1b = T("something"), T("dont", 1)
    def s1(t):
        lt = t - t1a; dart = lt - 0.35
        its = [Item(rc)]
        if 0 < dart < 0.55: x = -100 + dart / 0.55 * 1300; its.append(Item(RUN[int(dart * 30) % 6], pos=(x, 520 + 10 * math.sin(dart * 40))))
        if lt > 1.5:
            o = min(1, (lt - 1.5) / 0.2) * (0 if abs(lt - 2.4) < 0.07 else 1); its += [Item(glg, pos=(560, 1310), add=True, opacity=0.4 * o), Item(glint, pos=(560, 1310), opacity=o)]
        its.append(Item(fgB, pos=(-60 * lt, 0), par=1.4))
        return its, (560, 1250, 1.1 + 0.18 * EASE["sine"](min(1, lt / 2.8)))
    S.append(mk(t1a, t1b, s1))
    # S2 — hook card + an arrow thunks into the frame (camera shake)
    f = ImageFont.truetype(FB, 160); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    hk = "DON'T FOLLOW IT."; fs = 160
    while d.textlength(hk, font=f) > 980: fs -= 4; f = ImageFont.truetype(FB, fs)
    d.text(((W - d.textlength(hk, font=f)) / 2, 780), hk, font=f, fill=(198, 38, 38, 255))
    hook = Sprite(np.asarray(lay).copy(), 1, 0, 0); hookg = Sprite(np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).copy(), 1, 0, 0)
    ARW = arrow_sprite(420)
    t2a, t2b = T("dont", 1), T("because", 1) - 0.05
    def s2(t):
        lt = t - t2a; dd = t2b - t2a; op = 1.0 if lt < dd - 0.3 else max(0, (dd - lt) / 0.3); s_ = 1 + 0.035 * lt / dd
        hit = 0.45; ax = 1300 - 620 * min(1, max(0, (lt - 0.2) / (hit - 0.2))); quiver = 4 * math.sin(lt * 70) * math.exp(-(lt - hit) * 8) if lt > hit else 0
        sh = 10 * math.exp(-(lt - hit) * 14) * math.sin(lt * 90) if lt > hit else 0
        its = [Item(hookg, add=True, opacity=0.8 * op, scale=s_, anchor=(540, 860)), Item(hook, opacity=op, scale=s_, anchor=(540, 860))]
        if lt > 0.2: its.append(Item(ARW, pos=(ax - 470, 700), rot=-8 + quiver, anchor=(ax, 700), opacity=op))
        return its, (540 + sh, 960, 1.0)
    S.append(mk(t2a, t2b, s2))
    # S3 — "Because in the old stories of the Shoshone": a camp of lodges by firelight under the Milky Way, smoke, sparks
    CP = Painter((-160, -120, 1240, 2040), res=1.0); desert_sky(CP, 31)
    mountains(CP, 1060, range_peaks(-300, 1400, 1060, 260, 420, 120, 200, 32), haze=(40, 34, 48)); haze(CP, 1060, 120, (46, 38, 52), 140)
    CP.gpoly([(-160, 1140), (1240, 1140), (1240, 2040), (-160, 2040)], (56, 44, 40), (24, 20, 18))
    for (lx, lh) in [(150, 360), (420, 420), (760, 380), (1000, 320)]:
        CP.poly([(lx - lh * 0.45, 1400), (lx, 1400 - lh), (lx + lh * 0.45, 1400)], (16, 12, 12))
        for dx in (-30, -8, 14, 34): CP.line([(lx, 1400 - lh), (lx + dx, 1400 - lh - 70)], (16, 12, 12), 5)
    CP.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 6, 8, 0), (3, 3, 4, 255)); camp = CP.sprite()
    fire = glow_sprite(590, 1420, 380, (255, 140, 50), power=1.4); spark = glow_sprite(0, 0, 7, (255, 170, 80), power=1.4, res=2)
    sr = random.Random(3); sparks = [(sr.uniform(540, 640), sr.uniform(0, 1), sr.uniform(0.6, 1.4)) for _ in range(24)]
    FL = Painter((540, 1340, 640, 1440), res=2); FL.poly([(560, 1440), (590, 1350), (620, 1440)], (255, 190, 90)); FL.poly([(575, 1440), (590, 1390), (605, 1440)], (255, 240, 180)); flame = FL.sprite()
    t3a, t3b = T("because", 1), T("they", 1)
    def s3(t):
        lt = t - t3a; p = lt / (t3b - t3a)
        its = [Item(camp), Item(fire, add=True, opacity=0.6 * fire_flk(lt)), Item(flame, scale=0.9 + 0.15 * fire_flk(lt), anchor=(590, 1440))]
        for (x, ph, s) in sparks:
            q = (lt * 0.5 * s + ph) % 1; its.append(Item(spark, pos=(x + 30 * math.sin(q * 8), 1420 - q * 700), add=True, opacity=(1 - q) * 0.8, scale=s, anchor=(x, 1420 - q * 700)))
        return its + [Item(fgA, pos=(80 - 60 * lt, 0), par=1.35)], (580, 1260, 1.12 - 0.05 * p)
    S.append(mk(t3a, t3b, s3))
    # S3b (split at "those mountains"): the cliff face is full of crevices... eyes open one by one ("never empty")
    cw_sk = cave_wall(1.0, False, 5)
    EYESP = [(220, 600), (760, 520), (420, 980), (880, 1160), (160, 1320), (620, 1420), (340, 760), (980, 820)]
    t3c = T("those")
    def s3b(t):
        lt = t - t3c; its = [Item(cw_sk)]
        for i, (x, y) in enumerate(EYESP):
            o = min(1, max(0, (lt - i * 0.16) / 0.12)); its += [Item(glg, pos=(x, y), add=True, opacity=0.35 * o), Item(glint, pos=(x, y), opacity=o)]
        return its, (560, 980, 1.05 + 0.06 * lt)
    S[-1]["t1"] = t3c; S.append(mk(t3c, t3b, s3b))
    # S4 — title card (arrow whip in): a rock wall bursts, debris flies, dust clears to reveal the title and a cave mouth
    TW_ = cave_wall(0.8, True, 6)
    deb_r = random.Random(4); DEB = []
    for i in range(30):
        Pd = Painter((-30, -30, 30, 30), res=1.5); Pd.poly([(deb_r.uniform(-28, -10), deb_r.uniform(-28, 28)), (deb_r.uniform(10, 28), deb_r.uniform(-28, 0)), (deb_r.uniform(0, 28), deb_r.uniform(10, 28))], dim(ROCK, deb_r.uniform(0.6, 1.0))); DEB.append((Pd.sprite(), deb_r.uniform(0, 2 * math.pi), deb_r.uniform(500, 1400), deb_r.uniform(-400, 400)))
    CL = Painter((-400, -400, 400, 400), res=0.5, ss=1); CL.glow(0, 0, 400, DUST, 0.85, 1.1); cloud = CL.sprite()
    flash = Sprite(np.full((8, 8, 4), 255, np.uint8), 8 / W, 0, 0)
    lab = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    fr = ImageFont.truetype(FR, 30); fb = ImageFont.truetype(FB, 140)
    s_ = "W Y O M I N G   ·   S H O S H O N E   L E G E N D"
    d.rectangle([W / 2 - 22, 110, W / 2 + 22, 115], fill=(190, 46, 40, 255))
    d.text(((W - d.textlength(s_, font=fr)) / 2, 135), s_, font=fr, fill=(186, 170, 150, 255))
    d.text(((W - d.textlength("NIMERIGAR", font=fb)) / 2, 175), "NIMERIGAR", font=fb, fill=(232, 214, 186, 255))
    title = Sprite(np.asarray(lab).copy(), 1, 0, 0)
    NSIL = Painter((440, 760, 660, 1240), res=2); nimerigar(NSIL, 550, 1220, 420, sil=True); nsil = NSIL.sprite()
    t4a, t4b = T("they", 1), T("in", 3)
    def s4(t):
        lt = t - t4a; p = lt / (t4b - t4a)
        its = [Item(TW_), Item(nsil, opacity=min(1, max(0, (lt - 1.2) / 0.6)))]
        for (sp, ang, v, spin) in DEB:
            q = lt * 0.9; x = 550 + math.cos(ang) * v * q; y = 940 + math.sin(ang) * v * q + 700 * q * q
            if q < 1.6: its.append(Item(sp, pos=(x, y), rot=spin * q, anchor=(x, y), opacity=max(0, 1 - q / 1.6)))
        its.append(Item(cloud, pos=(550, 940), scale=0.6 + 1.8 * ease_out(min(1, lt / 1.5)), anchor=(550, 940), opacity=max(0, 0.95 - 0.7 * lt / (t4b - t4a))))
        fo = max(0, 1 - lt / 0.18) * 0.7
        if fo > 0: its.append(Item(flash, opacity=fo, par=0.0))
        ta = ease_out(min(1, max(0, (lt - 0.6) / 0.9)))
        its.append(Item(title, opacity=ta, par=0.0))
        return its, (550 + 8 * math.sin(lt * 50) * max(0, 1 - lt / 0.4), 1000, 1.0 + 0.06 * EASE["sine"](p))
    S.append(mk(t4a, t4b, s4, whip=True))
    # S5a — "In the 1930s, two gold prospectors": silhouettes on a ridge, Model A pickup, pickaxe, dynamite plunger (arrow whip in)
    PR = Painter((-160, -120, 1240, 2040), res=1.0); desert_sky(PR, 51)
    PR.poly([(-160, 1500), (200, 1300), (700, 1260), (1240, 1380), (1240, 2040), (-160, 2040)], (20, 16, 16))
    boulder(PR, 760, 1300, 480, 520, dim(ROCK_D, 0.8), 52)
    model_a_truck(PR, 200, 1330, 1.0); prospector(PR, 520, 1290, 380, pick=True); prospector(PR, 690, 1280, 360, plunger=True)
    for i in range(14): PR.line([(780 + i * 18, 1230), (700 + i * 4, 1290)], (40, 30, 24), 2) if False else None
    PR.line([(780, 1260), (930, 1130)], (60, 50, 40), 3)
    PR.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 6, 8, 0), (3, 3, 4, 255)); pros = PR.sprite()
    lamp = glow_sprite(430, 1180, 160, LANT, power=1.5)
    t5a, t5b = T("in", 3), T("blasted")
    def s5(t):
        lt = t - t5a; p = lt / (t5b - t5a)
        return [Item(pros), Item(lamp, add=True, opacity=0.5 * fire_flk(lt))] + dustA(lt + 4, 0.25), (560 + 40 * p, 1260, 1.12 + 0.05 * p)
    S.append(mk(t5a, t5b, s5, whip=True))
    # S5b — "blasted open a cave in the Pedro Mountains": blast flash at the rock, debris, dust, a black hole is left
    rk2 = cave_wall(0.9, False, 9); rk2h = cave_wall(0.9, True, 9)
    t5c, t5d = T("blasted"), T("inside")
    def s5b(t):
        lt = t - t5c; b = 0.25
        its = [Item(rk2 if lt < b + 0.1 else rk2h)]
        if lt > b:
            q = lt - b
            for (sp, ang, v, spin) in DEB:
                x = 550 + math.cos(ang) * v * q; y = 940 + math.sin(ang) * v * q + 700 * q * q
                if q < 1.4: its.append(Item(sp, pos=(x, y), rot=spin * q, anchor=(x, y), opacity=max(0, 1 - q / 1.4)))
            its.append(Item(cloud, pos=(550, 940), scale=0.5 + 2.0 * ease_out(min(1, q / 1.2)), anchor=(550, 940), opacity=max(0, 0.95 - 0.35 * q)))
            fo = max(0, 1 - q / 0.15) * 0.8
            if fo > 0: its.append(Item(flash, opacity=fo, par=0.0))
        sh = 14 * math.exp(-max(0, lt - b) * 9) * math.sin(lt * 80) if lt > b else 0
        return its, (550 + sh, 980, 1.05 + 0.05 * lt)
    S.append(mk(t5c, t5d, s5b))
    # S6 — "Inside, sitting cross-legged on a ledge, was a mummified figure barely 14 inches tall": lantern-lit cave, the ledge
    cin = cave_wall(1.4, False, 12)
    LG = Painter((-160, 1100, 1240, 1400), res=1.0); LG.poly([(-160, 1180), (1240, 1150), (1240, 1400), (-160, 1400)], dim(ROCK, 0.7)); LG.line([(-160, 1180), (1240, 1150)], dim(ROCK_L, 0.8), 5); ledge = LG.sprite()
    MU = Painter((380, 660, 720, 1190), res=2); mummy(MU, 550, 1175, 1.15); mum = MU.sprite()
    lbeam = beam_sprite(1240, 400, 560, 1000, 120, 700, LANT, 0.35, 0.05, res=0.4, blur=50)
    lglow = glow_sprite(560, 1000, 520, LANT, power=1.5)
    RUL = Painter((700, 640, 790, 1180), res=2); RUL.rect((720, 660, 770, 1176), (210, 190, 140))
    for i in range(15): y = 1176 - i * 34.4; RUL.line([(720, y), (745 if i % 2 else 760, y)], (40, 30, 20), 3)
    fn_ = ImageFont.truetype(FB, int(36 * RUL.k)); RUL.d.text(RUL.P(745, 690), "14\"", font=fn_, fill=(30, 24, 18, 255), anchor="mm"); ruler = RUL.sprite()
    t6a, t6b = T("inside"), T("years")
    def s6(t):
        lt = t - t6a; tw_ = T("was", 1) - t6a; t14 = T("14") - t6a
        cam = kf([(0, (780, 900, 1.3)), (tw_ - 0.3, (690, 960, 1.32), "lin"), (tw_ + 0.4, (560, 930, 1.75), "io"), (t6b - t6a, (580, 930, 1.85), "lin")], lt)
        its = [Item(cin), Item(lglow, add=True, opacity=0.6 * fire_flk(lt)), Item(lbeam, add=True, opacity=0.7 * fire_flk(lt, 1)), Item(ledge), Item(mum)]
        if lt > t14 - 0.1: its.append(Item(ruler, opacity=min(1, (lt - t14 + 0.1) / 0.3)))
        return its, cam
    S.append(mk(t6a, t6b, s6))
    # S7 — "Years later, it disappeared": the same ledge, the figure fades to an empty outline in the dust
    t7a, t7b = T("years"), T("according")
    def s7(t):
        lt = t - t7a; m = ease_io(min(1, max(0, (lt - 0.6) / 1.2)))
        return [Item(cin, opacity=0.8), Item(lglow, add=True, opacity=0.35 * fire_flk(lt)), Item(ledge), Item(mum, opacity=1 - m)] + dustA(lt, 0.3, 10), (560, 930, 1.6 - 0.1 * lt)
    S.append(mk(t7a, t7b, s7))
    # S8 — "According to the legend, the Nimerigar were fierce little hunters of the Wind River Mountains": tiny hunters on a ridge (arrow whip)
    RG = Painter((-160, -120, 1240, 2040), res=1.0); desert_sky(RG, 61)
    mountains(RG, 1200, range_peaks(-300, 1400, 1200, 420, 640, 160, 240, 62), haze=(40, 34, 48)); haze(RG, 1200, 140, (46, 38, 52), 140)
    RG.poly([(-160, 1420), (300, 1330), (700, 1310), (1240, 1380), (1240, 2040), (-160, 2040)], (16, 12, 12))
    RG.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 6, 8, 0), (3, 3, 4, 255)); ridge = RG.sprite()
    rmd, rmg, rga = moon(560, 520, 160, res=1.2)
    HUN = []
    for i in range(6):
        HP = Painter((-150, 1000, 280, 1340), res=2); nimerigar(HP, 0, 1330, 300 + (i % 3) * 20, sil=True, stoop=0.1 * (i % 2)); HUN.append(HP.sprite())
    t8a, t8b = T("according"), T("they", 2)
    def s8(t):
        lt = t - t8a; p = lt / (t8b - t8a)
        its = [Item(ridge), Item(rmg, add=True, opacity=rga), Item(rmd)]
        for i, x in enumerate((180, 330, 470, 610, 760, 900)):
            its.append(Item(HUN[i], pos=(x + 30 * lt, -abs(math.sin(lt * 7 + i)) * 6 - 10 * (i % 2))))
        return its, (560, 1220, 1.15 + 0.10 * EASE["sine"](p))
    S.append(mk(t8a, t8b, s8, whip=True))
    # S9 — "They fired tiny poisoned arrows": a volley of small arrows streaks across the night sky, green tips
    arrows_r = random.Random(9); VOL = [(arrows_r.uniform(-0.3, 0.6), arrows_r.uniform(500, 1500), arrows_r.uniform(-14, -4)) for _ in range(9)]
    pg = glow_sprite(0, 0, 30, POIS, power=1.5)
    t9a, t9b = T("they", 2), T("and", 1) if False else T("their", 1)
    def s9(t):
        lt = t - t9a; its = [Item(ridge), Item(rmg, add=True, opacity=rga), Item(rmd)]
        for (d0, y0, rt) in VOL:
            q = (lt - d0) / 1.1
            if 0 < q < 1: x = -400 + 1900 * q; y = y0 - 300 * q; its += [Item(ARW, pos=(x - 470, y), rot=rt, anchor=(x, y)), Item(pg, pos=(x + 40, y - 6), add=True, opacity=0.6)]
        return its, (560, 1100, 1.25)
    S.append(mk(t9a, t9b, s9))
    # S9b — "their name is often translated as people eaters": a black cave, eyes open in rows
    cdark = cave_wall(0.35, False, 14)
    EYES2 = [(x, y) for y in (700, 900, 1100, 1300) for x in (180, 400, 620, 860)]
    t9c, t9d = T("their", 1), T("but")
    def s9b(t):
        lt = t - t9c; its = [Item(cdark)]
        for i, (x, y) in enumerate(EYES2):
            o = min(1, max(0, (lt - random.Random(i).uniform(0, 2.6)) / 0.1)) * (0 if (lt * 3 + i) % 4.7 < 0.08 else 1)
            its += [Item(glg, pos=(x, y), add=True, opacity=0.3 * o), Item(glint, pos=(x, y), opacity=o)]
        return its, (540, 1000, 1.0 + 0.10 * lt / (t9d - t9c))
    S.append(mk(t9c, t9d, s9b))
    # S10 — "But here's the terrifying part": the camper's face in a headlamp's glow, beanie, flannel; trembling
    cface, ceyes = camper_portrait()
    PB = Painter((-60, -60, 1140, 1980), res=1.0); PB.gfill((8, 6, 6), (20, 14, 12)); PB.glow(540, 900, 700, (90, 60, 34), 0.9, 1.5); pbg = PB.sprite()
    t10a, t10b = T("but"), T("youd", 1)
    def s10(t):
        lt = t - t10a; sh = 2 * math.sin(lt * 31)
        return [Item(pbg, opacity=fire_flk(lt)), Item(cface, pos=(sh, 0)), Item(ceyes, pos=(sh, 0), opacity=0 if abs(lt - 1.2) < 0.06 else 1)], (540, 960, 1.0 + 0.08 * lt / (t10b - t10a))
    S.append(mk(t10a, t10b, s10))
    # S11 — "You'd never see them coming": low POV across the sagebrush, nothing there; slow pan
    sg = wyoming_wide(11, peaks=False)
    t11a, t11b = T("youd", 1), T("youd", 2)
    def s11(t):
        lt = t - t11a
        return [Item(sg)] + dustA(lt + 9, 0.25) + [Item(fgA, pos=(200 - 260 * lt, 0), par=1.5)], (380 + 140 * lt, 1450, 1.6)
    S.append(mk(t11a, t11b, s11))
    # S12 — "You'd only hear the arrows": three arrows thunk into a tent pole and a juniper trunk out of nowhere
    TP_ = Painter((-160, -120, 1240, 2040), res=1.0); desert_sky(TP_, 81)
    TP_.gpoly([(-160, 1300), (1240, 1300), (1240, 2040), (-160, 2040)], (56, 44, 40), (24, 20, 18))
    TP_.poly([(560, -120), (700, -120), (720, 2040), (540, 2040)], (54, 40, 30)); [TP_.line([(570 + i * 24, -120), (560 + i * 26, 2040)], (40, 30, 22), 3) for i in range(6)]
    TP_.gpoly([(-160, 1860), (1240, 1860), (1240, 2040), (-160, 2040)], (6, 6, 8, 0), (3, 3, 4, 255)); trunk = TP_.sprite()
    HITS = [(0.25, 700), (0.85, 1060), (1.5, 880)]
    t12a, t12b = T("youd", 2), T("they", 3)
    def s12(t):
        lt = t - t12a; its = [Item(trunk)]; shake = 0
        for (th, y) in HITS:
            if lt > th - 0.18:
                q = min(1, (lt - th + 0.18) / 0.18); x = -500 + (560 - -500) * q; qv = 3 * math.sin(lt * 70) * math.exp(-(lt - th) * 8) if lt > th else 0
                its.append(Item(ARW, pos=(x - 470, y), rot=-4 + qv, anchor=(x, y)))
                if lt > th: shake += 8 * math.exp(-(lt - th) * 14) * math.sin(lt * 90)
        return its, (560 + shake, 900, 1.1)
    S.append(mk(t12a, t12b, s12))
    # S13 — "They say they showed no mercy, not even to their own": shadow play — a ring of little figures around an old one
    cf = cave_wall(1.1, False, 15); fireB = glow_sprite(540, 1700, 700, (255, 140, 50), power=1.3)
    SH = Painter((-160, 600, 1240, 1500), res=0.6); r_ = random.Random(2)
    for i, x in enumerate((80, 260, 820, 1000)): nimerigar(SH, x, 1480, 640 + r_.uniform(-40, 40), sil=True, bow=False, club=(i % 2 == 0))
    nimerigar(SH, 540, 1480, 520, sil=True, bow=False, stoop=1.0)
    SH.blur(4); shadows = SH.sprite()
    t13a, t13b = T("they", 3), T("when")
    def s13(t):
        lt = t - t13a; fl = fire_flk(lt)
        return [Item(cf, opacity=0.9), Item(fireB, add=True, opacity=0.6 * fl), Item(shadows, opacity=0.85, scale=1 + 0.02 * math.sin(lt * 9), anchor=(540, 1480))], (540, 1060, 1.05 + 0.05 * lt)
    S.append(mk(t13a, t13b, s13))
    # S14 — "When one of them grew too old or too sick": the old one, hunched, leaning on a stick, in firelight
    OL = Painter((300, 820, 800, 1520), res=1.4); nimerigar(OL, 540, 1500, 620, bow=False, stoop=1.0); OL.line([(420, 1500), (460, 1180)], (60, 40, 26), 12); old = OL.sprite()
    t14a, t14b = T("when"), T("the", 13) if False else T("others") - 0.26
    def s14(t):
        lt = t - t14a
        return [Item(cf, opacity=0.9), Item(fireB, add=True, opacity=0.55 * fire_flk(lt)), Item(old, pos=(0, 3 * math.sin(lt * 1.5)))], (540, 1160, 1.35 + 0.06 * lt)
    S.append(mk(t14a, t14b, s14))
    # S14b — "the others ended it with a single blow": a club's shadow rises on the wall and falls; on "blow" hard cut to black
    CLB = Painter((-200, -600, 200, 100), res=0.8); CLB.line([(0, 0), (0, -520)], DK, 40); CLB.ell((-80, -640, 80, -470), DK); CLB.blur(3); club = CLB.sprite()
    t14c, t14d = T("others") - 0.26, T("so")
    def s14b(t):
        lt = t - t14c; tb = T("blow") - t14c
        if lt > tb: return [Item(cf, opacity=0.06)], (540, 1060, 1.1)
        ang = -40 + 120 * ease_io(min(1, max(0, (lt - tb + 0.45) / 0.45)))
        return [Item(cf, opacity=0.9), Item(fireB, add=True, opacity=0.6 * fire_flk(lt)), Item(shadows, opacity=0.85), Item(club, pos=(640, 1400), rot=ang, anchor=(640, 1400), opacity=0.9)], (560, 1100, 1.15 + 0.05 * lt)
    S.append(mk(t14c, t14d, s14b))
    # S15 — "So if you're ever camping alone in those mountains tonight": the tent on a slope, lantern glowing through canvas
    tout = tent_scene(False); tglow = glow_sprite(540, 1380, 260, LANT, power=1.4)
    t15a, t15b = T("so"), T("and", 2)
    def s15(t):
        lt = t - t15a; p = lt / (t15b - t15a)
        return [Item(tout), Item(md, pos=(-200, -40)), Item(tglow, add=True, opacity=0.6 * fire_flk(lt))] + dustA(lt + 2, 0.22) + [Item(fgA, pos=(150 - 80 * lt, 0), par=1.4)], (560, 1300 - 40 * p, 1.2 + 0.08 * p)
    S.append(mk(t15a, t15b, s15))
    # S16 — "and you hear tiny footsteps circling your tent": inside, small shadows pass along the lit canvas, round and round
    tin = tent_scene(True)
    SSH = Painter((-140, 700, 160, 1010), res=1.2); nimerigar(SSH, 0, 1000, 300, sil=True, bow=True); SSH.blur(4); ssh = SSH.sprite()
    t16a, t16b = T("and", 2), T("dont", 2)
    def s16(t):
        lt = t - t16a; its = [Item(tin), Item(tglow, pos=(0, 100), add=True, opacity=0.5 * fire_flk(lt))]
        for i in range(3):
            q = (lt * 0.45 + i / 3) % 1; side = -1 if q < 0.5 else 1; u = (q % 0.5) * 2
            x = 540 + side * (100 + 640 * (u if side > 0 else 1 - u)); its.append(Item(ssh, pos=(x, 380), scale=1.4, anchor=(x, 1380), opacity=0.55))
        return its, (540, 1150, 1.08 + 0.05 * lt)
    S.append(mk(t16a, t16b, s16))
    # S17 — "don't open it.": a hand on the zipper, trembling, freezes and pulls away
    ZP = Painter((-160, -120, 1240, 2040), res=1.0); ZP.gfill((62, 48, 32), (40, 30, 20)); ZP.line([(540, -120), (540, 2040)], (90, 90, 96), 16)
    for y in range(-120, 2040, 22): ZP.line([(526, y), (554, y + 8)], (120, 120, 126), 4)
    zp = ZP.sprite()
    HP_ = Painter((-20, -110, 820, 110), res=1.1); HP_.rrect((0, -62, 620, 62), 30, FLN); HP_.ell((610, -50, 730, 50), SKIN)
    for i, dy in enumerate((-0.30, -0.10, 0.10, 0.28)): HP_.rrect((690, 110 * dy - 11, 710 + (60, 70, 66, 52)[i], 110 * dy + 11), 10, SKIN)
    hand = HP_.sprite()
    t17a, t17b = T("dont", 2), T("because", 2)
    def s17(t):
        lt = t - t17a; back = ease_io(min(1, max(0, (lt - 0.6) / 0.4))); tr = 3 * math.sin(lt * 40)
        return [Item(zp), Item(tglow, pos=(0, -300), add=True, opacity=0.4), Item(hand, pos=(-260 - 260 * back + tr, 980), rot=-6, anchor=(-260, 980))], (540, 980, 1.3)
    S.append(mk(t17a, t17b, s17))
    # S18 — "Because the one they found in that cave... was never the only one.": lantern beam sweeps a cave mouth full of eyes,
    #        then one face, close; chitter rises (reveal variant for EP05)
    cmouth = cave_wall(0.7, True, 18)
    MANY = [(380 + (i % 4) * 110 + random.Random(i).uniform(-20, 20), 820 + (i // 4) * 110 + random.Random(i + 9).uniform(-20, 20)) for i in range(12)]
    beam = beam_sprite(1240, 1700, 560, 940, 120, 520, LANT, 0.45, 0.10, res=0.4, blur=40)
    np_rev = nim_portrait("reveal"); gl2 = nim_glints()
    PB2 = Painter((-60, -60, 1140, 1980), res=1.0); PB2.gfill((6, 4, 4), (14, 10, 8)); PB2.glow(540, 900, 700, (90, 56, 30), 0.9, 1.4); pbg2 = PB2.sprite()
    t18a = T("because", 2); t18b = T("never", 3)
    def s18(t):
        lt = t - t18a; sweep = ease_io(min(1, lt / (t18b - t18a)))
        its = [Item(cmouth), Item(beam, pos=(-500 + 600 * sweep, 0), add=True, opacity=0.8)]
        for i, (x, y) in enumerate(MANY):
            o = 1 if abs(x - (60 + 600 * sweep + 480)) < 340 or lt > 1.6 else 0.25
            its += [Item(glg, pos=(x, y), add=True, opacity=0.35 * o), Item(glint, pos=(x, y), opacity=o)]
        return its, (560, 960, 1.3 + 0.15 * sweep)
    S.append(mk(t18a, t18b, s18))
    def s18b(t):
        lt = t - t18b
        return [Item(pbg2, opacity=fire_flk(lt)), Item(np_rev), Item(gl2, opacity=0 if abs(lt - 1.5) < 0.06 else 1)], (540, 1000, 1.05 + 0.25 * EASE["sine"](min(1, lt / 2.4)))
    S.append(mk(t18b, END, s18b))
    # ---- extra cuts on long shots ----
    def split(idx_fn, t_cut, cam_fn):
        i = next(k for k, s_ in enumerate(S) if s_["fn"].__name__ == idx_fn)
        a = S[i]; f0 = a["fn"]
        def f2(t, f0=f0, t_cut=t_cut):
            its, cam = f0(t); return its, cam_fn(t - t_cut, cam)
        f2.__name__ = idx_fn + "b2"
        S[i] = mk(a["t0"], t_cut, f0, a["whip"]); S.insert(i + 1, mk(t_cut, a["t1"], f2))
    split("s1", T("between"), lambda lt, c: (560, 1310, 2.2 + 0.08 * lt))
    split("s8", T("fierce"), lambda lt, c: (520, 1200, 1.9 + 0.05 * lt))
    split("s5", T("prospectors"), lambda lt, c: (560, 1200, 1.8 + 0.05 * lt))
    split("s6", T("14"), lambda lt, c: (640, 920, 1.55 + 0.04 * lt))
    split("s6", T("was", 1), lambda lt, c: (560, 930, 1.8 + 0.05 * lt))
    return S

# ================= captions =================
CHUNKS = ["In Wyoming,", "if you hear", "something small", "moving between the rocks", "at night,", "#don't follow it into the dark.", "Because in", "the old stories",
          "of the Shoshone,", "those mountains", "were never empty.", "They call them", "the Nimerigar,", "the little people.", "In the 1930s,", "two gold prospectors",
          "blasted open a cave", "in the Pedro Mountains.", "Inside,", "sitting cross-legged", "on a ledge,", "was a mummified figure", "barely 14 inches tall.",
          "Years later,", "it disappeared.", "According to the legend,", "the Nimerigar", "were fierce little hunters", "of the Wind River Mountains.", "They fired",
          "tiny poisoned arrows,", "and their name", "is often translated", "as people-eaters.", "But here's the", "terrifying part.", "You'd never", "see them coming.",
          "You'd only", "hear the arrows.", "They say", "they showed no mercy,", "not even", "to their own.", "When one of them", "grew too old", "or too sick,",
          "the others ended it", "with a single blow.", "So, if you're ever", "camping alone", "in those mountains", "tonight,", "and you hear", "tiny footsteps",
          "circling your tent,", "don't open it.", "Because the one", "they found in that cave", "was never", "the only one."]
RED = {"WYOMING,", "SMALL", "ROCKS", "SHOSHONE,", "EMPTY.", "NIMERIGAR,", "LITTLE", "1930S,", "GOLD", "CAVE", "PEDRO", "MUMMIFIED", "14", "DISAPPEARED.", "LEGEND,",
       "FIERCE", "POISONED", "PEOPLE-EATERS.", "TERRIFYING", "COMING.", "ARROWS.", "MERCY,", "OWN.", "BLOW.", "ALONE", "FOOTSTEPS", "TENT,", "OPEN", "NEVER", "ONLY"}
def build_chunks():
    out = []; k = 0
    for c in CHUNKS:
        hidden = c.startswith("#"); ws = []
        for tok in c.lstrip("#").split():
            m = words[k]; k += 1
            while k < len(words) and words[k]["w"].strip().startswith("-"): k += 1          # "cross -legged", "people -eaters"
            txt = tok.upper()
            red = txt in RED and not (txt == "LITTLE" and "PEOPLE" not in c.upper()) and not (txt == "NEVER" and "WAS NEVER" not in c.upper()) and not (txt == "OPEN" and "DON'T" not in c.upper())
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
    WH = 0.24
    def frame(n):
        t = n / FPS; i = shot_at(t); img = rend(i, t)
        if SH[i]["whip"] and i > 0 and t - SH[i]["t0"] < WH:                              # arrow whip-pan: old frame flies left, new one in from the right
            a = (t - SH[i]["t0"]) / WH; a = a * a * (3 - 2 * a)
            prev = rend(i - 1, t); off = int(W * 0.9 * a)
            comb = np.zeros_like(img); comb[:, : W - off] = prev[:, off:]; comb[:, W - off:] = img[:, : off] if off else comb[:, W - off:]
            k = max(3, int(140 * math.sin(math.pi * a))); img = cv2.blur(comb, (k, 1))
            y = int(H * 0.46); img[y - 3:y + 3, :, :] = img[y - 3:y + 3, :, :] * 0.4 + np.array([200, 170, 120], np.float32) * 0.6 * math.sin(math.pi * a)
        hook = SH[i]["fn"].__name__ in ("s2", "s0j")          # no captions on the hook card or over the jump scare
        if SH[i]["fn"].__name__ != "s2":
            img = vignette(img, 0.6)
            lum = img.mean(axis=2, keepdims=True); img = img * 0.9 + lum * 0.1
            img = img * np.array([1.06, 0.98, 0.86], np.float32) + np.array([6, 2, 0], np.float32)     # EP05 grade: warm red rock / ochre
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
    out = os.path.join(EP, "ep05_noaudio.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    nf = int(math.ceil(END * FPS))
    for n in range(nf):
        pr.stdin.write(frame(n).tobytes())
        if n % 150 == 0: print("frame", n, "/", nf, flush=True)
    pr.stdin.close(); pr.wait(); print("wrote", out, "%.2f s" % (nf / FPS))

if __name__ == "__main__":
    main()
