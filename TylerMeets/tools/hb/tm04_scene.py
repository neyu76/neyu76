"""TM04 — Bryce, the habitual liar. 4 sets: outdoor basketball court, music room, school store, science fair.
Usage: blender -b --python tools/hb/tm04_scene.py -- <timeline.json> <out_dir> [--stills] [--check] [--only K,K] [--res WxH] [--samples N]"""
import bpy, sys, os, json, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, hb_lib, hb_props, hb_sets2, hb_sets4, hb_sets5, hb_sets6
for m_ in (hb_lib, hb_props, hb_sets2, hb_sets4, hb_sets5, hb_sets6): importlib.reload(m_)
from hb_lib import *
from hb_props import phone, tex_quad
from hb_sets2 import idle, breathe
from hb_sets4 import _cyl, _sph
from hb_sets6 import court, music_room, school_store, science_fair
hb_lib.SKIP_WORDS = hb_lib.SKIP_WORDS + ("ct_ground", "ct_asphalt", "ct_paint", "ct_key", "ct_line", "ct_ft", "mu_fx", "st_fx", "st_fy", "sf_fx", "_wrapper", "_slip", "ribbon", "rec_", "ct_ball")

argv = sys.argv[sys.argv.index("--") + 1:]
TL, OUT = os.path.abspath(argv[0]), os.path.abspath(argv[1]); STILLS = "--stills" in argv; CHECK = "--check" in argv
ONLY = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
RES = tuple(int(v) for v in argv[argv.index("--res") + 1].split("x")) if "--res" in argv else (1080, 1920)
SAMPLES = int(argv[argv.index("--samples") + 1]) if "--samples" in argv else 64
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); P = lambda p: os.path.join(ROOT, p)
FPS = 30
bpy.ops.wm.read_factory_settings(use_empty=True); render_setup(samples=SAMPLES)
CT, MU, ST, SF = 390, 420, 450, 480
ct = court((CT, 0, 0)); mu = music_room((MU, 0, 0)); st = school_store((ST, 0, 0)); sf = science_fair((SF, 0, 0)); lights((0, 0, 0))
SUN = bpy.data.objects["sun"]
FILLS = {}
for nm, loc, en, sz in (("fill_ct", (CT, -1.0, 4.0), 0, 6), ("fill_mu", (MU, -1.0, 3.2), 650, 6), ("fill_st", (ST, -1.0, 3.0), 420, 5),
                        ("fill_sf", (SF, -1.0, 3.4), 650, 7)):
    L = bpy.data.lights.new(nm, "AREA"); L.energy = en; L.size = sz; fo = bpy.data.objects.new(nm, L); bpy.context.scene.collection.objects.link(fo); fo.location = loc; FILLS[nm] = L

MK = lambda name, **kw: Char(name, **kw)
tyler = MK("ME", skin="f1c7a0", shirt="ffd23f", pants="3a3f47", shoes="f4f4f4", hair="1e1a18", hair_style="messy", print_img=P("assets/hb/prints/me_paused.png"))
lunchbox = box("ME_lunchbox", (0.26, 0.1, 0.2), (0, -0.04, -0.36), mat("lunchbox", srgb("2e86de"), 0.5), tyler.j["el_L"], 0.02, 2)
cash = box("ME_cash", (0.12, 0.02, 0.06), (0, -0.07, -0.37), mat("cash", srgb("6fbf73"), 0.7), tyler.j["el_R"])
clipb = box("ME_clipboard", (0.24, 0.015, 0.32), (0, -0.08, -0.36), mat("clipboard", srgb("b07a4a"), 0.6), tyler.j["el_L"])
box("ME_clippaper", (0.2, 0.004, 0.26), (0, -0.089, -0.37), mat("paper", srgb("f8f8f2"), 0.9), tyler.j["el_L"])
wrapper_h = box("ME_wrapper", (0.2, 0.02, 0.16), (0, -0.08, -0.37), mat("wrapper", srgb("f2efe6"), 0.9), tyler.j["el_R"])
box("ME_wrapsauce", (0.08, 0.022, 0.03), (0.03, -0.08, -0.33), mat("sauce", srgb("d9534f"), 0.6), tyler.j["el_R"])
# Bryce: snapback (worn forward), cobalt open jacket over the "100% REAL" tee, gold plastic watch, homework slip
bry = MK("BRY", skin="c68e5f", shirt="f4f4f4", pants="1b1b22", shoes="f4f4f4", hair="2a1a12", hair_style="buzz", print_img=P("assets/hb/prints/bry_real.png"),
         jacket="1f4fd1", sleeves="1f4fd1", long_sleeves=True, mood="smug")
CAP = mat("bry_cap", srgb("8b1e2d"), 0.6)
_sph("BRY_capdome", 0.268, (0, 0.03, 0.43), CAP, 16, 10, bry.j["head"], (1.0, 1.0, 0.62))
box("BRY_capbrim", (0.34, 0.24, 0.025), (0, -0.25, 0.43), CAP, bry.j["head"], 0.01, 1)
box("BRY_capbutton", (0.04, 0.04, 0.03), (0, 0.03, 0.6), CAP, bry.j["head"])
box("BRY_watch", (0.1, 0.1, 0.05), (0, 0, -0.27), mat("gold", srgb("d4a017"), 0.25), bry.j["el_L"])
slip = tex_quad("BRY_slip", 0.16, 0.21, "tm04_math_slip.png", (0, -80, 0), (R(90), 0, 0))
rec_h = _cyl("BRY_rec_hand", 0.018, 0.32, (0, -0.06, -0.38), mat("recorder", srgb("efe4c8"), 0.5), (0, 0, 0), 12, bry.j["el_R"])
rec_m = _cyl("BRY_rec_mouth", 0.018, 0.32, (0, -0.37, 0.1), mat("recorder", srgb("efe4c8"), 0.5), (R(-62), 0, 0), 12, bry.j["head"])
ribbon = tex_quad("BRY_ribbon", 0.12, 0.17, "tm04_ribbon.png", (-0.17, -0.168, 0.36), (R(90), 0, 0)); ribbon.parent = bry.j["chest"]
teach = MK("TEACH", skin="e8b896", shirt="f3e5d8", pants="34495e", shoes="5a3a22", hair="7a4a2e", hair_style="bun", jacket="6a8f5a", sleeves="6a8f5a",
           long_sleeves=True, glasses=True, female=True, mood="happy", build=1.02)
