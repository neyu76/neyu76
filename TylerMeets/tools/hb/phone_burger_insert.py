"""Phone insert for TM04: Bryce's own post of a burger "in Miami" (fictional app UI, no real brands/logos).
python tools/hb/phone_burger_insert.py <background.png> <out.png>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
G, O = sys.argv[1], sys.argv[2]
W, H = 1080, 1920
def _f(c, s):
    for p in c:
        if os.path.exists(p): return ImageFont.truetype(p, s)
B = lambda s: _f(["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"], s)
F = lambda s: _f(["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "C:/Windows/Fonts/arial.ttf"], s)
bg = Image.open(G).convert("RGB").resize((W, H)).filter(ImageFilter.GaussianBlur(18))
bg = Image.blend(bg, Image.new("RGB", (W, H), (20, 22, 28)), 0.5)
d = ImageDraw.Draw(bg)
PX, PY, PW, PH = 150, 170, 780, 1580
d.rounded_rectangle((PX - 18, PY - 18, PX + PW + 18, PY + PH + 18), 70, fill=(18, 18, 20))
scr = Image.new("RGB", (PW, PH), (250, 250, 250)); s = ImageDraw.Draw(scr)
s.text((40, 22), "12:07", font=B(34), fill=(20, 20, 20)); s.text((PW - 150, 22), "5G  64%", font=B(30), fill=(20, 20, 20))
s.text((40, 90), "pixpost", font=B(46), fill=(20, 20, 20))
# post header
y = 180
s.ellipse((30, y, 120, y + 90), fill=(31, 79, 209)); s.text((54, y + 22), "BR", font=B(38), fill="white")
s.text((140, y + 8), "bryce.100real", font=B(38), fill=(20, 20, 20)); s.text((140, y + 52), "Miami, FL  -  Yesterday", font=F(30), fill=(110, 110, 120))
# photo: a beach-sunset backdrop + a big burger on a plate
ph = Image.new("RGB", (PW, 760), (255, 170, 90)); p = ImageDraw.Draw(ph)
for k in range(380): p.line((0, k, PW, k), fill=(255, 140 + k // 6, 90 + k // 5))
p.rectangle((0, 380, PW, 470), fill=(60, 170, 200)); p.rectangle((0, 470, PW, 760), fill=(240, 214, 160))
p.ellipse((520, 120, 680, 280), fill=(255, 230, 120))
for x0 in (60, 640):   # palm trees
    p.rectangle((x0 + 30, 170, x0 + 50, 470), fill=(120, 80, 40))
    for dx, dy in ((-90, -20), (90, -20), (-60, 30), (60, 30)): p.polygon([(x0 + 40, 170), (x0 + 40 + dx, 170 + dy), (x0 + 40 + dx * 0.6, 170 + dy + 30)], fill=(40, 140, 60))
p.ellipse((150, 560, 630, 700), fill=(250, 250, 250))
cx = 390
p.ellipse((cx - 190, 380, cx + 190, 520), fill=(214, 140, 60))                       # top bun
for k in range(9): p.ellipse((cx - 140 + k * 33, 410 + (k % 2) * 18, cx - 132 + k * 33, 418 + (k % 2) * 18), fill=(250, 235, 200))   # sesame
p.rectangle((cx - 200, 490, cx + 200, 515), fill=(80, 170, 60))                        # lettuce
p.rectangle((cx - 195, 512, cx + 195, 535), fill=(245, 200, 40))                       # cheese
p.rounded_rectangle((cx - 190, 532, cx + 190, 585), 20, fill=(110, 60, 35))           # patty
p.rounded_rectangle((cx - 185, 582, cx + 185, 640), 26, fill=(214, 140, 60))          # bottom bun
scr.paste(ph, (0, y + 120))
y2 = y + 120 + 760 + 24
s.text((40, y2), "2 likes", font=B(36), fill=(20, 20, 20))
s.text((40, y2 + 56), "bryce.100real", font=B(34), fill=(20, 20, 20)); s.text((300, y2 + 58), "miami vibes. best burger", font=F(34), fill=(20, 20, 20))
s.text((40, y2 + 100), "of my life. no filter.", font=F(34), fill=(20, 20, 20))
s.text((40, y2 + 170), "View 1 comment", font=F(32), fill=(120, 120, 130))
s.text((40, y2 + 214), "mom: who took you to miami??", font=F(32), fill=(60, 60, 70))
s.text((40, y2 + 270), "1 day ago", font=F(28), fill=(150, 150, 160))
mask = Image.new("L", (PW, PH), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, PW, PH), 56, fill=255)
bg.paste(scr, (PX, PY), mask)
bg.save(O); print("ok", O)
