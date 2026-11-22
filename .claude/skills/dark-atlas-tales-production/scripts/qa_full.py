"""qa_full.py — one-shot QA for a finished episode against the format tolerances (references/qa_checklist.md).
Usage (from DA/): python -I tools/qa_full.py EPxx_name/EPxx_Final.mp4
Reads EPxx_name/voice_milo_transcript.json, prints every metric with PASS/FAIL and writes EPxx_name/qa_sheet.jpg (1 fps)."""
import sys, os, json, re, subprocess, numpy as np
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
sys.path.insert(0, os.path.dirname(__file__))
from qa_metrics import cuts, speech  # noqa: E402  (module also runs its reference loop; harmless when refs are absent)
vid = sys.argv[1]; ep = os.path.dirname(vid); tr = os.path.join(ep, "voice_milo_transcript.json")
c = cuts(vid); sp = speech(tr)
er = subprocess.run(["ffmpeg", "-nostats", "-i", vid, "-filter_complex", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", er)[-1]); peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", er)[-1])
sil = subprocess.run(["ffmpeg", "-i", vid, "-af", "silencedetect=n=-45dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr.count("silence_start")
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", vid, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16).astype(np.float32) / 32768
W = [w for s in json.load(open(tr, encoding="utf-8")) for w in s["words"]]; m = np.zeros(len(a), bool)
for w in W: m[int(w["s"] * 16000):int(w["e"] * 16000)] = True
e = int(W[-1]["e"] * 16000); db = lambda x: 10 * np.log10(np.mean(x ** 2) + 1e-12); sp_gap = db(a[:e][m[:e]]) - db(a[:e][~m[:e]])
rows = [("Thời lượng (s)", c["dur"], 68, 78), ("Số lần cắt", c["cuts"], 26, 34), ("Cảnh trung bình (s)", c["shot_mean"], 2.1, 2.7), ("Cảnh dài nhất (s)", c["shot_max"], 0, 7),
        ("Khung đứng yên", c["static_frac"], 0.0001, 1), ("Từ/phút", sp["wpm"], 138, 152), ("Khoảng nghỉ > 0,35 s", sp["pauses"], 0, 18),
        ("LUFS", lufs, -16.5, -15.5), ("Đỉnh (dBFS)", peak, -99, -1.0), ("Nói − nghỉ (dB)", round(sp_gap, 1), 1, 5), ("Đoạn lặng < −45 dB", sil, 0, 0)]
ok = True
for name, v, lo, hi in rows:
    good = lo <= v <= hi; ok &= good; print(f"{'PASS' if good else 'FAIL'}  {name:22s} {v}   (cho phép {lo}–{hi})")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-vf", "fps=1,scale=180:-1,tile=10x8", "-frames:v", "1", os.path.join(ep, "qa_sheet.jpg")])
print("=> ĐẠT" if ok else "=> CHƯA ĐẠT — sửa rồi đo lại", "| bảng khung 1 fps:", os.path.join(ep, "qa_sheet.jpg"))
