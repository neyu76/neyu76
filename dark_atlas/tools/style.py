"""style.py — shared Dark Atlas Tales drawing kit (palette, mountains, moon, beams, characters) extracted from the
V03 fidelity test (render_v03test.py v5, approved by the user 17/11/2026)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from engine import *
rng = random.Random(11)
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

