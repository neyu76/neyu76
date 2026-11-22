"""render_v03test.py — like-for-like fidelity test: rebuild V03 0–32.7 s (same text, same shot plan) with Milo voice.
INTERNAL COMPARISON ONLY — uses the reference's narration text; never publish.
Usage: python -I render_v03test.py <dark_atlas_dir>
"""
import sys, os, json, math, random, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from engine import *

ROOT = sys.argv[1]; OUTD = os.path.join(ROOT, "test_v03")
FB = os.path.join(ROOT, "fonts", "Oswald-Bold.ttf"); FR = os.path.join(ROOT, "fonts", "Oswald-Regular.ttf")
rng = random.Random(11)

# ======================= time map: reference time -> Milo time =======================
milo = [w for s in json.load(open(os.path.join(OUTD, "voice_milo_transcript.json"), encoding="utf-8")) for w in s["words"]]
ref = [w for s in json.load(open(os.path.join(ROOT, "analysis", "V03_look_at_feet_transcript.json"), encoding="utf-8")) for w in s["words"]]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
pairs = [(0.0, 0.0)]
j = 0
for w in milo:
    while j < len(ref) and norm(ref[j]["w"]) != norm(w["w"]): j += 1
    if j < len(ref): pairs.append((ref[j]["s"], w["s"])); j += 1
pairs.sort()
def f(tr):
    for (a0, b0), (a1, b1) in zip(pairs[:-1], pairs[1:]):
        if tr <= a1: return b0 + (tr - a0) * (b1 - b0) / max(1e-6, a1 - a0)
    return pairs[-1][1] + (tr - pairs[-1][0])
REF_CUTS = [0, 2.70, 4.77, 5.90, 7.47, 10.17, 12.80, 15.90, 19.60, 22.80, 24.90, 26.93, 29.50, 32.67]
CUT = [f(t) for t in REF_CUTS]
END = max(CUT[-1], milo[-1]["e"] + 0.45)
print("cuts", ["%.2f" % c for c in CUT], "end %.2f" % END)

# ======================= shared drawing =======================
SKY_T, SKY_B = (7, 10, 17), (30, 40, 56)
M_LIGHT, M_DARK, SNOW = (74, 86, 106), (54, 64, 82), (150, 160, 178)

