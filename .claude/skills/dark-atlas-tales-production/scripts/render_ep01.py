"""render_ep01.py — EP01 "Kuchisake-onna" (Japan) in the Dark Atlas Tales style, Milo narration.
Usage: python -I render_ep01.py <dark_atlas_dir> [stills "t1,t2,..."]
Original script (EP01_kuchisake/script.txt). Visual language = approved V03 fidelity test v5 (style.py + engine.py).
"""
import sys, os, json, math, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from style import *

ROOT = sys.argv[1]; EP = os.path.join(ROOT, "EP01_kuchisake")
FB = os.path.join(ROOT, "fonts", "Oswald-Bold.ttf"); FR = os.path.join(ROOT, "fonts", "Oswald-Regular.ttf")
words = [w for s in json.load(open(os.path.join(EP, "voice_milo_transcript.json"), encoding="utf-8")) for w in s["words"]]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
def T(word, n=1, end=False):
    k = 0
    for w in words:
        if norm(w["w"]) == norm(word):
            k += 1
            if k == n: return w["e"] if end else w["s"]
    raise KeyError(word)
VOICE_END = words[-1]["e"]; END = VOICE_END + 0.75

# ---------------- palette ----------------
STY = json.load(open(os.path.join(EP, "style.json"), encoding="utf-8"))
tup = lambda k: tuple(STY[k])
COAT_T, COAT_B, COAT_D, COAT_L = tup("woman_coat_top"), tup("woman_coat_bot"), tup("woman_coat_dark"), tup("woman_coat_light")
COAT_M = tuple((a + b) // 2 for a, b in zip(COAT_T, COAT_D))
UNI, UNI_T = tup("victim_uniform"), tup("victim_trim")
LANTERN, VEND = tup("accent_lantern"), tup("vending_light")
JPF = STY["jp_font"]
SKIN = (214, 192, 164); SKIN_D = (192, 168, 140); MASK = (236, 236, 232); MASK_D = (206, 206, 202)
NIGHT_T, NIGHT_B = (7, 10, 17), (24, 34, 48)
WARM_WIN = (214, 160, 86)

# ================= scenery =================
def house_row(P, y_base, x0, x1, hmin, hmax, col, seed, win=0.3):
    r = random.Random(seed); x = x0
    while x < x1:
        bw = r.uniform(110, 190); hh = r.uniform(hmin, hmax); top = y_base - hh
        P.rect((x, top, x + bw, y_base + 2), col)
        rc = tuple(max(0, c - 6) for c in col)
        P.poly([(x - 26, top - 2), (x - 16, top + 6), (x + bw + 16, top + 6), (x + bw + 26, top - 2), (x + bw * 0.80, top - hh * 0.34), (x + bw * 0.20, top - hh * 0.34)], rc)   # kawara roof, upturned eaves
        P.line([(x + bw * 0.20, top - hh * 0.34), (x + bw * 0.80, top - hh * 0.34)], tuple(min(255, c + 14) for c in rc), 3)
        if r.random() < win: P.rect((x + bw * 0.35, top + hh * 0.3, x + bw * 0.35 + bw * 0.18, top + hh * 0.3 + hh * 0.28), WARM_WIN)
        x += bw + r.uniform(4, 24)

def jp_text(P, txt, x, y, size, col, squash=1.0, anchor="mm"):
    """draw Japanese text at world (x,y) into the painter (optionally squashed vertically, e.g. road paint)."""
    f = ImageFont.truetype(JPF, max(8, int(size * P.k)))
    tw = int(f.getlength(txt)) + 8; th = int(size * P.k * 1.4)
    lay = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); ImageDraw.Draw(lay).text((tw / 2, th / 2), txt, font=f, fill=tuple(int(v) for v in col) + ((255,) if len(col) == 3 else ()), anchor="mm")
    if squash != 1.0: lay = lay.resize((tw, max(1, int(th * squash))), Image.LANCZOS)
    px, py = P.P(x, y); P.img.alpha_composite(lay, (int(px - lay.size[0] / 2), int(py - lay.size[1] / 2))); P.d = ImageDraw.Draw(P.img)

def stop_sign(P, x, base, size):
    """Japanese 止まれ sign: red inverted triangle on a grey pole."""
    P.rect((x - size * 0.035, base - size * 2.6, x + size * 0.035, base), (120, 124, 130))
    top = base - size * 2.6
    P.poly([(x - size * 0.62, top - size * 0.45), (x + size * 0.62, top - size * 0.45), (x, top + size * 0.62)], (236, 236, 236))
    P.poly([(x - size * 0.52, top - size * 0.39), (x + size * 0.52, top - size * 0.39), (x, top + size * 0.50)], (188, 30, 34))
    jp_text(P, "止まれ", x, top - size * 0.12, size * 0.26, (250, 250, 250))

def vending_machine(P, x0, base, w, h, seed=0):
    r = random.Random(seed)
    P.rrect((x0, base - h, x0 + w, base), w * 0.04, (196, 206, 220))
    P.rect((x0 + w * 0.07, base - h * 0.93, x0 + w * 0.93, base - h * 0.47), (226, 236, 246))
    for row in range(3):
        for c in range(6):
            cx = x0 + w * (0.12 + c * 0.14); cy = base - h * (0.86 - row * 0.14)
            P.rrect((cx - w * 0.04, cy - h * 0.045, cx + w * 0.04, cy + h * 0.045), 2, r.choice([(196, 40, 40), (40, 90, 180), (40, 150, 80), (230, 150, 40), (240, 240, 240), (120, 70, 40)]))
    P.rect((x0 + w * 0.12, base - h * 0.40, x0 + w * 0.88, base - h * 0.36), (60, 64, 74))
    P.rect((x0 + w * 0.30, base - h * 0.16, x0 + w * 0.70, base - h * 0.06), (40, 44, 52))

def curve_mirror(P, x, base, h):
    P.rect((x - h * 0.02, base - h, x + h * 0.02, base), (226, 116, 40))
    P.circ(x, base - h, h * 0.16, (226, 116, 40)); P.circ(x, base - h, h * 0.13, (54, 66, 88)); P.arc((x - h * 0.10, base - h * 1.10, x + h * 0.06, base - h * 0.94), 200, 260, (160, 180, 210), 3)

def chochin(P, x, y, r):
    P.line([(x, y - r * 2.2), (x, y - r * 1.2)], (20, 20, 24), 2)
    P.rect((x - r * 0.55, y - r * 1.25, x + r * 0.55, y - r * 1.05), (20, 18, 18)); P.rect((x - r * 0.55, y + r * 1.05, x + r * 0.55, y + r * 1.25), (20, 18, 18))
    P.ell((x - r, y - r * 1.15, x + r, y + r * 1.15), LANTERN)
    for k in (-0.6, -0.2, 0.2, 0.6): P.line([(x - r * math.sqrt(max(0, 1 - k * k)) * 0.98, y + k * r * 1.15), (x + r * math.sqrt(max(0, 1 - k * k)) * 0.98, y + k * r * 1.15)], tuple(max(0, c - 50) for c in LANTERN), 2)

def utility_pole(P, x, top, bottom, w, col=(12, 13, 18)):
    P.rect((x - w / 2, top, x + w / 2, bottom), col)
    for k, yy in enumerate((top + w * 2.2, top + w * 4.4)):
        P.rect((x - w * 3.2 + k * w * 0.6, yy, x + w * 3.2 - k * w * 0.6, yy + w * 0.5), col)
    P.rect((x + w * 0.5, top + w * 6, x + w * 2.4, top + w * 8.2), col)                                    # transformer box

def catenary(P, a, b, sag, col=(12, 13, 18), w=2.5):
    pts = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t + sag * math.sin(math.pi * t)) for t in np.linspace(0, 1, 30)]
    P.line(pts, col, w)

