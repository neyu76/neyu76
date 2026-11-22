"""TM04 sets (Bryce, the habitual liar): outdoor basketball court (morning), music room, school store, science fair.
Convention as hb_sets5: back wall / background at +Y, open side toward the camera at -Y. Seat tops at z=0.47 (+ riser height).
Every function returns key spots."""
import bpy, math, random
from hb_lib import box, mat, srgb, R, empty
from hb_props import tex_quad, light_panel, chips_bag, backpack
from hb_sets4 import _sph, _cyl
from hb_sets5 import tree

def _C(prefix):
    return lambda h, r=0.7, e=0.0: mat(f"{prefix}_{h}", srgb(h), r, emit=e)

def chair(name, x, y, z, col, C, yaw=0):
    g = empty(name, (x, y, z)); g.rotation_euler = (0, 0, R(yaw))
    box(name + "_seat", (0.46, 0.44, 0.05), (0, 0, 0.45), C(col, 0.5), g, 0.01, 1)
    box(name + "_seatb", (0.46, 0.05, 0.42), (0, 0.22, 0.7), C(col, 0.5), g, 0.01, 1)
    for sx in (-1, 1):
        for sy in (-1, 1): box(f"{name}_seatl{sx}{sy}", (0.03, 0.03, 0.44), (sx * 0.2, sy * 0.19, 0.22), C("333333", 0.4), g)
    return g

