"""sonic_tts.py — Sonic Voice (sonicvoice.pro) API client for narration.

The API key is read ONLY from the environment variable SONIC_API_KEY (never from files or arguments) and is never
printed. Set it once in PowerShell:  setx SONIC_API_KEY "wp_..."  then restart the app/terminal.

Usage:
  python sonic_tts.py balance
  python sonic_tts.py voice VOICE_ID                      # show voice details (provider, language, name)
  python sonic_tts.py models [eleven|mini]
  python sonic_tts.py estimate TEXT_FILE [--model eleven_v4]   # characters x credit_ratio, no job created
  python sonic_tts.py speak TEXT_FILE OUT.(wav|mp3) --voice VOICE_ID [--provider eleven] [--model eleven_v4]
                      [--language English] [--speed 1.0] [--stability 0.5] [--similarity 0.75] [--srt]
Docs: https://sonicvoice.pro/api (pasted by the user 12/11/2026)."""
import os, sys, time, json, argparse
import requests

BASE = "https://sonicvoice.pro/api"

def session():
    key = os.environ.get("SONIC_API_KEY")
    if not key and sys.platform == "win32":          # setx writes to HKCU; read it even if this process predates it
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k: key = winreg.QueryValueEx(k, "SONIC_API_KEY")[0]
        except OSError: key = None
    if not key: sys.exit("SONIC_API_KEY chưa được đặt. Chạy: setx SONIC_API_KEY \"wp_...\" rồi mở lại terminal.")
    s = requests.Session(); s.headers["X-API-Key"] = key; return s

def die(r):
    msg = {401: "sai/thiếu khoá", 402: "không đủ ký tự", 404: "không tìm thấy", 422: "tham số không hợp lệ", 429: "quá nhiều request"}.get(r.status_code, "")
    try: body = r.json()
    except Exception: body = r.text[:300]
    sys.exit(f"HTTP {r.status_code} {msg}: {body}")

def get(s, path, **params):
    r = s.get(BASE + path, params=params, timeout=60)
    if not r.ok: die(r)
    return r.json()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("args", nargs="*")
    ap.add_argument("--voice"); ap.add_argument("--provider", default="eleven"); ap.add_argument("--model", default="eleven_v4")
    ap.add_argument("--language", default="English"); ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--stability", type=float, default=0.5); ap.add_argument("--similarity", type=float, default=0.75)
    ap.add_argument("--srt", action="store_true"); ap.add_argument("--title")
    a = ap.parse_args(); s = session()

    if a.cmd == "balance":
        print(json.dumps(get(s, "/v1/me/balance"), ensure_ascii=False)); return
    if a.cmd == "voice":
        print(json.dumps(get(s, f"/v1/voices/{a.args[0]}"), ensure_ascii=False, indent=1)); return
    if a.cmd == "models":
        p = {"provider": a.args[0]} if a.args else {}
        for m in get(s, "/v1/models", **p): print(m["model_id"], m.get("provider"), "ratio", m["credit_ratio"], "max", m.get("max_chars"))
        return
    text = open(a.args[0], encoding="utf-8").read().strip()
    if a.cmd == "estimate":
        ratio = next((m["credit_ratio"] for m in get(s, "/v1/models", provider=a.provider) if m["model_id"] == a.model), None)
        bal = get(s, "/v1/me/balance")
        print(json.dumps(dict(chars=len(text), model=a.model, credit_ratio=ratio, est_cost=None if ratio is None else round(len(text) * ratio),
                              available_chars=bal["available_chars"]))); return
    if a.cmd == "speak":
        if not a.voice: sys.exit("--voice bắt buộc")
        payload = dict(kind="single", provider=a.provider, voice_id=a.voice, text=text, language=a.language, speed=a.speed,
                       srt_out=a.srt, title=a.title or os.path.basename(a.args[1]))
        if a.provider == "eleven": payload.update(model=a.model, stability=a.stability, similarity_boost=a.similarity)
        r = s.post(BASE + "/v1/tts/jobs", json=payload, timeout=60)
        if not r.ok: die(r)
        job = r.json(); print("job", job["id"], "cost_chars", job.get("cost_chars"), flush=True)
        t0 = time.time()
        while job["status"] in ("admitted", "running"):
            if time.time() - t0 > 600: sys.exit("quá 10 phút chưa xong")
            time.sleep(3); job = get(s, f"/v1/tts/jobs/{job['id']}")
            print(f"  {job['progress_done']}/{job['progress_total']} {job['status']}", flush=True)
        if job["status"] != "succeeded": sys.exit(f"Thất bại ({job['status']}): {job.get('error')}")
        r = s.get(BASE + f"/v1/tts/jobs/{job['id']}/audio", timeout=120)
        if not r.ok: die(r)
        raw = a.args[1] + ".download"; open(raw, "wb").write(r.content)
        os.replace(raw, a.args[1])
        if a.srt:
            r = s.get(BASE + f"/v1/tts/jobs/{job['id']}/srt", timeout=60)
            if r.ok: open(os.path.splitext(a.args[1])[0] + ".srt", "w", encoding="utf-8").write(r.text)
        json.dump(dict(job_id=job["id"], voice=a.voice, provider=a.provider, model=a.model, cost_chars=job.get("cost_chars"),
                       chars=len(text), created=job.get("created_at")), open(os.path.splitext(a.args[1])[0] + ".job.json", "w"), indent=1)
        print("saved", a.args[1]); return
    sys.exit("lệnh không hợp lệ")

if __name__ == "__main__":
    main()