def jp_street(lamp=True, corner=False, seed=1):
    """perspective residential street at night (vanishing point VX,HY), poles+wires, block walls, houses, street lamp."""
    VX, HY = 560, 1010
    P = Painter((-160, -120, 1240, 2040), res=1.1)
    P.gfill(NIGHT_T, NIGHT_B); stars(P, (-160, -120, 1240, 900), 150, 70 + seed)
    house_row(P, HY, -160, 1240, 50, 120, (20, 24, 33), 3 + seed, 0.35)
    haze(P, HY, 90, (30, 38, 52), 120)
    road = [(VX - 46, HY), (VX + 46, HY), (1220, 2040), (-140, 2040)]
    P.gpoly(road, (40, 42, 48), (60, 62, 66))
    P.line([(VX - 38, HY), (-60, 2040)], (120, 120, 116), 4); P.line([(VX + 38, HY), (1140, 2040)], (120, 120, 116), 4)   # side lines
    # block walls + houses on both sides (perspective)
    for side in (-1, 1):
        xin = VX + side * 52; xout = -160 if side < 0 else 1240
        wall = [(xin, HY - 12), (xin, HY + 4), (xout, 1640), (xout, 1060)]
        P.gpoly(wall, (34, 38, 48), (26, 30, 38))
        for k in range(6):
            t = (k + 1) / 7; xx = xin + (xout - xin) * t ** 1.6
            P.line([(xx, HY - 12 + (1060 - HY + 12) * t ** 1.6), (xx, HY + 4 + (1640 - HY - 4) * t ** 1.6)], (22, 25, 33), 2)
        hb = [(xin, HY - 30), (xin, HY - 12), (xout, 1060), (xout, 560)]
        P.poly(hb, (16, 19, 27))
        for k, t in enumerate((0.15, 0.4, 0.7)):
            xx = xin + (xout - xin) * t ** 1.6; yy = HY - 30 + (560 - HY + 30) * t ** 1.6; sz = 14 + 70 * t ** 1.6
            if (k + seed) % 2 == 0: P.rect((xx - sz * 0.4 * side, yy + sz * 0.6, xx + sz * 0.1 * side, yy + sz * 1.3), WARM_WIN)
    # poles (perspective) + wires
    polesL = [(80, 260, 1900, 26), (330, 700, 1180, 11), (450, 880, 1060, 6)]
    polesR = [(1000, 240, 1900, 26), (790, 690, 1180, 11), (670, 875, 1060, 6)]
    for (x, tp, bt, w) in polesL + polesR: utility_pole(P, x, tp, bt, w)
    for poles in (polesL, polesR):
        for (a, b) in zip(poles[:-1], poles[1:]):
            for dy in (0, 1):
                catenary(P, (a[0], a[1] + a[3] * (2.2 + 2.2 * dy)), (b[0], b[1] + b[3] * (2.2 + 2.2 * dy)), 26 - dy * 8)
    for dy in (0, 1): catenary(P, (80, 260 + 26 * (2.2 + 2.2 * dy)), (1000, 240 + 26 * (2.2 + 2.2 * dy)), 120)
    if corner:   # foreground block-wall corner on the right (she steps out from behind it)
        P.poly([(760, 900), (1240, 820), (1240, 2040), (760, 2040)], (30, 34, 44))
        P.poly([(760, 900), (800, 900), (800, 2040), (760, 2040)], (44, 50, 62))
        for yy in range(960, 2000, 90): P.line([(800, yy), (1240, yy - 50)], (24, 28, 36), 2)
    # Japanese street furniture
    jp_text(P, "止まれ", VX - 10, 1760, 150, (210, 210, 206, 170), squash=0.38)                               # road paint
    curve_mirror(P, 360, 1150, 300)
    stop_sign(P, 210, 1650, 150)
    if not corner: vending_machine(P, 880, 1560, 150, 330, seed); vending_machine(P, 1036, 1600, 150, 340, seed + 1)
    chochin(P, 150, 1050, 34); chochin(P, 455, 1030, 14)
    P.gpoly([(-160, 1840), (1240, 1840), (1240, 2040), (-160, 2040)], (10, 10, 14, 0), (4, 4, 6, 255))
    bg = P.sprite()
    vglow = glow_sprite(990, 1400, 300, VEND, power=1.6); cglow = glow_sprite(150, 1050, 120, LANTERN, power=1.5); cglow2 = glow_sprite(455, 1030, 50, LANTERN, power=1.5)
    lamp_xy = (790 - 34, 700 + 30)
    lampcone = beam_sprite(lamp_xy[0], lamp_xy[1], lamp_xy[0] - 60, 1260, 20, 360, (255, 230, 180), 0.45, 0.10, res=0.5, blur=30)
    lampglow = glow_sprite(lamp_xy[0], lamp_xy[1], 90, (255, 236, 190), power=1.5)
    L = Painter((lamp_xy[0] - 30, lamp_xy[1] - 30, lamp_xy[0] + 40, lamp_xy[1] + 14), res=2)
    L.line([(lamp_xy[0] + 36, lamp_xy[1] - 24), (lamp_xy[0] + 10, lamp_xy[1] - 6)], (14, 14, 18), 4)
    L.rrect((lamp_xy[0] - 22, lamp_xy[1] - 8, lamp_xy[0] + 14, lamp_xy[1] + 2), 3, (20, 20, 24)); L.rect((lamp_xy[0] - 18, lamp_xy[1] + 1, lamp_xy[0] + 10, lamp_xy[1] + 5), (255, 240, 200))
    md, mg, ga = moon(860, 330, 80, res=1.4)
    return dict(bg=bg, cone=lampcone, lglow=lampglow, lamp=L.sprite(), md=md, mg=mg, ga=ga, VX=VX, HY=HY,
                vglow=None if corner else vglow, cglow=cglow, cglow2=cglow2)

def street_items(A, lt, lamp_on=1.0):
    its = [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"]),
           Item(A["cone"], add=True, opacity=lamp_on), Item(A["lglow"], add=True, opacity=lamp_on), Item(A["lamp"]),
           Item(A["cglow"], add=True, opacity=0.55 + 0.05 * math.sin(lt * 3)), Item(A["cglow2"], add=True, opacity=0.5)]
    if A["vglow"] is not None: its.append(Item(A["vglow"], add=True, opacity=0.32))
    return its

def flick(lt, seed=0.0):
    v = 1.0
    for a, b in [(1.3, 1.42), (1.5, 1.55), (3.1, 3.2), (4.4, 4.46)]:
        if a + seed < lt < b + seed: v = 0.25
    return v