# ---------------------------------------------------------------- 1 OUTDOOR BASKETBALL COURT
def court(o):
    """Court x -8..8, y -6..6 (hoop at +Y). Fence at y=6.6 and x=+-8.6. School building behind at y=13."""
    ox, oy, oz = o; C = _C("ct")
    box("ct_ground", (40, 34, 0.1), (ox, oy, oz - 0.06), C("8fbf6a", 0.95))
    box("ct_asphalt", (18, 14, 0.04), (ox, oy, oz - 0.01), C("3f6e8c", 0.85))
    box("ct_paint", (15, 11.4, 0.006), (ox, oy, oz + 0.012), C("2f8f6f", 0.8))
    W = C("f4f4f4", 0.6)
    for sy in (-1, 1): box(f"ct_line_s{sy}", (15, 0.08, 0.004), (ox, oy + sy * 5.7, oz + 0.017), W)
    for sx in (-1, 1): box(f"ct_line_e{sx}", (0.08, 11.4, 0.004), (ox + sx * 7.5, oy, oz + 0.017), W)
    box("ct_line_mid", (15, 0.08, 0.004), (ox, oy - 5.7 + 0.04, oz + 0.017), W)
    box("ct_key", (3.6, 4.6, 0.005), (ox, oy + 3.4, oz + 0.016), C("c0392b", 0.8))
    box("ct_ft", (3.6, 0.08, 0.004), (ox, oy + 1.1, oz + 0.019), W)
    bpy.ops.mesh.primitive_torus_add(major_radius=1.8, minor_radius=0.04, location=(ox, oy + 1.1, oz + 0.018)); t = bpy.context.active_object
    t.name = "ct_line_circle"; t.scale = (1, 1, 0.05); t.data.materials.append(W)
    bpy.ops.mesh.primitive_torus_add(major_radius=6.0, minor_radius=0.04, location=(ox, oy + 5.7, oz + 0.018)); t = bpy.context.active_object
    t.name = "ct_line_arc"; t.scale = (1, 1, 0.05); t.data.materials.append(W)
    # hoop: pole, arm, backboard, square, rim, net
    box("ct_hooppole", (0.2, 0.2, 3.4), (ox, oy + 6.3, oz + 1.7), C("2c3e50", 0.4))
    box("ct_hooparm", (0.12, 1.2, 0.12), (ox, oy + 5.75, oz + 3.3), C("2c3e50", 0.4))
    box("ct_board", (1.8, 0.06, 1.05), (ox, oy + 5.15, oz + 3.45), C("f4f4f4", 0.3))
    for sx in (-1, 1): box(f"ct_sq{sx}", (0.05, 0.02, 0.45), (ox + sx * 0.3, oy + 5.11, oz + 3.25), C("e74c3c", 0.5))
    box("ct_sqt", (0.65, 0.02, 0.05), (ox, oy + 5.11, oz + 3.47), C("e74c3c", 0.5)); box("ct_sqb", (0.65, 0.02, 0.05), (ox, oy + 5.11, oz + 3.03), C("e74c3c", 0.5))
    rim = (ox, oy + 4.85, oz + 3.05)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.23, minor_radius=0.02, location=rim); t = bpy.context.active_object; t.name = "ct_rim"; t.data.materials.append(C("ff6b1a", 0.4))
    for k in range(10):
        a = k / 10 * 2 * math.pi
        n_ = box(f"ct_net{k}", (0.012, 0.012, 0.42), (rim[0] + math.cos(a) * 0.19, rim[1] + math.sin(a) * 0.19, rim[2] - 0.2), C("f4f4f4", 0.9)); n_.rotation_euler = (math.sin(a) * 0.2, -math.cos(a) * 0.2, 0)
    # chain-link fence: posts + horizontal rails + mesh look (thin grid)
    FN = C("9aa0a6", 0.35)
    for i in range(-8, 9):
        box(f"ct_fpost{i}", (0.06, 0.06, 3.0), (ox + i * 1.05, oy + 6.6, oz + 1.5), FN)
    for sx in (-1, 1):
        for j in range(-6, 7): box(f"ct_fposts{sx}{j}", (0.06, 0.06, 3.0), (ox + sx * 8.6, oy + j * 1.05, oz + 1.5), FN)
    for z in (0.1, 1.5, 2.95):
        box(f"ct_frail{z}", (17.2, 0.04, 0.04), (ox, oy + 6.6, oz + z), FN)
        for sx in (-1, 1): box(f"ct_frails{sx}{z}", (0.04, 13.2, 0.04), (ox + sx * 8.6, oy, oz + z), FN)
    MESH = mat("ct_mesh", srgb("b8bec4"), 0.4)
    for i in range(-34, 35): box(f"ct_fw{i}", (0.008, 0.008, 2.9), (ox + i * 0.25, oy + 6.62, oz + 1.5), MESH)
    for z in range(1, 12): box(f"ct_fh{z}", (17.2, 0.008, 0.008), (ox, oy + 6.62, oz + z * 0.25), MESH)
    tex_quad("ct_rules", 0.9, 0.6, "tm04_court_rules.png", (ox - 4.2, oy + 6.55, oz + 1.9), (R(90), 0, 0))
    # bench with water bottles + towel + backpacks, ball rack
    box("ct_bench", (2.0, 0.42, 0.07), (ox - 5.0, oy + 5.4, oz + 0.47), C("8a5a33", 0.6))
    for sx in (-1, 1): box(f"ct_benchleg{sx}", (0.06, 0.38, 0.45), (ox - 5.0 + sx * 0.85, oy + 5.4, oz + 0.23), C("2c3e50", 0.4))
    for k, col in enumerate(("2ecc71", "3498db", "e67e22")): _cyl(f"ct_bottle{k}", 0.04, 0.22, (ox - 4.75 + k * 0.12, oy + 5.4, oz + 0.62), C(col, 0.2))
    box("ct_towel", (0.4, 0.3, 0.03), (ox - 4.25, oy + 5.4, oz + 0.52), C("ecf0f1", 0.9))
    backpack("ct_bp1", (ox - 6.3, oy + 5.6, oz), "8e44ad", 20); backpack("ct_bp2", (ox - 3.7, oy + 5.7, oz), "16a085", -15)
    box("ct_rack", (1.2, 0.4, 0.06), (ox + 5.2, oy + 5.6, oz + 0.75), C("7f8c8d", 0.4))
    for sx in (-1, 1): box(f"ct_rackleg{sx}", (0.05, 0.05, 0.75), (ox + 5.2 + sx * 0.55, oy + 5.6, oz + 0.37), C("7f8c8d", 0.4))
    for k in range(3): _sph(f"ct_rackball{k}", 0.12, (ox + 4.85 + k * 0.35, oy + 5.6, oz + 0.9), C("e67e22", 0.6), 12, 8)
    # background: school gym wall + windows, trees, lamp posts
    box("ct_school", (34, 0.4, 6.0), (ox, oy + 13.0, oz + 3.0), C("b8643a", 0.8))
    box("ct_schooltrim", (34, 0.45, 0.25), (ox, oy + 12.98, oz + 5.9), C("e8e2d6", 0.6))
    for i in range(-7, 8):
        box(f"ct_swin{i}", (1.4, 0.05, 1.2), (ox + i * 2.2, oy + 12.78, oz + 3.8), C("8fb8d8", 0.1))
    box("ct_gymdoor", (2.4, 0.06, 2.4), (ox + 3.0, oy + 12.78, oz + 1.2), C("2c4a6e", 0.3))
    for i, (x, y) in enumerate(((-11, 9), (-6, 10.5), (7, 10), (12, 8.5), (-12, -2), (12.5, -1))): tree(f"ct_tree{i}", ox + x, oy + y, oz, 2.6, 1.2, C)
    for sx in (-1, 1):
        box(f"ct_lamp{sx}", (0.1, 0.1, 5.5), (ox + sx * 9.5, oy + 6.9, oz + 2.75), C("2c3e50", 0.4))
        box(f"ct_lamphead{sx}", (0.6, 0.3, 0.15), (ox + sx * 9.5, oy + 6.6, oz + 5.5), C("dfe6ee", 0.3))
    ball = _sph("ct_ball", 0.12, (ox, oy - 80, oz), C("e67e22", 0.6), 14, 10)
    for k in range(2): box(f"ct_ballseam{k}", (0.245, 0.245, 0.008), (0, 0, 0), C("1b1b1b", 0.6), ball).rotation_euler = (R(90 * k), 0, 0)
    return dict(rim=rim, bench=(ox - 5.0, oy + 5.4), ball=ball)

