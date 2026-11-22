"""render_ep06.py — EP06 "La Mala Hora" (New Mexico, Hispano folklore; TT-001) in the Dark Atlas Tales style, Milo narration.
Usage: python -I render_ep06.py <dark_atlas_dir> [stills "t1,t2,..." [out.jpg]]
Per-episode variations (bảng biến thể): title = a row of farolitos lights up left to right, the title rises in candle light;
soft transitions = a black REBOZO (shawl) wipes across the frame; camera = long, slow LATERAL dolly; grade = near-monochrome
indigo / moon-silver with chile-red accents; reveal = the woman in black slowly TURNS HER HEAD; hook accent = a shawled shadow
passes over the card; cold open = a black lump of wool breathing in the middle of a dirt crossroads.
Shot plan: dark_atlas/TT/TT-001_la-mala-hora/EXPORT/05-TT-SHOTLIST-la-mala-hora.csv (re-anchored on the real transcript).
"""
import sys, os, json, math, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from style import *

ROOT = sys.argv[1]; EP = os.path.join(ROOT, "EP06_la_mala_hora")
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
SKY_T, SKY_B, ADOBE, ADOBE_D, ADOBE_L = tup("sky_top"), tup("sky_bot"), tup("adobe"), tup("adobe_d"), tup("adobe_l")
DIRT, DIRT_D, MOONS, RISTRA, RISTRA_D = tup("dirt"), tup("dirt_d"), tup("moon_silver"), tup("ristra"), tup("ristra_d")
FARO, DOOR_B, DOOR_T = tup("farolito"), tup("door_blue"), tup("door_turq")
REB, REB_L, MSK, MSK_D, MHAIR = tup("mala_rebozo"), tup("mala_rebozo_l"), tup("mala_skin"), tup("mala_skin_d"), tup("mala_hair")
WOOL, WOOL_L, HOOD, HOOD_D, FLASH = tup("wool"), tup("wool_l"), tup("walker_hoodie"), tup("walker_hoodie_d"), tup("flash")
SKIN = (196, 160, 130); SKIN_D = (160, 128, 104); DK = (6, 6, 10)
def dim(c, k): return tuple(int(min(255, v * k)) for v in c[:3])
def flk(lt, ph=0.0): return 0.80 + 0.12 * math.sin(lt * 9 + ph) + 0.08 * math.sin(lt * 23 + ph * 2)
BOX = (-160, -120, 1240, 2040)

# ================= scenery =================
def night_sky(P, seed, horizon=1060):
    P.gfill(SKY_T, SKY_B); stars(P, (P.x0, P.y0, P.x1, P.y0 + (horizon - P.y0) * 0.85), 260, seed, a=160)

def mesa(P, x0, x1, base, top, col):
    w = x1 - x0
    pts = [(x0 - w * 0.3, base), (x0, top + (base - top) * 0.35), (x0 + w * 0.05, top), (x1 - w * 0.05, top), (x1, top + (base - top) * 0.3), (x1 + w * 0.35, base)]
    P.gpoly(pts, col, dim(col, 0.6), top, base); P.line([(x0 + w * 0.05, top + 3), (x1 - w * 0.05, top + 3)], dim(col, 1.35), 3)

def adobe_house(P, x, base, w, h, col=None, door=None, window=False, lit=False, ristra=True, vigas=True):
    """flat-roof adobe: rounded parapet, protruding vigas, deep-set door/window, optional red chile ristra."""
    c = col or ADOBE; k = w / 400
    P.rrect((x, base - h, x + w, base), 18 * k, c)
    P.gpoly([(x + w * 0.62, base - h + 10), (x + w, base - h + 10), (x + w, base), (x + w * 0.62, base)], (0, 0, 0, 0), (0, 0, 0, 70))
    P.rrect((x - 6 * k, base - h - 14 * k, x + w + 6 * k, base - h + 16 * k), 10 * k, dim(c, 1.12))
    if vigas:
        for i in range(5): vx = x + w * (0.12 + i * 0.19); P.rect((vx, base - h + 26 * k, vx + 16 * k, base - h + 42 * k), dim(c, 0.55))
    if door:
        P.rrect((x + w * 0.38, base - h * 0.55, x + w * 0.62, base), 30 * k, door); P.line([(x + w * 0.5, base - h * 0.55 + 20), (x + w * 0.5, base)], dim(door, 0.7), 3 * k)
    if window:
        wc = FARO if lit else (18, 20, 34)
        P.rect((x + w * 0.70, base - h * 0.72, x + w * 0.88, base - h * 0.44), wc)
        P.line([(x + w * 0.79, base - h * 0.72), (x + w * 0.79, base - h * 0.44)], dim(c, 0.5), 4 * k)
    if ristra:
        rx = x + w * (0.30 if door else 0.2); ry = base - h * 0.78
        P.line([(rx, ry - 10), (rx, ry + 150 * k)], (60, 40, 20), 3 * k)
        for i in range(12):
            yy = ry + i * 12 * k
            for sx in (-1, 1): P.ell((rx + sx * 4 * k - 9 * k, yy, rx + sx * 4 * k + 9 * k, yy + 22 * k), RISTRA if (i + sx) % 3 else RISTRA_D)

def adobe_church(P, x, base, w, h, col=None):
    c = col or ADOBE
    adobe_house(P, x, base, w, h, c, door=(40, 30, 26), ristra=False)
    bx0, bx1 = x + w * 0.3, x + w * 0.7
    P.rrect((bx0, base - h - 160, bx1, base - h + 10), 12, dim(c, 1.05))                       # bell tower
    P.rrect((bx0 + (bx1 - bx0) * 0.3, base - h - 130, bx1 - (bx1 - bx0) * 0.3, base - h - 50), 30, (14, 14, 22))
    P.ell((bx0 + (bx1 - bx0) * 0.38, base - h - 110, bx1 - (bx1 - bx0) * 0.38, base - h - 66), (120, 100, 60))   # bell
    P.line([((bx0 + bx1) / 2, base - h - 230), ((bx0 + bx1) / 2, base - h - 160)], dim(c, 0.6), 7)
    P.line([((bx0 + bx1) / 2 - 26, base - h - 205), ((bx0 + bx1) / 2 + 26, base - h - 205)], dim(c, 0.6), 7)

def yucca(P, x, base, s, col=(26, 30, 40)):
    P.line([(x, base), (x + 6 * s, base - 160 * s)], dim(col, 0.8), 10 * s)
    for i in range(16):
        a = math.radians(20 + i * 9.4); P.line([(x + 6 * s, base - 150 * s), (x + 6 * s + math.cos(a) * 90 * s, base - 150 * s - math.sin(a) * 90 * s)], col, 5 * s)

def cholla(P, x, base, s, col=(30, 34, 44)):
    P.line([(x, base), (x, base - 120 * s)], col, 18 * s)
    for sx, y in ((-1, 70), (1, 90), (-1, 110)): P.line([(x, base - y * s), (x + sx * 50 * s, base - (y + 20) * s), (x + sx * 56 * s, base - (y + 60) * s)], col, 13 * s)

def descanso(P, x, base, s, lit=True):
    """roadside memorial: small wooden cross wrapped with paper flowers, a candle at its foot."""
    wood = (70, 54, 40)
    P.rect((x - 7 * s, base - 200 * s, x + 7 * s, base), wood); P.rect((x - 50 * s, base - 160 * s, x + 50 * s, base - 146 * s), wood)
    for i, (dx, dy) in enumerate([(-30, 150), (20, 158), (0, 120), (-12, 60), (14, 40)]):
        P.circ(x + dx * s, base - dy * s, 10 * s, [(150, 40, 60), (170, 130, 50), (90, 60, 120)][i % 3])
    if lit: P.rect((x + 20 * s, base - 40 * s, x + 34 * s, base), (200, 190, 160)); P.circ(x + 27 * s, base - 46 * s, 5 * s, FARO)