# ================= characters =================
def woman_coat_side(P, x, feet, h, scissors=False, hand_up=False):
    """side view facing right: long beige coat with belt, long black hair down the back, white mask, dark stockings."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-150), Y(12), X(150), Y(-14)), (0, 0, 0, 90))
    P.poly([(X(-108), Y(960)), (X(-38), Y(985)), (X(-46), Y(700)), (X(-62), Y(540)), (X(-100), Y(500)), (X(-136), Y(530)), (X(-130), Y(720))], HAIR)
    for lx in (-44, 6):                                                                                     # legs + shoes
        P.rect((X(lx), Y(200), X(lx + 34), Y(28)), (32, 30, 34))
        P.rrect((X(lx - 4), Y(34), X(lx + 64), Y(0)), 10 * k, (12, 12, 14))
    coat = [(X(-74), Y(830)), (X(64), Y(830)), (X(80), Y(780)), (X(104), Y(400)), (X(130), Y(190)), (X(-136), Y(184)), (X(-110), Y(400)), (X(-90), Y(780))]
    P.gpoly(coat, COAT_T, COAT_B, Y(830), Y(184))
    P.gpoly([(X(-74), Y(830)), (X(-46), Y(830)), (X(-74), Y(400)), (X(-96), Y(186)), (X(-136), Y(184)), (X(-110), Y(400)), (X(-90), Y(780))], COAT_M, COAT_D, Y(830), Y(184))
    P.rect((X(-112), Y(540), X(100), Y(508)), COAT_D); P.rrect((X(40), Y(548), X(72), Y(500)), 4 * k, (60, 50, 40))   # belt + buckle
    P.line([(X(56), Y(820)), (X(70), Y(560)), (X(98), Y(200))], COAT_D, 3 * k)                              # front edge
    P.poly([(X(30), Y(830)), (X(70), Y(830)), (X(52), Y(720))], COAT_L)                                     # lapel
    # arm
    if hand_up:
        P.poly([(X(0), Y(810)), (X(54), Y(800)), (X(96), Y(880)), (X(70), Y(900))], COAT_M)
    else:
        P.poly([(X(-6), Y(812)), (X(52), Y(800)), (X(76), Y(500)), (X(30), Y(490))], COAT_M)
        P.ell((X(28), Y(500), X(80), Y(440)), SKIN)
    if scissors and not hand_up:
        for ang, c in ((-6, (176, 180, 188)), (6, (150, 154, 162))):
            a = math.radians(ang); bx, by = X(54), Y(470); L_ = 250 * k
            P.poly([(bx - 8 * k, by), (bx + 8 * k, by), (bx + L_ * math.sin(a) + 2, by + L_ * math.cos(a)), (bx + L_ * math.sin(a) - 2, by + L_ * math.cos(a))], c)
        P.ell((X(30), Y(500), X(62), Y(456)), (44, 40, 46)); P.ell((X(56), Y(500), X(88), Y(456)), (44, 40, 46))
    # head (profile facing right)
    P.ell((X(-94), Y(1000), X(40), Y(818)), HAIR)
    P.poly([(X(8), Y(962)), (X(56), Y(958)), (X(66), Y(930)), (X(70), Y(912)), (X(86), Y(896)), (X(74), Y(880)), (X(70), Y(840)), (X(30), Y(824)), (X(6), Y(860))], SKIN)
    P.poly([(X(20), Y(904)), (X(78), Y(900)), (X(88), Y(868)), (X(76), Y(836)), (X(26), Y(828))], MASK)    # mask
    for yy in (888, 870, 852): P.line([(X(26), Y(yy)), (X(80), Y(yy - 2))], MASK_D, 2 * k)
    P.line([(X(28), Y(898)), (X(-12), Y(890))], (226, 226, 222), 2.4 * k)
    P.ell((X(40), Y(936), X(62), Y(922)), (232, 224, 210)); P.ell((X(48), Y(934), X(60), Y(924)), (26, 18, 14)); P.line([(X(38), Y(938)), (X(64), Y(936))], (16, 10, 8), 3 * k)
    P.poly([(X(-20), Y(1000)), (X(52), Y(990)), (X(66), Y(950)), (X(10), Y(948))], HAIR)                    # fringe

def woman_coat_front(P, x, feet, h, sil=False, wind=0.0, scissors=False):
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    hair = (6, 6, 8) if sil else HAIR
    ct, cb = ((8, 8, 11), (8, 8, 11)) if sil else (COAT_T, COAT_B)
    if not sil: P.ell((X(-220), Y(12), X(220), Y(-14)), (0, 0, 0, 100))
    P.poly([(X(60), Y(930)), (X(160), Y(915 + wind * 0.3)), (X(260), Y(870 + wind * 0.6)), (X(350), Y(810 + wind)), (X(240), Y(835 + wind * 0.6)), (X(140), Y(860 + wind * 0.3)), (X(50), Y(870))], hair)
    P.poly([(X(-118), Y(940)), (X(118), Y(940)), (X(130), Y(600)), (X(-130), Y(600))], hair)                 # long hair behind
    for lx in (-58, 22):
        P.rect((X(lx), Y(190), X(lx + 36), Y(26)), (8, 8, 11) if sil else (32, 30, 34)); P.rrect((X(lx - 4), Y(34), X(lx + 42), Y(0)), 8 * k, (6, 6, 8) if sil else (12, 12, 14))
    P.rrect((X(-126), Y(820), X(126), Y(560)), 46 * k, ct)
    P.gpoly([(X(-126), Y(600)), (X(126), Y(600)), (X(170), Y(180)), (X(-170), Y(180))], ct, cb, Y(600), Y(180))
    if not sil:
        P.rect((X(-140), Y(530), X(140), Y(502)), COAT_D); P.line([(X(0), Y(800)), (X(0), Y(190))], COAT_D, 3 * k)
        P.poly([(X(-50), Y(820)), (X(50), Y(820)), (X(0), Y(700))], COAT_L)
        for sx in (-1, 1): P.line([(X(sx * 92), Y(780)), (X(sx * 104), Y(480))], COAT_D, 4 * k)
    P.ell((X(-118), Y(1000), X(108), Y(800)), hair)
    if not sil:
        P.ell((X(-46), Y(960), X(42), Y(840)), SKIN)
        P.rrect((X(-46), Y(906), X(42), Y(842)), 18 * k, MASK)
        P.chord((X(-60), Y(995), X(54), Y(905)), 180, 360, hair)
        for ex in (-22, 18): P.ell((X(ex - 9), Y(926), X(ex + 9), Y(916)), (24, 16, 12))
    if scissors:
        c = (6, 6, 8) if sil else (170, 174, 182)
        P.poly([(X(118), Y(500)), (X(134), Y(500)), (X(150), Y(300)), (X(146), Y(298))], c); P.poly([(X(126), Y(500)), (X(142), Y(500)), (X(132), Y(298)), (X(128), Y(300))], c)
        P.circ(X(122), Y(512), 14 * k, c); P.circ(X(140), Y(512), 14 * k, c)

def young_man_back(P, x, feet, h, step=0):
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-150), Y(12), X(150), Y(-14)), (0, 0, 0, 90))
    off = 30 if step else -30
    P.rect((X(-70), Y(460), X(-14), Y(10 + max(0, off))), UNI); P.rect((X(14), Y(460), X(70), Y(10 + max(0, -off))), UNI)
    P.rrect((X(-130), Y(840), X(130), Y(420)), 60 * k, UNI)                             # gakuran
    P.rect((X(-60), Y(860), X(60), Y(820)), UNI)                                        # standing collar
    P.rrect((X(60), Y(640), X(150), Y(420)), 10 * k, (96, 62, 36)); P.line([(X(100), Y(840)), (X(120), Y(640))], (70, 44, 26), 6 * k)   # school bag
    P.rect((X(-36), Y(880), X(36), Y(830)), (150, 110, 80))
    P.ell((X(-80), Y(1000), X(80), Y(840)), (16, 14, 14))                               # hair (back of head)

def runner(P, x, feet, h, phase):
    """side-view running young man (facing left), phase in [0,1)."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    a = math.sin(phase * 2 * math.pi)
    def limb(x0, y0, ang, L, w, col):
        ex, ey = x0 + math.sin(ang) * L, y0 + math.cos(ang) * L
        P.line([(X(x0), Y(y0)), (X(ex), Y(ey))], col, w * k); return ex, ey
    for s, col in ((1, tuple(max(0, c - 8) for c in UNI)), (-1, UNI)):                     # legs
        kx, ky = limb(0, 470, math.radians(180 + 40 * a * s), 230, 54, col)
        limb(kx, ky, math.radians(180 + 40 * a * s - 50 * max(0, -a * s) - 20), 230, 46, col)
    P.poly([(X(-70), Y(840)), (X(70), Y(820)), (X(80), Y(450)), (X(-60), Y(450))], UNI)                      # torso (gakuran)
    for k_, by in enumerate((760, 680, 600)): P.circ(X(66), Y(by), 9 * k, UNI_T)                                # gold buttons
    for s, col in ((-1, tuple(max(0, c - 6) for c in UNI)), (1, tuple(min(255, c + 14) for c in UNI))):
        limb(0, 790, math.radians(-60 * a * s + 180), 200, 40, col)
    P.ell((X(-80), Y(1000), X(60), Y(850)), (150, 110, 80)); P.chord((X(-84), Y(1006), X(64), Y(890)), 180, 360, (16, 14, 14))
    P.ell((X(-70), Y(950), X(-52), Y(938)), (20, 14, 12))

# ---------- portraits ----------
def portrait_bg(warm=True):
    P = Painter((-60, -60, 1140, 1980), res=1.0)
    P.gfill((6, 7, 10), (12, 13, 17)); P.glow(540, 860, 820, (78, 64, 42) if warm else (40, 50, 70), 1.0, 1.4)
    for r in (300, 420): P.arc((860 - r, 640 - r, 860 + r, 640 + r), 200, 260, (120, 100, 70, 60) if warm else (90, 100, 120, 60), 3)
    return P.sprite()