# ---------------------------------------------------------------- 2 MUSIC ROOM
def music_room(o):
    """Room x -5..5, y -4..4 (front open toward -Y). 3 straight risers at y 0.6/1.6/2.6 (heights 0, 0.2, 0.4)."""
    ox, oy, oz = o; C = _C("mu")
    box("mu_floor", (10.4, 11.0, 0.1), (ox, oy - 1.5, oz - 0.05), C("b98a5a", 0.6))
    for i in range(-10, 11): box(f"mu_fx{i}", (0.01, 11.0, 0.004), (ox + i * 0.5, oy - 1.5, oz + 0.002), C("a87a4c"))
    for n, sz, lc in (("wb", (10.4, 0.15, 3.4), (ox, oy + 4.1, oz + 1.7)), ("wl", (0.15, 11, 3.4), (ox - 5.2, oy - 1.5, oz + 1.7)),
                      ("wr", (0.15, 11, 3.4), (ox + 5.2, oy - 1.5, oz + 1.7)), ("ceil", (10.4, 11, 0.1), (ox, oy - 1.5, oz + 3.45))):
        box("mu_" + n, sz, lc, C("e9dfc8" if n != "ceil" else "f4f4f4", 0.8))
    for i in range(-4, 5): box(f"mu_acoustic{i}", (0.9, 0.06, 0.5), (ox + i * 1.1, oy + 4.0, oz + 3.1), C("4a6fa5" if i % 2 else "c0703f", 0.95))
    for k in range(2): light_panel(f"mu_light{k}", (ox - 2 + k * 4, oy + 0.5, oz + 3.38), (1.4, 0.6))
    # whiteboard with PERIOD 2 sign, music staff lines
    box("mu_wbframe", (4.0, 0.05, 1.2), (ox - 0.6, oy + 4.0, oz + 2.38), C("bdc3c7", 0.3))
    tex_quad("mu_period2", 3.8, 1.04, "tm04_period2.png", (ox - 0.6, oy + 3.96, oz + 2.38), (R(90), 0, 0))
    for k in range(5): box(f"mu_staff{k}", (3.6, 0.01, 0.012), (ox - 0.6, oy + 3.955, oz + 1.55 + k * 0.06), C("1b1b1b", 0.6))
    tex_quad("mu_poster", 0.6, 0.86, "tm04_music_poster.png", (ox + 2.4, oy + 3.99, oz + 1.9), (R(90), 0, 0))
    # risers + chairs + music stands (students face -Y)
    risers = []
    for r, (y, h) in enumerate(((0.6, 0.0), (1.6, 0.2), (2.6, 0.4))):
        if h: box(f"mu_riser{r}", (8.4, 1.0, h), (ox, oy + y, oz + h / 2), C("8a6a4a", 0.6))
        for c in range(-3, 4):
            x = ox + c * 1.15; chair(f"mu_chair{r}_{c}", x, oy + y + 0.12, oz + h, ("2c3e50", "34495e")[r % 2], C, 0); risers.append((r, c, x, oy + y, h))
            if (r == 1 and c % 2 == 0) or (r == 0 and abs(c) == 3):
                box(f"mu_standp{r}{c}", (0.03, 0.03, 0.9), (x + 0.3, oy + y - 0.45, oz + h + 0.45), C("1b1b1b", 0.4))
                box(f"mu_standd{r}{c}", (0.42, 0.03, 0.3), (x + 0.3, oy + y - 0.47, oz + h + 1.0), C("1b1b1b", 0.4)).rotation_euler = (R(-20), 0, 0)
    # drum kit (left), upright piano (right), guitar on stand, xylophone, cabinet
    dk = (ox - 3.9, oy + 3.3)
    _cyl("mu_kick", 0.32, 0.36, (dk[0], dk[1], oz + 0.33), C("c0392b", 0.4), (R(90), 0, 0), 20)
    _cyl("mu_kickhead", 0.3, 0.01, (dk[0], dk[1] - 0.19, oz + 0.33), C("f4f4f4", 0.6), (R(90), 0, 0), 20)
    for k, (dx, dy, z, r) in enumerate(((-0.45, -0.3, 0.6, 0.18), (0.45, -0.25, 0.62, 0.2), (0.2, 0.15, 0.78, 0.14))):
        _cyl(f"mu_tom{k}", r, 0.18, (dk[0] + dx, dk[1] + dy, oz + z), C("c0392b", 0.4), (0, 0, 0), 18)
        _cyl(f"mu_tomhead{k}", r * 0.95, 0.01, (dk[0] + dx, dk[1] + dy, oz + z + 0.095), C("f4f4f4", 0.6), (0, 0, 0), 18)
    for k, (dx, z) in enumerate(((-0.7, 1.05), (0.75, 1.15))):
        box(f"mu_cymstand{k}", (0.025, 0.025, z), (dk[0] + dx, dk[1] + 0.1, oz + z / 2), C("9aa0a6", 0.3))
        _cyl(f"mu_cym{k}", 0.24, 0.012, (dk[0] + dx, dk[1] + 0.1, oz + z), C("d4a017", 0.25), (R(8), 0, 0), 20)
    box("mu_piano", (1.5, 0.6, 1.25), (ox + 3.9, oy + 3.6, oz + 0.62), C("2b1d14", 0.35), None, 0.02, 1)
    box("mu_pianokeys", (1.36, 0.25, 0.05), (ox + 3.9, oy + 3.2, oz + 0.75), C("f4f4f4", 0.4))
    for k in range(9): box(f"mu_pianoblack{k}", (0.05, 0.14, 0.03), (ox + 3.3 + k * 0.15, oy + 3.25, oz + 0.79), C("111111", 0.4))
    box("mu_pianobench", (0.9, 0.35, 0.06), (ox + 3.9, oy + 2.75, oz + 0.47), C("2b1d14", 0.4))
    for sx in (-1, 1): box(f"mu_pianobenchl{sx}", (0.05, 0.3, 0.45), (ox + 3.9 + sx * 0.38, oy + 2.75, oz + 0.22), C("2b1d14", 0.4))
    box("mu_gstand", (0.04, 0.04, 0.6), (ox - 4.6, oy + 1.2, oz + 0.3), C("1b1b1b", 0.4))
    _sph("mu_gbody", 0.22, (ox - 4.6, oy + 1.12, oz + 0.62), C("c8892e", 0.4), 14, 8, None, (1, 0.45, 1.25))
    box("mu_gneck", (0.06, 0.04, 0.62), (ox - 4.6, oy + 1.12, oz + 1.18), C("5a3a22", 0.5))
    box("mu_xylo", (1.0, 0.4, 0.06), (ox - 4.3, oy - 0.6, oz + 0.75), C("8a5a33", 0.5))
    for k, col in enumerate(("e74c3c", "e67e22", "f1c40f", "2ecc71", "3498db", "9b59b6")): box(f"mu_xbar{k}", (0.11, 0.36 - k * 0.03, 0.03), (ox - 4.7 + k * 0.15, oy - 0.6, oz + 0.8), C(col, 0.4))
    box("mu_xylolegs", (0.9, 0.3, 0.7), (ox - 4.3, oy - 0.6, oz + 0.36), C("5a3a22", 0.6))
    box("mu_cabinet", (0.5, 2.4, 2.0), (ox + 4.9, oy + 0.6, oz + 1.0), C("8a5a33", 0.6))
    for k in range(4): box(f"mu_cabcase{k}", (0.06, 0.45, 0.35), (ox + 4.62, oy - 0.3 + k * 0.6, oz + 0.6 + (k % 2) * 0.8), C(("1b1b1b", "2c3e50", "7f8c8d", "c0392b")[k], 0.5))
    box("mu_clock", (0.4, 0.04, 0.4), (ox + 1.6, oy + 4.0, oz + 2.95), C("f4f4f4", 0.5))
    return dict(risers={(r, c): (x, y, h) for r, c, x, y, h in risers}, kit=dk, piano=(ox + 3.9, oy + 2.75))

