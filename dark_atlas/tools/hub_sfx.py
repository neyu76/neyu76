"""hub_sfx.py — generate a monster SFX via the ThuyenMCP ElevenLabs proxy (replaces Magnific audio_sfx_generate).

Usage (from dark_atlas/):
  python -I tools/hub_sfx.py OUT.mp3 "prompt describing the sound" --dur 2.5 [--influence 0.5]

COSTS ElevenLabs credits — quote the user first (kit rule: 2-3 sounds x 2-3 s per new monster).
Auth: THUYENMCP_TOKEN (Bearer) or, in Claude cloud sessions, the network proxy injects it.
Save into assets/sfx/epXX_<name>/ and add a line to assets/sfx/README.md."""
import argparse, os, sys
import requests

BASE = os.environ.get("ELEVEN_BASE", "https://sound.thuyenlabs.io.vn/proxy/elevenlabs")
ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("prompt")
ap.add_argument("--dur", type=float, default=2.5); ap.add_argument("--influence", type=float, default=0.5)
a = ap.parse_args()
h = {"Content-Type": "application/json", "Accept": "audio/mpeg"}
if os.environ.get("THUYENMCP_TOKEN"): h["Authorization"] = "Bearer " + os.environ["THUYENMCP_TOKEN"]
r = requests.post(BASE + "/v1/sound-generation", headers=h, timeout=180,
                  json=dict(text=a.prompt, duration_seconds=a.dur, prompt_influence=a.influence))
if not r.ok or not r.headers.get("content-type", "").startswith("audio"):
    sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, "wb").write(r.content); print("saved", a.out, len(r.content), "bytes")