def portrait_woman(mode="mask"):
    """V01-style front portrait. mode: mask | pulling | reveal."""
    D = Painter((140, 300, 940, 1980), res=1.2)
    D.rrect((262, 400, 818, 1460), 270, HAIR)                                                            # hair mass
    D.rect((482, 1040, 598, 1230), SKIN_D)                                                               # neck (short)
    D.ell((120, 1180, 960, 2100), COAT_D)                                                                 # coat shoulders (darker so red captions stay readable)
    D.poly([(420, 1190), (540, 1320), (660, 1190), (660, 1240), (540, 1380), (420, 1240)], COAT_B)        # collar V
    pale = mode == "reveal"
    sk, skd = ((226, 214, 202), (198, 186, 176)) if pale else (SKIN, SKIN_D)
    D.ell((362, 520, 718, 1100), sk); D.pie((362, 520, 718, 1100), 270, 450, skd) if False else D.pie((362, 520, 718, 1100), -90, 90, skd)
    D.chord((346, 440, 734, 740), 180, 360, HAIR)
    D.poly([(346, 590), (372, 600), (360, 900), (330, 960)], HAIR); D.poly([(734, 590), (708, 600), (720, 900), (750, 960)], HAIR)
    D.line([(430, 735), (502, 726)], (30, 22, 18), 8); D.line([(578, 726), (650, 735)], (30, 22, 18), 8)   # brows
    if mode == "mask":
        D.rrect((370, 820, 710, 1062), 70, MASK)
        for yy in (880, 940, 1000): D.line([(392, yy), (688, yy)], MASK_D, 4)
        D.line([(370, 870), (346, 820)], (226, 226, 222), 5); D.line([(710, 870), (734, 820)], (226, 226, 222), 5)
    elif mode == "pulling":
        D.chord((380, 830, 700, 1060), 180, 360, (60, 44, 36))                                           # shadow where the mask has lifted
        D.rrect((370, 900, 710, 1130), 70, MASK)
        for yy in (960, 1020, 1080): D.line([(392, yy), (688, yy)], MASK_D, 4)
        D.ell((640, 860, 760, 1000), sk); D.rect((660, 960, 740, 1180), sk)                              # fingers pulling the mask down
        for fx in (650, 678, 706): D.line([(fx, 880), (fx + 6, 940)], skd, 3)
    else:  # reveal: the slit smile (stylised, no blood)
        D.rrect((410, 1070, 670, 1150), 34, MASK)                                                        # mask hanging under the chin
        D.line([(410, 1080), (352, 900)], (226, 226, 222), 4); D.line([(670, 1080), (728, 900)], (226, 226, 222), 4)
        top = [(380, 905), (430, 935), (480, 950), (540, 955), (600, 950), (650, 935), (700, 905)]
        bot = [(700, 905), (650, 975), (600, 1000), (540, 1008), (480, 1000), (430, 975), (380, 905)]
        D.poly(top + bot, (34, 8, 10))
        for i in range(9):                                                                               # teeth
            tx = 446 + i * 24
            D.rect((tx, 942 + abs(i - 4) * 2, tx + 18, 962 + abs(i - 4)), (226, 220, 206))
            D.rect((tx, 982 - abs(i - 4) * 3, tx + 18, 996 - abs(i - 4) * 3), (214, 208, 194))
        D.line(top, (110, 22, 26), 5); D.line(bot, (110, 22, 26), 5)
        D.line([(380, 905), (352, 860)], (110, 22, 26), 5); D.line([(700, 905), (728, 860)], (110, 22, 26), 5)   # slit up to the ears
    return D.sprite()

def eyes_sprite(mode="calm", look=0.0):
    E = Painter((400, 740, 690, 820), res=2.0)
    for ex in (466, 614):
        cy = 778
        if mode == "dead":
            E.ell((ex - 46, cy - 24, ex + 46, cy + 22), (30, 24, 26)); E.ell((ex - 34, cy - 14, ex + 34, cy + 14), (232, 226, 220))
            E.circ(ex, cy, 7, (8, 4, 4))
        else:
            E.ell((ex - 44, cy - 18, ex + 44, cy + 18), (234, 226, 214)); E.circ(ex + 12 * look, cy + 1, 16, (34, 22, 16)); E.circ(ex + 12 * look, cy + 1, 7, (6, 4, 4))
            E.arc((ex - 46, cy - 24, ex + 46, cy + 20), 190, 350, (16, 10, 8), 7)
            E.line([(ex + (40 if ex > 540 else -40), cy - 6), (ex + (58 if ex > 540 else -58), cy - 16)], (16, 10, 8), 5)   # eyeliner wing
    return E.sprite()

def young_man_portrait():
    K = 1.5
    def q(x, y): return (x * K, y * K)
    def b(x0, y0, x1, y1): return (x0 * K, y0 * K, x1 * K, y1 * K)
    D = Painter((0, 400, 1080, 1960), res=1.2)
    D.chord(b(50, 790, 670, 1400), 180, 360, UNI); D.rect(b(50, 1090, 670, 1300), UNI)                # gakuran
    D.rrect(b(296, 770, 424, 835), 10, tuple(min(255, c + 8) for c in UNI)); D.rect(b(300, 826, 420, 834), (220, 220, 214))   # standing collar + white edge
    for by in (900, 980, 1060): D.circ(360 * K, by * K, 9, UNI_T)                                         # gold buttons
    D.rect(b(318, 680, 402, 805), (150, 108, 74)); D.poly([q(318, 680), q(402, 680), q(402, 720), q(318, 740)], (128, 92, 62))
    D.ell(b(222, 528, 248, 574), (172, 124, 86)); D.ell(b(474, 528, 500, 574), (152, 108, 74))
    face = [q(250, 430), q(480, 430), q(482, 520), q(474, 580), q(452, 632), q(418, 670), q(360, 692), q(302, 670), q(268, 632), q(250, 580), q(244, 520)]
    D.poly(face, (172, 124, 86)); D.poly([q(370, 430), q(480, 430), q(482, 520), q(474, 580), q(452, 632), q(418, 670), q(375, 690)], (152, 108, 74))
    D.poly([q(236, 470), q(250, 380), q(300, 340), q(400, 330), q(470, 360), q(492, 440), q(486, 520), q(470, 470), q(400, 430), q(300, 440), q(258, 520)], (16, 14, 14))   # hair
    D.arc(b(280, 488, 344, 518), 200, 340, (24, 16, 12), 7); D.arc(b(376, 488, 442, 518), 200, 340, (24, 16, 12), 7)   # raised brows
    D.line([q(372, 520), q(356, 602)], (124, 86, 56), 4); D.arc(b(348, 592, 384, 612), 10, 170, (124, 86, 56), 4)
    D.ell(b(342, 628, 380, 656), (54, 26, 22))                                                          # mouth open (fear)
    face_spr = D.sprite()
    E = Painter((410, 770, 680, 850), res=2)
    for ex in (312, 412):
        cx = ex * K; cy = 540 * K
        E.ell((cx - 42, cy - 20, cx + 42, cy + 20), (236, 228, 214)); E.circ(cx, cy, 10, (36, 22, 14)); E.circ(cx, cy, 4, (6, 4, 4))
        E.arc((cx - 44, cy - 24, cx + 44, cy + 18), 195, 345, (20, 14, 10), 6)
    return face_spr, E.sprite()

# ================= SHOT BUILDERS (each returns fn(t)->(items, cam)) =================
def mk(t0, t1, fn, dissolve=0.0): return dict(t0=t0, t1=t1, fn=fn, dz=dissolve)

