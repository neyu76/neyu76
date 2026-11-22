"""engine.py — tiny 2D vector-scene engine for Dark Atlas Tales style videos.

Concepts
- Painter: draws vector shapes (PIL, supersampled) into an RGBA sprite in *world units*.
- Sprite: RGBA numpy image + `res` (pixels per world unit) + origin (world coords of its top-left).
- Item: a sprite placed per-frame (position/scale/rotation/opacity/parallax/blend).
- Camera: (cx, cy, zoom) keyframes with easing; world point (cx,cy) maps to frame centre.
- Frame render = warp every item into the output with ONE affine (camera x item), alpha-blend or add.
- Motion blur: number of sub-samples chosen from the fastest on-screen displacement (camera + items).
"""
import math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30

# ---------------- easing / keyframes ----------------
def ease_io(p):  # cubic in-out
    p = min(1, max(0, p)); return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
def ease_out(p): p = min(1, max(0, p)); return 1 - (1 - p) ** 3
def lin(p): return min(1, max(0, p))
EASE = dict(io=ease_io, out=ease_out, lin=lin, sine=lambda p: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, p))))

def kf(keys, t):
    """keys: [(t, value(s), ease_to_this_key)] ; returns interpolated tuple/float."""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0, *_), (t1, v1, *e) in zip(keys[:-1], keys[1:]):
        if t <= t1:
            p = EASE[e[0] if e else "io"]((t - t0) / max(1e-9, t1 - t0))
            if isinstance(v0, (tuple, list)): return tuple(a + (b - a) * p for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * p
    return keys[-1][1]

# ---------------- painter ----------------
class Painter:
    """Draw in world units inside box (x0,y0,x1,y1); output sprite at `res` px/unit, supersampled `ss`."""
    def __init__(self, box, res=1.0, ss=2, bg=(0, 0, 0, 0)):
        self.x0, self.y0, self.x1, self.y1 = box; self.res = res; self.ss = ss; self.k = res * ss
        self.img = Image.new("RGBA", (int((self.x1 - self.x0) * self.k), int((self.y1 - self.y0) * self.k)), bg)
        self.d = ImageDraw.Draw(self.img)
    def P(self, x, y): return ((x - self.x0) * self.k, (y - self.y0) * self.k)
    def pts(self, pts): return [self.P(x, y) for x, y in pts]
    def box(self, b): x0, y0 = self.P(b[0], b[1]); x1, y1 = self.P(b[2], b[3]); return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
    def poly(self, pts, fill): self.d.polygon(self.pts(pts), fill=_c(fill))
    def rect(self, b, fill): self.d.rectangle(self.box(b), fill=_c(fill))
    def rrect(self, b, r, fill): self.d.rounded_rectangle(self.box(b), radius=r * self.k, fill=_c(fill))
    def ell(self, b, fill): self.d.ellipse(self.box(b), fill=_c(fill))
    def circ(self, x, y, r, fill): self.ell((x - r, y - r, x + r, y + r), fill)
    def line(self, pts, fill, w): self.d.line(self.pts(pts), fill=_c(fill), width=max(1, int(w * self.k)), joint="curve")
    def arc(self, b, a0, a1, fill, w): self.d.arc(self.box(b), a0, a1, fill=_c(fill), width=max(1, int(w * self.k)))
    def chord(self, b, a0, a1, fill): self.d.chord(self.box(b), a0, a1, fill=_c(fill))
    def pie(self, b, a0, a1, fill): self.d.pieslice(self.box(b), a0, a1, fill=_c(fill))
    def gpoly(self, pts, top, bot, ya=None, yb=None):
        """polygon filled with vertical gradient (colors RGBA/RGB) between world y ya..yb."""
        ys = [p[1] for p in pts]; ya = min(ys) if ya is None else ya; yb = max(ys) if yb is None else yb
        mask = Image.new("L", self.img.size, 0); ImageDraw.Draw(mask).polygon(self.pts(pts), fill=255)
        g = vgrad_img(self.img.size, self.P(0, ya)[1], self.P(0, yb)[1], _c(top), _c(bot))
        self.img = Image.composite(Image.alpha_composite(self.img, g), self.img, mask); self.d = ImageDraw.Draw(self.img)
    def gfill(self, top, bot):
        self.gpoly([(self.x0, self.y0), (self.x1, self.y0), (self.x1, self.y1), (self.x0, self.y1)], top, bot)
    def glow(self, x, y, r, color, a=1.0, power=2.0):
        """soft radial glow, alpha-over."""
        sz = self.img.size; cx, cy = self.P(x, y); R = r * self.k
        x0, y0, x1, y1 = int(max(0, cx - R)), int(max(0, cy - R)), int(min(sz[0], cx + R)), int(min(sz[1], cy + R))
        if x1 <= x0 or y1 <= y0: return
        yy, xx = np.mgrid[y0:y1, x0:x1]
        al = np.clip(1 - np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / R, 0, 1) ** power * a
        lay = np.zeros((y1 - y0, x1 - x0, 4), np.uint8); lay[..., :3] = color[:3]; lay[..., 3] = (al * 255).astype(np.uint8)
        self.img.alpha_composite(Image.fromarray(lay, "RGBA"), (x0, y0))
    def blur(self, r): self.img = self.img.filter(ImageFilter.GaussianBlur(r * self.k)); self.d = ImageDraw.Draw(self.img)
    def sprite(self, ox=None, oy=None):
        im = self.img.convert("RGBa").resize((max(1, int(self.img.size[0] / self.ss)), max(1, int(self.img.size[1] / self.ss))), Image.LANCZOS).convert("RGBA")
        return Sprite(np.asarray(im).copy(), self.res, self.x0 if ox is None else ox, self.y0 if oy is None else oy)

def _c(c): return tuple(int(v) for v in c) + ((255,) if len(c) == 3 else ())

def vgrad_img(size, ya, yb, top, bot):
    w, h = size; y = np.arange(h)[:, None]
    t = np.clip((y - ya) / max(1, (yb - ya)), 0, 1)[..., None]
    a = np.array(top, np.float32); b = np.array(bot, np.float32)
    g = (a * (1 - t) + b * t).astype(np.uint8)
    return Image.fromarray(np.repeat(g, w, 1), "RGBA")

class Sprite:
    def __init__(self, rgba, res, ox, oy):
        self.a = rgba; self.res = res; self.ox = ox; self.oy = oy
        # premultiplied float for fast compositing
        self.rgb = rgba[..., :3].astype(np.float32) * (rgba[..., 3:4].astype(np.float32) / 255.0)
        self.al = rgba[..., 3].astype(np.float32) / 255.0
        self._half = None
    def half(self):
        if self._half is None:
            hh, ww = self.al.shape
            self._half = (cv2.resize(self.rgb, (max(1, ww // 2), max(1, hh // 2)), interpolation=cv2.INTER_AREA),
                          cv2.resize(self.al, (max(1, ww // 2), max(1, hh // 2)), interpolation=cv2.INTER_AREA))
        return self._half

# ---------------- items & frame compositor ----------------
class Item:
    """sprite placed in world. pos=(dx,dy) offset of sprite origin, scale about anchor (ax,ay) world, rot deg, opacity, parallax, add."""
    def __init__(self, sprite, pos=(0, 0), scale=1.0, rot=0.0, anchor=None, opacity=1.0, par=1.0, add=False):
        self.s, self.pos, self.scale, self.rot, self.anchor, self.op, self.par, self.add = sprite, pos, scale, rot, anchor, opacity, par, add

def cam_matrix(cam, par=1.0, base=(W / 2, H / 2)):
    cx, cy, z = cam
    cx = base[0] + (cx - base[0]) * par; cy = base[1] + (cy - base[1]) * par; z = 1 + (z - 1) * par
    return np.array([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy], [0, 0, 1]], np.float64)

def item_matrix(it, cam):
    s = it.s
    # sprite px -> world
    M = np.array([[1 / s.res, 0, s.ox + it.pos[0]], [0, 1 / s.res, s.oy + it.pos[1]], [0, 0, 1]], np.float64)
    if it.scale != 1.0 or it.rot:
        ax, ay = it.anchor if it.anchor else (s.ox + it.pos[0], s.oy + it.pos[1])
        c, sn = math.cos(math.radians(it.rot)) * it.scale, math.sin(math.radians(it.rot)) * it.scale
        R = np.array([[c, -sn, ax - c * ax + sn * ay], [sn, c, ay - sn * ax - c * ay], [0, 0, 1]])
        M = R @ M
    return cam_matrix(cam, it.par) @ M

def composite(items, cam, out=None):
    out = np.zeros((H, W, 3), np.float32) if out is None else out
    for it in items:
        if it.op <= 0.001: continue
        M = item_matrix(it, cam)
        h, w = it.s.a.shape[:2]
        C = M @ np.array([[0, w, 0, w], [0, 0, h, h], [1, 1, 1, 1]], np.float64)
        x0, x1 = int(max(0, math.floor(C[0].min()) - 1)), int(min(W, math.ceil(C[0].max()) + 1))
        y0, y1 = int(max(0, math.floor(C[1].min()) - 1)), int(min(H, math.ceil(C[1].max()) + 1))
        if x1 <= x0 or y1 <= y0: continue
        Ms = M.copy(); Ms[0, 2] -= x0; Ms[1, 2] -= y0
        z = math.sqrt(abs(np.linalg.det(M[:2, :2])))
        interp = cv2.INTER_AREA if z < 0.7 else cv2.INTER_LINEAR
        src_rgb, src_al = it.s.rgb, it.s.al
        if z < 0.75 and min(h, w) > 8:   # mip level: halve the sprite to avoid aliasing on minification
            src_rgb, src_al = it.s.half()
            Ms = Ms @ np.array([[2, 0, 0.5], [0, 2, 0.5], [0, 0, 1]])
        rgb = cv2.warpAffine(src_rgb, Ms[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        sub = out[y0:y1, x0:x1]
        if it.add:
            sub += rgb * it.op
        else:
            al = cv2.warpAffine(src_al, Ms[:2], (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) * it.op
            sub *= (1 - al[..., None]); sub += rgb * it.op
    return out

def screen_motion(items_fn, t, dt):
    """max pixel displacement of sprite corners between t-dt/2 and t+dt/2 (camera + items)."""
    a_items, a_cam = items_fn(t - dt / 2); b_items, b_cam = items_fn(t + dt / 2)
    best = 0.0
    for ia, ib in zip(a_items, b_items):
        if ia.op <= 0.01 or ia.add: continue
        h, w = ia.s.a.shape[:2]
        C = np.array([[0, 0, 1], [w, 0, 1], [0, h, 1], [w, h, 1], [w / 2, h / 2, 1]], np.float64).T
        pa = (item_matrix(ia, a_cam) @ C)[:2]; pb = (item_matrix(ib, b_cam) @ C)[:2]
        # only count points near the screen
        vis = (pa[0] > -W) & (pa[0] < 2 * W) & (pa[1] > -H) & (pa[1] < 2 * H)
        if vis.any(): best = max(best, float(np.max(np.hypot(*(pa - pb))[vis])))
    return best

def render_frame(items_fn, t, shutter=0.5, max_sub=10):
    """items_fn(t)->(items, cam). Motion-blurred render: shutter = fraction of frame interval."""
    disp = screen_motion(items_fn, t, shutter / FPS)
    n = int(min(max_sub, max(1, math.ceil(disp / 2.5))))
    if n == 1:
        its, cam = items_fn(t); return composite(its, cam)
    acc = np.zeros((H, W, 3), np.float32)
    for i in range(n):
        ts = t + ((i + 0.5) / n - 0.5) * shutter / FPS
        its, cam = items_fn(ts); acc += composite(its, cam)
    return acc / n

# ---------------- post FX ----------------
_vig = None
def vignette(img, k=0.55):
    global _vig
    if _vig is None:
        y, x = np.ogrid[:H, :W]; d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
        _vig = np.clip(1 - k * np.clip(d - 0.45, 0, 1.2) ** 1.4, 0, 1)[..., None].astype(np.float32)
    return img * _vig

_grain = np.random.default_rng(5).normal(0, 1, (8, H // 2, W // 2)).astype(np.float32)
def grain(img, i, amt=2.2):
    g = cv2.resize(_grain[i % 8], (W, H), interpolation=cv2.INTER_LINEAR)
    return img + g[..., None] * amt

# ---------------- captions (Oswald, additive word reveal, red keywords) ----------------
class Captioner:
    def __init__(self, font_path, size=82, y_center=0.675, white=(240, 233, 218), red=(206, 50, 46), max_chars=16):
        self.f = ImageFont.truetype(font_path, size); self.size = size; self.yc = y_center
        self.white, self.red, self.maxc = white, red, max_chars
        self.cache = {}
    def layout(self, chunk):
        lines, cur = [], []
        for w in chunk:
            if cur and len(" ".join(x["txt"] for x in cur + [w])) > self.maxc: lines.append(cur); cur = []
            cur.append(w)
        if cur: lines.append(cur)
        return lines
    def render(self, chunk, n_shown, alpha=1.0):
        key = (id(chunk), n_shown)
        if key not in self.cache:
            lines = self.layout(chunk); lh = int(self.size * 0.98)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
            shadow = Image.new("L", (W, H), 0); ds = ImageDraw.Draw(shadow)
            y = int(H * self.yc - lh * len(lines) / 2); k = 0
            for ln in lines:
                full = " ".join(w["txt"] for w in ln); x = (W - d.textlength(full, font=self.f)) / 2
                for w in ln:
                    if k >= n_shown: break
                    d.text((x, y), w["txt"], font=self.f, fill=(self.red if w["red"] else self.white) + (255,), stroke_width=3, stroke_fill=(12, 8, 8, 255))
                    ds.text((x, y + 3), w["txt"], font=self.f, fill=200)
                    x += d.textlength(w["txt"] + " ", font=self.f); k += 1
                y += lh
            sh = shadow.filter(ImageFilter.GaussianBlur(7))
            a = np.asarray(layer).astype(np.float32) / 255; s = np.asarray(sh).astype(np.float32)[..., None] / 255
            self.cache[key] = (a[..., :3] * 255, a[..., 3:4], s * 0.85)
        rgb, al, sh = self.cache[key]
        return rgb, al * alpha, sh * alpha
    def apply(self, img, chunk, n_shown, alpha=1.0):
        rgb, al, sh = self.render(chunk, n_shown, alpha)
        img = img * (1 - sh)
        return img * (1 - al) + rgb * al
