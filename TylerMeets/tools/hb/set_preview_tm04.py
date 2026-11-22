"""Preview TM04 empty sets. blender -b --python tools/hb/set_preview_tm04.py -- <ABSOLUTE out_dir>"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib, hb_lib, hb_props, hb_sets4, hb_sets5, hb_sets6
for m in (hb_lib, hb_props, hb_sets4, hb_sets5, hb_sets6): importlib.reload(m)
from hb_lib import *
from hb_sets6 import court, music_room, school_store, science_fair
OUT = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True); render_setup(samples=16)
CT, MU, ST, SF = 390, 420, 450, 480
court((CT, 0, 0)); music_room((MU, 0, 0)); school_store((ST, 0, 0)); science_fair((SF, 0, 0)); lights((0, 0, 0))
for nm, loc, en, sz in (("fill_mu", (MU, -1, 3.2), 900, 6), ("fill_st", (ST, -1, 3.0), 600, 5), ("fill_sf", (SF, -1, 3.4), 1000, 7)):
    L = bpy.data.lights.new(nm, "AREA"); L.energy = en; L.size = sz; fo = bpy.data.objects.new(nm, L); bpy.context.scene.collection.objects.link(fo); fo.location = loc
W = bpy.context.scene.world.node_tree.nodes["Background"]
cam, tgt = camera("cam", 22); sc = bpy.context.scene; sc.camera = cam
sc.render.resolution_x, sc.render.resolution_y = 360, 640
for name, p, l, out in (("ct", (CT + 1.5, -5.5, 2.2), (CT, 4.0, 1.8), True), ("mu", (MU + 1.0, -5.0, 2.0), (MU, 2.0, 1.2), False),
                        ("st", (ST - 0.5, -4.5, 1.8), (ST, 1.8, 1.1), False), ("sf", (SF - 0.5, -5.0, 2.0), (SF, 1.5, 1.0), False)):
    if out: W.inputs[0].default_value = (0.42, 0.62, 0.92, 1); W.inputs[1].default_value = 0.75
    else: W.inputs[0].default_value = (0.85, 0.82, 0.78, 1); W.inputs[1].default_value = 0.55
    cam_key(cam, tgt, 1, p, l, 18); sc.frame_set(1); sc.render.filepath = os.path.join(OUT, name + ".png"); bpy.ops.render.render(write_still=True)
print("PREVIEW OK")
