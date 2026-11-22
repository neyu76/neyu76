"""Prints + set textures for TM04 (Bryce, the habitual liar). Original art only, no real brands.
Linux fonts (Liberation Sans = Arial metrics, Montserrat Black for poster weight); falls back to Windows fonts.
python tools/hb/make_tex_tm04.py"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEX, PR = os.path.join(ROOT, "assets/hb/tex"), os.path.join(ROOT, "assets/hb/prints")

def _font(cands, s):
    for c in cands:
        if os.path.exists(c): return ImageFont.truetype(c, s)
    raise SystemExit(f"no font among {cands}")
B = lambda s: _font(["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"], s)
K = lambda s: _font(["/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf", "C:/Windows/Fonts/impact.ttf"], s)
HW = lambda s: _font(["/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf", "C:/Windows/Fonts/arialbi.ttf"], s)

def centered(d, y, txt, f, fill, W):
    w = d.textlength(txt, font=f); d.text(((W - w) / 2, y), txt, font=f, fill=fill)

def sign(name, size, bg, lines, fg="#111111", border=None, font=B):
    im = Image.new("RGB", size, bg); d = ImageDraw.Draw(im); W, H = size
    if border: d.rectangle((8, 8, W - 9, H - 9), outline=border, width=10)
    tot = sum(s for _, s in lines) * 1.15; y = (H - tot) / 2
    for t, s in lines: centered(d, y, t, font(s), fg, W); y += s * 1.15
    im.save(os.path.join(TEX, name))

# Bryce's tee print: "100% REAL" with a fake gold seal
im = Image.new("RGBA", (512, 512), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.ellipse((186, 40, 326, 180), fill=(212, 160, 23, 255), outline=(20, 20, 24, 255), width=6)
centered(d, 82, "100%", B(40), (20, 20, 24, 255), 512); centered(d, 124, "LEGIT", B(26), (20, 20, 24, 255), 512)
centered(d, 220, "100%", K(118), (20, 20, 24, 255), 512); centered(d, 350, "REAL", K(118), (20, 20, 24, 255), 512)
im.save(os.path.join(PR, "bry_real.png"))

# props / signs
sign("tm04_math_slip.png", (420, 560), "#ffffff", [("MATH HOMEWORK", 44), ("Name: BRYCE", 40), ("Day: MON", 40), ("Period 4", 34), ("1) 3x + 4 = 19", 30), ("x = 5", 30)],
     fg="#1b2a4a", border="#7fa7d9")
sign("tm04_period2.png", (1100, 300), "#ffffff", [("PERIOD 2 - MUSIC", 110), ("Recorder test today!", 56)], fg="#1f4e8c")
sign("tm04_music_poster.png", (420, 600), "#f7d046", [("PRACTICE", 70), ("MAKES", 70), ("PROGRESS", 62), ("(not noise)", 40)], fg="#2b2b2b", border="#2b2b2b")
sign("tm04_store_sign.png", (1100, 240), "#7a1f2b", [("WILDCATS SCHOOL STORE", 86), ("cash or card  -  no IOUs", 44)], fg="#ffd23f")
sign("tm04_prices.png", (520, 700), "#1d2b24", [("PRICES", 70), ("Chips ..... $1", 48), ("Water ..... $1", 48), ("Juice ...... $2", 48), ("Hoodie ... $25", 48), ("Pencil ... 50c", 48)],
     fg="#f4f4f4", border="#c9a24a")
sign("tm04_shirt_wb.png", (400, 420), "#1f3a68", [("WEST", 96), ("BROOK", 96)], fg="#ffd23f", font=K)
sign("tm04_fair_banner.png", (1400, 300), "#14284b", [("WESTBROOK SCIENCE FAIR", 104), ("judging at 3:30", 56)], fg="#ffd23f")
sign("tm04_japan.png", (360, 150), "#ffffff", [("MADE IN", 52), ("JAPAN", 64)], fg="#c0392b", border="#c0392b")
sign("tm04_ribbon.png", (300, 420), "#1f5fd1", [("1st", 120), ("PLACE", 70)], fg="#ffd23f", border="#ffd23f")
sign("tm04_detention.png", (700, 420), "#ffc2d6", [("DETENTION", 110), ("Name: TYLER", 56), ("Reason: \"lying to a judge\"", 42)], fg="#8b1a1a", border="#8b1a1a")
sign("tm04_judge.png", (300, 140), "#ffffff", [("JUDGE", 90)], fg="#14284b", border="#14284b")
sign("tm04_court_rules.png", (600, 400), "#ffffff", [("COURT RULES", 70), ("no hanging on rims", 44), ("no glass", 44), ("have fun", 44)], fg="#2c3e50", border="#c0392b")
for k, (bg, t1, t2) in enumerate((("#e8f6ef", "PLANT", "GROWTH"), ("#fdf0d5", "SOLAR", "OVENS"), ("#e8eefc", "MAGNETS", "& YOU"))):
    sign(f"tm04_tri{k}.png", (600, 420), bg, [(t1, 96), (t2, 96), ("hypothesis • results", 34)], fg="#1b2a4a", border="#1b2a4a")

# Tyler's lie detector label: hand-written look
im = Image.new("RGB", (600, 200), "#c8a06a"); d = ImageDraw.Draw(im)
d.text((36, 52), "LIE DETECTOR", font=HW(68), fill="#1b1b1b"); d.line((40, 150, 560, 156), fill="#1b1b1b", width=8)
im.save(os.path.join(TEX, "tm04_liedetector.png"))
print("ok")