def build_all():
    S = []
    street = jp_street(seed=1)
    # S0 — wide street, moon, tiny woman under the far lamp (push-in)
    Wf = Painter((520, 860, 640, 1030), res=3); woman_coat_front(Wf, 580, 1020, 130); far_w = Wf.sprite()
    fglow = glow_sprite(580, 960, 110, (200, 196, 180))
    def s0(t):
        lt = t; p = lt / 2.66
        cam = (560, 960 - 40 * p, 1.0 + 0.08 * EASE["sine"](p))
        return street_items(street, lt) + [Item(fglow, add=True, opacity=0.6), Item(far_w)], cam
    S.append(mk(0, T("stops"), s0))
    # S1 — side view of the woman under the lamp, she steps then stops
    side = Painter((-160, -120, 1240, 2040), res=1.0)
    side.gfill(NIGHT_T, NIGHT_B); stars(side, (-160, -120, 1240, 1000), 140, 81)
    house_row(side, 1420, -160, 1240, 160, 300, (20, 24, 33), 82, 0.4); haze(side, 1420, 120, (30, 38, 52), 120)
    side.rect((-160, 1420, 1240, 2040), (30, 32, 38)); side.rect((-160, 1590, 1240, 1600), (60, 62, 66))
    utility_pole(side, 900, 120, 1600, 28); catenary(side, (-160, 230), (900, 182), 60, w=3); catenary(side, (900, 182), (1240, 200), 30, w=3)
    vending_machine(side, 940, 1590, 170, 380, 9); chochin(side, 120, 1240, 30)
    side.gpoly([(-160, 1840), (1240, 1840), (1240, 2040), (-160, 2040)], (10, 10, 14, 0), (4, 4, 6, 255))
    side_bg = side.sprite(); s_vg = glow_sprite(1025, 1400, 300, VEND, power=1.6); s_cg = glow_sprite(120, 1240, 110, LANTERN, power=1.5); smd, smg, sga = moon(220, 380, 78, res=1.4)
    WS = Painter((150, 500, 760, 1640), res=1.25); woman_coat_side(WS, 420, 1600, 1000); ws = WS.sprite()
    sc = beam_sprite(862, 520, 760, 1640, 40, 700, (255, 232, 186), 0.5, 0.08, res=0.5, blur=40)
    sg = glow_sprite(862, 520, 120, (255, 236, 196), power=1.5)
    def s1(t):
        lt = t - T("stops"); p = lt / (T("asks") - T("stops") + 0.4)
        step = 60 * (1 - ease_out(min(1, lt / 0.9)))
        cam = (540, 960, 1.0 + 0.05 * p)
        return [Item(side_bg), Item(smg, add=True, opacity=sga), Item(smd), Item(s_vg, add=True, opacity=0.3), Item(s_cg, add=True, opacity=0.55), Item(sc, add=True, opacity=flick(lt, 0.5)), Item(sg, add=True, opacity=flick(lt, 0.5)),
                Item(ws, pos=(-step, 2 * abs(math.sin(lt * 6)) * (step > 1)))], cam
    S.append(mk(T("stops"), T("and", 1), s1))
    # S2 — portrait, mask, ripples "Am I pretty?"
    pbg = portrait_bg(True); pw_mask = portrait_woman("mask"); e_calm = eyes_sprite("calm", 0.3)
    R = Painter((-400, -400, 400, 400), res=1.2)
    for r in (120, 220, 330): R.arc((-r, -r, r, r), 0, 360, (220, 200, 160, 110), 2.5)
    rings = R.sprite()
    def s2(t):
        lt = t - T("and", 1); p = lt / 2.4
        cam = (540, 900, 1.02 + 0.05 * p)
        its = [Item(pbg), Item(pw_mask), Item(e_calm, opacity=0 if abs(lt - 0.5) < 0.06 else 1)]
        for k in range(3):
            ph = (lt * 0.7 + k / 3) % 1
            its.append(Item(rings, pos=(540, 940), scale=0.3 + ph, anchor=(540, 940), opacity=(1 - ph) * 0.7 * min(1, lt / 0.4)))
        return its, cam
    S.append(mk(T("and", 1), T("dont", 1), s2))
    # S3 — hook card
    f = ImageFont.truetype(FB, 160); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text(((W - d.textlength("DON'T SAY NO.", font=f)) / 2, 780), "DON'T SAY NO.", font=f, fill=(198, 38, 38, 255))
    hook = Sprite(np.asarray(lay).copy(), 1, 0, 0); g = np.asarray(lay.filter(ImageFilter.GaussianBlur(26))).copy(); hookg = Sprite(g, 1, 0, 0)
    t3a, t3b = T("dont", 1), T("because", 1) - 0.05
    def s3(t):
        lt = t - t3a; dd = t3b - t3a; op = 1.0 if lt < dd - 0.3 else max(0, (dd - lt) / 0.3); s_ = 1 + 0.035 * lt / dd
        return [Item(hookg, add=True, opacity=0.8 * op, scale=s_, anchor=(540, 860)), Item(hook, opacity=op, scale=s_, anchor=(540, 860))], (540, 960, 1.0)
    S.append(mk(t3a, t3b, s3))
    # S4 — tall side world: full figure -> eased tilt UP to the masked face (the mask hides her mouth)
    TW = Painter((-200, -600, 1300, 2300), res=0.9)
    TW.gfill(NIGHT_T, (30, 40, 56)); stars(TW, (-200, -600, 1300, 900), 200, 91)
    house_row(TW, 1700, -200, 1300, 200, 380, (20, 24, 33), 92, 0.4); haze(TW, 1700, 200, (30, 38, 52), 130)
    TW.rect((-200, 1700, 1300, 2300), (26, 28, 34)); TW.rect((-200, 1860, 1300, 1872), (56, 58, 64))
    tw_bg = TW.sprite(); tmd, tmg, tga = moon(820, -260, 120, res=1.3)
    WT = Painter((60, 60, 1020, 1900), res=1.7); woman_coat_side(WT, 420, 1862, 1760); wt = WT.sprite()
    tbeam = beam_sprite(1300, 1000, -300, 1500, 100, 800, (255, 236, 196), 0.35, 0.05, res=0.4, blur=60)
    rr = random.Random(5); dust = [(rr.uniform(-100, 1200), rr.uniform(300, 1900), rr.uniform(1.5, 4), rr.uniform(0, 6.28)) for _ in range(60)]
    dot = glow_sprite(0, 0, 6, (255, 245, 220), power=1.2, res=2)
    FULL = (600, 1060, 0.86); FACE = (500, 1862 - 0.90 * 1760, 2.1)
    t4a, t4b = T("because", 1), T("they", 1)
    def s4(t):
        lt = t - t4a
        cam = kf([(0, FULL), (0.55, (FULL[0], FULL[1] - 10, FULL[2] * 1.01), "lin"), (1.6, FACE, "io"), (t4b - t4a, (FACE[0], FACE[1], FACE[2] * 1.06), "lin")], lt)
        its = [Item(tw_bg), Item(tmg, add=True, opacity=tga), Item(tmd), Item(tbeam, add=True, opacity=0.8), Item(wt)]
        for (x, y, s_, ph) in dust:
            yy = y - (lt * 16 * s_) % 600; its.append(Item(dot, pos=(x + 12 * math.sin(lt + ph), yy), add=True, opacity=0.3, scale=s_ / 3, anchor=(x, yy)))
        return its, cam
    S.append(mk(t4a, t4b, s4))
    # S5 — title card (dissolve in)
    TP = Painter((-80, -80, 1160, 2000), res=1.1); TP.gfill((6, 8, 12), (22, 24, 30)); stars(TP, (-80, -80, 1160, 1100), 90, 31, a=90); tbg = TP.sprite()
    t_md, t_mg, t_ga = moon(540, 1090, 330, res=1.2, glow_r=2.0, glow_a=0.75)
    TF = Painter((-80, 900, 1160, 2000), res=1.1)
    TF.poly([(-80, 1640), (200, 1560), (420, 1400), (520, 1350), (560, 1350), (660, 1400), (880, 1560), (1160, 1640), (1160, 2000), (-80, 2000)], (8, 9, 12))
    utility_pole(TF, 130, 1010, 1640, 18, (8, 9, 12)); utility_pole(TF, 960, 1060, 1640, 16, (8, 9, 12))
    catenary(TF, (130, 1050), (960, 1095), 90, (8, 9, 12), 3); catenary(TF, (130, 1090), (960, 1130), 80, (8, 9, 12), 3)
    tx_, tb_ = 800, 1540                                                                      # torii gate on the slope
    TF.rect((tx_ - 60, tb_ - 150, tx_ - 48, tb_), (8, 9, 12)); TF.rect((tx_ + 48, tb_ - 150, tx_ + 60, tb_), (8, 9, 12))
    TF.poly([(tx_ - 92, tb_ - 156), (tx_ + 92, tb_ - 156), (tx_ + 100, tb_ - 172), (tx_ - 100, tb_ - 172)], (8, 9, 12)); TF.rect((tx_ - 72, tb_ - 130, tx_ + 72, tb_ - 120), (8, 9, 12))
    TF.gpoly([(-80, 1700), (1160, 1700), (1160, 2000), (-80, 2000)], (8, 9, 12, 0), (4, 4, 6, 255)); tfg = TF.sprite()
    lab = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    fr = ImageFont.truetype(FR, 30); fb = ImageFont.truetype(FB, 132)
    s_ = "J A P A N   ·   U R B A N   L E G E N D"
    d.rectangle([W / 2 - 22, 110, W / 2 + 22, 115], fill=(190, 46, 40, 255))
    d.text(((W - d.textlength(s_, font=fr)) / 2, 135), s_, font=fr, fill=(178, 172, 158, 255))
    d.text(((W - d.textlength("KUCHISAKE-ONNA", font=fb)) / 2, 180), "KUCHISAKE-ONNA", font=fb, fill=(228, 216, 194, 255))
    title = Sprite(np.asarray(lab).copy(), 1, 0, 0)
    sils = []
    for k in range(8):
        SP = Painter((300, 900, 820, 1400), res=1.6); woman_coat_front(SP, 540, 1356, 405, sil=True, wind=12 * math.sin(k / 8 * 2 * math.pi), scissors=True); sils.append(SP.sprite())
    tb = beam_sprite(540, -100, 540, 1400, 300, 700, (200, 196, 180), 0.16, 0.0, res=0.4, blur=60)
    t5a, t5b = T("they", 1), T("in", 3)
    def s5(t):
        lt = t - t5a; p = lt / (t5b - t5a); ta = min(1, max(0, (lt - 0.35) / 0.55))
        return [Item(tbg), Item(tb, add=True, opacity=0.9), Item(t_mg, add=True, opacity=t_ga), Item(t_md), Item(tfg), Item(sils[int(lt * 8) % 8]),
                Item(title, opacity=ta, par=0.0, scale=1.03 - 0.03 * ta, anchor=(540, 260))], (540, 1000, 1.0 + 0.06 * EASE["sine"](p))
    S.append(mk(t5a, t5b, s5, dissolve=0.27))
    # S6 — 1979: town skyline at night
    SK = Painter((-160, -80, 1240, 2000), res=1.0); SK.gfill(NIGHT_T, (30, 40, 56)); stars(SK, (-160, -80, 1240, 1100), 160, 101)
    house_row(SK, 1260, -160, 1240, 120, 260, (26, 32, 44), 102, 0.45); house_row(SK, 1380, -160, 1240, 100, 220, (18, 22, 30), 103, 0.4)
    utility_pole(SK, 180, 760, 1700, 22); utility_pole(SK, 940, 820, 1700, 20); catenary(SK, (180, 810), (940, 865), 70, w=3)
    SK.poly([(520, 1260), (700, 980), (790, 900), (860, 890), (940, 950), (1240, 1120), (1240, 1260)], (16, 20, 28))     # Mt. Kinka
    cx_, cy_ = 830, 890                                                                                                    # Gifu Castle (tenshu)
    for i, (w_, h_) in enumerate([(70, 26), (54, 22), (38, 20)]):
        y_ = cy_ - i * 30; SK.rect((cx_ - w_ / 2, y_ - h_, cx_ + w_ / 2, y_), (14, 16, 22))
        SK.poly([(cx_ - w_ / 2 - 14, y_ - h_), (cx_ + w_ / 2 + 14, y_ - h_), (cx_ + w_ / 2, y_ - h_ - 10), (cx_ - w_ / 2, y_ - h_ - 10)], (10, 12, 16))
    SK.rect((cx_ - 6, cy_ - 54, cx_ + 6, cy_ - 46), (230, 190, 110))
    SK.rect((-160, 1380, 1240, 2000), (10, 12, 16)); sk = SK.sprite(); kmd, kmg, kga = moon(300, 420, 74, res=1.4)
    t6a, t6b = T("in", 3), T("rumors")
    def s6(t):
        lt = t - t6a; p = lt / (t6b - t6a)
        return [Item(sk), Item(kmg, add=True, opacity=kga), Item(kmd)], (540 + 30 * p, 1000, 1.0 + 0.06 * p)
    S.append(mk(t6a, t6b, s6))
    # S7 — whispering silhouettes in a lit window
    WI = Painter((-60, -60, 1140, 1980), res=1.0); WI.gfill((14, 12, 12), (24, 20, 18)); WI.glow(540, 860, 560, (96, 66, 32), 1.0, 1.6)
    WI.rect((300, 560, 780, 1080), (236, 190, 120))
    WI.ell((380, 700, 500, 830), (30, 20, 14)); WI.rrect((350, 820, 530, 1090), 70, (30, 20, 14))
    WI.ell((590, 720, 700, 840), (30, 20, 14)); WI.rrect((560, 830, 730, 1090), 70, (30, 20, 14))
    for x in range(300, 781, 60): WI.rect((x - 3, 560, x + 3, 1080), (70, 46, 26))
    for y in range(560, 1081, 65): WI.rect((300, y - 3, 780, y + 3), (70, 46, 26))
    chochin(WI, 860, 760, 40); WI.rect((280, 540, 800, 556), (52, 36, 22)); WI.rect((280, 1080, 800, 1100), (52, 36, 22))
    wi = WI.sprite()
    t7a, t7b = T("rumors"), T("across")
    def s7(t):
        lt = t - t7a; p = lt / (t7b - t7a)
        its = [Item(wi)]
        for k in range(3):
            ph = (lt * 0.6 + k / 3) % 1; its.append(Item(rings, pos=(540, 780), scale=0.3 + ph * 1.2, anchor=(540, 780), opacity=(1 - ph) * 0.6))
        return its, (540, 860, 1.04 + 0.06 * p)
    S.append(mk(t7a, t7b, s7))
    # S8 — rumours spreading: skyline, windows light up one by one + rings across the rooftops
    lights = [(x, y) for x, y in [(80, 1230), (260, 1160), (420, 1210), (610, 1150), (800, 1220), (960, 1170), (150, 1330), (520, 1320), (880, 1330)]]
    win = Painter((-14, -16, 14, 16), res=2); win.rect((-12, -14, 12, 14), WARM_WIN); winspr = win.sprite()
    wg = glow_sprite(0, 0, 40, (230, 170, 90))
    t8a, t8b = T("across"), T("parents")
    def s8(t):
        lt = t - t8a; p = lt / (t8b - t8a)
        its = [Item(sk), Item(kmg, add=True, opacity=kga), Item(kmd)]
        for i, (x, y) in enumerate(lights):
            o = min(1, max(0, (lt - i * 0.14) / 0.12)); its += [Item(wg, pos=(x, y), add=True, opacity=0.6 * o), Item(winspr, pos=(x, y), opacity=o)]
        for k in range(2):
            ph = (lt * 0.5 + k / 2) % 1; its.append(Item(rings, pos=(540, 1240), scale=0.5 + ph * 2.2, anchor=(540, 1240), opacity=(1 - ph) * 0.5))
        return its, (600 - 60 * p, 1050, 1.08 - 0.05 * p)
    S.append(mk(t8a, t8b, s8))
    # S9 — dusk: children walking home in a group with an adult
    DK = Painter((-160, -80, 1240, 2000), res=1.0); DK.gfill((50, 22, 22), (196, 96, 44)); DK.glow(540, 1150, 500, (140, 76, 24), 1.0, 1.4)
    DK.circ(540, 1150, 120, (246, 196, 120)); house_row(DK, 1220, -160, 1240, 90, 200, (40, 18, 16), 111, 0.0)
    DK.rect((-160, 1220, 1240, 2000), (26, 12, 12)); utility_pole(DK, 120, 560, 1230, 16, (30, 14, 12)); utility_pole(DK, 1000, 600, 1230, 14, (30, 14, 12))
    catenary(DK, (120, 600), (1000, 640), 70, (30, 14, 12), 3)
    DK.rect((930, 980, 942, 1230), (40, 18, 14)); DK.poly([(936, 900), (1000, 990), (872, 990)], (230, 190, 40)); DK.poly([(936, 918), (986, 982), (886, 982)], (40, 18, 14))   # school-zone sign
    dk = DK.sprite()
    kids = []
    for st in range(2):
        KP = Painter((-60, -260, 60, 10), res=2)
        col = (24, 10, 10)
        o = 10 if st else -10
        KP.rect((-14, -70, -4, o if o > 0 else 0), col); KP.rect((4, -70, 14, -o if o < 0 else 0), col)
        KP.rrect((-28, -180, 28, -64), 14, col); KP.ell((-24, -236, 24, -188), col)
        KP.chord((-30, -246, 30, -200), 180, 360, (232, 196, 40)); KP.rrect((-44, -172, -18, -110), 6, (150, 30, 30))
        kids.append(KP.sprite())
    AP = Painter((-70, -420, 70, 10), res=2); col = (22, 9, 9)
    AP.rect((-26, -170, -6, 0), col); AP.rect((6, -170, 26, 0), col); AP.rrect((-44, -330, 44, -160), 24, col); AP.ell((-30, -400, 30, -334), col)
    adult = AP.sprite()
    t9a, t9b = T("parents"), T("according")
    def s9(t):
        lt = t - t9a; p = lt / (t9b - t9a)
        its = [Item(dk)]
        for i in range(5):
            x = 260 + i * 110 + lt * 45; its.append(Item(kids[int(lt * 6 + i) % 2], pos=(x, 1240 - 4 * abs(math.sin(lt * 6 + i)))))
        its.append(Item(adult, pos=(160 + lt * 45, 1244 - 3 * abs(math.sin(lt * 5)))))
        return its, (560 + 40 * p, 1000, 1.03 + 0.04 * p)
    S.append(mk(t9a, t9b, s9, dissolve=0.27))
    # S10 — "According to the legend": street, the woman appears far down the road (dissolve in)
    street2 = jp_street(seed=2)
    WF2 = Painter((480, 820, 680, 1040), res=3); woman_coat_front(WF2, 580, 1020, 200, wind=6); wf2 = WF2.sprite()
    g2 = glow_sprite(580, 940, 170, (210, 206, 190))
    t10a, t10b = T("according"), T("wears")
    def s10(t):
        lt = t - t10a; p = lt / (t10b - t10a)
        return street_items(street2, lt) + [Item(g2, add=True, opacity=0.6), Item(wf2, scale=0.9 + 0.15 * p, anchor=(580, 1020))], (560, 980, 1.0 + 0.05 * p)
    S.append(mk(t10a, t10b, s10))
    # S11 — long coat and scissors: tilt from coat down to the hand holding scissors
    WT2 = Painter((60, 60, 1020, 1900), res=1.7); woman_coat_side(WT2, 420, 1862, 1760, scissors=True); wt2 = WT2.sprite()
    glint = glow_sprite(0, 0, 40, (255, 255, 255), power=2.5, res=2)
    HAND = (520, 1862 - 0.36 * 1760, 1.9); COAT = (560, 1862 - 0.62 * 1760, 1.15)
    t11a, t11b = T("wears"), T("say", 2)
    def s11(t):
        lt = t - t11a; tb_ = T("pair") - t11a
        cam = kf([(0, COAT), (tb_ - 0.6, (COAT[0], COAT[1] + 20, COAT[2] * 1.02), "lin"), (tb_ + 0.4, HAND, "io"), (t11b - t11a, (HAND[0], HAND[1] + 10, HAND[2] * 1.04), "lin")], lt)
        gx, gy = 420 + 0.06 * 1760, 1862 - 0.30 * 1760
        go = max(0, 1 - abs(lt - (T("scissors") - t11a + 0.2)) / 0.25)
        return [Item(tw_bg), Item(tmg, add=True, opacity=tga), Item(tmd), Item(tbeam, add=True, opacity=0.8), Item(wt2), Item(glint, pos=(gx, gy), add=True, opacity=go)], cam
    S.append(mk(t11a, t11b, s11))
    # S12 — "Say no, and she uses them": scissors close-up, blades snap shut on "uses"
    SB = Painter((-60, -60, 1140, 1980), res=1.0); SB.gfill((8, 8, 12), (18, 16, 20)); SB.glow(540, 900, 700, (70, 30, 30), 1.0, 1.4); sbg = SB.sprite()
    BL = Painter((-60, -60, 980, 60), res=1.2)
    BL.poly([(0, -50), (900, -8), (940, 0), (900, 8), (0, 50)], (176, 180, 190)); BL.poly([(0, -50), (900, -8), (940, 0), (0, 0)], (214, 218, 226))
    BL.circ(0, 0, 26, (60, 60, 66)); blade = BL.sprite()
    HD = Painter((-330, -150, 20, 150), res=1.2); HD.d.ellipse(HD.box((-320, -140, -60, 140)), outline=(70, 20, 24, 255), width=int(46 * HD.k)); HD.rect((-80, -24, 10, 24), (70, 20, 24)); handle = HD.sprite()
    flash = Sprite(np.full((8, 8, 4), 255, np.uint8), 8 / W, 0, 0)
    t12a, t12b = T("say", 2), T("say", 3)
    def s12(t):
        lt = t - t12a; tu = T("uses") - t12a + 0.1
        op = 32 * (1 - ease_io(min(1, max(0, (lt - tu + 0.25) / 0.25)))) + 2 * math.sin(lt * 3)
        piv = (380, 980); its = [Item(sbg)]
        for sgn in (1, -1):
            its.append(Item(blade, pos=piv, rot=-20 + sgn * op / 2, anchor=piv))
            its.append(Item(handle, pos=piv, rot=-20 - sgn * op / 2, anchor=piv))
        fo = max(0, 1 - abs(lt - tu) / 0.12) * 0.55
        its.append(Item(glint, pos=(piv[0] + 300, piv[1] - 110), add=True, opacity=fo * 1.5, scale=3, anchor=(piv[0] + 300, piv[1] - 110)))
        return its, (540, 960, 1.0 + 0.04 * lt / (t12b - t12a))
    S.append(mk(t12a, t12b, s12))
    # S13 — "Say yes, and she pulls down her mask": portrait with the hand pulling the mask
    pw_pull = portrait_woman("pulling"); e_side = eyes_sprite("calm", 0.0)
    t13a, t13b = T("say", 3), T("but")
    def s13(t):
        lt = t - t13a; tp = T("pulls") - t13a
        m = Item(pw_mask if lt < tp else pw_pull)
        return [Item(pbg), m, Item(e_side)], (540, 880, 1.0 + 0.10 * EASE["sine"](lt / (t13b - t13a)))
    S.append(mk(t13a, t13b, s13))
    # S14 — "But here's the terrifying part": the young man, frightened
    ym_face, ym_eyes = young_man_portrait()
    YB = Painter((-60, -60, 1140, 1980), res=1.0); YB.gfill((5, 6, 9), (12, 14, 20)); YB.glow(760, 500, 500, (60, 70, 90), 1.0, 1.5)
    utility_pole(YB, 960, -60, 1980, 30, (14, 16, 22)); yb = YB.sprite()
    t14a, t14b = T("but"), T("her", 5)
    def s14(t):
        lt = t - t14a; p = lt / (t14b - t14a)
        return [Item(yb), Item(ym_face, pos=(0, 2 * math.sin(lt * 7))), Item(ym_eyes, pos=(0, 2 * math.sin(lt * 7)), opacity=0 if abs(lt - 1.4) < 0.06 else 1)], (540, 900, 1.0 + 0.07 * p)
    S.append(mk(t14a, t14b, s14))
    # S15 — "Her smile runs from ear to ear": the reveal, slow push
    pw_rev = portrait_woman("reveal"); e_dead = eyes_sprite("dead")
    cbg = portrait_bg(False)
    t15a, t15b = T("her", 5), T("asks", 2) - 0.48
    def s15(t):
        lt = t - t15a; p = lt / (t15b - t15a)
        return [Item(cbg), Item(pw_rev), Item(e_dead)], (540, 900, 1.05 + 0.15 * EASE["sine"](p))
    S.append(mk(t15a, t15b, s15))
    # S16 — "How about now?": closer on the grin, ripples, light flicker
    t16a, t16b = t15b, T("they", 2)
    def s16(t):
        lt = t - t16a; fl = flick(lt, -0.6)
        its = [Item(cbg, opacity=fl), Item(pw_rev), Item(e_dead)]
        for k in range(3):
            ph = (lt * 0.7 + k / 3) % 1; its.append(Item(rings, pos=(540, 960), scale=0.3 + ph * 1.2, anchor=(540, 960), opacity=(1 - ph) * 0.6))
        return its, (540, 1000, 1.40 + 0.10 * lt / (t16b - t16a))
    S.append(mk(t16a, t16b, s16))
    # S17 — "only one answer saves you": back of the young man in the foreground, her under the lamp
    YM = [Painter((60, 980, 560, 2040), res=1.2) for _ in range(2)]
    for st, Pm in enumerate(YM): young_man_back(Pm, 300, 2030, 1000, st)
    ymb = [p_.sprite() for p_ in YM]
    t17a, t17b = T("they", 2), T("tell")
    def s17(t):
        lt = t - t17a; p = lt / (t17b - t17a)
        return street_items(street, lt) + [Item(fglow, add=True, opacity=0.7, scale=1.6, anchor=(580, 1020)), Item(far_w, scale=1.6, anchor=(580, 1020)), Item(ymb[0])], (560, 1000, 1.0 + 0.04 * p)
    S.append(mk(t17a, t17b, s17))
    # S18 — "Tell her she looks... average": masked portrait, eyes drift away, head tilts (confused)
    e_away = eyes_sprite("calm", -0.9)
    t18a, t18b = T("tell"), T("while")
    def s18(t):
        lt = t - t18a; tilt = 6 * ease_io(min(1, max(0, (lt - (T("average") - t18a)) / 0.6)))
        e = e_calm if lt < T("average") - t18a else e_away
        return [Item(pbg), Item(pw_mask, rot=tilt, anchor=(540, 1400)), Item(e, rot=tilt, anchor=(540, 1400))], (540, 850, 1.0)
    S.append(mk(t18a, t18b, s18))
    # S19 — "you run": runner crossing the street, camera tracking
    RUN = []
    for i in range(8):
        RP = Painter((-260, -40, 260, 1040), res=1.0); runner(RP, 0, 1000, 1000, i / 8); RUN.append(RP.sprite())
    t19a, t19b = T("while"), T("so")
    def s19(t):
        lt = t - t19a; p = lt / (t19b - t19a); tr = T("run") - t19a - 1.2
        rx = 1180 - max(0, lt - tr) * 620
        its = street_items(street, lt) + [Item(fglow, add=True, opacity=0.6), Item(far_w)]
        if lt > tr: its.append(Item(RUN[int(lt * 14) % 8], pos=(rx, 760), scale=0.85, anchor=(rx, 1760)))
        return its, (560 - 60 * max(0, p - 0.5), 1000, 1.05)
    S.append(mk(t19a, t19b, s19))
    # S20 — "walk home alone tonight": lone walker from behind, camera follows
    street3 = jp_street(seed=3)
    t20a, t20b = T("so"), T("and", 12) if False else T("woman", 3) - 0.6
    def s20(t):
        lt = t - t20a; p = lt / (t20b - t20a)
        return street_items(street3, lt) + [Item(ymb[int(lt * 3) % 2], scale=0.62 - 0.08 * p, anchor=(300, 2030), pos=(240, -260 - 120 * p))], (560, 1000 - 30 * p, 1.0 + 0.05 * p)
    S.append(mk(t20a, t20b, s20))
    # S21 — "a woman in a mask steps out from a street corner": corner wall, she slides out, lamp flickers
    corner = jp_street(seed=4, corner=True)
    WC = Painter((540, 660, 980, 1310), res=1.6); woman_coat_front(WC, 730, 1300, 560, wind=4); wc = WC.sprite()
    wcg = glow_sprite(730, 1100, 260, (200, 196, 180))
    CW = Painter((760, 800, 1240, 2040), res=1.0); CW.poly([(760, 900), (1240, 820), (1240, 2040), (760, 2040)], (30, 34, 44)); CW.poly([(760, 900), (800, 900), (800, 2040), (760, 2040)], (44, 50, 62))
    for yy in range(960, 2000, 90): CW.line([(800, yy), (1240, yy - 50)], (24, 28, 36), 2)
    cwall = CW.sprite()
    t21a, t21b = t20b, T("dont", 2)
    def s21(t):
        lt = t - t21a; ts = T("steps") - t21a
        dx = 230 * (1 - ease_io(min(1, max(0, (lt - ts + 0.2) / 0.8))))
        fl = flick(lt, 0.2)
        return street_items(corner, lt, fl) + [Item(wcg, add=True, opacity=0.5 * fl, pos=(dx, 0)), Item(wc, pos=(dx, 0)), Item(cwall)], (600, 1040, 1.0 + 0.06 * lt / (t21b - t21a))
    S.append(mk(t21a, t21b, s21))
    # S22 — "don't say yes. Don't say no." masked portrait, staring, push in
    e_stare = eyes_sprite("calm", 0.0)
    t22a, t22b = T("dont", 2), T("because", 2)
    def s22(t):
        lt = t - t22a; p = lt / (t22b - t22a)
        return [Item(pbg), Item(pw_mask), Item(e_stare)], (540, 900, 1.05 + 0.20 * EASE["sine"](p))
    S.append(mk(t22a, t22b, s22))
    # S23 — "Because she isn't asking if she's pretty." eyes extreme close-up
    t23a, t23b = T("because", 2), T("shes", 2)
    def s23(t):
        lt = t - t23a; p = lt / (t23b - t23a)
        return [Item(pbg), Item(pw_mask), Item(e_stare)], (540, 960, 1.55 + 0.15 * p)
    S.append(mk(t23a, t23b, s23))
    # S24 — reveal with a flash cut, final hold
    t24a = T("shes", 2)
    def s24(t):
        lt = t - t24a
        fl = 1.0 if (lt % 0.9) > 0.06 else 0.2
        its = [Item(cbg, opacity=fl), Item(pw_rev), Item(e_dead)]
        return its, (540, 1020, 1.22 + 0.14 * EASE["sine"](min(1, lt / 3.2)))
    S.append(mk(t24a, END, s24))
    # ---- extra cuts: the reference cuts every 2.3-2.6 s; split long shots into a second framing (punch-in / reframe) ----
    def split(idx_fn, t_cut, cam_fn):
        i = next(k for k, s_ in enumerate(S) if s_["fn"].__name__ == idx_fn)
        a = S[i]; f0 = a["fn"]
        def f2(t, f0=f0, t_cut=t_cut):
            its, cam = f0(t); return its, cam_fn(t - t_cut, cam)
        f2.__name__ = idx_fn + "b"
        S[i] = mk(a["t0"], t_cut, f0, a["dz"]); S.insert(i + 1, mk(t_cut, a["t1"], f2))
    split("s4", T("hiding"), lambda lt, c: (500, 1862 - 0.885 * 1760, 2.65 + 0.06 * lt))
    split("s5", T("the", 2), lambda lt, c: (540, 1160, 1.45 + 0.04 * lt))
    split("s9", T("children"), lambda lt, c: (470, 1140, 1.55 + 0.04 * lt))
    split("s11", T("carries"), lambda lt, c: (520, 1862 - 0.36 * 1760, 1.9 + 0.03 * lt))
    split("s13", T("pulls"), lambda lt, c: (540, 960, 1.35 + 0.04 * lt))
    split("s15", T("ear", 1), lambda lt, c: (540, 1005, 1.45 + 0.05 * lt))
    split("s21", T("steps"), lambda lt, c: (680, 1060, 1.3 + 0.04 * lt))
    split("s24", T("look"), lambda lt, c: (540, 1045, 1.7 + 0.05 * lt))
    return S

