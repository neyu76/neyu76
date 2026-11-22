"""check_transcript.py — diff the whisper transcript against the script and flag suspicious words.
Usage: python -I check_transcript.py EP_DIR
Prints: word counts, every insert/delete/replace (with time), and words shorter than 0.1 s (whisper hallucinations).
Whisper splits "cross-legged" into "cross" + "-legged" and writes numbers as digits; that is handled.
Fix mismatches by editing voice_milo_transcript.json (re-transcribe the segment alone to get real timings), then build captions."""
import sys, os, json, difflib, re
ep = sys.argv[1]
W = [w for s in json.load(open(os.path.join(ep, "voice_milo_transcript.json"), encoding="utf-8")) for w in s["words"]]
norm = lambda s: "".join(c for c in s.lower() if c.isalnum())
NUM = {"fourteen": "14", "twelve": "12", "two hundred": "200"}
txt = open(os.path.join(ep, "script.txt"), encoding="utf-8").read()
for k, v in NUM.items(): txt = re.sub(r"\b%s\b" % k, v, txt, flags=re.I)
sw = [norm(t) for t in txt.replace("-", " -").split() if norm(t)]
tw = [norm(w["w"]) for w in W]
print("transcript words", len(tw), "| script words", len(sw))
bad = 0
for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, tw, sw).get_opcodes():
    if op != "equal":
        bad += 1; t = W[a1]["s"] if a1 < len(W) else W[-1]["e"]
        print(f"  {op:8s} at {t:6.2f}s  transcript={tw[a1:a2]}  script={sw[b1:b2]}")
short = [(w["w"].strip(), round(w["s"], 2)) for w in W if w["e"] - w["s"] < 0.1]
if short: print("  very short words (check):", short)
print("OK" if bad == 0 else f"{bad} mismatch(es) — fix the JSON before rendering")
