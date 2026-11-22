"""mix_episode.py — mix narration + the SHARED music bed (+ optional SFX) for any Dark Atlas episode.
No new music generation needed: the bed is assets/music/dark_bed_master_5min.wav (seamless loop, 73 s cycle).
Usage: python -I mix_episode.py VOICE OUT.wav DURATION_S [--offset SEC] [--sfx SFX.wav]
  --offset: where to start inside the 5-min bed (default = hash of the voice file name, so each episode
            starts at a different place in the loop and does not sound identical).
Levels measured on V01-V03: during narration pauses the mix only drops 1-4 dB (pause level ~-17..-20 dB) -> bed at -21 LUFS before the final -16 LUFS normalisation.
"""
import sys, os, argparse, subprocess, zlib
ap = argparse.ArgumentParser(); ap.add_argument("voice"); ap.add_argument("out"); ap.add_argument("dur", type=float)
ap.add_argument("--offset", type=float); ap.add_argument("--sfx"); ap.add_argument("--sfx_gain", type=float, default=0.55)
ap.add_argument("--bed", default="dark_bed_master_5min.wav", help="file in assets/music: dark_bed_master_5min.wav (country series) | us_bed_master_5min.wav (US states series)")
ap.add_argument("--bed_lufs", type=float, default=-25.0, help="bed level before the final -16 LUFS normalisation (lower = quieter music)")
a = ap.parse_args()
BED = os.path.join(os.path.dirname(__file__), "..", "assets", "music", a.bed)
off = a.offset if a.offset is not None else (zlib.crc32(os.path.abspath(a.voice).replace("\\", "/").split("/")[-2].encode()) % 200)  # hash of the EPISODE folder (all voices are named voice_milo.mp3)
off = min(off, 300 - a.dur - 1)
inputs = ["-i", a.voice, "-ss", f"{off:.2f}", "-i", BED]
fc = (f"[0:a]aresample=44100,pan=stereo|c0=c0|c1=c0[v];"
      f"[1:a]aresample=44100,loudnorm=I={a.bed_lufs:.1f}:TP=-4,afade=t=in:d=0.3,afade=t=out:st={a.dur - 0.9:.2f}:d=0.9,atrim=0:{a.dur:.2f}[b];")
mix = "[v][b]"; n = 2
if a.sfx:
    inputs += ["-i", a.sfx]; fc += f"[2:a]aresample=44100,volume={a.sfx_gain}[s];"; mix += "[s]"; n = 3
fc += f"{mix}amix=inputs={n}:duration=longest:normalize=0,atrim=0:{a.dur:.2f},loudnorm=I=-16:TP=-1.5:LRA=7[a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[a]", "-ar", "44100", "-c:a", "pcm_s16le", a.out], check=True)
# one-pass loudnorm lands ~0.5-1 dB low on dynamic mixes: measure, correct, limit true peak to about -1.5 dB
import re, shutil
m = re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run(["ffmpeg", "-nostats", "-i", a.out, "-filter_complex", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)
if m and abs(float(m[-1]) + 16) > 0.2:
    tmp = a.out + ".tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.out, "-af", f"volume={-16 - float(m[-1]):.2f}dB,alimiter=limit=0.80:level=false", "-c:a", "pcm_s16le", tmp], check=True)
    shutil.move(tmp, a.out)
print(f"mixed {a.out} (bed {a.bed} at {a.bed_lufs} LUFS, offset {off:.1f}s)")