# ================= captions =================
CHUNKS = ["In Japan,", "if a woman", "in a white mask", "stops you on an empty street", "at night,", "and asks,", "Am I pretty?", "#Don't say no,",
          "because that mask", "is the only thing", "hiding her mouth.", "They call her", "Kuchisake Onna,", "the slit-mouthed woman.", "In 1979,",
          "rumors about her", "spread out of Gifu", "and across Japan.", "Parents and teachers", "started walking", "children home in groups.",
          "According to the legend,", "she wears a long coat", "and carries", "a pair of scissors.", "Say no,", "and she uses them.", "Say yes,",
          "and she pulls down", "her mask.", "But here's the", "terrifying part.", "Her smile", "runs from ear to ear.", "And she asks again,",
          "How about now?", "They say only", "one answer", "saves you.", "Tell her she looks", "average.", "While she decides", "what that means,",
          "you run.", "So, if you ever", "walk home alone", "tonight,", "and a woman", "in a mask", "steps out", "from a street corner,", "don't say yes.",
          "Don't say no.", "Because she isn't asking", "if she's pretty.", "She's asking", "if you want", "to look like her."]
RED = {"JAPAN,", "WHITE", "MASK", "PRETTY?", "MOUTH.", "KUCHISAKE", "ONNA,", "SLIT-MOUTHED", "1979,", "GIFU", "GROUPS.", "SCISSORS.", "NO,", "YES,",
       "TERRIFYING", "EAR", "TO", "EAR.", "NOW?", "AVERAGE.", "RUN.", "ALONE", "YES.", "NO.", "LIKE", "HER."}