def zia_sign(P, x, base, s):
    """New Mexico state route marker: square sign, red Zia sun on yellow, on a post."""
    P.rect((x - 5 * s, base - 260 * s, x + 5 * s, base), (60, 60, 66))
    P.rect((x - 60 * s, base - 360 * s, x + 60 * s, base - 240 * s), (150, 130, 50))
    cx, cy = x, base - 300 * s; red = (150, 34, 30)
    P.circ(cx, cy, 18 * s, red)
    for a in (0, 90, 180, 270):
        r = math.radians(a); ux, uy = math.cos(r), math.sin(r); px, py = -uy, ux
        for j in (-1.5, -0.5, 0.5, 1.5):
            ox, oy = cx + px * j * 7 * s, cy + py * j * 7 * s; L = (42 if abs(j) < 1 else 34) * s
            P.line([(ox + ux * 22 * s, oy + uy * 22 * s), (ox + ux * L, oy + uy * L)], red, 4 * s)

def farolito_sprite(lit):
    P = Painter((-40, -80, 40, 10), res=2)
    P.poly([(-26, 0), (26, 0), (22, -66), (-22, -66)], (150, 120, 80) if lit else (60, 54, 52))
    P.poly([(-22, -66), (22, -66), (16, -74), (-16, -74)], (120, 96, 64) if lit else (48, 44, 42))
    if lit: P.glow(0, -24, 30, (255, 220, 150), 0.9, 1.4)
    return P.sprite()

def wool_lump(seed=1, w=300, h=150):
    """black wool lump: many overlapping dark tufts, coarse strands, faint silver rim on top (moonlight). Base at y=0."""
    r = random.Random(seed); P = Painter((-w * 0.8, -h * 1.6, w * 0.8, h * 0.25), res=1.2)
    P.ell((-w * 0.62, -h * 0.12, w * 0.62, h * 0.18), (0, 0, 0, 120))
    for _ in range(70):
        cx = r.gauss(0, w * 0.22); cy = -h * 0.45 - r.random() * h * 0.6 + abs(cx) / w * h * 0.8; rr = r.uniform(18, 42) * w / 300
        P.ell((cx - rr * 1.3, cy - rr, cx + rr * 1.3, cy + rr), dim(WOOL, r.uniform(0.7, 1.25)))
    for _ in range(90):
        a = r.uniform(0, math.pi); x0 = math.cos(a) * w * 0.42; y0 = -math.sin(a) * h * 0.8 - h * 0.05
        L = r.uniform(18, 50); P.line([(x0, y0), (x0 + math.cos(a + r.uniform(-0.6, 0.6)) * L, y0 - math.sin(a) * L * 0.8)], WOOL_L if r.random() < 0.3 else WOOL, 2.5)
    P.arc((-w * 0.4, -h * 1.3, w * 0.4, -h * 0.2), 200, 340, dim(MOONS, 0.45), 4)
    return P.sprite()

def fleece_sprite(seed=3):
    """a whole sheep's fleece lying flat (top-down): irregular hide outline with leg flaps, matted dark curls."""
    r = random.Random(seed); P = Painter((-420, -300, 420, 300), res=1.0)
    pts = [(math.cos(a) * (330 + r.uniform(-30, 30) + (90 if abs(math.sin(2 * a)) > 0.92 else 0)), math.sin(a) * (220 + r.uniform(-20, 20))) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
    P.poly(pts, dim(WOOL, 1.1))
    for _ in range(260):
        x, y = r.uniform(-300, 300), r.uniform(-190, 190)
        if (x / 320) ** 2 + (y / 210) ** 2 < 1: P.arc((x - 16, y - 12, x + 16, y + 12), r.uniform(0, 180), r.uniform(200, 360), WOOL_L if r.random() < 0.35 else dim(WOOL, 0.7), 3)
    return P.sprite()

def ground(P, top, col=None):
    c = col or DIRT; P.gpoly([(P.x0, top), (P.x1, top), (P.x1, P.y1), (P.x0, P.y1)], c, dim(c, 0.45))

def bottom_fade(P): P.gpoly([(P.x0, 1860), (P.x1, 1860), (P.x1, P.y1), (P.x0, P.y1)], (4, 4, 8, 0), (2, 2, 4, 255))

def crossroads_bg(seed=1, church=True):
    """the cold-open set: indigo sky, mesa, adobe village + church, dirt crossroads in perspective, descanso, Zia marker."""
    P = Painter(BOX, res=1.0); night_sky(P, seed)
    mesa(P, 560, 1100, 1040, 860, (30, 32, 52)); mesa(P, -200, 160, 1050, 940, (26, 28, 46))
    haze(P, 1040, 110, (40, 44, 70), 120)
    if church: adobe_church(P, 640, 1080, 300, 170, dim(ADOBE, 0.8))
    adobe_house(P, 120, 1085, 260, 140, dim(ADOBE, 0.75), door=dim(DOOR_B, 0.7), window=True, lit=True)
    adobe_house(P, 960, 1080, 220, 120, dim(ADOBE, 0.7), window=True, ristra=False)
    ground(P, 1070)
    P.gpoly([(-160, 1150), (1240, 1150), (1240, 1250), (-160, 1250)], dim(DIRT, 1.25), dim(DIRT, 1.05))      # E-W road
    P.gpoly([(500, 1070), (580, 1070), (900, 2040), (180, 2040)], dim(DIRT, 1.1), dim(DIRT, 1.3))           # N-S road (perspective)
    for i in range(30):
        rr = random.Random(seed * 50 + i); P.circ(rr.uniform(-160, 1240), rr.uniform(1260, 1900), rr.uniform(2, 5), dim(DIRT, 0.6))
    descanso(P, 150, 1420, 1.3); zia_sign(P, 960, 1330, 1.1); yucca(P, -40, 1560, 1.6); cholla(P, 1120, 1640, 1.5); yucca(P, 1060, 1180, 0.6)
    bottom_fade(P); return P.sprite()

def lane_bg(seed=2):
    """adobe wall along the dirt lane: ristras, blue door, farolitos on the wall top."""
    P = Painter((-500, -120, 1700, 2040), res=1.0); night_sky(P, seed, 900)
    mesa(P, 700, 1500, 1000, 820, (30, 32, 52))
    P.rect((-500, 640, 1700, 1300), dim(ADOBE, 0.9)); P.rect((-500, 620, 1700, 660), dim(ADOBE_L, 0.8))
    for x in range(-460, 1700, 260): P.rrect((x, 700, x + 120, 1300), 8, dim(ADOBE, 0.82))
    P.rrect((380, 860, 560, 1300), 40, DOOR_B); P.line([(470, 870), (470, 1300)], dim(DOOR_B, 0.7), 4)
    for rx in (330, 610, 1210): P.line([(rx, 720), (rx, 900)], (60, 40, 20), 3); [P.ell((rx - 12 + (i % 2) * 6, 720 + i * 14, rx + 12 + (i % 2) * 6, 744 + i * 14), RISTRA if i % 3 else RISTRA_D) for i in range(13)]
    ground(P, 1300); bottom_fade(P); return P.sprite()

def walker_back(P, x, feet, h, col=None):
    """modern walker from behind: hood up, hands in pockets, jeans; muted denim hoodie (never white)."""
    c = col or HOOD; k = h / 1000
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-150), Y(20), X(150), Y(-20)), (0, 0, 0, 90))
    for lx, sw in ((-70, 0), (10, 0)): P.rrect((X(lx), Y(470), X(lx + 62), Y(0)), 16 * k, (30, 34, 48))
    P.rrect((X(-150), Y(860), X(150), Y(420)), 60 * k, c); P.gpoly([(X(30), Y(860)), (X(150), Y(860)), (X(150), Y(420)), (X(30), Y(420))], (0, 0, 0, 0), (0, 0, 0, 60))
    P.ell((X(-100), Y(1000), X(100), Y(800)), dim(c, 0.9)); P.arc((X(-90), Y(990), X(90), Y(820)), 200, 300, dim(MOONS, 0.5), 4 * k)

