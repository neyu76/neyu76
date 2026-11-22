import json, os
p = "episodes/TM04/timeline.json"; T = json.load(open(p, encoding="utf-8"))
C, ST = "work/tm04/clips", "work/tm04/inserts"
STILL = {"INS_PHONE_BURGER": "phone_burger.png"}
for s in T["shots"]:
    k = s["key"]
    if k in STILL: s.update(kind="still", src=f"{ST}/{STILL[k]}", push=1.045)
    else:
        d = f"{C}/{s['id']}_{k}"; assert os.path.isdir(d), d; s.update(kind="frames", src=d, push=1.0)
# Linux cloud machine: Arial Black is not installed -> Montserrat Black (same heavy caption look); Windows keeps Arial Black
FONT = next((f for f in ("/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf", "C:/Windows/Fonts/ariblk.ttf") if os.path.exists(f)), None)
T.update(words="episodes/TM04/audio/vo16k.cap.json", caption_style="hb", music="assets/music/bed_main_V07.wav", music_gain_db=-9.5, tail=0.6,
         font=FONT, hb_font=FONT,
         keywords=["Bro-bro-bro,", "Miami!", "yesterday,", "bro!", "Bryce.", "never", "truth.", "math", "class.", "dunked", "pro.", "Twice.",
                   "rim.", "ball", "face.", "Second", "Music.", "toured", "band.", "Drums,", "bass,", "piano.", "everything.", "recorder.",
                   "Fweee!", "FWEEEE!", "note.", "smoke", "alarm.", "school", "store.", "sandwich.", "allergic", "bread.", "Allergic.", "burger",
                   "pay.", "back.", "Relax.", "salad.", "sandwich.", "Science", "fair.", "lie", "detector.", "Miami?", "Obviously,", "Green",
                   "light.", "Nothing.", "yourself?", "yes.", "off.", "Disqualified.", "judge.", "first", "place.", "detention.", "salad."])
json.dump(T, open(p, "w", encoding="utf-8"), indent=1); print("timeline ready", len(T["shots"]), "shots")