# ---------------------------------------------------------------- 3 SCHOOL STORE
def school_store(o):
    """Room x -4.5..4.5, y -3..3 (front open). Counter along Y at x=+1.2 (y -1.2..1.6). Shelves on the back wall, fridge back-left."""
    ox, oy, oz = o; C = _C("st")
    box("st_floor", (9.4, 9.0, 0.1), (ox, oy - 1.4, oz - 0.05), C("a89c86", 0.6))
    for i in range(-9, 10): box(f"st_fx{i}", (0.01, 9.0, 0.004), (ox + i * 0.5, oy - 1.4, oz + 0.002), C("978b76"))
    for i in range(-9, 6): box(f"st_fy{i}", (9.4, 0.01, 0.004), (ox, oy + i * 0.5, oz + 0.002), C("978b76"))
    for n, sz, lc in (("wb", (9.4, 0.15, 3.2), (ox, oy + 3.1, oz + 1.6)), ("wl", (0.15, 9.0, 3.2), (ox - 4.7, oy - 1.4, oz + 1.6)),
                      ("wr", (0.15, 9.0, 3.2), (ox + 4.7, oy - 1.4, oz + 1.6)), ("ceil", (9.4, 9.0, 0.1), (ox, oy - 1.4, oz + 3.25))):
        box("st_" + n, sz, lc, C("f2e6c9" if n != "ceil" else "f4f4f4", 0.8))
    box("st_stripe", (9.3, 0.02, 0.3), (ox, oy + 3.02, oz + 1.1), C("7a1f2b", 0.6))
    for k in range(3): light_panel(f"st_light{k}", (ox - 3 + k * 3, oy, oz + 3.18), (1.2, 0.5))
    tex_quad("st_sign", 4.4, 0.96, "tm04_store_sign.png", (ox - 0.6, oy + 3.0, oz + 2.6), (R(90), 0, 0))
    # back-wall shelves full of snacks
    rnd = random.Random(4)
    for s in range(4):
        z = 0.35 + s * 0.48
        box(f"st_shelf{s}", (5.2, 0.45, 0.04), (ox - 0.9, oy + 2.75, oz + z), C("8a5a33", 0.5))
        for k in range(13):
            col = rnd.choice(("e63c28", "f1c40f", "2ecc71", "3498db", "9b59b6", "e67e22", "1abc9c", "ff6fae"))
            h = rnd.uniform(0.18, 0.32); box(f"st_snack{s}_{k}", (0.28, 0.2, h), (ox - 3.3 + k * 0.4, oy + 2.75, oz + z + 0.02 + h / 2), C(col, 0.5), None, 0.01, 1)
    for sx in (-1, 1): box(f"st_shelfside{sx}", (0.04, 0.45, 1.9), (ox - 0.9 + sx * 2.62, oy + 2.75, oz + 0.95), C("8a5a33", 0.5))
    # drinks fridge (glowing) back-left
    box("st_fridge", (1.2, 0.8, 2.1), (ox - 4.0, oy + 2.55, oz + 1.05), C("dfe6ee", 0.3))
    box("st_fridgeglass", (1.0, 0.02, 1.8), (ox - 4.0, oy + 2.14, oz + 1.1), mat("st_fridgeglow", srgb("cfe9ff"), 0.1, emit=1.6))
    for s in range(4):
        for k in range(5): _cyl(f"st_can{s}{k}", 0.05, 0.16, (ox - 4.4 + k * 0.2, oy + 2.3, oz + 0.4 + s * 0.42), C(("e74c3c", "2ecc71", "3498db", "f1c40f")[s], 0.3))
    # counter + register + gum rack + tip jar; cashier side at x>1.2
    box("st_counter", (0.7, 2.8, 1.0), (ox + 1.2, oy + 0.2, oz + 0.5), C("7a1f2b", 0.5))
    box("st_countertop", (0.85, 2.95, 0.05), (ox + 1.2, oy + 0.2, oz + 1.02), C("e8dcc6", 0.4))
    box("st_register", (0.4, 0.45, 0.25), (ox + 1.3, oy + 1.0, oz + 1.17), C("2c3e50", 0.4))
    box("st_regscreen", (0.3, 0.03, 0.2), (ox + 1.25, oy + 0.85, oz + 1.42), mat("st_scr", srgb("9fe2a0"), 0.2, emit=1.0)).rotation_euler = (R(-15), 0, R(90))
    box("st_gumrack", (0.35, 0.25, 0.4), (ox + 1.15, oy - 0.9, oz + 1.25), C("f1c40f", 0.5))
    _cyl("st_tipjar", 0.08, 0.18, (ox + 1.1, oy - 0.45, oz + 1.13), mat("st_glass", srgb("e8f4fa"), 0.05))
    box("st_stool", (0.4, 0.4, 0.06), (ox + 2.2, oy + 0.6, oz + 0.62), C("2c3e50", 0.5)); box("st_stoolleg", (0.06, 0.06, 0.6), (ox + 2.2, oy + 0.6, oz + 0.3), C("9aa0a6", 0.3))
    # hoodies/tees hanging on the left wall + price board on the right wall
    for k, col in enumerate(("1f3a68", "7a1f2b", "1f3a68", "95a5a6")):
        y = oy - 1.6 + k * 0.9
        box(f"st_rod{k}", (0.04, 0.8, 0.04), (ox - 4.5, y, oz + 2.05), C("9aa0a6", 0.3))
        box(f"st_tee{k}", (0.06, 0.62, 0.72), (ox - 4.55, y, oz + 1.62), C(col, 0.9), None, 0.02, 1)
        tex_quad(f"st_teeprint{k}", 0.34, 0.36, "tm04_shirt_wb.png", (ox - 4.515, y, oz + 1.66), (R(90), 0, R(90)))
    tex_quad("st_prices", 0.9, 1.2, "tm04_prices.png", (ox + 4.61, oy + 1.3, oz + 1.8), (R(90), 0, R(-90)))
    # floor display bin of chips + cooler
    box("st_bin", (0.8, 0.6, 0.55), (ox - 1.8, oy - 0.2, oz + 0.27), C("2c3e50", 0.5))
    for k in range(6): chips_bag(f"st_binchip{k}", (ox - 2.05 + (k % 3) * 0.25, oy - 0.2 + (k // 3) * 0.15, oz + 0.62), (R(-20), 0, R(k * 13)))
    return dict(counter=(ox + 1.2, oy + 0.2), register=(ox + 1.3, oy + 1.0), top_z=oz + 1.045)

# ---------------------------------------------------------------- 4 SCIENCE FAIR
def fair_table(name, x, y, C, cloth="1f4e8c"):
    box(name, (2.0, 0.8, 0.05), (x, y, 0.76), C("e8dcc6", 0.5))
    box(name + "_cloth", (2.04, 0.84, 0.5), (x, y, 0.52), C(cloth, 0.9))
    for sx in (-1, 1): box(f"{name}_leg{sx}", (0.05, 0.7, 0.74), (x + sx * 0.92, y, 0.37), C("9aa0a6", 0.3))

def trifold(name, x, y, z, img):
    tex_quad(name, 0.9, 0.63, img, (x, y, z + 0.32), (R(90), 0, 0))
    for sx in (-1, 1):
        w = tex_quad(f"{name}_wing{sx}", 0.4, 0.63, img, (x + sx * 0.6, y - 0.12, z + 0.32), (R(90), 0, R(sx * 35)))

def science_fair(o):
    """Art room turned science fair: x -6..6, y -4.5..4.5 (front open). Tyler's table A at (+1.2, 0.6); Bryce's table B at (-2.6, 0.6).
    Presenters stand behind tables (+Y side) facing -Y."""
    ox, oy, oz = o; C = _C("sf")
    box("sf_floor", (12.4, 13.0, 0.1), (ox, oy - 2.0, oz - 0.05), C("8e979f", 0.6))
    for i in range(-12, 13): box(f"sf_fx{i}", (0.01, 13.0, 0.004), (ox + i * 0.5, oy - 2.0, oz + 0.002), C("7d868e"))
    for n, sz, lc in (("wb", (12.4, 0.15, 3.6), (ox, oy + 4.6, oz + 1.8)), ("wl", (0.15, 13, 3.6), (ox - 6.2, oy - 2.0, oz + 1.8)),
                      ("wr", (0.15, 13, 3.6), (ox + 6.2, oy - 2.0, oz + 1.8)), ("ceil", (12.4, 13, 0.1), (ox, oy - 2.0, oz + 3.65))):
        box("sf_" + n, sz, lc, C("dff0f5" if n != "ceil" else "f4f4f4", 0.8))
    for k in range(3): light_panel(f"sf_light{k}", (ox - 4 + k * 4, oy, oz + 3.58), (1.4, 0.6))
    tex_quad("sf_banner", 5.2, 1.11, "tm04_fair_banner.png", (ox, oy + 4.5, oz + 2.75), (R(90), 0, 0))
    # art-room leftovers: easels + paint splats + windows
    for k, x in enumerate((-5.3, 5.3)):
        box(f"sf_easel{k}", (0.06, 0.06, 1.6), (ox + x, oy + 3.6, oz + 0.8), C("8a5a33", 0.6)).rotation_euler = (R(-10), 0, 0)
        box(f"sf_canvas{k}", (0.7, 0.03, 0.6), (ox + x, oy + 3.45, oz + 1.25), C(("f39c12", "8e44ad")[k], 0.9)).rotation_euler = (R(-10), 0, 0)
    for k in range(5): box(f"sf_splat{k}", (0.5, 0.01, 0.35), (ox - 4.5 + k * 2.2, oy + 4.52, oz + 1.2), C(("e74c3c", "3498db", "f1c40f", "2ecc71", "9b59b6")[k], 0.9))
    for k in range(3): box(f"sf_win{k}", (0.05, 1.4, 1.2), (ox + 6.12, oy - 2.5 + k * 2.2, oz + 1.9), C("8fb8d8", 0.1))
    # back row of projects
    for k, (x, img, cl) in enumerate(((-3.6, "tm04_tri0.png", "27ae60"), (0.0, "tm04_tri1.png", "c0392b"), (3.6, "tm04_tri2.png", "8e44ad"))):
        fair_table(f"sf_back{k}", ox + x, oy + 3.4, C, cl); trifold(f"sf_trib{k}", ox + x, oy + 3.62, oz + 0.79, img)
    for k in range(4): _cyl(f"sf_plant{k}", 0.06, 0.12, (ox - 4.2 + k * 0.3, oy + 3.25, oz + 0.85), C("f4f4f4", 0.5)); _sph(f"sf_leaf{k}", 0.07 + k * 0.015, (ox - 4.2 + k * 0.3, oy + 3.25, oz + 0.97 + k * 0.02), C("3f8a3f", 0.8), 8, 6)
    box("sf_oven", (0.5, 0.4, 0.25), (ox + 0.3, oy + 3.3, oz + 0.92), C("1b1b1b", 0.3)); box("sf_ovenfoil", (0.46, 0.02, 0.3), (ox + 0.3, oy + 3.08, oz + 1.05), C("dfe6ee", 0.15)).rotation_euler = (R(30), 0, 0)
    for k in range(5): _cyl(f"sf_magnet{k}", 0.05, 0.03, (ox + 3.3 + k * 0.15, oy + 3.25, oz + 0.8), C(("c0392b", "2980b9")[k % 2], 0.4))
    # solar system mobile hanging from the ceiling
    box("sf_mobilebar", (2.4, 0.03, 0.03), (ox - 0.8, oy + 1.8, oz + 3.3), C("9aa0a6", 0.3))
    for k, (r, col) in enumerate(((0.22, "f1c40f"), (0.06, "95a5a6"), (0.09, "e67e22"), (0.1, "3498db"), (0.08, "c0392b"), (0.17, "d68a2e"))):
        x = ox - 1.9 + k * 0.45; zz = oz + 2.75 - (k % 2) * 0.15
        box(f"sf_string{k}", (0.006, 0.006, oz + 3.3 - zz), (x, oy + 1.8, (oz + 3.3 + zz) / 2), C("dddddd", 0.6)); _sph(f"sf_planet{k}", r, (x, oy + 1.8, zz), C(col, 0.6), 12, 8)
    # table A (Tyler: lie detector) and table B (Bryce: volcano)
    A = (ox + 1.2, oy + 0.6); B = (ox - 2.6, oy + 0.6)
    fair_table("sf_tableA", *A, C, "2c3e50"); fair_table("sf_tableB", *B, C, "c0703f")
    LD = empty("sf_ld", (A[0] - 0.45, A[1] - 0.05, oz + 0.785))
    box("sf_ldbox", (0.6, 0.4, 0.34), (0, 0, 0.17), C("c8a06a", 0.9), LD, 0.01, 1)
    tex_quad("sf_ldlabel", 0.56, 0.19, "tm04_liedetector.png", (0, -0.202, 0.12), (R(90), 0, 0)).parent = LD
    gb = _sph("sf_bulbG", 0.06, (-0.14, -0.05, 0.38), mat("sf_green", srgb("2ecc71"), 0.2, emit=0.0), 12, 8, LD)
    rb = _sph("sf_bulbR", 0.06, (0.14, -0.05, 0.38), mat("sf_red", srgb("e74c3c"), 0.2, emit=0.0), 12, 8, LD)
    _cyl("sf_dial", 0.08, 0.01, (0, -0.205, 0.27), C("f4f4f4", 0.5), (R(90), 0, 0), 16, LD)
    needle = box("sf_needle", (0.008, 0.004, 0.07), (0, -0.212, 0.29), C("c0392b", 0.4), LD)
    for k in range(2): box(f"sf_wire{k}", (0.012, 0.6, 0.012), (-0.36 - k * 0.05, -0.15, 0.02), C(("e74c3c", "1b1b1b")[k], 0.5), LD).rotation_euler = (0, 0, R(30 + k * 10))
    box("sf_stoolA", (0.4, 0.4, 0.06), (A[0] - 1.55, A[1] - 0.05, oz + 0.47), C("2c3e50", 0.5)); box("sf_stoolAleg", (0.06, 0.06, 0.45), (A[0] - 1.55, A[1] - 0.05, oz + 0.22), C("9aa0a6", 0.3))
    VB = (B[0] + 0.1, B[1] + 0.05, oz + 0.785)
    bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.32, radius2=0.08, depth=0.42, location=(VB[0], VB[1], VB[2] + 0.21)); v = bpy.context.active_object
    v.name = "sf_volcano"; v.data.materials.append(C("7a5230", 0.9))
    _sph("sf_lava", 0.09, (VB[0], VB[1], VB[2] + 0.44), mat("sf_lavam", srgb("ff5a1a"), 0.3, emit=2.0), 10, 6, None, (1, 1, 0.6))
    box("sf_volcanobase", (0.8, 0.6, 0.03), (VB[0], VB[1], VB[2] + 0.015), C("3f8a3f", 0.8))
    tex_quad("sf_japan", 0.36, 0.15, "tm04_japan.png", (VB[0], VB[1] - 0.305, VB[2] + 0.09), (R(90), 0, 0))
    trifold("sf_triB", B[0] - 0.5, B[1] + 0.25, oz + 0.79, "tm04_tri1.png")
    # visitors' rope + stacked chairs, judge score table at the side
    for k in range(5): chair(f"sf_vchair{k}", ox + 5.0, oy - 2.5 + k * 0.55, oz, "4a90c2", C, -90)
    return dict(A=A, B=B, ld=LD, bulbG=gb, bulbR=rb, needle=needle, volcano=VB, stool=(A[0] - 1.55, A[1] - 0.05))