def traveler_1910(P, x, feet, h):
    k = h / 1000
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    for lx in (-60, 14): P.rect((X(lx), Y(460), X(lx + 46), Y(0)), DK)
    P.poly([(X(-110), Y(820)), (X(110), Y(820)), (X(130), Y(420)), (X(-130), Y(420))], DK)
    P.ell((X(-62), Y(980), X(62), Y(840)), DK); P.ell((X(-130), Y(950), X(130), Y(915)), DK); P.rrect((X(-70), Y(1030), X(70), Y(930)), 18 * k, DK)
    P.line([(X(110), Y(780)), (X(190), Y(560))], DK, 34 * k); P.line([(X(190), Y(560)), (X(190), Y(470))], (40, 40, 40), 4 * k)
    P.rrect((X(160), Y(470), X(220), Y(380)), 8 * k, (90, 80, 60)); P.rect((X(172), Y(455), X(208), Y(395)), FARO)

def mala_back(P, x, feet, h, hair_ph=0.0, hands=True):
    """La Mala Hora from behind: black rebozo over the head and shoulders, very long tangled hair below it, black dress, ash hands."""
    k = h / 1000
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-220), Y(16), X(220), Y(-20)), (0, 0, 0, 120))
    P.gpoly([(X(-120), Y(600)), (X(120), Y(600)), (X(230), Y(0)), (X(-230), Y(0))], REB, dim(REB, 0.7), Y(600), Y(0))           # dress
    for i in range(15):                                                                                                   # tangled hair below the shawl
        hx = -110 + i * 15.7; ph = hair_ph + i * 0.9
        pts = [(X(hx + 10 * math.sin(ph + j)), Y(760 - j * 95)) for j in range(8)]
        P.line(pts, MHAIR, 15 * k)
    P.poly([(X(-60), Y(1000)), (X(60), Y(1000)), (X(150), Y(900)), (X(210), Y(560)), (X(170), Y(520)), (X(-170), Y(520)), (X(-210), Y(560)), (X(-150), Y(900))], REB)   # rebozo
    for fx in (-120, -60, 0, 60, 120): P.line([(X(fx * 0.4), Y(960)), (X(fx), Y(540))], REB_L, 3 * k)
    for fx in range(-160, 170, 22): P.line([(X(fx), Y(530)), (X(fx + 4), Y(480))], REB_L, 2 * k)                           # fringe
    P.arc((X(-150), Y(1010), X(150), Y(560)), 200, 300, dim(MOONS, 0.55), 5 * k)                                          # moon rim
    if hands:
        for sx in (-1, 1): P.poly([(X(sx * 190), Y(560)), (X(sx * 214), Y(560)), (X(sx * 222), Y(470)), (X(sx * 196), Y(460))], MSK)

def mala_portrait(mode="dark", turn=1.0):
    """close portrait: rebozo hood framing an ash-grey split-tone face, hollow black eyes, tangled hair; mode 'reveal' opens a
    mouth of stylised teeth (no blood). turn<1 = 3/4 view (face shifted, far eye narrow)."""
    D = Painter((-60, 300, 1140, 1980), res=1.2); off = (1 - turn) * -170; nw = 0.65 + 0.35 * turn
    D.poly([(-60, 1980), (1140, 1980), (1000, 1340), (80, 1340)], REB)                                                     # shoulders/shawl
    for i in range(22):                                                                                                    # hair strands
        sx = -1 if i < 11 else 1; j = i % 11; x0 = 540 + sx * (210 + j * 18) + off * 0.5
        D.line([(x0, 820 + j * 10), (x0 + sx * 20 + 18 * math.sin(i), 1300), (x0 + sx * 40 - 10 * math.sin(i * 2), 1950)], MHAIR, 14)
    D.ell((120, 360, 960, 1500), REB); D.ell((190, 470, 890, 1380), (4, 4, 6))                                             # hood + its shadow
    cx = 540 + off; fw = 210 * nw
    D.ell((cx - fw, 620, cx + fw, 1290), MSK); D.pie((cx - fw, 620, cx + fw, 1290), -90, 90, MSK_D)
    D.chord((cx - fw - 20, 560, cx + fw + 20, 860), 180, 360, MHAIR)                                                          # hair under hood
    for sx in (-1, 1):
        ex = cx + sx * 92 * nw; ew = 62 * (nw if sx > 0 else 1) * (0.55 if (turn < 0.8 and sx > 0) else 1)
        D.ell((ex - ew, 860, ex + ew, 980), (2, 2, 4)); D.arc((ex - ew - 14, 840, ex + ew + 14, 1000), 200, 340, MSK_D, 8)
        D.arc((ex - ew, 980, ex + ew, 1040), 20, 160, MSK_D, 4)
    D.arc((cx - fw * 0.8, 1040, cx - fw * 0.2, 1200), 100, 200, MSK_D, 6); D.arc((cx + fw * 0.2, 1040, cx + fw * 0.8, 1200), 340, 80, MSK_D, 6)   # hollow cheeks
    D.poly([(cx - 10, 1000), (cx + 10, 1000), (cx + 26, 1090), (cx - 26, 1090)], MSK_D); D.ell((cx - 22, 1080, cx - 6, 1094), (20, 20, 26)); D.ell((cx + 6, 1080, cx + 22, 1094), (20, 20, 26))
    for i in range(4): D.line([(cx - 120 * nw + i * 30, 700 + i * 8), (cx - 100 * nw + i * 30, 760 + i * 6)], MSK_D, 3)        # ash cracks
    if mode == "reveal":
        D.chord((cx - 120 * nw, 1120, cx + 120 * nw, 1260), 0, 180, (10, 8, 12))
        for i in range(11): tx = cx - 108 * nw + i * 21 * nw; D.poly([(tx, 1150), (tx + 18 * nw, 1150), (tx + 9 * nw, 1192)], (186, 184, 176))
        for i in range(9): tx = cx - 92 * nw + i * 22 * nw; D.poly([(tx, 1238), (tx + 18 * nw, 1238), (tx + 9 * nw, 1204)], (166, 164, 156))
    else:
        D.line([(cx - 70 * nw, 1170), (cx, 1182), (cx + 70 * nw, 1170)], (30, 30, 36), 7)
    return D.sprite()

def mala_glints(turn=1.0):
    off = (1 - turn) * -170; nw = 0.65 + 0.35 * turn; E = Painter((200, 880, 900, 960), res=2)
    for sx in (-1, 1):
        if turn < 0.8 and sx > 0: continue
        ex = 540 + off + sx * 92 * nw; E.circ(ex + 14, 906, 10, (236, 240, 255)); E.circ(ex - 16, 930, 4, (180, 186, 200))
    return E.sprite()

def head_back_sprite():
    """close back of the head for the head-turn reveal: hood + hair, no face."""
    D = Painter((-60, 300, 1140, 1980), res=1.2)
    D.poly([(-60, 1980), (1140, 1980), (1000, 1340), (80, 1340)], REB)
    for i in range(26): x0 = 300 + i * 19; D.line([(x0, 900), (x0 + 16 * math.sin(i), 1500), (x0 - 12 * math.sin(i * 1.7), 1960)], MHAIR, 15)
    D.ell((120, 360, 960, 1500), REB)
    for fx in range(200, 900, 70): D.line([(540 + (fx - 540) * 0.3, 420), (fx, 1440)], REB_L, 4)
    D.arc((130, 370, 950, 1490), 200, 320, dim(MOONS, 0.5), 10)
    return D.sprite()

# ================= SHOTS =================
def mk(t0, t1, fn, wipe=False): return dict(t0=t0, t1=t1, fn=fn, wipe=wipe)

