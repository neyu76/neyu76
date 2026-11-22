"""build_sfx.py — place library SFX on a timeline with automatic ducking under the narration.
Usage: python -I build_sfx.py EP_DIR cues.json OUT.wav
cues.json: {"duration": 73.45, "cues": [{"file": "horror/sub_boom.mp3", "t": 6.42, "db": -3, "duck": 10, "pitch": 0, "len": null, "loop": false}, ...]}
  file  : path under assets/sfx/
  t     : start time (s);  db: gain;  duck: dB of reduction while Milo is speaking (0 = none)
  pitch : semitones (vary repeated sounds between episodes);  len: cut to N seconds (fade 0.3 s);  loop: repeat to len
Voice activity comes from the episode's voice_milo.mp3 (smoothed RMS), so SFX sit in the pauses and dip under words.
"""
import sys, os, json, subprocess, numpy as np, wave
SR = 44100
EPD, CUES, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
LIB = os.path.join(os.path.dirname(__file__), "..", "assets", "sfx")
cfg = json.load(open(CUES, encoding="utf-8")); dur = cfg["duration"]; n = int(dur * SR)

def load(path, pitch=0.0):
    af = []
    if pitch: af.append(f"asetrate={SR}*{2 ** (pitch / 12):.5f},aresample={SR}")
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-af", ",".join(af)] if af else []) + ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).copy()

v = load(os.path.join(EPD, "voice_milo.mp3"))
win = int(0.05 * SR); env = np.sqrt(np.convolve(v[:n] ** 2, np.ones(win) / win, "same")) if len(v) else np.zeros(n)
env = np.pad(env, (0, max(0, n - len(env))))[:n]
env = np.clip(env / (np.percentile(env[env > 1e-4], 60) + 1e-9), 0, 1)
k = int(0.25 * SR); env = np.convolve(env, np.ones(k) / k, "same")                       # smooth attack/release
out = np.zeros(n, np.float32)
for c in cfg["cues"]:
    x = load(os.path.join(LIB, c["file"]), c.get("pitch", 0))
    L = c.get("len")
    if L:
        m = int(L * SR)
        if c.get("loop") and len(x) < m: x = np.tile(x, m // len(x) + 1)
        x = x[:m]; f = min(len(x), int(0.3 * SR)); x[-f:] *= np.linspace(1, 0, f)
    i = int(c["t"] * SR); j = min(n, i + len(x)); x = x[: j - i] * 10 ** (c.get("db", 0) / 20)
    d = c.get("duck", 0)
    if d: x = x * (1 - (1 - 10 ** (-d / 20)) * env[i:j])
    out[i:j] += x
pk = np.abs(out).max(); out = out / pk * 0.9 if pk > 0.9 else out
w = wave.open(OUT, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.column_stack([out, out]) * 32767).astype(np.int16).tobytes()); w.close()
print("wrote", OUT, "cues", len(cfg["cues"]), "peak", round(float(pk), 2))