rec_t = _cyl("TEACH_rec", 0.018, 0.32, (0, -0.06, -0.38), mat("recorder", srgb("efe4c8"), 0.5), (R(80), 0, 0), 12, teach.j["el_R"])
harg = MK("HARG", skin="c98c63", shirt="f4f4f4", pants="2c3e50", shoes="222222", hair="5a4a3e", hair_style="bald", tie="ffd23f", jacket="2c3e50", sleeves="2c3e50",
          long_sleeves=True, glasses=True, mustache="3a2a1e", build=1.15, mood="deadpan")
for k in range(3): box(f"HARG_duck{k}", (0.03, 0.022, 0.03), (0, -0.155, 0.44 - k * 0.1), mat("duck", srgb("f39c12"), 0.5), harg.j["chest"])
badge = tex_quad("HARG_badge", 0.13, 0.06, "tm04_judge.png", (0.13, -0.153, 0.42), (R(90), 0, 0)); badge.parent = harg.j["chest"]
hclip = box("HARG_clipboard", (0.24, 0.015, 0.32), (0, -0.08, -0.36), mat("clipboard", srgb("b07a4a"), 0.6), harg.j["el_L"])
LOOKS = [("c98c63", "3f7fd1", "2a3550", "5a3a22", "messy", False), ("f0c9a4", "e85d9c", "4a4a4a", "c9a24a", "ponytail", True), ("8d5a3b", "e67e22", "2a2a2a", "141414", "buzz", False),
         ("f3d2b5", "9b59b6", "34495e", "d1a06a", "messy", False), ("6e4430", "16a085", "283040", "121212", "bun", True), ("e8b896", "e74c3c", "2c3e50", "8a5a33", "buzz", False),
         ("b07a55", "7f8c8d", "3d3d4a", "2a1a12", "waves", False), ("f6d0b0", "2980b9", "5d6d7e", "e0c068", "ponytail", True), ("a86a45", "f1c40f", "2c3e50", "1a120c", "messy", False),
         ("f0c9a4", "1abc9c", "4a4a4a", "6b4a2f", "bun", True), ("7a4a2e", "c0392b", "283040", "141414", "buzz", False), ("e8b896", "34495e", "6f8fb8", "c9a24a", "messy", False)]
ext = [MK(f"X{i}", skin=s, shirt=sh, pants=pa, shoes="eeeeee", hair=ha, hair_style=stl, female=fe, build=0.94 if fe else 1.0)
       for i, (s, sh, pa, ha, stl, fe) in enumerate(LOOKS)]
# Tyler's sandwich (full + bitten), wrapper on the counter, crumbs, detention slip on the table
SWL = [("tsw_b1", (0.19, 0.15, 0.035), -0.05, "toast", "c98a3e"), ("tsw_let", (0.22, 0.17, 0.012), -0.026, "lettuce", "4fae3a"),
       ("tsw_ham", (0.21, 0.15, 0.016), -0.01, "ham", "e9738a"), ("tsw_ch", (0.2, 0.17, 0.008), 0.004, "cheese", "f5c518"), ("tsw_b2", (0.19, 0.15, 0.035), 0.028, "toast", "c98a3e")]
SW = empty("tyler_sandwich", (0, -80, 0))
for nm, sz, dz, mn, c in SWL: box(nm, sz, (0, 0, dz), mat(mn, srgb(c), 0.8), SW, 0.006, 2)
SWB = empty("tyler_sandwich_bitten", (0, -80, 0))
for nm, sz, dz, mn, c in SWL: box(nm + "_b", (sz[0] * 0.55, sz[1], sz[2]), (-sz[0] * 0.2, 0, dz), mat(mn, srgb(c), 0.8), SWB, 0.006, 2)
wrap_t = box("tsw_wrapper", (0.34, 0.3, 0.008), (0, -80, 0), mat("wrapper", srgb("f2efe6"), 0.9))
stub = box("tsw_stub", (0.06, 0.05, 0.04), (0, -80, 0), mat("toast", srgb("c98a3e"), 0.8))
crumbs = [box(f"tsw_crumb{k}", (0.025, 0.02, 0.012), (0, -80, 0), mat("toast", srgb("c98a3e"), 0.8)) for k in range(7)]
dslip = tex_quad("table_slip", 0.34, 0.2, "tm04_detention.png", (0, -80, 0), (0, 0, 0))
BALL = ct["ball"]
cam, tgt = camera("cam", 28); bpy.context.scene.camera = cam
ALL = list(bpy.data.objects); REST = {o.name: (tuple(o.location), tuple(o.rotation_euler), tuple(o.scale)) for o in ALL}
EVERYONE = [tyler, bry, teach, harg] + ext
PROPS = [lunchbox, cash, clipb, bpy.data.objects["ME_clippaper"], wrapper_h, bpy.data.objects["ME_wrapsauce"], slip, rec_h, rec_m, ribbon, rec_t, hclip,
         wrap_t, stub, dslip] + crumbs
def show(objs, on, f=1):
    for o in objs: o.hide_render = not on; o.keyframe_insert("hide_render", frame=f)
EMIT = {m.name: m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value for m in bpy.data.materials if m.node_tree and "Principled BSDF" in m.node_tree.nodes}
def reset():
    for m in bpy.data.materials:
        if m.node_tree and m.name in EMIT:
            m.node_tree.animation_data_clear(); m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = EMIT[m.name]
    for o in ALL:
        o.animation_data_clear(); l, r, s = REST[o.name]; o.location, o.rotation_euler, o.scale = l, r, s; o.hide_render = False
    cam.data.animation_data_clear()
OFF = lambda c: c.place(1, 0, -80, 0, 0)
W = bpy.context.scene.world.node_tree.nodes["Background"]
def world(kind):
    if kind == "out":
        W.inputs[0].default_value = (0.42, 0.62, 0.92, 1); W.inputs[1].default_value = 0.75; SUN.data.energy = 4.8
    else:
        W.inputs[0].default_value = (0.85, 0.82, 0.78, 1); W.inputs[1].default_value = 0.55; SUN.data.energy = 4.5