def build_all():
    S = []
    cross = crossroads_bg(1); md, mg, ga = moon(800, 330, 70, res=1.4)
    WL = [wool_lump(11)]; dust = glow_sprite(0, 0, 10, dim(MOONS, 0.7), power=1.3, res=1.5)
    dr = random.Random(5); DP = [(dr.uniform(-160, 1240), dr.uniform(1000, 1900), dr.uniform(0.5, 1.5), dr.uniform(0, 6.28)) for _ in range(36)]
    def dusts(lt, op=0.25, wind=30):
        return [Item(dust, pos=(-160 + ((x + 160) + lt * wind * s) % 1400, y + 10 * math.sin(lt + ph)), add=True, opacity=op * min(1, s), scale=s, anchor=(-160 + ((x + 160) + lt * wind * s) % 1400, y)) for (x, y, s, ph) in DP]
    def breathe(lt, rate=1.6, amt=0.06): return 1 + amt * (0.5 + 0.5 * math.sin(lt * rate * 2 * math.pi / 3))
    def wool_item(lt, x=540, y=1205, s=0.9, amt=0.06): return Item(WL[0], pos=(x, y), scale=s * breathe(lt, amt=amt), anchor=(x, y))
    # s0 — cold open: dirt crossroads in an adobe village, wool lump breathing in the centre; long lateral dolly
    def s0(t):
        lt = t
        return [Item(cross), Item(mg, add=True, opacity=ga), Item(md), wool_item(lt)] + dusts(lt), (640 - 60 * lt, 1120, 1.12)
    S.append(mk(0, 0.85, s0))
    # s0j — JUMP SCARE: her face whips in from the left edge, fills the frame; silver-white flash, hard shake
    pj = mala_portrait("reveal"); gj = mala_glints()
    JB = Painter((-60, -60, 1140, 1980), res=0.5, ss=1); JB.gfill((4, 4, 10), (0, 0, 2)); JB.glow(540, 1000, 900, (40, 50, 90), 0.9, 1.2); jbg = JB.sprite()
    RIM = glow_sprite(540, 1000, 700, (150, 170, 230), power=1.6)
    SHD = Painter((-60, 300, 1140, 1980), res=0.5, ss=1); SHD.gpoly([(-60, 300), (1140, 300), (1140, 1000), (-60, 1000)], (0, 0, 0, 220), (0, 0, 0, 0))
    SHD.glow(540, 1700, 520, (120, 140, 200), 0.5, 1.3); jshade = SHD.sprite()
    whf = Sprite(np.dstack([np.full((8, 8), FLASH[0], np.uint8), np.full((8, 8), FLASH[1], np.uint8), np.full((8, 8), FLASH[2], np.uint8), np.full((8, 8), 255, np.uint8)]), 8 / W, 0, 0)
    tj1 = T("walk", 1)
    def s0j(t):
        lt = t - 0.85; lunge = ease_out(min(1, lt / 0.16))
        z = 3.2 - 1.75 * lunge + 0.08 * lt; xin = -700 * (1 - lunge)
        sh = 26 * math.exp(-lt * 6) * math.sin(lt * 95); sv = 18 * math.exp(-lt * 6) * math.cos(lt * 83)
        its = [Item(jbg), Item(RIM, add=True, opacity=0.5), Item(pj, pos=(xin, 0)), Item(jshade), Item(gj, pos=(xin, 0))]
        fo = 0.8 if lt < 0.07 else max(0, 0.35 - (lt - 0.07) * 1.2)
        if fo > 0: its.append(Item(whf, opacity=fo, par=0.0))
        return its, (540 + sh, 1060 + sv, z)
    S.append(mk(0.85, tj1, s0j))
    # s1 — "walk home alone at night": walker from behind along an adobe wall with ristras and a blue door; lateral track
    lane = lane_bg(2); WK = Painter((300, 900, 780, 1820), res=1.4); walker_back(WK, 540, 1800, 860); wk = WK.sprite()
    t1a, t1b = tj1, T("black", 1)
    def s1(t):
        lt = t - t1a
        return [Item(lane), Item(wk, pos=(150 * lt, 4 * abs(math.sin(lt * 6))))], (520 + 150 * lt, 1200, 1.0)
    S.append(mk(t1a, t1b, s1))
    # s2 — "and black wool is lying at the crossroads": ground-level push toward the lump at the centre of the four roads
    t2a, t2b = T("black", 1), T("dont", 1)
    def s2(t):
        lt = t - t2a; p = lt / (t2b - t2a)
        return [Item(cross), Item(mg, add=True, opacity=ga), Item(md), wool_item(lt, s=1.0, amt=0.08)] + dusts(lt + 3, 0.3), (540, 1170, 1.5 + 0.8 * EASE["sine"](p))
    S.append(mk(t2a, t2b, s2))
    # s3 — HOOK CARD "DON'T CROSS IT." + a shawled shadow passes across the card
    f = ImageFont.truetype(FB, 160); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    hk = "DON'T CROSS IT."; fs = 160
    while d.textlength(hk, font=f) > 980: fs -= 4; f = ImageFont.truetype(FB, fs)
    d.text(((W - d.textlength(hk, font=f)) / 2, 780), hk, font=f, fill=(198, 38, 38, 255))
    hook = Sprite(np.asarray(lay).copy(), 1, 0, 0); hookg = Sprite(np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).copy(), 1, 0, 0)
    SHP = Painter((-300, 200, 300, 1900), res=0.4, ss=1); mala_back(SHP, 0, 1880, 1600, hands=False); SHP.blur(30); shadow = SHP.sprite()
    t3a, t3b = T("dont", 1), T("isnt", 1)
    def s3(t):
        lt = t - t3a; dd = t3b - t3a; op = 1.0 if lt < dd - 0.3 else max(0, (dd - lt) / 0.3); s_ = 1 + 0.035 * lt / dd
        sx = -500 + 2100 * ease_io(min(1, max(0, (lt - 0.5) / 1.1)))
        return [Item(hookg, add=True, opacity=0.8 * op, scale=s_, anchor=(540, 860)), Item(hook, opacity=op, scale=s_, anchor=(540, 860)),
                Item(shadow, pos=(sx, 0), opacity=0.85 * op)], (540, 960, 1.0)
    S.append(mk(t3a, t3b, s3))
    # s4 — "isn't wool": macro on the lump, coarse strands, it rises and falls like breathing
    t4a, t4b = T("isnt", 1), T("waits")
    def s4(t):
        lt = t - t4a
        return [Item(cross, opacity=0.5), wool_item(lt, s=1.0, amt=0.10)], (540, 1150, 4.2 + 0.3 * lt)
    S.append(mk(t4a, t4b, s4))
    # s5 — "only waits for people who are alone": top-down over the four roads; tiny walker approaches the centre
    TD = Painter(BOX, res=1.0); TD.gfill(dim(DIRT, 0.9), dim(DIRT, 0.7))
    TD.rect((-160, 860, 1240, 1060), dim(DIRT, 1.3)); TD.rect((440, -120, 640, 2040), dim(DIRT, 1.3))
    for (hx, hy) in ((-60, 300), (760, 260), (-80, 1300), (780, 1320)): TD.rrect((hx, hy, hx + 420, hy + 420), 30, dim(ADOBE, 0.75)); TD.rect((hx + 20, hy + 20, hx + 400, hy + 400), dim(ADOBE, 0.68))
    TD.circ(330, 1180, 22, (60, 50, 40)); bottom_fade(TD); topd = TD.sprite()
    TW = Painter((-40, -40, 40, 40), res=2); TW.circ(0, 0, 30, HOOD); TW.circ(0, -6, 18, dim(HOOD, 0.8)); tw = TW.sprite()
    t5a, t5b = T("waits"), T("they", 1)
    def s5(t):
        lt = t - t5a; p = lt / (t5b - t5a)
        return [Item(topd), Item(WL[0], pos=(540, 990), scale=0.55 * breathe(lt), anchor=(540, 990)), Item(tw, pos=(540, 1700 - 520 * p))], (540, 1100, 1.0 + 0.15 * p)
    S.append(mk(t5a, t5b, s5))
    # s6 — TITLE CARD: farolitos on an adobe wall light one by one left to right; LA MALA HORA rises in the candle light (rebozo wipe in)
    TC = Painter(BOX, res=1.0); night_sky(TC, 61, 1000); mesa(TC, 300, 1000, 1020, 860, (28, 30, 50))
    TC.rect((-160, 1100, 1240, 1500), dim(ADOBE, 0.55)); TC.rect((-160, 1080, 1240, 1110), dim(ADOBE_L, 0.5)); ground(TC, 1500); bottom_fade(TC); tcb = TC.sprite()
    FOFF, FON = farolito_sprite(False), farolito_sprite(True); FX = [-80 + i * 120 for i in range(12)]
    fglow = glow_sprite(0, 0, 160, FARO, power=1.5)
    lab = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    fr = ImageFont.truetype(FR, 30); fb = ImageFont.truetype(FB, 150)
    s_ = "N E W   M E X I C O   ·   L E G E N D"
    d.rectangle([W / 2 - 22, 110, W / 2 + 22, 115], fill=(190, 46, 40, 255))
    d.text(((W - d.textlength(s_, font=fr)) / 2, 135), s_, font=fr, fill=(186, 176, 160, 255))
    tt = "LA MALA HORA"
    while d.textlength(tt, font=fb) > 980: fb = ImageFont.truetype(FB, fb.size - 4)
    d.text(((W - d.textlength(tt, font=fb)) / 2, 175), tt, font=fb, fill=(232, 220, 196, 255))
    title = Sprite(np.asarray(lab).copy(), 1, 0, 0)
    t6a, t6b = T("they", 1), T("in", 2)
    def s6(t):
        lt = t - t6a; p = lt / (t6b - t6a); its = [Item(tcb)]; lit_n = int(lt / 0.14)
        for i, x in enumerate(FX):
            on = i < lit_n; its.append(Item(FON if on else FOFF, pos=(x, 1100)))
            if on: its.append(Item(fglow, pos=(x, 1060), add=True, opacity=0.45 * flk(lt, i)))
        ta = ease_out(min(1, max(0, (lt - 0.9) / 0.9)))
        its.append(Item(title, pos=(0, 430 + 40 * (1 - ta)), opacity=ta, par=0.0))
        return its, (600 - 90 * p, 1060, 1.12)
    S.append(mk(t6a, t6b, s6, wipe=True))
    # s7 — "In 1910": an old journal page, JOURNAL OF AMERICAN FOLK-LORE, a red 1910 stamp lands (lamp light)
    def paper(sketch=False):
        Pp = Painter(BOX, res=1.0); Pp.gfill((40, 30, 22), (20, 14, 10))
        Pp.gpoly([(60, 140), (1020, 100), (1060, 1980), (40, 2000)], (100, 88, 68), (30, 26, 22), 100, 2000)
        for y in range(520, 1900, 64): Pp.line([(120, y), (980, y - 8)], (84, 74, 58), 2)
        if not sketch:
            fh = ImageFont.truetype(FB, int(54 * Pp.k)); Pp.d.text(Pp.P(540, 330), "JOURNAL OF", font=fh, fill=(40, 30, 24, 255), anchor="mm")
            Pp.d.text(Pp.P(540, 410), "AMERICAN FOLK-LORE", font=fh, fill=(40, 30, 24, 255), anchor="mm")
        else:
            for (a, b) in [((300, 900), (800, 860)), ((560, 560), (520, 1300))]: Pp.line([a, b], (50, 42, 34), 7)
            Pp.line([(540, 640), (540, 700)], (50, 42, 34), 2)
        Pp.glow(300, 200, 700, (255, 190, 110), 0.25, 1.6); return Pp.sprite()
    pg = paper(); ST = Painter((260, 560, 820, 860), res=1.4); ST.rrect((280, 580, 800, 840), 20, (0, 0, 0, 0))
    fst = ImageFont.truetype(FB, int(200 * ST.k)); ST.d.text(ST.P(540, 710), "1910", font=fst, fill=(170, 34, 30, 230), anchor="mm")
    ST.arc((290, 590, 790, 830), 0, 360, (170, 34, 30, 200), 10); stamp = ST.sprite()
    t7a, t7b = T("in", 2), T("recording")
    def s7(t):
        lt = t - t7a; land = T("1910") - t7a; q = ease_out(min(1, max(0, (lt - land + 0.1) / 0.12)))
        its = [Item(pg)]
        if lt > land - 0.1: its.append(Item(stamp, scale=1.6 - 0.6 * q, anchor=(540, 710), opacity=q))
        sh = 6 * math.exp(-max(0, lt - land) * 12) * math.sin(lt * 80) if lt > land else 0
        return its, (540 + sh, 760, 1.25 + 0.06 * lt)
    S.append(mk(t7a, t7b, s7))
    # s8 — "recording Spanish folklore in New Mexico, wrote about her": 1910 adobe room by an oil lamp, a man writing; NM stamp
    IN = Painter(BOX, res=1.0); IN.gfill((52, 40, 30), (30, 22, 18)); IN.glow(360, 1100, 800, (220, 150, 80), 0.75, 1.4)
    for x in range(-160, 1240, 180): IN.rect((x, -120, x + 60, 120), (36, 26, 18))
    IN.rect((700, 420, 1060, 860), (12, 14, 30)); IN.line([(880, 420), (880, 860)], (40, 30, 22), 12); IN.line([(700, 640), (1060, 640)], (40, 30, 22), 12)
    IN.circ(960, 520, 40, dim(MOONS, 0.8))
    IN.rect((-160, 1300, 1240, 1360), (60, 42, 28)); IN.rect((-160, 1360, 1240, 2040), (26, 20, 16))
    IN.rect((60, 1180, 640, 1230), (70, 50, 34)); IN.rect((90, 1230, 120, 1500), (50, 36, 26)); IN.rect((580, 1230, 610, 1500), (50, 36, 26))
    IN.poly([(170, 1150), (330, 1140), (340, 1180), (160, 1180)], (150, 136, 106)); IN.line([(250, 1144), (252, 1180)], (90, 80, 60), 3)
    IN.ell((-20, 760, 120, 900), DK); IN.poly([(-60, 900), (130, 890), (220, 1140), (-40, 1240)], DK); IN.line([(100, 960), (230, 1150)], DK, 34)
    IN.rect((470, 1180, 510, 1300), (90, 80, 60)); IN.ell((450, 1120, 530, 1200), (200, 170, 110)); bottom_fade(IN); inter = IN.sprite()
    lamp = glow_sprite(490, 1150, 300, (255, 190, 100), power=1.5)
    NMS = Painter((780, 1480, 1060, 1760), res=1.5); NMS.poly([(800, 1500), (1000, 1500), (1000, 1520), (1040, 1520), (1040, 1740), (800, 1740)], (0, 0, 0, 0))
    NMS.line([(800, 1500), (1000, 1500), (1000, 1520), (1040, 1520), (1040, 1740), (800, 1740), (800, 1500)], (170, 34, 30, 220), 8)
    fn_ = ImageFont.truetype(FB, int(34 * NMS.k)); NMS.d.text(NMS.P(920, 1630), "NEW MEXICO", font=fn_, fill=(170, 34, 30, 230), anchor="mm"); nms = NMS.sprite()
    t8a, t8b = T("recording"), T("described")
    def s8(t):
        lt = t - t8a; tn = T("new", 2) - t8a
        its = [Item(inter), Item(lamp, add=True, opacity=0.5 * flk(lt))]
        if lt > tn - 0.1: its.append(Item(nms, opacity=min(1, (lt - tn + 0.1) / 0.15), scale=1.3 - 0.3 * ease_out(min(1, (lt - tn + 0.1) / 0.15)), anchor=(920, 1620)))
        return its, (330 + 80 * lt, 1060, 1.12)
    S.append(mk(t8a, t8b, s8))
    # s9 — "a spirit": notebook sketch, a crossroads drawn in pencil, a black scribble appears at its centre
    sk = paper(True); SC = Painter((470, 640, 610, 760), res=2); r9 = random.Random(9)
    for _ in range(40): SC.line([(540 + r9.uniform(-40, 40), 700 + r9.uniform(-30, 30)), (540 + r9.uniform(-40, 40), 700 + r9.uniform(-30, 30))], (14, 12, 10), 3)
    scrib = SC.sprite()
    t9a, t9b = T("described"), T("haunts")
    def s9(t):
        lt = t - t9a
        return [Item(sk), Item(scrib, opacity=min(1, lt / 0.7))], (540, 760 + 20 * lt, 1.5 + 0.1 * lt)
    S.append(mk(t9a, t9b, s9))
    # s10 — "that haunts dark crossroads": wide desert crossroads, mesa, cholla, a Zia route marker; a cloud slides over the moon
    cross2 = crossroads_bg(7, church=False)
    CLD = Painter((-300, -80, 300, 80), res=0.6); CLD.ell((-300, -60, 300, 60), (20, 22, 40, 220)); CLD.blur(20); cld = CLD.sprite()
    t10a, t10b = T("haunts"), T("people", 2)
    def s10(t):
        lt = t - t10a
        return [Item(cross2), Item(mg, add=True, opacity=ga * 0.8), Item(md), Item(cld, pos=(500 + 120 * lt, 330))] + dusts(lt + 6, 0.2), (760 - 80 * lt, 1100, 1.05)
    S.append(mk(t10a, t10b, s10))
    # s11 — "terrorizing people who walk alone at night": a 1910 traveler with a tin lantern, small against the night road
    TR = Painter((-200, 600, 400, 1700), res=1.4); traveler_1910(TR, 100, 1660, 760); trav = TR.sprite()
    lglow = glow_sprite(0, 0, 220, FARO, power=1.5)
    t11a, t11b = T("people", 2), T("most")
    def s11(t):
        lt = t - t11a; x = 120 * lt
        return [Item(cross2), Item(trav, pos=(80 + x, -60)), Item(lglow, pos=(375 + x, 1300), add=True, opacity=0.55 * flk(lt))], (420 + 100 * lt, 1180, 1.35)
    S.append(mk(t11a, t11b, s11))
    # s12 — "Most of the time, it looks like a lock of wool": a single lock tumbles along the road toward the lantern light
    LK = [wool_lump(31, 120, 70)]
    t12a, t12b = T("most"), T("sometimes")
    def s12(t):
        lt = t - t12a; x = 900 - 160 * lt
        return [Item(cross2, opacity=0.9), Item(lglow, pos=(260, 1300), add=True, opacity=0.4 * flk(lt)), Item(LK[0], pos=(x, 1320), rot=-60 * lt, anchor=(x, 1290))] + dusts(lt + 2, 0.25, -60), (x - 40, 1250, 2.2)
    S.append(mk(t12a, t12b, s12))
    # s13 — "Sometimes, a whole sheep's fleece": top-down, an empty fleece spread across the crossroads; its edges ripple
    FL = fleece_sprite(3)
    t13a, t13b = T("sometimes"), T("according")
    def s13(t):
        lt = t - t13a
        return [Item(topd), Item(FL, pos=(540, 960), scale=1 + 0.02 * math.sin(lt * 5), anchor=(540, 960), rot=2 * math.sin(lt * 1.3))], (540, 980, 1.25 + 0.08 * lt)
    S.append(mk(t13a, t13b, s13))
    # s14 — "According to the legend": the fleece rises upright into a standing shape (rebozo wipe in)
    RS = Painter((300, 500, 780, 1500), res=1.2); mala_back(RS, 540, 1480, 940, hands=False); rising = RS.sprite()
    t14a, t14b = T("according"), T("she", 1)
    def s14(t):
        lt = t - t14a; p = ease_io(min(1, lt / (t14b - t14a)))
        return [Item(cross, opacity=0.9), Item(mg, add=True, opacity=ga), Item(md), Item(WL[0], pos=(540, 1480), scale=1.2 * (1 - p) + 0.01, anchor=(540, 1480)),
                Item(rising, scale=0.15 + 0.85 * p, anchor=(540, 1480), opacity=p)], (540, 1060 + 120 * (1 - p), 1.15 + 0.15 * p)
    S.append(mk(t14a, t14b, s14, wipe=True))
    # s15 — "she can also become a woman in black": from behind at the centre of the crossroads, hair moving without wind
    MB = []
    for i in range(6):
        Pm = Painter((260, 400, 820, 1500), res=1.2); mala_back(Pm, 540, 1480, 980, hair_ph=i * 0.8); MB.append(Pm.sprite())
    t15a, t15b = T("she", 1), T("but")
    def s15(t):
        lt = t - t15a; ang = 0.5 * lt
        return [Item(cross), Item(mg, add=True, opacity=ga), Item(md), Item(MB[int(lt * 6) % 6])], (540 + 160 * math.sin(ang), 1060, 1.25)
    S.append(mk(t15a, t15b, s15))
    # s16 — "But here's the terrifying part": slow push toward her back; descanso candle in the foreground gutters out
    DSC = Painter((-200, 1100, 500, 2040), res=1.0); descanso(DSC, 140, 1980, 3.2, lit=False); DSC.blur(6); dsc = DSC.sprite()
    cflame = glow_sprite(0, 0, 60, FARO, power=1.4)
    t16a, t16b = T("but"), T("she", 2)
    def s16(t):
        lt = t - t16a; p = lt / (t16b - t16a); fl = max(0, 1 - max(0, lt - 1.2) / 0.4)
        return [Item(cross, opacity=0.85), Item(md), Item(MB[int(lt * 5) % 6]), Item(dsc, par=1.3), Item(cflame, pos=(226, 1833), add=True, opacity=0.8 * fl * flk(lt), par=1.3)], (540, 1000, 1.3 + 0.5 * EASE["sine"](p))
    S.append(mk(t16a, t16b, s16))
    # s17 — "She isn't there for you": the walker's face lit by a phone, breath fog, eyes widen
    WP = Painter((-60, 300, 1140, 1980), res=1.2)
    WP.chord((40, 1300, 1040, 2300), 180, 360, HOOD); WP.rect((40, 1800, 1040, 1980), HOOD); WP.ell((180, 420, 900, 1420), HOOD_D)
    WP.ell((330, 600, 750, 1240), SKIN); WP.pie((330, 600, 750, 1240), -90, 90, SKIN_D); WP.chord((320, 560, 760, 820), 180, 360, (24, 20, 18))
    WP.arc((400, 800, 500, 840), 200, 340, (50, 36, 28), 9); WP.arc((580, 800, 680, 840), 200, 340, (50, 36, 28), 9)
    WP.line([(546, 900), (530, 1000)], SKIN_D, 5); WP.ell((508, 1080, 572, 1120), (70, 34, 28)); wface = WP.sprite()
    WE = Painter((400, 850, 700, 920), res=2)
    for ex in (456, 624): WE.ell((ex - 38, 865, ex + 38, 905), (208, 206, 204)); WE.circ(ex + 6, 885, 13, (30, 24, 18)); WE.circ(ex + 2, 880, 3, (255, 255, 255))
    weyes = WE.sprite()
    PB = Painter((-60, -60, 1140, 1980), res=1.0); PB.gfill((4, 4, 10), (10, 12, 24)); PB.glow(540, 1600, 700, (120, 150, 200), 0.7, 1.4); pbg = PB.sprite()
    t17a, t17b = T("she", 2), T("they", 2)
    def s17(t):
        lt = t - t17a; sh = 2 * math.sin(lt * 31)
        return [Item(pbg), Item(wface, pos=(sh, 0)), Item(weyes, pos=(sh, 0), scale=1 + 0.08 * min(1, lt / 1.2), anchor=(540, 885))], (540, 960, 1.0 + 0.08 * lt)
    S.append(mk(t17a, t17b, s17))
    # s18 — "They say if you see her at the crossroads": walker POV, her figure small at the crossroads; streetlight flickers
    SL = glow_sprite(980, 900, 260, (200, 210, 240), power=1.6)
    t18a, t18b = T("they", 2), T("someone")
    def s18(t):
        lt = t - t18a; on = 0 if (lt * 7) % 5 < 0.6 else 1
        return [Item(cross), Item(mg, add=True, opacity=ga), Item(md), Item(MB[int(lt * 4) % 6], pos=(0, -30), scale=0.42, anchor=(540, 1230)), Item(SL, add=True, opacity=0.35 * on)], (540 + 10 * math.sin(lt * 0.9), 1150, 1.18 + 0.04 * lt)
    S.append(mk(t18a, t18b, s18))
    # s19 — "someone you love will die soon": an adobe house far away, one warm window with a family inside; the light goes out
    HS = Painter(BOX, res=1.0); night_sky(HS, 91, 1000); mesa(HS, 200, 1100, 1040, 880, (28, 30, 50)); ground(HS, 1080)
    adobe_house(HS, 250, 1300, 560, 380, dim(ADOBE, 0.8), door=DOOR_T, window=True, lit=False); bottom_fade(HS); hs = HS.sprite()
    WIN = Painter((640, 1020, 760, 1140), res=2); WIN.rect((642, 1026, 750, 1134), FARO)
    for fx, fh in ((670, 70), (700, 90), (728, 56)): WIN.ell((fx - 10, 1134 - fh, fx + 10, 1134 - fh + 22), (60, 40, 24)); WIN.rect((fx - 12, 1134 - fh + 18, fx + 12, 1134), (60, 40, 24))
    win = WIN.sprite(); wglow = glow_sprite(696, 1080, 200, FARO, power=1.5)
    t19a, t19b = T("someone"), T("she", 3)
    def s19(t):
        lt = t - t19a; off = T("die") - t19a + 0.25; o = 1 if lt < off else max(0, 1 - (lt - off) / 0.12)
        return [Item(hs), Item(win, opacity=o), Item(wglow, add=True, opacity=0.5 * o * flk(lt))], (600, 1100, 1.2 + 0.15 * lt / (t19b - t19a))
    S.append(mk(t19a, t19b, s19))
    # s20 — "She doesn't chase you": locked-off wide; nothing moves except her hair
    t20a, t20b = T("she", 3), T("she", 4)
    def s20(t):
        lt = t - t20a
        return [Item(cross), Item(mg, add=True, opacity=ga), Item(md), Item(MB[int(lt * 6) % 6], scale=0.62, anchor=(540, 1220), pos=(0, -260))], (540, 1060, 1.0)
    S.append(mk(t20a, t20b, s20))
    # s21 — "She doesn't make a sound": the walker hurries past close behind her, her shawl edge in the foreground
    REBF = Painter((-300, 300, 700, 2040), res=0.8); mala_back(REBF, 200, 2400, 2600, hands=False); rebf = REBF.sprite()
    t21a, t21b = T("she", 4), T("she", 5)
    def s21(t):
        lt = t - t21a
        return [Item(lane), Item(wk, pos=(-200 + 260 * lt, 0)), Item(rebf, pos=(-100, 0), par=1.4)], (600 + 120 * lt, 1200, 1.0)
    S.append(mk(t21a, t21b, s21))
    # s22 — "She just watches you walk home": street lined with farolitos; far behind, her small figure turned toward us
    ST2 = Painter((-500, -120, 1700, 2040), res=1.0); night_sky(ST2, 22, 900); mesa(ST2, 600, 1500, 1000, 860, (30, 32, 52))
    for (hx, w_, h_) in ((-420, 380, 300), (20, 420, 340), (520, 360, 280), (960, 420, 320), (1420, 300, 260)): adobe_house(ST2, hx, 1200, w_, h_, dim(ADOBE, 0.8), door=DOOR_B if hx % 2 else DOOR_T)
    ground(ST2, 1200); bottom_fade(ST2); st2 = ST2.sprite()
    t22a, t22b = T("she", 5), T("see", 2)
    def s22(t):
        lt = t - t22a; its = [Item(st2)]
        for i in range(14): x = -440 + i * 150; its += [Item(FON, pos=(x, 1210)), Item(fglow, pos=(x, 1170), add=True, opacity=0.35 * flk(lt, i))]
        its += [Item(MB[int(lt * 5) % 6], scale=0.22, anchor=(1150, 1200), pos=(610, -280)), Item(wk, pos=(-40 + 80 * lt, 40), scale=0.75, anchor=(540, 1800))]
        return its, (500 + 140 * lt, 1180, 1.05)
    S.append(mk(t22a, t22b, s22))
    # s23 — "to see which door you open": three adobe doors with ristras; the walker's hand lifts one latch
    DR = Painter((-500, -120, 1700, 2040), res=1.0); DR.gfill(dim(ADOBE, 0.75), dim(ADOBE, 0.55))
    for i, (dx, dc) in enumerate(((-300, DOOR_B), (300, DOOR_T), (900, (80, 56, 40)))):
        DR.rrect((dx, 600, dx + 360, 1600), 60, dc); DR.line([(dx + 180, 620), (dx + 180, 1600)], dim(dc, 0.7), 6)
        DR.circ(dx + 300, 1120, 16, (40, 40, 44)); DR.line([(dx - 60, 560), (dx - 60, 900)], (60, 40, 20), 4)
        for k_ in range(18): DR.ell((dx - 76 + (k_ % 2) * 10, 560 + k_ * 18, dx - 44 + (k_ % 2) * 10, 590 + k_ * 18), RISTRA if k_ % 3 else RISTRA_D)
    DR.rect((-500, 1600, 1700, 2040), dim(DIRT, 0.8)); bottom_fade(DR); drs = DR.sprite()
    HN = Painter((0, -60, 380, 60), res=1.2); HN.rrect((0, -40, 260, 40), 20, HOOD); HN.ell((240, -34, 340, 34), SKIN); hand = HN.sprite()
    t23a, t23b = T("see", 2), T("so")
    def s23(t):
        lt = t - t23a; reach = ease_io(min(1, lt / 1.2))
        return [Item(drs), Item(hand, pos=(1300 - 500 * reach, 1120), par=1.2)], (300 + 260 * lt, 1100, 1.0)
    S.append(mk(t23a, t23b, s23))
    # s24 — "So if you're ever on a dark New Mexico road tonight": empty two-lane highway, a Zia route marker, tail lights vanish
    HW = Painter(BOX, res=1.0); night_sky(HW, 41, 1060); mesa(HW, 500, 1200, 1060, 900, (28, 30, 50)); ground(HW, 1060)
    HW.poly([(500, 1060), (580, 1060), (1100, 2040), (-20, 2040)], (24, 24, 32))
    for i in range(10): y0 = 1080 + i ** 1.6 * 24; HW.poly([(536, y0), (544, y0), (546 + i * 3, y0 + 10 + i * 6), (534 - i * 3, y0 + 10 + i * 6)], (150, 130, 60))
    zia_sign(HW, 900, 1500, 1.6); yucca(HW, 120, 1400, 1.1); cholla(HW, -40, 1700, 1.4); bottom_fade(HW); hw = HW.sprite()
    TL = glow_sprite(0, 0, 14, (220, 30, 24), power=1.4, res=2)
    t24a, t24b = T("so"), T("dont", 2)
    def s24(t):
        lt = t - t24a; q = min(1, lt / 2.5); its = [Item(hw), Item(mg, add=True, opacity=ga * 0.7), Item(md, pos=(-300, -60))]
        if q < 1:
            for dx in (-10, 10): its.append(Item(TL, pos=(540 + dx * (1 - q), 1300 - 230 * q), add=True, opacity=1 - q, scale=1 - 0.8 * q))
        return its, (700 - 70 * lt, 1180, 1.08)
    S.append(mk(t24a, t24b, s24))
    # s25 — "don't cross alone": two friends walk together with one flashlight; in-world red line (caption carries the words)
    FR2 = Painter((200, 900, 900, 1820), res=1.3); walker_back(FR2, 430, 1800, 820); walker_back(FR2, 660, 1800, 780, col=(70, 60, 74)); fr2 = FR2.sprite()
    BM = beam_sprite(560, 1200, 560, 600, 60, 420, (220, 230, 255), 0.35, 0.0, res=0.4, blur=30)
    t25a, t25b = T("dont", 2), T("because", 2)
    def s25(t):
        lt = t - t25a
        return [Item(cross2), Item(fr2, pos=(0, -100 * lt)), Item(BM, add=True, opacity=0.6, rot=8 * math.sin(lt * 2), anchor=(560, 1200))], (540 + 60 * lt, 1180, 1.0)
    S.append(mk(t25a, t25b, s25))
    # s26 — "Because that wool isn't lying in the road by accident": back to the opening crossroads (loop seam), same dolly
    t26a, t26b = T("because", 2), T("road", 2)
    def s26(t):
        lt = t - t26a
        return [Item(cross), Item(mg, add=True, opacity=ga), Item(md), wool_item(lt, amt=0.09)] + dusts(lt), (640 - 60 * lt, 1120, 1.12 + 0.1 * lt)
    S.append(mk(t26a, t26b, s26))
    # s27 — "by accident": close, strands of the wool crawl toward the lens like fingers of hair
    STR = Painter((-500, -200, 500, 200), res=1.0); r27 = random.Random(27)
    for i in range(26): y0 = r27.uniform(-160, 160); STR.line([(-480, y0), (-200, y0 + r27.uniform(-40, 40)), (100 + r27.uniform(0, 300), y0 + r27.uniform(-60, 60))], MHAIR, r27.uniform(6, 12))
    strands = STR.sprite()
    t27a, t27b = T("road", 2), T("its", 1)
    def s27(t):
        lt = t - t27a; reach = ease_io(min(1, lt / 1.4))
        return [Item(cross, opacity=0.6), wool_item(lt, s=1.1, amt=0.1), Item(strands, pos=(540 - 300 + 400 * reach, 1230), scale=0.6 + 0.6 * reach, anchor=(540, 1230))], (540, 1180, 3.0 + 0.4 * lt)
    S.append(mk(t27a, t27b, s27))
    # s28 — REVEAL by a slow head turn: back of the head -> 3/4 -> full face with teeth; push in
    hb = head_back_sprite(); p34 = mala_portrait("dark", 0.45); g34 = mala_glints(0.45); prv = mala_portrait("reveal", 1.0); grv = mala_glints(1.0)
    PB2 = Painter((-60, -60, 1140, 1980), res=1.0); PB2.gfill((2, 2, 8), (8, 10, 22)); PB2.glow(540, 900, 700, (60, 70, 120), 0.8, 1.4); pbg2 = PB2.sprite()
    t28a = T("its", 1)
    def s28(t):
        lt = t - t28a; a = min(1, max(0, (lt - 0.7) / 0.25)); b = min(1, max(0, (lt - 1.45) / 0.2))
        its = [Item(pbg2), Item(hb, opacity=1 - a)]
        if a > 0: its += [Item(p34, opacity=a * (1 - b), pos=(40 * (1 - a), 0)), Item(g34, opacity=a * (1 - b), pos=(40 * (1 - a), 0))]
        if b > 0: its += [Item(prv, opacity=b), Item(grv, opacity=b if abs(lt - 2.4) > 0.05 else 0)]
        return its, (540, 1000, 1.0 + 0.22 * EASE["sine"](min(1, lt / 2.6)))
    S.append(mk(t28a, END, s28))
    return S

