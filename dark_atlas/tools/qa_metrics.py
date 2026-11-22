# qa_metrics.py — pacing/speech metrics vs the 3 references. Run from DA/: python -I tools/qa_metrics.py "EP02|EP02_x/EP02.mp4|EP02_x/voice_milo_transcript.json"
import cv2, numpy as np, json, sys, subprocess
def cuts(path):
    cap=cv2.VideoCapture(path); prev=None; d=[]; mot=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        g=cv2.resize(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY),(90,160)).astype(np.float32); g[80:115]=0
        if prev is not None: d.append(np.abs(g-prev).mean())
        prev=g
    d=np.array(d); n=len(d)+1
    hard=[(k+1)/30 for k in range(len(d)) if d[k]>6 and d[k]>=d[max(0,k-2):k+3].max()]
    # dissolve: runs of 5+ frames with diff 1.2-6
    el=(d>1.0)&(d<6); runs=[];i=0
    while i<len(d):
        if el[i]:
            j=i
            while j<len(d) and el[j]: j+=1
            if j-i>=6: runs.append((i/30,j/30))
            i=j
        else: i+=1
    seg=np.diff([0]+hard+[n/30])
    still=np.mean(d<0.05)   # fraction of frames with almost no change
    return dict(dur=n/30,cuts=len(hard),shot_mean=round(seg.mean(),2),shot_max=round(seg.max(),2),moves_or_dissolves=len(runs),static_frac=round(float(still),3))
def speech(tr):
    w=[x for s in json.load(open(tr,encoding='utf-8')) for x in s['words']]
    gaps=[b['s']-a['e'] for a,b in zip(w[:-1],w[1:])]
    big=[g for g in gaps if g>0.35]
    return dict(words=len(w),wpm=round(len(w)/((w[-1]['e']-w[0]['s'])/60)),pauses=len(big),pause_mean=round(float(np.mean(big)),2),first_word=round(w[0]['s'],2),tail=None)
if __name__ == "__main__":
  for name,vid,tr in [("V01","refs/V01_mother_calls.mp4","analysis/V01_mother_calls_transcript.json"),("V02","refs/V02_ticking_roof.mp4","analysis/V02_ticking_roof_transcript.json"),("V03","refs/V03_look_at_feet.mp4","analysis/V03_look_at_feet_transcript.json"),*[tuple(a.split("|")) for a in __import__("sys").argv[1:]]]:
      if not (__import__("os").path.exists(vid) and __import__("os").path.exists(tr)): continue   # reference videos are not shipped in the hand-off kit
      c=cuts(vid); s=speech(tr)
      print(name, c, s)