def build_chunks():
    out = []; k = 0
    ws_all = list(words)
    for c in CHUNKS:
        hidden = c.startswith("#"); toks = c.lstrip("#").split()
        ws = []
        for tok in toks:
            while k < len(ws_all) and ws_all[k]["w"].strip().startswith("-"): k += 1
            m = ws_all[k]; k += 1
            txt = tok.upper()
            if txt == "SLIT-MOUTHED":
                while k < len(ws_all) and ws_all[k]["w"].strip().startswith("-"): k += 1
            red = txt in RED and not (txt == "TO" and "EAR" not in c.upper()) and not (txt == "MASK" and "WHITE" not in c.upper() and "PULLS" not in c.upper() and "IN A MASK" not in c.upper())
            ws.append(dict(txt=txt, s=m["s"], e=m["e"], red=red))
        out.append(dict(words=ws, hidden=hidden))
    assert k == len(ws_all), (k, len(ws_all))
    return out

def main():
    print("building shots...", flush=True)
    SH = build_all(); chunks = build_chunks(); cap = Captioner(FB, size=84)
    for a, b in zip(SH[:-1], SH[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6 or b["t0"] >= a["t1"] - 1e-6, (a["t1"], b["t0"])
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
        hook = SH[i]["fn"].__name__ == "s3"
        if not hook: img = vignette(img, 0.6)
        img = grain(img, 0, 2.0)          # static grain (the reference has no animated noise: ~15-20% of its frames are fully still)
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
        sheet.save(os.path.join(EP, "stills.jpg"), quality=90); print("stills"); return
    out = os.path.join(EP, "ep01_noaudio.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    nf = int(math.ceil(END * FPS))
    for n in range(nf):
        pr.stdin.write(frame(n).tobytes())
        if n % 150 == 0: print("frame", n, "/", nf, flush=True)
    pr.stdin.close(); pr.wait(); print("wrote", out, "%.2f s" % (nf / FPS))

if __name__ == "__main__":
    main()
