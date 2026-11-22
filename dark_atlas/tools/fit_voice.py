"""fit_voice.py — bring a Milo narration into the format's window (68–78 s, 140–150 wpm) WITHOUT regenerating it.
Usage: python -I fit_voice.py IN.mp3 OUT.mp3 [--keep "4.56:0.6,12.77:0.6"] [--cap 0.33] [--tempo 0.97]
- Every pause longer than --cap (detected at -40 dB, >= 0.4 s) is shortened to --cap, centred so breaths/tails survive.
- --keep: pauses (start time in the ORIGINAL file : length) that stay longer for drama (pre-hook, pre-title, before the twist).
- --tempo: final atempo (pitch preserved), e.g. 0.97 to slow down after trimming, 1.03 to speed up.
Then re-transcribe (transcribe.py) and diff against the script (check_transcript.py)."""
import argparse, subprocess, re, numpy as np, soundfile as sf, os, tempfile
ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out"); ap.add_argument("--keep", default=""); ap.add_argument("--cap", type=float, default=0.33); ap.add_argument("--tempo", type=float, default=1.0)
a = ap.parse_args(); SR = 44100
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.inp, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
log = subprocess.run(["ffmpeg", "-i", a.inp, "-af", "silencedetect=n=-40dB:d=0.4", "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", log)]; en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", log)]
keep = {float(k): float(v) for k, v in (p.split(":") for p in a.keep.split(",") if p)}
out = []; cur = 0.0
for s, e in zip(st, en):
    tgt = next((v for k, v in keep.items() if abs(k - s) < 0.08), a.cap)
    if e - s <= tgt: continue
    mid = (s + e) / 2; out.append(x[int(cur * SR):int((mid - tgt / 2) * SR)]); cur = mid + tgt / 2
out.append(x[int(cur * SR):]); y = np.concatenate(out)
tmp = os.path.join(tempfile.gettempdir(), "fit_voice_tmp.wav"); sf.write(tmp, y, SR)
af = ["-af", f"atempo={a.tempo}"] if abs(a.tempo - 1) > 1e-3 else []
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp] + af + ["-b:a", "192k", a.out], check=True); os.remove(tmp)
print("pauses found %d, %.2f s -> %.2f s (before tempo), tempo %.3f -> ~%.2f s" % (len(st), len(x) / SR, len(y) / SR, a.tempo, len(y) / SR / a.tempo))