def stars(P, box, n, seed=1, a=150):
    r = random.Random(seed)
    for _ in range(n):
        x = r.uniform(box[0], box[2]); y = r.uniform(box[1], box[3]); s = r.uniform(1.0, 2.2)
        P.circ(x, y, s, (200, 205, 220, r.randint(a // 3, a)))

def mountains(P, base, peaks, light=M_LIGHT, dark=M_DARK, snow=True, fill_below=None, haze=(30, 40, 56)):
    for (x, py, hw) in peaks:
        lo = lambda c: tuple(int(a * 0.55 + b * 0.45) for a, b in zip(c, haze))
        P.gpoly([(x - hw, base), (x, py), (x, base)], light, lo(light), py, base)
        P.gpoly([(x, py), (x + hw, base), (x, base)], dark, lo(dark), py, base)
        if snow:
            k = 0.09
            P.poly([(x - hw * k, py + (base - py) * k), (x, py), (x + hw * k * 0.9, py + (base - py) * k * 0.9), (x + hw * 0.02, py + (base - py) * 0.06), (x - hw * 0.03, py + (base - py) * 0.1)], SNOW)
    if fill_below: P.rect((P.x0, base - 1, P.x1, P.y1), fill_below)

def haze(P, y, hgt, col=(40, 52, 70), a=150):
    P.gpoly([(P.x0, y - hgt), (P.x1, y - hgt), (P.x1, y), (P.x0, y)], col + (0,), col + (a,))

def range_peaks(x0, x1, base, hmin, hmax, wmin, wmax, seed):
    r = random.Random(seed); out = []; x = x0
    while x < x1:
        hw = r.uniform(wmin, wmax) * 1.55; out.append((x, base - r.uniform(hmin, hmax) * 0.85, hw)); x += hw * r.uniform(1.0, 1.5)
    return out

def pine(P, x, base, h, col):
    w = h * 0.36
    for k in range(4):
        y1 = base - h * (0.15 + k * 0.22); P.poly([(x - w * (1 - k * 0.2), y1 + h * 0.28), (x, y1 - h * 0.12), (x + w * (1 - k * 0.2), y1 + h * 0.28)], col)
    P.rect((x - h * 0.03, base - h * 0.15, x + h * 0.03, base), col)

def moon(cx, cy, r, res=1.0, glow_r=3.6, glow_a=0.95):
    P = Painter((cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2), res=res, ss=3)
    P.circ(cx, cy, r, (226, 212, 178))
    P.glow(cx - r * 0.25, cy - r * 0.3, r * 1.15, (246, 238, 214), 0.85, 1.4)          # light centre (spherical feel)
    ov = Image.new("RGBA", P.img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for ox, oy, rr in [(-.33, -.18, .19), (.3, .16, .13), (-.04, .42, .1), (.4, -.36, .08), (-.5, .3, .065), (.12, -.5, .06)]:
        od.ellipse(P.box((cx + (ox - rr) * r, cy + (oy - rr) * r, cx + (ox + rr) * r, cy + (oy + rr) * r)), fill=(200, 184, 148, 80))
    P.img = Image.alpha_composite(P.img, ov.filter(ImageFilter.GaussianBlur(r * P.k * 0.01))); P.d = ImageDraw.Draw(P.img)
    # clip to disc (remove crater spill) + darker rim
    a = np.asarray(P.img).copy(); hh, ww = a.shape[:2]
    yy, xx = np.mgrid[:hh, :ww]; d = np.hypot(xx - (cx - P.x0) * P.k, yy - (cy - P.y0) * P.k) / (r * P.k)
    a[..., 3] = (np.clip((1 - d) * r * P.k / 2, 0, 1) * a[..., 3]).astype(np.uint8)
    rim = np.clip((d - 0.86) / 0.14, 0, 1)[..., None]
    a[..., :3] = (a[..., :3] * (1 - 0.18 * rim)).astype(np.uint8)
    P.img = Image.fromarray(a, "RGBA"); P.d = ImageDraw.Draw(P.img)
    disk = P.sprite()
    G = Painter((cx - r * glow_r, cy - r * glow_r, cx + r * glow_r, cy + r * glow_r), res=0.5, ss=1)
    G.glow(cx, cy, r * glow_r, (92, 84, 64), 1.0, 1.8)          # wide faint halo
    G.glow(cx, cy, r * 2.1, (150, 138, 104), 1.0, 1.6)          # bright halo ~2x radius (as on V03)
    G.glow(cx, cy, r * 1.25, (120, 110, 84), 1.0, 1.0)
    g = G.sprite()
    return disk, g, glow_a

def glow_sprite(cx, cy, r, color, power=2.0, res=0.5):
    G = Painter((cx - r, cy - r, cx + r, cy + r), res=res, ss=1); G.glow(cx, cy, r, color, 1.0, power); return G.sprite()

def beam_sprite(x0, y0, x1, y1, w0, w1, color, a0=1.0, a1=0.0, res=0.5, blur=30):
    """light beam from (x0,y0) to (x1,y1), widths w0->w1, alpha a0->a1 (for additive use)."""
    xs = [x0, x1]; ys = [y0, y1]; m = max(w0, w1) + blur * 2
    box = (min(xs) - m, min(ys) - m, max(xs) + m, max(ys) + m)
    P = Painter(box, res=res, ss=1)
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    steps = 40
    for i in range(steps):
        t0 = i / steps; t1 = (i + 1) / steps
        wa = w0 + (w1 - w0) * t0; wb = w0 + (w1 - w0) * t1; al = a0 + (a1 - a0) * t0
        pa = (x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0); pb = (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
        P.poly([(pa[0] + nx * wa / 2, pa[1] + ny * wa / 2), (pb[0] + nx * wb / 2, pb[1] + ny * wb / 2), (pb[0] - nx * wb / 2, pb[1] - ny * wb / 2), (pa[0] - nx * wa / 2, pa[1] - ny * wa / 2)], tuple(color) + (int(255 * al),))
    P.blur(blur)
    return P.sprite()

# ---------- characters ----------
DRESS_T, DRESS_B, FOLD = (226, 220, 204), (196, 190, 174), (176, 170, 156)
SKIN_PALE = (222, 212, 194); HAIR = (8, 8, 10)

def woman_side(P, x, feet, h, dress_top=None, dress_bot=None):
    """side view facing right, arm reaching forward-down (asking for a ride), long black hair panel down the back,
    BARE FEET POINTING LEFT (backwards). Coordinates measured on V03 frame 3.8 s (h = head top to sole)."""
    dt = dress_top or (210, 204, 190); db = dress_bot or (188, 182, 168)
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    P.ell((X(-170), Y(10), X(150), Y(-14)), (0, 0, 0, 70))
    # long hair panel behind (crown -> below the waist), slightly curved
    P.poly([(X(-112), Y(960)), (X(-40), Y(985)), (X(-48), Y(700)), (X(-60), Y(470)), (X(-100), Y(420)), (X(-142), Y(450)), (X(-136), Y(700))], HAIR)
    foot_pair(P, X, Y, k)                    # feet first: ankles disappear under the hem
    # dress
    body = [(X(-70), Y(834)), (X(62), Y(834)), (X(74), Y(800)), (X(110), Y(400)), (X(140), Y(66)), (X(80), Y(58)), (X(0), Y(54)), (X(-90), Y(58)), (X(-144), Y(68)), (X(-120), Y(400)), (X(-86), Y(790))]
    P.gpoly(body, dt, db, Y(834), Y(26))
    P.gpoly([(X(-70), Y(834)), (X(-44), Y(834)), (X(-78), Y(400)), (X(-100), Y(60)), (X(-144), Y(68)), (X(-120), Y(400)), (X(-86), Y(790))],
            (196, 190, 176), (172, 166, 152), Y(834), Y(36))
    for fx0, fx1 in [(-30, -80), (0, -20), (26, 40), (50, 98)]:
        P.line([(X(fx0), Y(700)), (X((fx0 + fx1) / 2 + 4), Y(380)), (X(fx1), Y(80))], (176, 170, 156), 2.6 * k)
    # head: dome of hair (face turned away / hidden)
    P.ell((X(-116), Y(1000), X(76), Y(812)), HAIR)
    P.arc((X(-96), Y(992), X(60), Y(860)), 200, 300, (40, 40, 46), 3 * k)            # soft rim light on the hair
    # front strand over the shoulder
    P.poly([(X(8), Y(880)), (X(50), Y(860)), (X(48), Y(684)), (X(14), Y(680))], HAIR)
    # arm: shoulder -> wrist, pointing forward and slightly DOWN
    P.poly([(X(20), Y(830)), (X(62), Y(812)), (X(214), Y(724)), (X(198), Y(696)), (X(36), Y(770))], (204, 198, 184))
    P.poly([(X(46), Y(822)), (X(62), Y(812)), (X(214), Y(724)), (X(208), Y(714))], (226, 220, 206))
    # hand: palm + pointing fingers
    P.poly([(X(206), Y(728)), (X(236), Y(726)), (X(270), Y(712)), (X(272), Y(704)), (X(246), Y(704)), (X(250), Y(690)), (X(240), Y(686)), (X(222), Y(700)), (X(200), Y(702))], SKIN_PALE)

def foot_pair(P, X, Y, k):
    def foot(dx, dy, col, toe_col, shade):
        pts = [(-152, 2), (-156, 10), (-150, 20), (-128, 28), (-96, 36), (-60, 46), (-26, 60), (-4, 80), (34, 82), (40, 60), (46, 40), (44, 16), (34, 2), (14, -2), (-120, -2)]
        P.poly([(X(x + dx), Y(y + dy)) for x, y in pts], col)
        P.poly([(X(x + dx), Y(y + dy)) for x, y in [(-60, 46), (-26, 60), (-4, 80), (34, 82), (40, 60), (14, 40), (-20, 34)]], shade)   # top of foot / ankle shading
        P.ell((X(-4 + dx), Y(44 + dy), X(48 + dx), Y(-2 + dy)), col)                                      # heel
        for i, tx in enumerate((-150, -138, -126, -114)):
            P.ell((X(tx + dx), Y(6 + dy), X(tx + dx + 13 - i), Y(-4 + dy)), toe_col)                          # toes underneath
        P.line([(X(-140 + dx), Y(2 + dy)), (X(-60 + dx), Y(2 + dy))], toe_col, 2.2 * k)
    foot(74, 6, (150, 146, 136), (128, 124, 114), (140, 136, 126))       # far foot (behind, darker)
    foot(0, 0, (206, 198, 182), (182, 174, 158), (196, 188, 172))        # near foot
    P.ell((X(-6), Y(70), X(20), Y(60)), (226, 220, 204))                 # small anklet glint as on V03

def title_silhouette(P, cx, base, h, sway=0.0):
    """moon-backed silhouette (V03 title card): round head, hair to the shoulders, thin hanging arms, narrow waist,
    dress flaring to a wide hem, two long crescent hair streams blowing to the right."""
    u = h / 540.0; c = (6, 6, 8)
    def T(px, py): return (cx + (px - 432) * u, base - (640 - py) * u)
    P.poly([T(380, 130), T(484, 130), T(488, 205), T(376, 205)], c)                     # hair down to shoulders
    P.ell((*T(395, 98), *T(470, 165)), c)                                                # head
    P.poly([T(362, 196), T(502, 196), T(508, 220), T(472, 302), T(394, 302), T(356, 220)], c)   # shoulders/torso
    P.poly([T(350, 214), T(368, 214), T(372, 372), T(354, 372)], c)                     # left arm
    P.poly([T(496, 214), T(514, 214), T(512, 372), T(496, 372)], c)                     # right arm
    P.poly([T(396, 296), T(470, 296), T(604, 646), T(266, 646)], c)                     # dress
    s1, s2 = sway, sway * 1.4
    P.poly([T(436, 112), T(520, 128), T(600, 170 + s1 * 0.5), T(658, 222 + s1), T(600, 196 + s1 * 0.6), T(520, 178), T(470, 172)], c)
    P.poly([T(470, 186), T(540, 236), T(596, 290 + s2 * 0.5), T(632, 346 + s2), T(580, 300 + s2 * 0.6), T(526, 262), T(478, 226)], c)

def woman_front(P, x, feet, h, silhouette=False, hair_wind=0.0):
    """front view: black hair framing a small pale face, one hair stream blowing to the right, rounded shoulders,
    straight torso with arms down, dress flaring to ~2x shoulder width. h = head top to hem."""
    k = h / 1000.0
    def X(v): return x + v * k
    def Y(v): return feet - v * k
    hair = (6, 6, 8) if silhouette else (10, 10, 12)
    d_top, d_bot = ((10, 10, 13), (10, 10, 13)) if silhouette else ((226, 220, 206), (204, 198, 184))
    if not silhouette: P.ell((X(-280), Y(14), X(280), Y(-16)), (0, 0, 0, 110))
    w = hair_wind
    P.poly([(X(70), Y(900)), (X(150), Y(880 + w * 0.3)), (X(240), Y(835 + w * 0.6)), (X(320), Y(780 + w)), (X(220), Y(805 + w * 0.6)), (X(130), Y(830 + w * 0.3)), (X(60), Y(845))], hair)   # stream
    P.ell((X(-118), Y(1000), X(108), Y(760)), hair)                                                          # hair mass
    P.poly([(X(-122), Y(880)), (X(-90), Y(880)), (X(-92), Y(720)), (X(-128), Y(740))], hair)                 # hair over left shoulder
    P.rrect((X(-126), Y(810), X(126), Y(420)), 48 * k, d_top)                                                # shoulders + torso
    P.gpoly([(X(-126), Y(450)), (X(126), Y(450)), (X(200), Y(200)), (X(258), Y(14)), (X(150), Y(4)), (X(0), Y(0)), (X(-150), Y(4)), (X(-258), Y(14)), (X(-200), Y(200))], d_top, d_bot, Y(450), Y(0))
    if not silhouette:
        for sx in (-1, 1):
            P.line([(X(sx * 84), Y(770)), (X(sx * 88), Y(450))], (198, 192, 178), 4 * k)                   # arms hanging
        P.ell((X(-40), Y(955), X(36), Y(850)), (228, 214, 192))                                              # face
        P.chord((X(-54), Y(992), X(50), Y(890)), 180, 360, hair)                                             # fringe

def jeep_rear(P, x, base, w):
    k = w / 1000.0
    def X(v): return x + v * k
    def Y(v): return base - v * k
    P.ell((X(-560), Y(40), X(560), Y(-40)), (0, 0, 0, 120))
    P.rrect((X(-500), Y(560), X(500), Y(60)), 40 * k, (22, 26, 34))
    P.rrect((X(-420), Y(820), X(420), Y(540)), 50 * k, (26, 30, 40))
    P.rrect((X(-330), Y(780), X(330), Y(600)), 20 * k, (12, 16, 24))   # rear window
    P.circ(X(0), Y(330), 170 * k, (14, 16, 22)); P.circ(X(0), Y(330), 90 * k, (30, 34, 44)); P.circ(X(0), Y(330), 30 * k, (14, 16, 22))  # spare tyre
    for s in (-1, 1):
        P.rrect((X(s * 430 - 45), Y(470), X(s * 430 + 45), Y(380)), 10 * k, (200, 40, 36))
        P.rect((X(s * 500 - 120), Y(80), X(s * 500 + 40), Y(-40)), (8, 8, 10))
    P.rect((X(-60), Y(140), X(60), Y(100)), (210, 210, 210))

# ======================= SHOTS =======================
SHOTS = []
def shot(i):
    def deco(fn): SHOTS.append((i, fn)); return fn
    return deco
def L(t, i):  # local progress helpers
    return t - CUT[i], CUT[i + 1] - CUT[i]

# ---------- S0: wide mountains + winding road, car headlights travel, push-in ----------
def build_s0():
    P = Painter((-80, -80, 1160, 2000), res=1.25)
    P.gfill((8, 11, 18), (30, 38, 52)); stars(P, (-80, -80, 1160, 1000), 150, 1)
    mountains(P, 1160, [(50, 690, 200), (235, 650, 190), (470, 835, 200), (660, 850, 180), (850, 836, 190), (1080, 790, 210)])
    haze(P, 1170, 160, (44, 54, 72), 170)
    mountains(P, 1240, [(-20, 930, 260), (270, 1000, 250), (540, 975, 260), (810, 1000, 250), (1100, 925, 260)], light=(56, 66, 84), dark=(46, 54, 70), snow=False)
    haze(P, 1250, 120, (40, 48, 64), 190)
    mountains(P, 1330, [(260, 1075, 300), (700, 1180, 330), (1050, 1150, 300)], light=(44, 50, 64), dark=(38, 44, 58), snow=False)
    P.gpoly([(-80, 1345), (300, 1325), (600, 1318), (900, 1340), (1160, 1370), (1160, 2000), (-80, 2000)], (30, 34, 44), (18, 20, 28))
    road = [(250, 1652), (520, 1640), (760, 1612), (930, 1570), (990, 1520), (960, 1468), (820, 1430), (560, 1410), (380, 1402), (335, 1398)]
    P.line(road, (50, 56, 70), 34); P.line([(x, y - 6) for x, y in road], (60, 66, 80), 10)
    for x, b, hh in [(-40, 1980, 640), (90, 1990, 520), (190, 2000, 360), (1040, 1990, 560), (1150, 1990, 480)]: pine(P, x, b, hh, (10, 12, 17))
    P.gpoly([(-80, 1780), (1160, 1780), (1160, 2000), (-80, 2000)], (12, 14, 20, 0), (6, 8, 12, 255))
    bg = P.sprite()
    md, mg, ga = moon(263, 397, 126, res=1.6)
    W0 = Painter((900, 1440, 990, 1580), res=3); woman_front(W0, 942, 1560, 92); wf = W0.sprite()
    wglow = glow_sprite(942, 1520, 90, (200, 192, 168))
    hl = glow_sprite(0, 0, 40, (255, 240, 200), power=1.5)
    beam = beam_sprite(0, 0, 230, -14, 10, 90, (255, 232, 180), 0.8, 0.0, blur=10)
    return dict(bg=bg, md=md, mg=mg, ga=ga, wf=wf, wglow=wglow, hl=hl, beam=beam, road=road)
@shot(0)
def s0(t, A):
    lt, d = L(t, 0); p = lt / d
    cam = (540 - 20 * p, 960 - 60 * EASE["sine"](p), 1.0 + 0.10 * EASE["sine"](p))
    # car along road segment index 0..4
    u = 0.02 + 0.30 * p; road = A["road"]; seg = u * (len(road) - 1); i0 = int(seg); fr = seg - i0
    (xa, ya), (xb, yb) = road[i0], road[min(i0 + 1, len(road) - 1)]
    cx, cy = xa + (xb - xa) * fr, ya + (yb - ya) * fr; ang = math.degrees(math.atan2(yb - ya, xb - xa))
    its = [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"]),
           Item(A["wglow"], add=True, opacity=0.55 + 0.1 * math.sin(lt * 3)), Item(A["wf"]),
           Item(A["beam"], pos=(cx, cy), rot=ang, anchor=(cx + A["beam"].ox, cy + A["beam"].oy), add=True, opacity=0.8),
           Item(A["hl"], pos=(cx, cy), add=True, opacity=0.9)]
    # anchor fix for rotated beam: rotate around car point
    its[5] = Item(A["beam"], pos=(cx, cy), rot=ang, anchor=(cx, cy), add=True, opacity=0.8)
    return its, cam

# ---------- S1: woman side + jeep approaching from right, headlight beam ----------
def build_s1():
    P = Painter((-100, -100, 1180, 2020), res=1.15)
    P.gfill(SKY_T, (26, 34, 48)); stars(P, (-100, -100, 1180, 1000), 140, 7)
    mountains(P, 1200, [(150, 960, 210), (520, 940, 220), (930, 980, 200)]); haze(P, 1200, 160)
    mountains(P, 1330, [(-40, 1100, 260), (330, 1090, 270), (760, 1120, 270), (1120, 1080, 260)], light=(52, 62, 80), dark=(40, 48, 64), snow=False)
    haze(P, 1340, 140, (36, 44, 58), 200)
    P.gpoly([(-100, 1380), (1180, 1380), (1180, 1580), (-100, 1580)], (34, 40, 52), (26, 30, 40))
    P.rect((-100, 1580, 1180, 2020), (16, 18, 24)); P.rect((-100, 1580, 1180, 1588), (46, 50, 60))
    for x in range(-60, 1180, 170): P.rrect((x, 1540, x + 46, 1556), 5, (170, 170, 164))
    P.gpoly([(-100, 1800), (1180, 1800), (1180, 2020), (-100, 2020)], (16, 18, 24, 0), (6, 6, 9, 255))
    bg = P.sprite()
    md, mg, ga = moon(225, 410, 78, res=1.4)
    Wp = Painter((0, 560, 900, 1640), res=1.25); woman_side(Wp, 360, 1600, 950); ws = Wp.sprite()
    J = Painter((840, 1260, 1400, 1700), res=1.3)
    J.poly([(1050, 1305), (1400, 1305), (1400, 1597), (900, 1597), (873, 1570), (873, 1430), (900, 1402), (975, 1395)], (19, 21, 28))   # body, cabin, bonnet
    J.line([(975, 1395), (1050, 1305), (1400, 1305)], (62, 70, 86), 4)                                                                 # windscreen / roof edge
    J.line([(900, 1402), (975, 1395)], (40, 46, 58), 3); J.line([(873, 1430), (873, 1570)], (34, 38, 48), 3)
    J.rrect((868, 1527, 932, 1562), 8, (34, 36, 44))                                                                                     # bumper
    J.ell((885, 1413, 909, 1464), (240, 232, 205))                                                                                       # round headlight
    J.circ(1032, 1602, 52, (10, 10, 13)); J.circ(1032, 1602, 16, (55, 58, 66))                                                           # wheel + hub
    jeep = J.sprite()
    beam = beam_sprite(890, 1438, -250, 1500, 40, 520, (255, 238, 200), 0.7, 0.05, blur=40)
    hl = glow_sprite(897, 1438, 110, (255, 240, 205), power=1.5)
    return dict(bg=bg, md=md, mg=mg, ga=ga, ws=ws, jeep=jeep, beam=beam, hl=hl)
@shot(1)
def s1(t, A):
    lt, d = L(t, 1); p = lt / d
    cam = (540, 960, 1.0 + 0.05 * p)
    dx = 170 * (1 - ease_out(min(1, p * 1.2)))
    return [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"]),
            Item(A["beam"], pos=(dx, 0), add=True, opacity=0.25 + 0.55 * min(1, p * 1.5)),
            Item(A["ws"]), Item(A["jeep"], pos=(dx, 3 * math.sin(lt * 18))), Item(A["hl"], pos=(dx, 0), add=True, opacity=0.9)], cam

# ---------- S2: driver front view, charm swinging ----------
def build_s2():
    K = 1.5
    def q(x, y): return (x * K, y * K)
    def b(x0, y0, x1, y1): return (x0 * K, y0 * K, x1 * K, y1 * K)
    P = Painter((-60, -60, 1140, 1980), res=1.1)
    P.gfill((3, 4, 7), (6, 7, 10))
    P.gpoly([q(60, 118), q(665, 118), q(690, 1090), q(30, 1090)], (20, 27, 40), (14, 19, 29))                   # windscreen
    for x0, w in ((100, 14), (150, 8), (205, 20)): P.poly([q(x0, 130), q(x0 + w, 130), q(x0 - 60 + w, 1080), q(x0 - 60, 1080)], (26, 34, 48, 140))   # glass streaks
    P.rrect(b(215, 268, 505, 712), 36, (12, 16, 25))                                                            # rear window behind the head
    P.rect(b(-40, 1090, 760, 1320), (4, 4, 6))
    bg = P.sprite()
    D = Painter((0, 480, 1080, 1960), res=1.2)
    skinL, skinR, hair, shirt, shawl = (160, 112, 76), (140, 96, 62), (16, 12, 10), (76, 86, 106), (108, 84, 58)
    D.chord(b(50, 790, 670, 1400), 180, 360, shirt); D.rect(b(50, 1090, 670, 1300), shirt)                      # shoulders
    D.poly([q(50, 1095), q(62, 960), q(110, 870), q(190, 815), q(268, 800), q(262, 1095)], shawl)              # shawl over the left shoulder
    for x0 in (95, 140, 190): D.line([q(x0 + 25, 860), q(x0, 1090)], (92, 70, 48), 4)
    D.line([q(360, 840), q(360, 1095)], (60, 70, 88), 3); D.circ(360 * K, 955 * K, 5, (60, 70, 88))           # placket + button
    D.rect(b(318, 680, 402, 805), (132, 90, 58)); D.poly([q(318, 680), q(402, 680), q(402, 720), q(318, 740)], (112, 76, 48))   # neck + chin shadow
    D.poly([q(320, 792), q(360, 842), q(400, 792), q(400, 806), q(360, 852), q(320, 806)], (60, 70, 88))       # V collar
    D.ell(b(222, 528, 248, 574), skinL); D.ell(b(474, 528, 500, 574), skinR)                                    # ears
    face = [q(250, 430), q(480, 430), q(482, 520), q(474, 580), q(452, 632), q(418, 670), q(360, 692), q(302, 670), q(268, 632), q(250, 580), q(244, 520)]
    D.poly(face, skinL)
    D.poly([q(370, 430), q(480, 430), q(482, 520), q(474, 580), q(452, 632), q(418, 670), q(375, 690)], skinR)
    D.poly([q(238, 430), q(262, 430), q(256, 540), q(240, 528)], hair); D.poly([q(466, 430), q(492, 430), q(488, 528), q(472, 540)], hair)   # hair below the cap
    D.rect(b(244, 418, 488, 440), hair)
    D.ell(b(245, 338, 475, 398), (154, 132, 98)); D.rrect(b(230, 370, 490, 432), 30, (138, 116, 84))            # pakol: dome + rolled band
    D.line([q(236, 404), q(484, 404)], (122, 102, 74), 3); D.circ(345 * K, 340 * K, 5, (122, 102, 74))
    D.arc(b(280, 498, 344, 528), 200, 340, (24, 16, 12), 7); D.arc(b(376, 498, 442, 528), 200, 340, (24, 16, 12), 7)   # heavy brows
    D.line([q(372, 520), q(356, 602)], (112, 74, 46), 4); D.arc(b(348, 592, 384, 612), 10, 170, (112, 74, 46), 4)     # nose
    D.poly([q(322, 628), q(342, 618), q(360, 622), q(378, 618), q(400, 628), q(394, 638), q(360, 632), q(328, 638)], (22, 14, 10))   # moustache
    D.ell(b(342, 640, 382, 652), (146, 86, 70))                                                                   # lower lip
    D.line([q(286, 562), q(334, 562)], (176, 128, 92), 3); D.line([q(388, 562), q(436, 562)], (154, 108, 74), 3)   # eye bags
    driver = D.sprite()
    E = Painter((410, 770, 680, 850), res=2)
    for ex in (312, 412):
        cx = ex * K; cy = 540 * K
        E.ell((cx - 42, cy - 17, cx + 42, cy + 17), (226, 214, 196)); E.circ(cx + 10, cy + 1, 15, (48, 30, 20)); E.circ(cx + 10, cy + 1, 6, (8, 6, 6))
        E.chord((cx - 46, cy - 26, cx + 46, cy + 8), 180, 360, (154 if ex < 360 else 136, 108 if ex < 360 else 94, 72 if ex < 360 else 60))   # heavy upper lid
        E.arc((cx - 44, cy - 20, cx + 44, cy + 16), 190, 350, (20, 14, 10), 7)
    eyes = E.sprite()
    Wh = Painter((-40, 1440, 1120, 1960), res=1.2)
    Wh.rect(b(-30, 1088, 750, 1320), (5, 5, 7))                                                                   # dashboard
    Wh.arc(b(150, 990, 570, 1320), 192, 348, (24, 24, 29), 46)                                                     # thick wheel rim
    for hx in (188, 532): Wh.ell(b(hx - 38, 1040, hx + 38, 1086), (150, 104, 68))                                  # hands
    Wh.poly([q(190, 1080), q(225, 1080), q(215, 1300), q(150, 1300)], (52, 60, 76)); Wh.poly([q(495, 1080), q(530, 1080), q(570, 1300), q(505, 1300)], (52, 60, 76))   # forearms
    Wh.rect(b(340, 1090, 380, 1300), (10, 10, 12))
    wheel = Wh.sprite()
    C = Painter((480, 250, 580, 520), res=1.5)
    C.line([q(358, 176), q(354, 250)], (110, 90, 60), 3)
    for i, (x, y) in enumerate([(355, 258), (360, 272), (352, 284), (346, 296), (342, 308), (340, 320)]): C.circ(x * K, y * K, 6, (150, 116, 70))
    charm = C.sprite()
    M = Painter((400, 230, 680, 280), res=1.2); M.rrect(b(280, 160, 440, 176), 6, (52, 60, 74)); mirror = M.sprite()
    return dict(bg=bg, driver=driver, eyes=eyes, wheel=wheel, charm=charm, mirror=mirror)
@shot(2)
def s2(t, A):
    lt, d = L(t, 2); p = lt / d
    cam = (540, 960, 1.0 + 0.04 * p); bob = 3 * math.sin(lt * 9)
    blink = abs(lt - 0.95) < 0.06
    return [Item(A["bg"]), Item(A["driver"], pos=(0, bob)), Item(A["eyes"], pos=(0, bob), opacity=0 if blink else 1),
            Item(A["wheel"], pos=(0, bob * 0.5)), Item(A["charm"], rot=8 * math.sin(lt * 4.2), anchor=(358 * 1.5, 176 * 1.5)), Item(A["mirror"])], cam

# ---------- S3: hook card ----------
def build_s3():
    f = ImageFont.truetype(FB, 150)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i, ln in enumerate(["LOOK AT HER", "FEET."]):
        d.text(((W - d.textlength(ln, font=f)) / 2, 700 + i * 150), ln, font=f, fill=(198, 38, 38, 255))
    glow = lay.filter(ImageFilter.GaussianBlur(26))
    g = np.asarray(glow).copy(); g[..., 3] = (g[..., 3] * 0.9).astype(np.uint8)
    return dict(txt=Sprite(np.asarray(lay).copy(), 1, 0, 0), glow=Sprite(g, 1, 0, 0))
@shot(3)
def s3(t, A):
    lt, d = L(t, 3); p = lt / d
    op = 1.0 if lt < d - 0.32 else max(0, (d - lt) / 0.32)
    s = 1.0 + 0.035 * p
    return [Item(A["glow"], add=True, opacity=0.8 * op, scale=s, anchor=(540, 840)), Item(A["txt"], opacity=op, scale=s, anchor=(540, 840))], (540, 960, 1.0)

# ---------- S4 + S8: woman side close-up world (tilt down to the backward feet / tilt up to the hair) ----------
def build_side_world():
    P = Painter((-200, -900, 1300, 2300), res=0.9)
    P.gfill(SKY_T, (30, 40, 56)); stars(P, (-200, -900, 1300, 900), 220, 13)
    mountains(P, 1500, range_peaks(-300, 1400, 1500, 360, 700, 160, 260, 14)); haze(P, 1500, 300)
    mountains(P, 1700, range_peaks(-300, 1400, 1700, 160, 360, 200, 300, 15), light=(48, 60, 80), dark=(30, 38, 54), snow=False)
    P.rect((-200, 1860, 1300, 2300), (14, 16, 22)); P.rect((-200, 1860, 1300, 1872), (52, 56, 66))
    bg = P.sprite()
    md, mg, ga = moon(300, -330, 135, res=1.3)
    Wp = Painter((40, 60, 1220, 1900), res=1.7, ss=2); woman_side(Wp, 400, 1862, 1760); ws = Wp.sprite()
    beam = beam_sprite(1400, 1540, -300, 1980, 120, 900, (255, 238, 200), 0.55, 0.05, res=0.4, blur=60)
    beam2 = beam_sprite(1400, 1500, -300, 1100, 60, 600, (220, 226, 236), 0.25, 0.0, res=0.4, blur=60)
    rr = random.Random(21)
    dust = [(rr.uniform(-100, 1200), rr.uniform(1100, 1900), rr.uniform(1.5, 4), rr.uniform(0, 6.28)) for _ in range(70)]
    dot = glow_sprite(0, 0, 6, (255, 245, 220), power=1.2, res=2)
    return dict(bg=bg, md=md, mg=mg, ga=ga, ws=ws, beam=beam, beam2=beam2, dust=dust, dot=dot)
FEET_CAM = (337, 1862 - (0.52 * H - H / 2) / 1.45, 1.45)
HAIR_CAM = (470, 100 + 120 - (0.30 * H - H / 2) / 1.42, 1.42)
FULL_CAM = (600, 1060, 0.86)
def side_items(A, lt, cam_, beam_op=1.0):
    its = [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"]),
           Item(A["beam2"], add=True, opacity=0.6 * beam_op), Item(A["beam"], add=True, opacity=beam_op * (0.85 + 0.1 * math.sin(lt * 2.3)))]
    its.append(Item(A["ws"]))
    for (x, y, s, ph) in A["dust"]:
        yy = y - (lt * 18 * s) % 500; xx = x + 14 * math.sin(lt * 0.8 + ph)
        its.append(Item(A["dot"], pos=(xx, yy), scale=s / 3, anchor=(xx, yy), add=True, opacity=0.35))
    return its
@shot(4)
def s4(t, A):
    lt, d = L(t, 4)
    t_a, t_b = f(7.77) - CUT[4], f(8.73) - CUT[4]
    cam = kf([(0, FULL_CAM), (t_a, (FULL_CAM[0], FULL_CAM[1] + 20, FULL_CAM[2] * 1.01), "lin"), (t_b, FEET_CAM, "io"), (d, (FEET_CAM[0], FEET_CAM[1] + 6, FEET_CAM[2] * 1.035), "lin")], lt)
    return side_items(A, lt, cam), cam
@shot(8)
def s8(t, A):
    lt, d = L(t, 8)
    t_a, t_b = f(20.80) - CUT[8], f(21.53) - CUT[8]
    start = (430, 1862 - (0.67 * H - H / 2) / 1.35, 1.35)
    cam = kf([(0, start), (t_a, (start[0], start[1] - 30, start[2] * 1.02), "lin"), (t_b, HAIR_CAM, "io"), (d, (HAIR_CAM[0], HAIR_CAM[1] - 8, HAIR_CAM[2] * 1.03), "lin")], lt)
    return side_items(A, lt, cam, 0.8), cam

# ---------- S5: title card ----------
def build_s5():
    P = Painter((-80, -80, 1160, 2000), res=1.1)
    P.gfill((6, 8, 12), (22, 24, 30)); stars(P, (-80, -80, 1160, 1100), 90, 31, a=90)
    bg = P.sprite()
    md, mg, ga = moon(540, 1090, 330, res=1.2, glow_r=2.0, glow_a=0.75)
    B = Painter((-80, 1150, 1160, 2000), res=1.1)
    mountains(B, 1640, [(60, 1330, 260), (1020, 1300, 260), (300, 1430, 240), (800, 1420, 240)], light=(78, 80, 88), dark=(62, 64, 72), snow=False)
    back = B.sprite()
    F = Painter((-80, 1150, 1160, 2000), res=1.1)
    F.poly([(-80, 1640), (200, 1560), (420, 1400), (520, 1350), (560, 1350), (660, 1400), (880, 1560), (1160, 1640), (1160, 2000), (-80, 2000)], (8, 9, 12))
    for x, hgt in [(-30, 470), (70, 360), (1010, 360), (1110, 470)]: pine(F, x, 1690, hgt, (8, 9, 12))
    F.gpoly([(-80, 1700), (1160, 1700), (1160, 2000), (-80, 2000)], (8, 9, 12, 0), (4, 4, 6, 255))
    fg = F.sprite()
    lab = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lab)
    fr = ImageFont.truetype(FR, 30); fb = ImageFont.truetype(FB, 168)
    s_ = "N O R T H E R N   P A K I S T A N   ·   L E G E N D"
    d.rectangle([W / 2 - 22, 110, W / 2 + 22, 115], fill=(190, 46, 40, 255))
    d.text(((W - d.textlength(s_, font=fr)) / 2, 135), s_, font=fr, fill=(178, 172, 158, 255))
    d.text(((W - d.textlength("PICHAL PERI", font=fb)) / 2, 175), "PICHAL PERI", font=fb, fill=(228, 216, 194, 255))
    title = Sprite(np.asarray(lab).copy(), 1, 0, 0)
    hairs = []
    for k in range(8):
        Hh = Painter((300, 900, 820, 1400), res=1.6); title_silhouette(Hh, 540, 1356, 405, sway=10 * math.sin(k / 8 * 2 * math.pi)); hairs.append(Hh.sprite())
    beam = beam_sprite(540, -100, 540, 1400, 300, 700, (200, 196, 180), 0.16, 0.0, res=0.4, blur=60)
    return dict(bg=bg, md=md, mg=mg, ga=ga, back=back, fg=fg, title=title, hairs=hairs, beam=beam)
@shot(5)
def s5(t, A):
    lt, d = L(t, 5); p = lt / d
    cam = (540, 1000, 1.0 + 0.06 * EASE["sine"](p))
    ta = min(1, max(0, (lt - 0.35) / 0.55))
    wind = A["hairs"][int(lt * 8) % 8]
    return [Item(A["bg"]), Item(A["beam"], add=True, opacity=0.9), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"]), Item(A["back"]), Item(A["fg"]), Item(wind),
            Item(A["title"], opacity=ta, par=0.0, scale=1.03 - 0.03 * ta, anchor=(540, 260))], cam

# ---------- S6: mountains of the north, glowing eyes in the forest ----------
def build_s6():
    K = 1.5
    P = Painter((-160, -80, 1240, 2000), res=1.1)
    P.gfill((6, 9, 15), (22, 30, 42)); stars(P, (-160, -80, 1240, 1000), 200, 41)
    pk = lambda L: [(x * K, y * K, hw * K) for x, y, hw in L]
    mountains(P, 830 * K, pk([(-20, 640, 150), (118, 545, 150), (355, 615, 140), (578, 597, 150), (760, 640, 150)]), light=(76, 88, 108), dark=(60, 70, 88))
    haze(P, 830 * K, 90 * K, (40, 50, 66), 150)
    mountains(P, 900 * K, pk([(-40, 700, 160), (160, 645, 150), (335, 650, 150), (555, 695, 150), (740, 660, 150)]), light=(58, 68, 86), dark=(48, 56, 72))
    haze(P, 900 * K, 80 * K, (34, 42, 56), 160)
    mountains(P, 990 * K, pk([(20, 830, 190), (180, 800, 180), (400, 820, 190), (600, 810, 190)]), light=(38, 44, 56), dark=(32, 37, 48), snow=False)
    haze(P, 990 * K, 70 * K, (26, 30, 40), 170)
    mountains(P, 1200 * K, pk([(85, 930, 230), (320, 920, 230), (610, 945, 230)]), light=(20, 23, 30), dark=(17, 20, 26), snow=False)
    P.rect((-160, 1180 * K, 1240, 2000), (7, 8, 11))
    for x, base, h in [(45, 1250, 350), (125, 1250, 245), (650, 1250, 315)]: pine(P, x * K, base * K, h * K, (8, 9, 12))
    P.gpoly([(-160, 1150 * K), (1240, 1150 * K), (1240, 2000), (-160, 2000)], (6, 7, 10, 0), (3, 3, 5, 255))
    bg = P.sprite()
    md, mg, ga = moon(810, 462, 105, res=1.4)
    E = Painter((-16, -6, 16, 6), res=3); E.circ(-9, 0, 3.4, (246, 186, 86)); E.circ(9, 0, 3.4, (246, 186, 86)); eye = E.sprite()
    eg = glow_sprite(0, 0, 34, (230, 150, 60))
    # two clusters of eyes (pairs), as on V03
    spots = [(338, 1566, 0.2), (390, 1578, 1.1), (700, 1596, 0.6), (735, 1606, 1.6)]
    return dict(bg=bg, md=md, mg=mg, ga=ga, eye=eye, eg=eg, spots=spots)
@shot(6)
def s6(t, A):
    lt, d = L(t, 6); p = lt / d
    cam = (520 + 40 * EASE["sine"](p), 960, 1.0 + 0.05 * p)
    its = [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"], par=0.92)]
    for (x, y, ph) in A["spots"]:
        o = 0.0 if ((lt + ph) % 2.3) < 0.12 else min(1, max(0, (lt - ph * 0.3) / 0.4))
        its += [Item(A["eg"], pos=(x, y), add=True, opacity=0.5 * o), Item(A["eye"], pos=(x, y), opacity=o)]
    return its, cam

# ---------- S7/S9/S10: road in the mountain pass (perspective) ----------
def build_road():
    HY = 998
    P = Painter((-160, -120, 1240, 2040), res=1.1)
    P.gfill((7, 10, 17), (24, 34, 48)); stars(P, (-160, -120, 1240, 950), 160, 51)
    mountains(P, HY, [(495, 802, 150), (615, 758, 150), (760, 860, 140), (862, 735, 160), (1035, 840, 150), (1190, 800, 140)],
              light=(44, 56, 72), dark=(30, 40, 54)); haze(P, HY, 120, (24, 32, 44), 160)
    P.rect((-160, HY, 1240, 2040), (20, 25, 33))                                                     # ground right of the road
    rl = lambda y: 518 + (y - HY) * (154 - 518) / (1920 - HY); rr = lambda y: 630 + (y - HY) * (867 - 630) / (1920 - HY)
    P.gpoly([(518, HY), (630, HY), (rr(2040), 2040), (rl(2040), 2040)], (56, 57, 60), (44, 44, 46))            # road
    P.gpoly([(560, HY), (590, HY), (700, 2040), (390, 2040)], (62, 63, 66, 120), (54, 54, 56, 120))            # lit centre band
    # left mountain wall: big dark dome, convex edge from the upper-left down to the road at the horizon
    wall = [(-160, -120), (-160, 230), (0, 240), (120, 300), (225, 390), (310, 490), (375, 600), (430, 720), (465, 840), (492, 940), (515, HY)]
    wall += [(rl(y) - 6, y) for y in (1100, 1300, 1500, 1700, 1920)] + [(rl(2040) - 6, 2040), (-160, 2040)]
    P.gpoly(wall, (6, 8, 12), (9, 12, 18))
    P.line([(0, 240), (120, 300), (225, 390), (310, 490), (375, 600), (430, 720), (465, 840), (492, 940), (515, HY)], (22, 27, 36), 5)   # rim
    P.line([(-20, 510), (90, 600), (180, 700), (260, 820), (320, 950), (368, 1102)], (21, 24, 31), 8)                     # strata arcs
    P.line([(-20, 880), (60, 980), (130, 1100), (190, 1220), (225, 1305)], (21, 24, 31), 8)
    for (x, y, w, hh) in [(847, 1368, 34, 16), (930, 1497, 36, 18), (1012, 1630, 40, 20)]:
        P.rrect((x - w / 2, y - hh / 2, x + w / 2, y + hh / 2), 5, (150, 150, 150))                                  # reflector posts
    P.ell((-300, 1815, 1380, 2300), (5, 5, 7))                                                                         # bonnet edge
    bg = P.sprite()
    md, mg, ga = moon(885, 368, 86, res=1.4)
    Wf = Painter((520, 880, 800, 1140), res=3); woman_front(Wf, 660, 1118, 200, hair_wind=0); wf = Wf.sprite()
    Wf2 = Painter((520, 880, 800, 1140), res=3); woman_front(Wf2, 660, 1118, 200, hair_wind=14); wf2 = Wf2.sprite()
    wg = glow_sprite(660, 1040, 190, (210, 206, 190))
    J = Painter((220, 1080, 820, 1720), res=1.3)
    J.ell((250, 1650, 790, 1700), (0, 0, 0, 150))
    J.rrect((259, 1290, 778, 1663), 34, (22, 24, 32))
    J.rrect((324, 1112, 670, 1300), 36, (26, 28, 36))
    J.rrect((350, 1130, 470, 1250), 14, (14, 16, 22)); J.rrect((490, 1130, 645, 1250), 14, (14, 16, 22))
    J.ell((372, 1160, 430, 1225), (8, 8, 10)); J.rect((376, 1195, 426, 1250), (8, 8, 10))
    J.circ(518, 1458, 119, (16, 18, 24)); J.circ(518, 1458, 72, (30, 32, 40)); J.circ(518, 1458, 26, (14, 16, 22))
    J.rrect((282, 1385, 330, 1420), 6, (200, 36, 34)); J.rrect((700, 1385, 748, 1420), 6, (200, 36, 34))
    J.rrect((475, 1572, 572, 1604), 4, (190, 190, 186))
    J.rect((259, 1620, 778, 1663), (12, 12, 16))
    jeep = J.sprite()
    tl = glow_sprite(0, 0, 70, (255, 40, 30))
    R = Painter((-400, -400, 400, 400), res=1.2)
    for r in (120, 220, 330): R.arc((-r, -r, r, r), 0, 360, (200, 200, 196, 110), 2.5)
    rings = R.sprite()
    return dict(bg=bg, md=md, mg=mg, ga=ga, wf=wf, wf2=wf2, wg=wg, jeep=jeep, tl=tl, rings=rings)
def road_items(A, lt, ws=1.0, wpos=(0, 0), extra=()):
    a = (660, 1118); spr = A["wf2"] if (lt * 2.2) % 2 < 1 else A["wf"]       # hair stream flutters
    its = [Item(A["bg"]), Item(A["mg"], add=True, opacity=A["ga"]), Item(A["md"]),
           Item(A["wg"], add=True, opacity=0.7, scale=ws, anchor=a, pos=wpos), Item(spr, scale=ws, anchor=a, pos=wpos)]
    return its + list(extra)
@shot(7)
def s7(t, A):
    lt, d = L(t, 7); p = lt / d
    cam = (560, 960, 1.0 + 0.05 * EASE["sine"](p))
    ws = 0.86 + 0.20 * p; bob = 3 * abs(math.sin(lt * 4.5))
    return road_items(A, lt, ws, (0, 12 * p - bob)), cam
@shot(9)
def s9(t, A):
    lt, d = L(t, 9); p = lt / d
    cam = (600, 1000, 1.08 + 0.06 * p)
    rings = []
    for k in range(3):
        ph = (lt * 0.55 + k / 3) % 1
        rings.append(Item(A["rings"], pos=(660, 1030), scale=0.2 + ph * 1.0, anchor=(660, 1030), opacity=(1 - ph) * 0.9))
    return road_items(A, lt, 1.1, (0, 0), rings), cam
@shot(10)
def s10(t, A):
    lt, d = L(t, 10); p = lt / d
    cam = (540, 960, 1.0 + 0.03 * p)
    jp = ease_out(min(1, p * 1.05)); js = 1.02 - 0.10 * jp; jy = -60 - 70 * jp
    brake = 0.5 + 0.5 * min(1, max(0, (p - 0.55) / 0.2))
    anchor = (518, 1663)
    its = road_items(A, lt, 1.62, (139, 145))
    its.append(Item(A["jeep"], scale=js, anchor=anchor, pos=(0, jy + 2.5 * math.sin(lt * 15) * (1 - jp))))
    for lx in (306, 724):
        gx = anchor[0] + (lx - anchor[0]) * js; gy = anchor[1] + jy + (1402 - anchor[1]) * js
        its.append(Item(A["tl"], pos=(gx, gy), add=True, opacity=brake))
    return its, cam

# ---------- S11: flashback dusk (one version of the legend) ----------
def build_s11():
    K = 1.5
    P = Painter((-160, -80, 1240, 2000), res=1.0)
    P.gpoly([(-160, -80), (1240, -80), (1240, 2000), (-160, 2000)], (34, 12, 10), (150, 64, 34), -80, 1150)
    P.glow(415 * K, 740 * K, 520 * K, (190, 96, 46), 0.75, 1.5)
    P.circ(415 * K, 740 * K, 105 * K, (232, 146, 86))                                                              # setting sun
    pk = lambda L: [(x * K, y * K, hw * K) for x, y, hw in L]
    mountains(P, 860 * K, pk([(62, 588, 140), (265, 592, 120), (428, 577, 130), (618, 605, 130), (760, 640, 120)]), light=(122, 50, 32), dark=(98, 38, 24), snow=False, haze=(120, 50, 30))
    mountains(P, 960 * K, pk([(92, 785, 190), (400, 800, 190), (700, 820, 170)]), light=(78, 30, 20), dark=(68, 26, 18), snow=False, haze=(70, 26, 18))
    P.poly([(-160, 1010 * K), (420 * K, 1000 * K), (720 * K, 950 * K), (1240, 940 * K), (1240, 2000), (-160, 2000)], (30, 12, 9))   # hill (right side higher)
    house = (24, 10, 8)
    P.rect((105 * K, 918 * K, 415 * K, 1090 * K), house); P.rect((95 * K, 912 * K, 425 * K, 924 * K), house)
    P.rect((25 * K, 990 * K, 105 * K, 1090 * K), house); P.rect((18 * K, 985 * K, 112 * K, 995 * K), house)
    P.rect((205 * K, 885 * K, 235 * K, 918 * K), house)
    for x0, y0, w, h in [(275, 927, 17, 17), (355, 968, 23, 26), (120, 1028, 23, 24)]: P.rect((x0 * K, y0 * K, (x0 + w) * K, (y0 + h) * K), (236, 160, 92))
    P.line([(318 * K, 905 * K), (312 * K, 860 * K), (322 * K, 820 * K), (314 * K, 770 * K)], (70, 30, 22, 160), 4)   # smoke wisp
    P.gpoly([(-160, 1080 * K), (1240, 1080 * K), (1240, 2000), (-160, 2000)], (16, 6, 5, 200), (8, 3, 3, 255))
    bg = P.sprite()
    S = Painter((780, 960, 1080, 1460), res=1.6); c = (16, 6, 5)
    S.circ(605 * K, 680 * K, 22 * K, c)                                                                            # head
    S.poly([(625 * K, 668 * K), (640 * K, 690 * K), (686 * K, 785 * K), (650 * K, 770 * K), (628 * K, 700 * K)], c)   # veil falling to the right
    S.poly([(585 * K, 700 * K), (630 * K, 700 * K), (640 * K, 760 * K), (660 * K, 965 * K), (550 * K, 965 * K), (568 * K, 820 * K), (580 * K, 760 * K)], c)   # robe
    S.ell((545 * K, 735 * K, 600 * K, 830 * K), c)                                                                  # belly (pregnant)
    sil = S.sprite()
    rr = random.Random(63)
    embers = [(rr.uniform(-100, 1180), rr.uniform(900, 1900), rr.uniform(0, 6.28), rr.uniform(0.6, 1.6)) for _ in range(30)]
    dot = glow_sprite(0, 0, 6, (255, 170, 90), res=2)
    return dict(bg=bg, sil=sil, embers=embers, dot=dot)
@shot(11)
def s11(t, A):
    lt, d = L(t, 11); p = lt / d
    cam = (540 + 25 * p, 960, 1.0 + 0.05 * p)
    its = [Item(A["bg"]), Item(A["sil"], pos=(-10 + 18 * p, 1.5 * math.sin(lt * 4)))]
    for (x, y, ph, sp) in A["embers"]:
        yy = y - (lt * 50 * sp) % 900; its.append(Item(A["dot"], pos=(x + 20 * math.sin(lt + ph), yy), add=True, opacity=0.45))
    return its, cam

# ---------- S12: room, bed, lamp -> lamp dies, moonlight from window ----------
def build_s12():
    out = {}
    for mode in ("warm", "cold"):
        P = Painter((-100, -80, 1180, 2000), res=1.0)
        if mode == "warm": P.gfill((64, 30, 16), (128, 62, 30)); P.glow(820, 1230, 900, (190, 110, 50), 0.45, 1.6)
        else: P.gfill((14, 14, 20), (26, 24, 30))
        P.rect((-100, 1690, 1180, 2000), (20, 10, 6) if mode == "warm" else (8, 8, 12))
        P.rrect((150, 1030, 330, 1250), 6, (30, 20, 16)); P.rect((168, 1048, 312, 1232), (52, 66, 90) if mode == "warm" else (70, 90, 120))   # window
        P.rrect((700, 1160, 900, 1400), 90, (26, 14, 8)); P.rect((700, 1290, 900, 1400), (26, 14, 8))                                       # niche
        P.rect((180, 1600, 960, 1630), (30, 18, 10)); P.rect((200, 1630, 225, 1720), (30, 18, 10)); P.rect((915, 1630, 940, 1720), (30, 18, 10))   # charpai
        col = (214, 186, 140) if mode == "warm" else (66, 80, 108)
        P.poly([(210, 1605), (250, 1520), (360, 1470), (470, 1500), (560, 1450), (700, 1470), (820, 1520), (930, 1605)], col)
        P.ell((850, 1660, 960, 1720), (30, 16, 10))
        out[mode] = P.sprite()
    out["beam"] = beam_sprite(240, 1140, 520, 1700, 180, 420, (150, 170, 210), 0.5, 0.15, res=0.5, blur=30)
    F = Painter((780, 1280, 820, 1350), res=3); F.ell((788, 1290, 812, 1340), (255, 200, 90)); F.ell((794, 1306, 806, 1336), (255, 245, 200)); out["flame"] = F.sprite()
    out["fg"] = glow_sprite(800, 1310, 260, (255, 170, 70))
    L0 = Painter((770, 1330, 830, 1370), res=2); L0.ell((770, 1334, 830, 1366), (70, 40, 20)); out["lamp"] = L0.sprite()
    return out
@shot(12)
def s12(t, A):
    lt, d = L(t, 12); p = lt / d
    cam = (560, 1250, 1.05 + 0.05 * p)
    tc = f(31.30) - CUT[12]; c = min(1, max(0, (lt - tc) / 0.16))
    fl = 0.85 + 0.15 * math.sin(lt * 21) * math.sin(lt * 7.3)
    return [Item(A["warm"], opacity=1 - c), Item(A["cold"], opacity=c), Item(A["beam"], add=True, opacity=c),
            Item(A["fg"], add=True, opacity=0.8 * fl * (1 - c)), Item(A["flame"], opacity=1 - c, scale=fl, anchor=(800, 1340)), Item(A["lamp"])], cam

# ======================= captions =======================
CHUNKS = ["In Pakistan,", "if a beautiful woman", "asks you for help", "on a mountain road", "at night,", "#look at her feet,", "because they might be",
          "facing backwards.", "They call her", "Pichal Peri,", "a spirit", "from the mountains", "of the north.", "They say she appears", "to men",
          "travelling alone.", "A white dress,", "long black hair,", "and a voice", "so soft", "you stop", "without thinking.", "According to",
          "one version", "of the legend,", "she was once a", "woman", "who died in childbirth."]
RED = {"PAKISTAN,", "BEAUTIFUL", "WOMAN", "FACING", "BACKWARDS.", "PICHAL", "PERI,", "SPIRIT", "TRAVELLING", "ALONE.", "WHITE", "DRESS,", "LONG", "BLACK",
       "HAIR,", "SOFT", "WITHOUT", "THINKING.", "DIED", "IN", "CHILDBIRTH."}
def build_chunks():
    out = []; k = 0
    for ci, c in enumerate(CHUNKS):
        hidden = c.startswith("#"); words = c.lstrip("#").split()
        ws = []
        for w in words:
            m = milo[k]; k += 1
            txt = w.upper()
            red = txt in RED and not (txt == "WOMAN" and ci != 1) and not (txt == "IN" and "CHILDBIRTH" not in c.upper())
            ws.append(dict(txt=txt, s=m["s"], e=m["e"], red=red))
        out.append(dict(words=ws, hidden=hidden))
    return out

# ======================= main =======================
def main():
    print("building assets..."); assets = {}
    builders = {0: build_s0, 1: build_s1, 2: build_s2, 3: build_s3, 5: build_s5, 6: build_s6, 11: build_s11, 12: build_s12}
    for i, b in builders.items(): assets[i] = b(); print(" asset", i, flush=True)
    side = build_side_world(); assets[4] = assets[8] = side
    road = build_road(); assets[7] = assets[9] = assets[10] = road
    fns = dict(SHOTS)
    chunks = build_chunks(); cap = Captioner(FB, size=84)
    DISSOLVE = {5: 0.27, 11: 0.27}       # shots that start with a dissolve from the previous shot (as measured on V03)
    def shot_at(t):
        for i in range(len(CUT) - 1):
            if t < CUT[i + 1]: return i
        return len(CUT) - 2
    def render_shot(i, t):
        fn = fns[i]; A = assets[i]
        return render_frame(lambda tt: fn(tt, A), t)
    if len(sys.argv) > 2:   # stills mode: comma separated ref-times -> PNG contact sheet
        ts = [f(float(x)) for x in sys.argv[2].split(",")]
        ims = []
        for t in ts:
            i = shot_at(t); img = render_shot(i, t)
            if i != 3: img = vignette(img, 0.6)
            act = None
            for c in chunks:
                if c["words"][0]["s"] <= t + 0.03: act = c
            if act and not act["hidden"] and not (CUT[3] <= t < CUT[4]):
                img = cap.apply(img, act["words"], sum(1 for w in act["words"] if w["s"] <= t + 0.03))
            ims.append(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((270, 480), Image.LANCZOS))
        sheet = Image.new("RGB", (270 * min(8, len(ims)), 480 * ((len(ims) + 7) // 8)))
        for k, im in enumerate(ims): sheet.paste(im, ((k % 8) * 270, (k // 8) * 480))
        sheet.save(os.path.join(OUTD, "stills.jpg"), quality=90); print("stills"); return
    out = os.path.join(OUTD, "v03test_noaudio.mp4")
    pr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    nf = int(math.ceil(END * FPS))
    for n in range(nf):
        t = n / FPS; i = shot_at(t)
        img = render_shot(i, t)
        dz = DISSOLVE.get(i)
        if dz and t - CUT[i] < dz:                       # dissolve: blend with previous shot continuing
            a = (t - CUT[i]) / dz; a = a * a * (3 - 2 * a)
            img = render_shot(i - 1, t) * (1 - a) + img * a
        if i != 3: img = vignette(img, 0.6)
        img = grain(img, n, 2.0)
        # captions
        act = None
        for c in chunks:
            if c["words"][0]["s"] <= t + 0.03: act = c
        if act and not act["hidden"] and not (CUT[3] <= t < CUT[4]):
            shown = sum(1 for w in act["words"] if w["s"] <= t + 0.03)
            img = cap.apply(img, act["words"], shown)
        pr.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
        if n % 60 == 0: print("frame", n, "/", nf, "shot", i, flush=True)
    pr.stdin.close(); pr.wait(); print("wrote", out, "dur %.2f" % (nf / FPS))

if __name__ == "__main__":
    main()
