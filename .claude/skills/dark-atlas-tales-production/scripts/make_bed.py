"""make_bed.py — synthesize a dark ambient bed + sparse SFX for the demo (no external assets).
Usage: python -I make_bed.py OUT.wav DURATION_S [hit_time ...]
Bed: low detuned drone (A1/E2) + band-limited air noise with slow swell, matching the reference's
continuous bed (~7 dB under voice, no silence). hit_time: soft low boom + reverse-swell into it."""
import sys, numpy as np, soundfile as sf
sr = 44100
out, dur = sys.argv[1], float(sys.argv[2]); hits = [float(x) for x in sys.argv[3:]]
n = int(sr * dur); t = np.arange(n) / sr
rng = np.random.default_rng(1)

def lp(x, a):  # one-pole lowpass, a in (0,1)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y

lfo = 0.6 + 0.4 * np.sin(2 * np.pi * t / 9.0)
drone = sum(np.sin(2 * np.pi * f * t + p) * g for f, p, g in [(55, 0, 0.5), (55.4, 1, 0.5), (82.4, 2, 0.28), (110.3, .5, 0.12), (164.8, 3, 0.05)])
drone *= lfo
noise = rng.standard_normal(n)
air = lp(noise, 0.06) - lp(noise, 0.01)          # rough band-pass ~ 100-400 Hz rumble/air
hiss = lp(noise, 0.35) * 0.15
bed = drone * 0.5 + air * 1.6 * (0.7 + 0.3 * np.sin(2 * np.pi * t / 13 + 1)) + hiss
for h in hits:
    i = int(h * sr)
    L = int(sr * 2.5); k = np.arange(L) / sr
    boom = np.sin(2 * np.pi * (48 - 14 * k) * k) * np.exp(-k * 2.2) * 2.2
    seg = boom[: max(0, min(L, n - i))]; bed[i:i + len(seg)] += seg
    S0 = int(sr * 1.2); j0 = max(0, i - S0)                     # reverse swell into the hit
    sw = lp(rng.standard_normal(i - j0), 0.12) * np.linspace(0, 1, i - j0) ** 3 * 1.4
    bed[j0:i] += sw
fade = np.minimum(1, np.minimum(t / 0.4, (dur - t) / 0.8))
bed *= fade
bed /= np.abs(bed).max() + 1e-9
sf.write(out, np.stack([bed, bed], 1) * 0.8, sr)
print("wrote", out)