def all_off(kind="in"):
    for c in EVERYONE: OFF(c)
    show(PROPS, False); SW.location = (0, -80, 0); SWB.location = (0, -80, 0); BALL.location = (0, -80, 0); world(kind)
    for k in FILLS: FILLS[k].energy = 0
def bake_to(obj, char, joint, f0, f1, off=(0, 0, 0.05), rot=None):
    sc = bpy.context.scene
    for f in range(f0, f1 + 1):
        sc.frame_set(f); h = char.j[joint].matrix_world.translation
        obj.location = (h.x + off[0], h.y + off[1], h.z + off[2]); obj.keyframe_insert("location", frame=f)
        if rot: obj.rotation_euler = rot; obj.keyframe_insert("rotation_euler", frame=f)
def put(obj, loc, f=1, rot=None):
    obj.location = loc; obj.keyframe_insert("location", frame=f)
    if rot is not None: obj.rotation_euler = rot; obj.keyframe_insert("rotation_euler", frame=f)
def run(c, f0, f1, p0, p1):
    c.walk(f0, f1, p0, p1, step=5)
    for f in range(f0, f1 + 1, 5): c.rot("chest", f, 10, 0, 0)
def flash(obj, n, every=6, on=7.0, phase=0):
    m = obj.data.materials[0]; e = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    for f in range(1, n + 1, every):
        e.default_value = on if (f // every + phase) % 2 == 0 else 0.0; e.keyframe_insert("default_value", frame=f)
def glow(obj, val, f=1):
    e = obj.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]; e.default_value = val; e.keyframe_insert("default_value", frame=f)