# ================= captions =================
CHUNKS = ["In New Mexico,", "if you walk home", "alone at night,", "and black wool", "is lying", "at the crossroads,", "#don't cross it,", "because that", "isn't wool,",
          "and it only waits", "for people", "who are alone.", "They call her", "La Mala Hora,", "the Evil Hour.", "In 1910,", "a folklorist", "recording",
          "Spanish folklore", "in New Mexico", "wrote about her.", "He described", "a spirit", "that haunts", "dark crossroads,", "terrorizing", "people", "who walk alone",
          "at night.", "Most of the time,", "it looks like", "a lock of wool,", "sometimes", "a whole", "sheep's fleece.", "According to", "the legend,", "she can also",
          "become", "a woman in black.", "But here's the", "terrifying part.", "She isn't", "there for you.", "They say", "if you see her", "at the crossroads,",
          "someone you love", "will die soon.", "She doesn't", "chase you.", "She doesn't", "make a sound.", "She just watches", "you walk home,", "to see",
          "which door", "you open.", "So, if you're ever", "on a dark", "New Mexico road", "tonight,", "don't cross alone,", "because that wool", "isn't lying",
          "in the road", "by accident.", "It's waiting", "to see", "who you'll lose."]
RED = {"MEXICO,", "ALONE", "WOOL", "CROSSROADS,", "ALONE.", "MALA", "HORA,", "EVIL", "HOUR.", "1910,", "SPIRIT", "HAUNTS", "TERRORIZING", "WOOL,", "FLEECE.",
       "LEGEND,", "BLACK.", "TERRIFYING", "DIE", "SOON.", "SOUND.", "DOOR", "TONIGHT,", "ALONE,", "LOSE."}
