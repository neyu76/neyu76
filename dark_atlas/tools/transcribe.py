import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=8)
for f in sys.argv[2:]:
    raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32)/32768
    segs, info = m.transcribe(audio, language="en", word_timestamps=True)
    out = [dict(start=s.start, end=s.end, text=s.text.strip(), words=[dict(w=w.word, s=w.start, e=w.end) for w in s.words]) for s in segs]
    name = f.replace("\\","/").split("/")[-1].rsplit(".",1)[0]
    json.dump(out, open(f"{sys.argv[1]}/{name}_transcript.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    w=[x for s in out for x in s['words']]
    print("==",name, "words",len(w), "first %.2f last %.2f wpm %d"%(w[0]['s'],w[-1]['e'],len(w)/((w[-1]['e']-w[0]['s'])/60)))
    for s in out: print("%6.2f-%6.2f %s"%(s['start'],s['end'],s['text']))