def chew(c, n, every=6, f0=1):
    for f in range(f0, n + 1, every):
        c.mouth.scale = (1.1, 1, 1.7 if (f // every) % 2 else 0.7); c.mouth.keyframe_insert("scale", frame=f)
def sit_at(c, x, y, yaw, z=0.0, f=1, arms=False):
    c.place(f, x, y, -0.34 + z, yaw); c.sit(f, arms_on_desk=arms)
def headpos(c, f=1, dz=0.27):
    bpy.context.scene.frame_set(f); h = c.j["head"].matrix_world.translation; return (h.x, h.y, h.z + dz)
def yaw_to(a, b):
    return math.degrees(math.atan2(b[0] - a[0], -(b[1] - a[1])))
def fcam(n, c, yaw, dist, side=0.0, dz=0.0, lens=32, ldz=-0.1, f=1, zoom=0.95, look_side=0.0):
    """camera in FRONT of character c (facing `yaw`): dist along the face vector, side along its right, slow push-in."""
    if dist < 1.5: dist *= 1.32; side *= 1.32   # match the reference CU framing (head + shoulders)
    hx, hy, hz = headpos(c, f); fx, fy = math.sin(R(yaw)), -math.cos(R(yaw)); rx, ry = -fy, fx
    lk = (hx + rx * look_side, hy + ry * look_side, hz + ldz)
    p = lambda d: (hx + fx * d + rx * side, hy + fy * d + ry * side, hz + dz)
    cam_key(cam, tgt, 1, p(dist), lk, lens); cam_key(cam, tgt, n, p(dist * zoom), lk, lens)
def still_cam(n, p, l, lens, p1=None, l1=None):
    cam_key(cam, tgt, 1, p, l, lens); cam_key(cam, tgt, n, p1 or p, l1 or l, lens)
def shoot_loop(c, n, seed=0):   # shooting-practice arm motion for background players
    rnd = random.Random(seed); f = rnd.randint(1, 20)
    while f < n:
        c.pose(f, sh_L=(-30, 0, 10), sh_R=(-30, 0, -10), el_L=(-90, 0, 0), el_R=(-90, 0, 0), kn_L=(15, 0, 0), kn_R=(15, 0, 0))
        c.pose(f + 10, sh_L=(-165, 0, 10), sh_R=(-165, 0, -10), el_L=(-15, 0, 0), el_R=(-15, 0, 0), kn_L=(0, 0, 0), kn_R=(0, 0, 0))
        f += rnd.randint(38, 55)
    breathe(c, 1, n, 1.2, 70, seed)

# ---------------------------------------------------------------- 1 BASKETBALL COURT (morning)
TX, TY = CT - 1.1, -0.2          # Tyler near the top of the key, lunchbox under his arm
BX, BY = CT + 0.15, -0.35        # where Bryce skids to a stop, facing Tyler
TYAW, BYAW = yaw_to((TX, TY), (BX, BY)) + 35, yaw_to((BX, BY), (TX, TY)) - 35
def scene_ct(n, bry_at=True):
    all_off("out")
    tyler.place(1, TX, TY, 0, TYAW); tyler.stand(1); tyler.pose(1, sh_L=(-15, 0, 18), el_L=(-80, 0, 0)); show([lunchbox], True)
    tyler.expr("deadpan", 1); breathe(tyler, 1, n, 1.0, 96, 1)
    if bry_at: bry.place(1, BX, BY, 0, BYAW); bry.stand(1); bry.expr("smug", 1); breathe(bry, 1, n, 1.4, 60, 2)
    for i, (x, y, yaw) in enumerate(((CT + 1.7, 3.3, 200), (CT - 1.9, 3.0, 160))):
        ext[i].place(1, x, y, 0, yaw); ext[i].stand(1); shoot_loop(ext[i], n, 30 + i)
    bx, by = ct["bench"]; sit_at(ext[2], bx - 0.4, by, 0); ext[2].pose(1, chest=(35, 0, 0), sh_L=(-70, 0, 0), sh_R=(-70, 0, 0), el_L=(-20, 0, 0), el_R=(-20, 0, 0))
    for f in range(1, n, 20): ext[2].rot("head", f, 25, 0, 8 if (f // 20) % 2 else -8)   # tying a shoelace
    ext[3].walk(1, n, (CT + 6.0, 1.5, 0), (CT + 6.0 - 1.1 * n / 30, 1.5, 0)); ext[3].expr("happy", 1)
    ext[4].place(1, CT - 6.2, 2.4, 0, 120); ext[4].stand(1); idle(ext[4], 1, n, "phone", 34)
def hold_slip(n, yaw=None, f=1):
    show([slip], True); bry.pose(f, sh_R=(-70, 0, -15), el_R=(-55, 0, 0))
    yw = BYAW if yaw is None else yaw
    bake_to(slip, bry, "hand_R", 1, n, (0, 0, 0.14), (R(90), 0, R(yw)))
def OPEN_BRY_RUN(n):
    scene_ct(n, bry_at=False); bry.pose(1, sh_R=(-70, 0, -15), el_R=(-55, 0, 0))
    run(bry, 1, n - 10, (CT - 5.2, BY - 0.2, 0), (BX, BY, 0)); bry.place(n - 6, BX, BY, 0, BYAW); bry.stand(n - 6); bry.expr("happy", 1)
    for f in range(1, n - 10, 6): bry.rot("sh_R", f, -150 if (f // 6) % 2 else -120, 0, -20)   # waving the homework slip
    show([slip], True); bake_to(slip, bry, "hand_R", 1, n, (0, 0, 0.14), (R(90), 0, R(90)))
    bry.pose(n - 6, chest=(-12, 0, 0), sh_R=(-140, 0, -20), el_R=(-30, 0, 0), sh_L=(-40, 0, 25)); bry.pose(n, chest=(-4, 0, 0)); bry.expr("yell", n - 8)
    tyler.expr("shock", n - 8)
    still_cam(n, (CT - 2.6, -3.9, 1.5), (CT - 4.0, BY, 1.2), 24, (CT - 2.4, -3.8, 1.5), (BX - 0.5, BY, 1.25))
def CU_BRY_HYPE(n):
    scene_ct(n); bry.expr("yell", 1); bry.expr("happy", n // 2); bry.expr("yell", n - 16)
    for k, f in enumerate(range(1, n, 8)):
        a = 10 if k % 2 else -10
        bry.pose(f, sh_R=(-150, 0, -25), el_R=(-25, 0, 0), chest=(-4, 0, a * 0.5), head=(0, 0, a * 0.4)); bry.loc(f, BX, BY, 0.04 if k % 2 else 0.0)
    show([slip], True); bake_to(slip, bry, "hand_R", 1, n, (0, 0, 0.14), (R(90), 0, R(BYAW)))
    fcam(n, bry, BYAW, 0.95, 0.2, -0.05, 30, -0.12)
def CU_ME_WTF(n):
    scene_ct(n); tyler.expr("deadpan", 1); tyler.blink(n // 2); tyler.rot("head", 1, 0, 0, -10)
    fcam(n, tyler, TYAW, 0.9, 0.25, -0.03, 34, -0.08)
def WIDE_COURT_BRY(n):
    scene_ct(n); bry.expr("happy", 1)
    for k, f in enumerate(range(1, n, 14)): bry.pose(f, sh_L=(-60 - 30 * (k % 2), 0, 40), sh_R=(-90 + 30 * (k % 2), 0, -40), el_L=(-20, 0, 0), el_R=(-20, 0, 0))
    still_cam(n, (CT + 2.4, -5.6, 2.3), (CT - 0.3, 1.6, 1.5), 20, (CT + 2.2, -5.3, 2.25))
def MS_BRY_GRIN(n):
    scene_ct(n); bry.expr("smug", 1); bry.blink(n // 2)
    bry.pose(1, sh_R=(-160, 0, -10), el_R=(-110, 0, 0)); bry.pose(n // 2, sh_R=(-150, 0, -15), el_R=(-100, 0, 0))   # adjusts the cap
    fcam(n, bry, BYAW, 1.9, 0.35, -0.25, 28, -0.45)
def INS_SLIP_DATE(n):
    scene_ct(n); bry.pose(1, sh_R=(-80, 0, -10), el_R=(-40, 0, 0)); bry.expr("smug", 1); hold_slip(n); bry.pose(1, sh_R=(-80, 0, -10), el_R=(-40, 0, 0))
    bpy.context.scene.frame_set(1); h = slip.matrix_world.translation.copy()
    fx, fy = math.sin(R(BYAW)), -math.cos(R(BYAW))
    still_cam(n, (h.x + fx * 0.62, h.y + fy * 0.62, h.z + 0.1), (h.x, h.y, h.z), 38, (h.x + fx * 0.58, h.y + fy * 0.58, h.z + 0.1))
def MS_BRY_BALL(n):
    scene_ct(n); bry.expr("smug", 1); bry.pose(1, sh_L=(-25, 0, 25), el_L=(-70, 0, 0), sh_R=(-165, 0, -10), el_R=(-5, 0, 0))   # ball tucked, two fingers up
    bry.pose(1, sh_L=(-35, 0, 15), el_L=(-70, 0, 0)); bake_to(BALL, bry, "hand_L", 1, n, (0, 0, 0.02))
    fcam(n, bry, BYAW, 2.0, 0.3, -0.2, 28, -0.4)
JX, JY = CT, 3.55
def WIDE_BRY_JUMP(n):
    scene_ct(n, bry_at=False); j = int(n * 0.62)
    run(bry, 1, j - 4, (CT - 0.2, 0.4, 0), (JX, JY, 0)); bry.expr("focused", 1)
    bry.place(j, JX, JY + 0.1, 0.5, 180); bry.pose(j, sh_L=(-170, 0, 10), sh_R=(-170, 0, -10), el_L=(-5, 0, 0), el_R=(-5, 0, 0), kn_L=(30, 0, 0), kn_R=(30, 0, 0))
    bry.place(n, JX, JY + 0.15, 0.0, 180); bry.stand(n)
    bake_to(BALL, bry, "hand_R", 1, j - 1, (0, 0, 0.05))
    rx, ry, rz = ct["rim"]; put(BALL, (rx + 0.05, ry - 0.25, rz - 0.15), n)
    still_cam(n, (CT + 4.4, 1.2, 1.8), (CT, 3.6, 2.0), 22, (CT + 4.2, 1.3, 1.8))
def CU_BRY_BALLFACE(n):
    scene_ct(n, bry_at=False); bry.place(1, JX, JY + 0.15, 0, 180); bry.stand(1); bry.expr("focused", 1); bry.rot("head", 1, -22, 0, 0)
    hit = max(6, int(n * 0.35)); hx, hy, hz = headpos(bry, 1)
    rx, ry, rz = ct["rim"]; put(BALL, (rx, ry - 0.2, rz - 0.1), 1); put(BALL, (hx, hy + 0.32, hz - 0.05), hit)
    put(BALL, (hx + 0.9, hy + 0.9, 0.12), n)
    bry.rot("head", hit, -40, 0, 0); bry.expr("shock", hit); bry.pose(hit + 3, chest=(-14, 0, 0), sh_L=(-60, 0, 40), sh_R=(-60, 0, -40)); bry.loc(hit + 3, JX, JY + 0.3, 0)
    bry.rot("head", n, -10, 0, 12); bry.expr("annoyed", n - 4)
    hx, hy, hz = headpos(bry, 1)
    still_cam(n, (hx + 0.55, hy + 1.25, hz + 0.05), (hx, hy, hz - 0.05), 30, (hx + 0.52, hy + 1.18, hz + 0.05))

# ---------------------------------------------------------------- 2 MUSIC ROOM (2nd period)
RZ = mu["risers"]
BRS = RZ[(0, 0)]; TYS = RZ[(0, 1)]           # Bryce row 0 centre, Tyler next to him (+X)
TEX, TEY = MU + 2.4, -1.0                     # teacher's spot by the piano side
def scene_mu(n):
    all_off("in"); FILLS["fill_mu"].energy = 650
    sit_at(bry, BRS[0], BRS[1] + 0.12, 0, BRS[2]); bry.expr("smug", 1); breathe(bry, 1, n, 1.2, 70, 5)
    sit_at(tyler, TYS[0], TYS[1] + 0.12, 0, TYS[2]); tyler.expr("deadpan", 1); breathe(tyler, 1, n, 1.0, 96, 1)
    seats = [(0, -2), (0, -3), (0, 2), (1, -2), (2, 0), (1, 1), (1, 3), (2, -1), (2, 1), (2, 2)]
    for i, rc in enumerate(seats):
        x, y, h = RZ[rc]; sit_at(ext[i], x, y + 0.12, 0, h); idle(ext[i], 1, n, ("talk", "look", "phone", "look", "talk", "laugh", "look", "phone", "talk", "look")[i], 300 + i)
    teach.place(1, TEX, TEY, 0, yaw_to((TEX, TEY), (BRS[0], BRS[1]))); teach.stand(1); idle(teach, 1, n, "look", 61); teach.expr("happy", 1)
def WIDE_MUSIC_ROOM(n):
    scene_mu(n); still_cam(n, (MU + 1.2, -5.2, 2.3), (MU - 0.2, 1.8, 1.25), 20, (MU + 1.1, -4.9, 2.25))
def MS_BRY_BRAG(n):
    scene_mu(n); bry.expr("happy", 1)
    for k, f in enumerate(range(1, n, 5)):   # air drums
        up = k % 2 == 0
        bry.pose(f, sh_L=(-70 if up else -40, 0, 15), el_L=(-80 if up else -40, 0, 0), sh_R=(-40 if up else -70, 0, -15), el_R=(-40 if up else -80, 0, 0), head=(4 if up else -2, 0, 0))
    tyler.rot("head", 1, 0, 0, 25); tyler.expr("deadpan", 1)
    fcam(n, bry, 0, 2.1, 0.65, -0.2, 26, -0.45, look_side=0.5)
def CU_BRY_COUNT(n):
    scene_mu(n); bry.expr("smug", 1)
    for k, f in enumerate(range(1, n, max(8, n // 5))):
        bry.pose(f, sh_R=(-100, 0, -10), el_R=(-80 - 10 * (k % 2), 0, 0), sh_L=(-60, 0, 20), el_L=(-90, 0, 0), head=(0, 0, 8 if k % 2 else -8))
    fcam(n, bry, 0, 0.95, 0.15, -0.05, 32, -0.15)
def MS_TEACH_RECORDER(n):
    scene_mu(n); show([rec_t], True); end = (BRS[0] + 0.5, BRS[1] - 0.62)
    teach.walk(1, int(n * 0.6), (MU + 2.6, end[1], 0), (end[0], end[1], 0)); y_ = yaw_to(end, BRS); teach.place(int(n * 0.6) + 2, end[0], end[1], 0, y_); teach.stand(int(n * 0.6) + 2)
    teach.pose(int(n * 0.6) + 6, sh_R=(-90, 0, 0), el_R=(-10, 0, 0)); bry.expr("smug", 1); bry.pose(int(n * 0.7), sh_R=(-75, 0, -10), el_R=(-20, 0, 0))
    still_cam(n, (MU - 0.9, -1.9, 1.6), (MU + 1.1, 0.2, 1.05), 24, (MU - 0.85, -1.8, 1.6))
def CU_BRY_SQUEAK(n):
    scene_mu(n); show([rec_m], True); bry.pose(1, sh_L=(-75, 0, 25), el_L=(-95, 0, 0), sh_R=(-75, 0, -25), el_R=(-95, 0, 0)); bry.expr("focused", 1)
    for f in range(1, n, 6): bry.mouth.scale = (0.6, 1, 0.8 if (f // 6) % 2 else 0.5); bry.mouth.keyframe_insert("scale", frame=f)
    for k, f in enumerate(range(1, n, 24)): bry.rot("head", f, -6 if k % 2 else 4, 0, 6 if k % 2 else -6)
    fcam(n, bry, 0, 1.0, -0.25, -0.02, 30, -0.12)
def CU_ME_FLINCH(n):
    scene_mu(n); show([rec_m], True); tyler.expr("annoyed", 1); tyler.rot("head", 1, 0, 0, 20); tyler.rot("head", 6, 6, 18, 28)
    tyler.pose(4, sh_R=(-150, 0, -40), el_R=(-125, 0, 0))   # hand over the ear
    fcam(n, tyler, 0, 0.95, 0.2, -0.03, 32, -0.1)
def WIDE_MUSIC_EARS(n):
    scene_mu(n); show([rec_m], True); bry.expr("focused", 1); teach.expr("shock", 1)
    for i in range(10):
        c = ext[i]; c.pose(4 + i, sh_L=(-150, 0, 40), el_L=(-125, 0, 0), sh_R=(-150, 0, -40), el_R=(-125, 0, 0)); c.expr("shock", 4 + i)
    tyler.pose(4, sh_L=(-150, 0, 40), el_L=(-125, 0, 0), sh_R=(-150, 0, -40), el_R=(-125, 0, 0)); tyler.expr("annoyed", 4)
    still_cam(n, (MU + 0.8, -4.3, 2.0), (MU, 1.4, 1.1), 20, (MU + 0.75, -4.0, 1.98))

# ---------------------------------------------------------------- 3 SCHOOL STORE (lunch)
CX, CY = st["counter"]; TOP = st["top_z"]
TSX, TSY = CX - 0.75, CY - 0.2                # Tyler at the counter (customer side)
BSX, BSY = CX - 1.75, CY - 0.55
SWSPOT = (CX - 0.22, CY - 0.25, TOP + 0.055)
def scene_st(n):
    all_off("in"); FILLS["fill_st"].energy = 420
    tyler.place(1, TSX, TSY, 0, 90); tyler.stand(1); tyler.expr("happy", 1); breathe(tyler, 1, n, 1.0, 96, 1)
    bry.place(1, BSX, BSY, 0, yaw_to((BSX, BSY), (TSX, TSY))); bry.stand(1); bry.expr("smug", 1); breathe(bry, 1, n, 1.2, 70, 5)
    k = ext[4]; k.place(1, CX + 0.85, CY + 0.35, 0, -90); k.stand(1); idle(k, 1, n, "look", 71)                 # cashier
    for i, (x, y, yaw, kind) in enumerate(((ST - 2.7, -0.9, 60, "phone"), (ST - 3.3, -1.5, 40, "phone"), (ST - 2.6, 1.9, 180, "look"))):
        ext[5 + i].place(1, x, y, 0, yaw); ext[5 + i].stand(1); idle(ext[5 + i], 1, n, kind, 80 + i)
    put(wrap_t, (SWSPOT[0], SWSPOT[1], TOP + 0.005)); show([wrap_t], True)
def WIDE_STORE(n):
    scene_st(n); put(SW, SWSPOT); still_cam(n, (ST - 2.9, -4.3, 2.2), (ST + 0.3, 0.8, 1.05), 20, (ST - 2.7, -4.0, 2.15))
def INS_ME_SANDWICH(n):
    scene_st(n); put(SW, SWSPOT); tyler.pose(1, sh_L=(-30, 0, 10), el_L=(-30, 0, 0), sh_R=(-35, 0, -10), el_R=(-35, 0, 0))
    x, y, z = SWSPOT; still_cam(n, (x + 0.55, y - 0.3, z + 0.42), (x, y, z), 34, (x + 0.5, y - 0.28, z + 0.39))
def CU_BRY_GASP(n):
    scene_st(n); put(SW, SWSPOT); by = yaw_to((BSX, BSY), (TSX, TSY)); OFF(tyler)
    bry.expr("shock", 1); bry.pose(3, sh_L=(-75, 0, 25), el_L=(-35, 0, 0), sh_R=(-75, 0, -25), el_R=(-35, 0, 0), chest=(-10, 0, 0), head=(-6, 0, 0))
    fcam(n, bry, by, 0.95, -0.2, -0.04, 32, -0.12)
def MS_BRY_BACKUP(n):
    scene_st(n); put(SW, SWSPOT); by = yaw_to((BSX, BSY), (TSX, TSY))
    bry.expr("shock", 1); bry.place(1, BSX, BSY, 0, by); bry.place(n, BSX, BSY, 0, by - 35)
    bry.pose(1, sh_L=(-110, 0, 20), el_L=(-25, 0, 0), sh_R=(-110, 0, -20), el_R=(-25, 0, 0)); bry.pose(n, chest=(-16, 0, 0), sh_L=(-120, 0, 25), sh_R=(-120, 0, -25))
    tyler.rot("head", 1, 0, 0, -60); tyler.expr("deadpan", 1)
    fcam(n, bry, by, 2.2, 0.9, -0.15, 26, -0.4, look_side=-0.2)
def CU_ME_SQUINT(n):
    scene_st(n); ty = yaw_to((TSX, TSY), (BSX, BSY)); OFF(bry); tyler.place(1, TSX, TSY, 0, ty); tyler.expr("annoyed", 1); tyler.blink(n // 2)
    tyler.pose(1, sh_R=(-60, 0, -10), el_R=(-80, 0, 0)); bake_to(SW, tyler, "hand_R", 1, n, (0, 0, 0.09), (0, 0, R(20)))
    fcam(n, tyler, ty, 0.95, 0.2, -0.03, 32, -0.1)
def MS_ME_PAY(n):
    scene_st(n); put(SW, SWSPOT); show([cash], True); tyler.pose(1, sh_R=(-80, 0, -5), el_R=(-15, 0, 0)); tyler.expr("happy", 1)
    k = ext[4]; k.pose(int(n * 0.4), sh_R=(-80, 0, 5), el_R=(-15, 0, 0))
    end = (CX - 0.95, CY - 0.5)
    bry.walk(1, int(n * 0.7), (BSX, BSY, 0), (end[0], end[1], 0)); bry.place(int(n * 0.7) + 2, end[0], end[1], 0, 70); bry.stand(int(n * 0.7) + 2)
    bry.pose(n, sh_R=(-60, 0, -10), el_R=(-30, 0, 0)); bry.expr("smug", 1)
    still_cam(n, (CX - 0.2, CY - 2.6, 1.95), (CX - 0.75, CY - 0.1, 1.05), 24, (CX - 0.22, CY - 2.45, 1.93))
BEND = (CX - 0.75, CY - 0.85)
def bry_eating(n, f0=1):
    bry.place(1, BEND[0], BEND[1], 0, -25); bry.stand(1); bry.pose(1, sh_R=(-120, 0, -5), el_R=(-105, 0, 0), sh_L=(-110, 0, 10), el_L=(-100, 0, 0))
    bake_to(SWB, bry, "hand_R", 1, n, (-0.06, -0.06, 0.08), (R(10), 0, R(-30)))
def CU_BRY_CHEWING(n):
    scene_st(n); bry_eating(n); chew(bry, n, 5); bry.expr("chill", 1)
    tyler.place(1, TSX, TSY, 0, -100)
    fcam(n, bry, -25, 0.95, 0.1, -0.05, 32, -0.15)
def CU_BRY_SALAD(n):
    scene_st(n); bry_eating(n); bry.pose(1, sh_R=(-140, 0, -10), el_R=(-60, 0, 0)); chew(bry, n // 2, 6); bry.expr("smug", 1); bry.blink(int(n * 0.6))
    tyler.place(1, TSX, TSY, 0, -100)
    fcam(n, bry, -25, 1.05, 0.25, -0.02, 30, -0.12)
def INS_SANDWICH_BITTEN(n):
    scene_st(n); OFF(bry); x, y, z = SWSPOT; put(stub, (x + 0.05, y + 0.03, TOP + 0.03)); show([stub], True)
    rnd = random.Random(5)
    for c in crumbs: put(c, (x + rnd.uniform(-0.12, 0.12), y + rnd.uniform(-0.1, 0.1), TOP + 0.012), 1, (0, 0, rnd.uniform(0, 3)))
    show(crumbs, True); tyler.pose(1, sh_R=(-50, 0, -10), el_R=(-35, 0, 0))
    still_cam(n, (x - 0.45, y - 0.42, z + 0.4), (x, y, TOP + 0.02), 36, (x - 0.41, y - 0.38, z + 0.37))
def POV_STORE(n):   # background for the phone insert (blurred)
    scene_st(n); OFF(tyler); OFF(bry); still_cam(n, (ST - 0.5, -1.5, 1.6), (ST - 0.8, 2.8, 1.3), 24)

# ---------------------------------------------------------------- 4 SCIENCE FAIR (after school)
AX, AY = sf["A"]; BTX, BTY = sf["B"]; LD = sf["ld"]
SX, SY = sf["stool"]
TFX, TFY = AX - 0.15, AY + 0.82                # Tyler behind table A
HFX, HFY = AX - 0.3, AY - 1.4                  # Hargrove (judge) in front of table A
BRX, BRY = BTX + 0.55, BTY + 0.82              # Bryce behind his volcano
TFYAW = yaw_to((TFX, TFY), (SX, SY))
def scene_sf(n, bry_stool=True):
    all_off("in"); FILLS["fill_sf"].energy = 650
    tyler.place(1, TFX, TFY, 0, TFYAW); tyler.stand(1); tyler.expr("focused", 1); breathe(tyler, 1, n, 1.0, 96, 1)
    if bry_stool: sit_at(bry, SX, SY, 90, 0.0); bry.pose(1, sh_R=(-75, 0, -10), el_R=(-25, 0, 0)); bry.expr("smug", 1); breathe(bry, 1, n, 1.2, 70, 5)
    for i, (x, y, yaw, kind) in enumerate(((SF - 3.6, 4.08, 0, "look"), (SF + 3.6, 4.08, 0, "look"), (SF - 3.0, 2.5, 180, "look"), (SF + 0.4, 2.45, 170, "look"),
                                           (SF + 3.0, 2.5, 190, "phone"))):
        ext[i].place(1, x, y, 0, yaw); ext[i].stand(1); idle(ext[i], 1, n, kind, 90 + i)
    ext[5].walk(1, n, (SF + 4.2, -1.8, 0), (SF + 4.2 - 1.0 * n / 30, -1.8, 0)); ext[6].walk(1, n, (SF - 5.0, -2.4, 0), (SF - 5.0 + 0.9 * n / 30, -2.4, 0))
def LDpos():
    bpy.context.scene.frame_set(1); return LD.matrix_world.translation.copy()
def WIDE_FAIR(n):
    scene_sf(n, bry_stool=False); bry.place(1, BRX, BRY, 0, 0); bry.stand(1); idle(bry, 1, n, "talk", 95)
    harg.place(1, SF + 3.2, -0.4, 0, 150); harg.stand(1); show([hclip], True); idle(harg, 1, n, "look", 96)
    still_cam(n, (SF + 0.9, -5.2, 2.4), (SF - 0.6, 1.6, 1.05), 20, (SF + 0.85, -4.9, 2.35))
def INS_LIE_DETECTOR(n):
    scene_sf(n); h = LDpos(); glow(sf["bulbG"], 0.4); glow(sf["bulbR"], 0.4)
    still_cam(n, (h.x, h.y - 1.45, h.z + 0.68), (h.x, h.y, h.z + 0.2), 28, (h.x, h.y - 1.35, h.z + 0.64))
def CU_ME_ASK(n):
    scene_sf(n); show(clip_objs := [clipb, bpy.data.objects["ME_clippaper"]], True); tyler.pose(1, sh_L=(-60, 0, 15), el_L=(-60, 0, 0)); tyler.expr("focused", 1)
    tyler.pose(n // 2, sh_R=(-70, 0, -15), el_R=(-30, 0, 0))   # points at Bryce like a lawyer
    fcam(n, tyler, TFYAW, 0.95, 0.15, -0.03, 32, -0.1)
def CU_BRY_SMUG(n):
    scene_sf(n); bry.expr("smug", 1); bry.pose(1, chest=(-6, 0, 0)); bry.blink(n // 2); bry.rot("head", 1, 0, 0, -12)
    fcam(n, bry, 90, 0.95, -0.15, -0.03, 32, -0.12)
def INS_DETECTOR_GREEN(n):
    scene_sf(n); h = LDpos(); glow(sf["bulbG"], 0.35); glow(sf["bulbR"], 0.0)
    still_cam(n, (h.x, h.y - 1.2, h.z + 0.55), (h.x, h.y, h.z + 0.25), 28, (h.x, h.y - 1.1, h.z + 0.52))
def MS_HARG_ASK(n):
    scene_sf(n); harg.place(1, HFX, HFY, 0, yaw_to((HFX, HFY), (TFX, TFY))); harg.stand(1); show([hclip], True)
    harg.pose(1, sh_L=(-60, 0, 15), el_L=(-60, 0, 0), chest=(8, 0, 0)); harg.expr("deadpan", 1); harg.blink(n // 2)
    tyler.place(1, TFX, TFY, 0, yaw_to((TFX, TFY), (HFX, HFY))); tyler.pose(1, sh_R=(-70, 0, -5), el_R=(-20, 0, 0))   # finger clipped to the box
    OFF(bry)
    hx, hy, hz = headpos(harg)
    still_cam(n, (TFX + 0.55, TFY + 0.9, hz + 0.25), (hx, hy, hz - 0.25), 30, (TFX + 0.52, TFY + 0.82, hz + 0.24))
def INS_DETECTOR_RED(n):
    scene_sf(n); OFF(bry); h = LDpos(); glow(sf["bulbG"], 0.0); flash(sf["bulbR"], n, 3, 0.45)
    for f in range(1, n, 2):
        LD.location = (h.x + (0.008 if (f // 2) % 2 else -0.008), h.y, h.z); LD.keyframe_insert("location", frame=f)
        sf["needle"].rotation_euler = (0, R(60 if (f // 2) % 2 else -60), 0); sf["needle"].keyframe_insert("rotation_euler", frame=f)
    still_cam(n, (h.x, h.y - 1.2, h.z + 0.55), (h.x, h.y, h.z + 0.25), 28, (h.x, h.y - 1.08, h.z + 0.52))
def CU_HARG_POINT(n):
    scene_sf(n); OFF(bry); y_ = yaw_to((HFX, HFY), (TFX, TFY)); harg.place(1, HFX, HFY, 0, y_); harg.stand(1); show([hclip], True)
    harg.expr("angry", 1); harg.pose(4, sh_R=(-95, 0, -5), el_R=(-5, 0, 0), sh_L=(-60, 0, 15), el_L=(-60, 0, 0), chest=(6, 0, 0))
    fcam(n, harg, y_, 1.25, 0.35, -0.02, 30, -0.15)
def MS_BRY_RIBBON(n):
    scene_sf(n, bry_stool=False); bry.place(1, BRX, BRY, 0, 0); bry.stand(1); show([ribbon], True); bry.expr("happy", 1)
    for k, f in enumerate(range(1, n, 8)): bry.pose(f, sh_R=(-160, 0, -20 if k % 2 else -40), el_R=(-20, 0, 0))   # waves
    for i in (2, 3): ext[i].pose(1, sh_L=(-80, 0, 30), sh_R=(-80, 0, -30), el_L=(-60, 0, 0), el_R=(-60, 0, 0))
    for i in (2, 3):
        for f in range(1, n, 6): ext[i].rot("el_L", f, -60 if (f // 6) % 2 else -85); ext[i].rot("el_R", f, -60 if (f // 6) % 2 else -85)   # clapping
    fcam(n, bry, 0, 2.1, 0.2, -0.2, 26, -0.45)
def INS_DETENTION_SLIP(n):
    scene_sf(n); OFF(bry); h = LDpos(); put(dslip, (h.x + 0.62, h.y - 0.12, 0.79), 1, (0, 0, R(-8))); show([dslip], True)
    p = dslip.location
    still_cam(n, (p.x + 0.16, p.y - 0.42, p.z + 0.42), (p.x, p.y, p.z), 34, (p.x + 0.15, p.y - 0.38, p.z + 0.38))
def CU_ME_CRUMBS(n):
    scene_sf(n, bry_stool=False); bry.place(1, BRX, BRY, 0, 0); bry.stand(1); show([ribbon], True); idle(bry, 1, n, "talk", 97)
    tyler.place(1, TFX, TFY, 0, 15); show([wrapper_h, bpy.data.objects["ME_wrapsauce"]], True)
    tyler.pose(1, sh_R=(-55, 0, -5), el_R=(-60, 0, 0)); tyler.rot("head", 1, 16, 0, 0); tyler.expr("sad", 1); tyler.blink(n // 2)
    fcam(n, tyler, 15, 0.95, 0.3, -0.02, 30, -0.18)

HELPERS = ("POV_STORE",)
SHOTS = {k: v for k, v in globals().items() if k.isupper() and callable(v) and k not in ("P", "R", "MK", "OFF")}
T = json.load(open(TL, encoding="utf-8")); os.makedirs(OUT, exist_ok=True); sc = bpy.context.scene
todo = [(s["id"], s["key"], round(s["end"] * FPS) - round(s["start"] * FPS)) for s in T["shots"]] + [("POV", k, 20) for k in HELPERS]
for sid, key, n in todo:
    if key not in SHOTS or (ONLY and key not in ONLY): continue
    t0 = time.time(); reset(); SHOTS[key](n)
    if CHECK:
        hits = []
        for fr in sorted({1, max(1, n // 2), n}):
            hits += [h for h in find_collisions(EVERYONE, fr) if h not in hits]
        for h in hits: print("COLLIDE", sid, key, *h)
        if not hits: print("CLEAN", sid, key)
        continue
    sc.frame_start, sc.frame_end = 1, n; sc.render.resolution_x, sc.render.resolution_y = RES
    if STILLS or key in HELPERS:
        sc.frame_set(max(1, n // 2)); sc.render.filepath = os.path.join(OUT, f"{sid}_{key}.png"); bpy.ops.render.render(write_still=True)
    else:
        d = os.path.join(OUT, f"{sid}_{key}")
        if os.path.isdir(d) and len([x for x in os.listdir(d) if x.endswith(".png")]) >= n:
            print("SKIP (already rendered)", sid, key, flush=True); continue
        os.makedirs(d, exist_ok=True); sc.render.filepath = os.path.join(d, "f_"); bpy.ops.render.render(animation=True)
    print("RENDERED", sid, key, n, f"{time.time() - t0:.1f}s", flush=True)
print("ALL DONE")