def build_chunks():
    out = []; k = 0
    for c in CHUNKS:
        hidden = c.startswith("#"); ws = []
        for tok in c.lstrip("#").split():
            m = words[k]; k += 1
            assert norm(m["w"]) == norm(tok), (m["w"], tok)
            ws.append(dict(txt=tok.upper(), s=m["s"], e=m["e"], red=tok.upper() in RED))
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
    WP_ = 0.27; yy = np.arange(H)[:, None].astype(np.float32)
    def frame(n):
        t = n / FPS; i = shot_at(t); img = rend(i, t)
        if SH[i]["wipe"] and i > 0 and t - SH[i]["t0"] < WP_:                              # black rebozo wipe left -> right, ragged fringe edge
            a = (t - SH[i]["t0"]) / WP_; a = a * a * (3 - 2 * a)
            prev = rend(i - 1, t); edge = -300 + (W + 600) * a + 40 * np.sin(yy / 37.0) + 18 * np.sin(yy / 11.0)
            xx = np.arange(W)[None, :].astype(np.float32); band = 260.0
            new_m = np.clip((edge - band / 2 - xx) / 30 + 0.5, 0, 1)[..., None]; old_m = np.clip((xx - edge - band / 2) / 30 + 0.5, 0, 1)[..., None]
            shawl = 1 - new_m - old_m
            img = img * new_m + prev * old_m + np.array(REB, np.float32) * np.clip(shawl, 0, 1)
        sname = SH[i]["fn"].__name__
        if sname != "s3":
            img = vignette(img, 0.62)
            lum = img.mean(axis=2, keepdims=True); img = img * 0.7 + lum * 0.3                   # EP06 grade: near-monochrome indigo / moon-silver
            img = img * np.array([0.90, 0.95, 1.10], np.float32) + np.array([0, 2, 8], np.float32)
        img = grain(img, 0, 2.0)
        act = None
        for c in chunks:
            if c["words"][0]["s"] <= t + 0.03: act = c
        if act and not act["hidden"] and sname not in ("s3", "s0j") and t < VOICE_END + 0.3:
            img = cap.apply(img, act["words"], sum(1 for w in act["words"] if w["s"] <= t + 0.03))
        return np.clip(img, 0, 255).astype(np.uint8)
    if len(sys.argv) > 2:
        ts = [float(x) for x in sys.argv[2].split(",")]; ims = [Image.fromarray(frame(int(t * FPS))).resize((270, 480), Image.LANCZOS) for t in ts]
        cols = min(8, len(ims)); sheet = Image.new("RGB", (270 * cols, 480 * ((len(ims) + cols - 1) // cols)))
        for k, im in enumerate(ims): sheet.paste(im, ((k % cols) * 270, (k // cols) * 480))
        out = os.path.join(EP, sys.argv[3] if len(sys.argv) > 3 else "stills.jpg"); sheet.save(out, quality=90); print("stills", out); return
    out = os.path.join(EP, "ep06_noaudio.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    nf = int(math.ceil(END * FPS))
    for n in range(nf):
        pr.stdin.write(frame(n).tobytes())
        if n % 150 == 0: print("frame", n, "/", nf, flush=True)
    pr.stdin.close(); pr.wait(); print("wrote", out, "%.2f s" % (nf / FPS))

if __name__ == "__main__":
    main()
