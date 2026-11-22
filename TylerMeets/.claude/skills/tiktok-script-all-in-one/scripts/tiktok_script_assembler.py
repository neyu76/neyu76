#!/usr/bin/env python3
"""
tiktok_script_assembler.py - TYLERMEETS v4.0-tm1 (from BASE_RAW v4.0). Profile: tylermeets-westbrook.
Part files use the kit shots.txt format:  L00 [BRY] beat / beat | KEY / KEY   (NARR = Tyler)
plus a sidecar PARTS/P0k.scenes.tsv:  KEY<TAB>SET<TAB>SHOT_DESCRIPTION
Subcommands: twin-seo-check, twin-5axis, init, verify-part, opening-audit, beat-audit, stitch-draft,
lock-export (01-04 TT files + 05-KIT-shots.txt + 06-KIT-SCENES.csv), fyp-diagnose. See SKILL.md.
"""

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROFILE_ID = "tylermeets-westbrook"
PROFILE_REVISION = 1
ASSEMBLER_VERSION = "4.0-tm1"

# ---------------- Channel locks (OWNER_LOCKED, from SKILL tyler-meets-homeboy-production v1.0) ----------------
WTF_LINE = "What the fuck is wrong with this dude?"
NARRATOR_CODE = "NARR"
KIT_LINE_GAP_SEC = 0.45      # sonicvoice_tts.py --gap 0.45
KIT_LAST_GAP_SEC = 1.0       # 1.0 s before the punchline line
KIT_TAIL_SEC = 0.6           # plan_shots.py end tail
KIT_MIN_SHOT_SEC = 0.9       # plan_shots.py merges shorter beats
SERIES_RUNTIME_WINDOW = (68.0, 77.0)   # MEASURED on TM01 76.6 s / TM02 76.3 s / TMG01 70.9 s
SIDE_LINE_MAX_WORDS = 8
KEY_RE = re.compile(r"^(OPEN|WIDE|MS|CU|INS|OTS|TWO_SHOT|POV)_[A-Z0-9_]+$")
LINE_RE = re.compile(r"^(L\d{2})\s+\[([A-Z0-9_]+)\]\s+(.+?)\s*\|\s*(.+)$")

# Sets already used by the series (never reuse as an episode set) — SKILL §6
USED_SETS = {
    "classroom", "cafeteria", "photo_studio", "detention_room",            # HB01-02
    "school_bus", "library",                                               # TM01
    "locker_hallway", "boys_bathroom", "gym_dance", "night_parking_lot",   # TM02
    "crosswalk_gate", "auditorium", "nurse_office", "outdoor_patio",       # TMG01
    "front_yard", "chem_lab", "computer_lab", "football_bleachers",        # TM03 (reserved, pending approval)
}
FREE_SETS = {
    "music_room", "pool", "art_room", "science_fair", "outdoor_basketball_court", "locker_room",
    "shuttle_van", "school_store", "rooftop", "bus_stop", "tyler_house",
}

# Own past hooks/titles (self-twin guard)
OWN_PAST_HOOKS = [
    "My homeboy posts sad stories while sitting RIGHT next to me",
    "My homeboy thinks he's the main character of every hallway",
    "My homeboy has been in GTA 6 for 31 hours he doesn't even own it",
    "Destiny wakes up mad at the world, Friend with an Attitude",
    "What the fuck is wrong with my homeboy, vending machine war",
]

# 5-Axis registry of the series' existing episodes
EPISODE_REGISTRY = [
    {"id": "TM01", "question": "why does he post sad stories about everything", "stage": "school bus library",
     "ladder": "sad stories multiply 14 stories in one period", "payoff": "tyler gets tagged as traitor in the story",
     "look": "beanie black hoodie broken heart phone raised"},
    {"id": "TM02", "question": "does the girl actually like the self proclaimed player", "stage": "locker hallway bathroom gym dance parking lot",
     "ladder": "selfies flirting louder claims at the party", "payoff": "the only girl is his cousin she was looking at the clock",
     "look": "wavy hair varsity jacket chewing gum"},
    {"id": "TMG01", "question": "how deep is he in the game addiction gta 6", "stage": "crosswalk gate golf cart auditorium nurse office outdoor patio",
     "ladder": "steals golf cart runs from stars asks nurse for armor", "payoff": "he does not even own the game watching a stream",
     "look": "dark circles gaming headset energy drink hoodie"},
    {"id": "TM03", "question": "why is she mad at everything attitude", "stage": "front yard chem lab computer lab football bleachers",
     "ladder": "snaps at greeting glares beaker boils mood swing with snacks", "payoff": "the attitude spreads to tyler",
     "look": "high bun plum hoodie dont airpod"},
]

FORBIDDEN_TAG_RE = re.compile(
    r"\[(sigh|laugh|gasp|whisper|pause|reset|cough|chuckle|cry|sob|breath|inhale|exhale|music|sfx)[^\]]*\]", re.I)
FORBIDDEN_PROSE_MARKERS_RE = re.compile(
    r"(https?://|\[HOOK[^\]]*\]|\[LOOP[^\]]*\]|\[CTA[^\]]*\]|\[SCENE[^\]]*\]|\[VISUAL[^\]]*\]|\[B-ROLL[^\]]*\]|\[DATA_CARD[^\]]*\])", re.I)
UNRESOLVED_EPISTEMIC_RE = re.compile(r"\[(GUESS|GỢI-Ý|GOI-Y|SUGGESTED_UNCONFIRMED|CẦN HỎI|CAN_HOI|NEEDS_CHECK)(?::[^\]]*)?\]", re.I)
AI_ESE_PUNCT_RE = re.compile(r"(—|→|–)")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
NUMBER_OR_CLOCK_RE = re.compile(r"\b(\d{1,2}:\d{2}|\d+(?:[.,]\d+)?%?)\b")
NUMBER_WORDS_RE = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|twenty|thirty|forty|fifty|hundred|thousand|first|second|third|fourth|fifth)\b", re.I)
PROFANITY_RE = re.compile(r"\b(fuck\w*|shit\w*|bitch\w*|damn|ass|asshole|motherfuck\w*)\b", re.I)

# FYP watchlist for a US teen-school comedy (rewrite naturally; profanity handled by PROFANITY_RE)
FYP_THROTTLE_WATCHLIST = {
    "kill": "take out / destroy (as joke verb, prefer 'cooked')",
    "die": "pass out / be done",
    "dead": "done / finished",
    "gun": "remove entirely",
    "shoot": "fire / launch",
    "suicide": "remove entirely",
    "vape": "remove entirely (minors + substance)",
    "weed": "remove entirely",
    "drunk": "remove entirely",
    "drugs": "remove entirely",
    "fight": "beef / argument",
    "blood": "remove entirely",
    "sexy": "remove entirely",
    "naked": "remove entirely",
    "scam": "hustle / shady deal",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_lf_utf8(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def count_units(text: str, unit_mode: str = "words") -> int:
    if unit_mode == "non_space_chars":
        return len(re.sub(r"\s+", "", text))
    return len(re.findall(r"\S+", text, flags=re.UNICODE))


def tokenize_text(text: str) -> set:
    return set(re.findall(r"[^\W_]+", text.lower(), flags=re.UNICODE))


def jaccard_similarity(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def scan_throttled_words(text: str) -> list:
    low = text.lower()
    return [{"flagged_term": t, "safer_natural_alternative": r}
            for t, r in FYP_THROTTLE_WATCHLIST.items() if re.search(r"\b" + re.escape(t) + r"\b", low)]


def parse_kit_lines(text: str, where: str) -> list:
    """Return list of dicts: line_id, speaker, beats[], keys[], spoken, raw."""
    out = []
    for n, raw in enumerate(normalize_lf_utf8(text).split("\n"), start=1):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        m = LINE_RE.match(raw)
        if not m:
            sys.exit(f"[BLOCKER] {where} line {n}: not in kit format 'Lxx [SPK] beat / beat | KEY / KEY': {raw[:90]}")
        lid, spk, text_part, keys_part = m.groups()
        beats = [b.strip() for b in text_part.split("/") if b.strip()]
        keys = [k.strip() for k in keys_part.split("/") if k.strip()]
        if len(keys) != len(beats):
            sys.exit(f"[BLOCKER] {where} {lid}: {len(beats)} beats but {len(keys)} scene keys (must match 1:1).")
        for k in keys:
            if not KEY_RE.match(k):
                sys.exit(f"[BLOCKER] {where} {lid}: scene key '{k}' must start with OPEN_/WIDE_/MS_/CU_/INS_/OTS_/TWO_SHOT_/POV_ and be UPPER_SNAKE.")
        out.append({"line_id": lid, "speaker": spk, "beats": beats, "keys": keys,
                    "spoken": " ".join(beats), "raw": raw})
    return out


def parse_scene_sidecar(path: Path) -> dict:
    if not path.exists():
        return {}
    rows = {}
    for n, raw in enumerate(normalize_lf_utf8(path.read_text(encoding="utf-8")).split("\n"), start=1):
        if not raw.strip() or raw.startswith("#"):
            continue
        cols = raw.split("\t")
        if len(cols) < 3:
            sys.exit(f"[BLOCKER] {path.name} row {n}: need KEY<TAB>SET<TAB>DESCRIPTION.")
        rows[cols[0].strip()] = {"set": cols[1].strip(), "description": cols[2].strip()}
    return rows


def split_sentences(text: str) -> list:
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]


def fyp_window_bucket(t: float) -> str:
    if t < 3.0:
        return "00_03s_FRAME0_SWIPE_GATE"
    if t < 15.0:
        return "03_15s_PREMISE_ANCHOR"
    if t < 30.0:
        return "15_30s_ESCALATION_ZONE"
    if t < 60.0:
        return "30_60s_CLIFF_BRIDGE"
    return "60s_PLUS_REWARDS_ZONE"


def timeline_from_lines(lines: list, state: dict) -> list:
    """Estimate per-beat timing with the kit's real gap model (0.45 s between lines, 1.0 s before the last line)."""
    rc = state["rate_spec"]["rate_center_upm"]
    t, rows = 0.0, []
    for i, ln in enumerate(lines):
        if i > 0:
            t += KIT_LAST_GAP_SEC if i == len(lines) - 1 else KIT_LINE_GAP_SEC
        for b, k in zip(ln["beats"], ln["keys"]):
            dur = count_units(b) / rc * 60.0
            rows.append({"line_id": ln["line_id"], "speaker": ln["speaker"], "beat": b, "key": k,
                         "start": t, "end": t + dur, "dur": dur})
            t += dur
    return rows


def non_speech_seconds(n_lines: int) -> float:
    if n_lines <= 1:
        return KIT_TAIL_SEC
    return KIT_LINE_GAP_SEC * (n_lines - 2) + KIT_LAST_GAP_SEC + KIT_TAIL_SEC


def runtime_estimates(lines: list, state: dict) -> dict:
    total_u = count_units(" ".join(l["spoken"] for l in lines))
    ns = non_speech_seconds(len(lines))
    rs = state["rate_spec"]
    return {"units": total_u, "non_speech": ns,
            "center": total_u / rs["rate_center_upm"] * 60 + ns,
            "fast": total_u / rs["rate_max_upm"] * 60 + ns,
            "slow": total_u / rs["rate_min_upm"] * 60 + ns}


# ---------------------------------------------------------------- commands
def cmd_twin_seo_check(args):
    cands = [c for c in (args.candidate or []) if c.strip()]
    if not cands:
        sys.exit("[ERROR] Provide at least one --candidate.")
    comps = [(r, tokenize_text(r)) for r in (args.competitor or []) if r.strip()]
    owns = [(o, tokenize_text(o)) for o in (OWN_PAST_HOOKS + (args.own_past or [])) if o.strip()]
    seo = [(k.strip(), tokenize_text(k)) for k in (args.seo_keywords or "").split(",") if k.strip()]
    results = []
    for c in cands:
        cs = tokenize_text(c)
        bc = max(((round(jaccard_similarity(cs, s), 4), r) for r, s in comps), default=(0.0, None))
        bo = max(((round(jaccard_similarity(cs, s), 4), o) for o, s in owns), default=(0.0, None))
        mj = max(bc[0], bo[0])
        verdict = ("HIGH_TWIN_CLONE_RISK (>0.55)" if mj > 0.55 else
                   "MODERATE_FAMILIAR_ANCHOR (0.30-0.55, confirm twin-5axis <= 2/5)" if mj >= 0.30 else
                   "CLEAR_DISTINCT_WORDING (<0.30)")
        results.append({"candidate": c, "max_competitor_jaccard": bc[0], "closest_competitor": bc[1],
                         "max_own_past_jaccard": bo[0], "closest_own_past": bo[1], "lexical_twin_verdict": verdict,
                         "tiktok_search_seo_matched": [k for k, s in seo if s and s <= cs],
                         "tiktok_search_seo_missing": [k for k, s in seo if s and not s <= cs],
                         "fyp_throttle_watchlist_hits": scan_throttled_words(c)})
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({"profile_id": PROFILE_ID, "candidates": results}, indent=2, ensure_ascii=False), encoding="utf-8")
    for r in results:
        print(f"[TT TWIN-SEO] '{r['candidate'][:70]}' -> Comp={r['max_competitor_jaccard']:.3f} Own={r['max_own_past_jaccard']:.3f} "
              f"| {r['lexical_twin_verdict']} | SEO={r['tiktok_search_seo_matched']} | Throttle={len(r['fyp_throttle_watchlist_hits'])}")


def cmd_twin_5axis(args):
    cand = {"question": args.question, "stage": args.stage, "ladder": args.ladder, "payoff": args.payoff, "look": args.look}
    th = float(args.axis_threshold)
    report, worst = [], 0
    for ep in EPISODE_REGISTRY:
        axes = {}
        for ax in cand:
            axes[ax] = round(jaccard_similarity(tokenize_text(cand[ax]), tokenize_text(ep[ax])), 3)
        hits = [ax for ax, v in axes.items() if v >= th]
        blocker = len(hits) >= 3 or ("question" in hits and "payoff" in hits)
        worst = max(worst, len(hits))
        report.append({"episode": ep["id"], "axis_similarity": axes, "matched_axes": hits,
                       "score_of_5": len(hits), "verdict": "TWIN_BLOCKER" if blocker else "CLEAR"})
    stage_sets = [s.strip() for s in (args.sets or "").split(",") if s.strip()]
    reused = [s for s in stage_sets if s in USED_SETS]
    unknown = [s for s in stage_sets if s not in USED_SETS and s not in FREE_SETS]
    overall = "TWIN_BLOCKER" if any(r["verdict"] == "TWIN_BLOCKER" for r in report) or reused else "CLEAR"
    payload = {"profile_id": PROFILE_ID, "candidate": cand, "sets": stage_sets, "reused_sets": reused,
               "new_sets_not_in_free_list": unknown, "per_episode": report, "overall_verdict": overall}
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    for r in report:
        print(f"[5-AXIS] vs {r['episode']}: {r['score_of_5']}/5 {r['matched_axes']} -> {r['verdict']}")
    print(f"[5-AXIS] sets reused={reused} new_unlisted={unknown} | OVERALL={overall}")
    if overall != "CLEAR" and not args.allow_exception:
        sys.exit("[TWIN BLOCKER] change Stage, Ladder or Payoff (not just synonyms).")


def cmd_init(args):
    ws = Path(args.workspace)
    (ws / "PARTS").mkdir(parents=True, exist_ok=True)
    budgets = [int(x) for x in args.part_budgets.split(",") if x.strip()]
    if not budgets:
        sys.exit("[BLOCKER] --part-budgets needs >= 1 integer.")
    if args.track == "creator_rewards" and len(budgets) < 2 and not args.allow_exception:
        sys.exit("[ANTI-SINGLE-SHOT BLOCKER] creator_rewards needs >= 2 parts (series default: 4 parts = 4 sets).")
    sets = [s.strip() for s in args.sets.split(",") if s.strip()]
    if len(sets) != len(budgets) and not args.allow_exception:
        sys.exit(f"[SERIES BLOCKER] One part per set: {len(budgets)} budgets but {len(sets)} sets.")
    reused = [s for s in sets if s in USED_SETS]
    if reused and not args.allow_exception:
        sys.exit(f"[SERIES BLOCKER] Sets already used by the series: {reused}.")
    cast = {}
    for pair in (args.cast or "").split(","):
        if "=" in pair:
            code, name = pair.split("=", 1)
            cast[code.strip().upper()] = name.strip()
    hero = args.hero.upper()
    if hero not in cast:
        sys.exit(f"[BLOCKER] --hero {hero} must be declared in --cast (e.g. BRY=Bryce).")
    cast[NARRATOR_CODE] = "Tyler"

    total = sum(budgets)
    ns = non_speech_seconds(int(args.est_lines))
    rc, rmin, rmax = float(args.rate), float(args.rate_min), float(args.rate_max)
    c, f, s = total / rc * 60 + ns, total / rmax * 60 + ns, total / rmin * 60 + ns
    if args.track == "creator_rewards" and f < 62.0 and not args.allow_exception:
        sys.exit(f"[MONETIZATION BLOCKER] fast estimate {f:.1f}s < 62.0s.")
    lo, hi = SERIES_RUNTIME_WINDOW
    if not (lo <= c <= hi) and not args.allow_exception:
        sys.exit(f"[SERIES BLOCKER] center estimate {c:.1f}s outside series window {lo}-{hi}s.")

    reg = {f"P{i:02d}": {"part_id": f"P{i:02d}", "budget_units": b, "set": sets[i - 1] if i - 1 < len(sets) else None,
                         "revision": 0, "file": None, "status": "PENDING", "actual_units": 0, "line_count": 0,
                         "beat_count": 0, "sha256": None, "first_line": None, "last_line": None}
           for i, b in enumerate(budgets, start=1)}
    state = {
        "schema": "TIKTOK_SCRIPT_STATE_V1", "profile_id": PROFILE_ID, "profile_revision": PROFILE_REVISION,
        "assembler_version": ASSEMBLER_VERSION, "topic_id": args.topic_id, "slug": args.slug, "kit_episode_id": args.kit_id,
        "track": args.track, "mode": "dialogue_scenes", "count_unit": "words", "hero_code": hero, "cast": cast,
        "sets": sets, "strict_natural_speech": True, "max_beat_sec": float(args.max_beat_sec),
        "max_open_sentence_units": int(args.max_open_sentence_units), "blueprint_version": 1, "script_version": 1,
        "current_workflow": "WF03_BLUEPRINT_LOCKED", "state": "BLUEPRINT_LOCKED",
        "rate_spec": {"rate_center_upm": rc, "rate_min_upm": rmin, "rate_max_upm": rmax, "rate_basis": args.rate_basis,
                      "total_unit_budget": total, "est_lines": int(args.est_lines), "non_speech_model":
                      f"{KIT_LINE_GAP_SEC}s x (lines-2) + {KIT_LAST_GAP_SEC}s + {KIT_TAIL_SEC}s tail",
                      "planned_center_seconds": round(c, 1), "planned_range_seconds": [round(f, 1), round(s, 1)]},
        "parts_expected": len(budgets), "parts_delivered": 0, "next_part": "P01", "parts_registry": reg,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    sp = ws / f"{args.topic_id}_TT_STATE_V1.json"
    sp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[TT INIT OK] {sp} | {args.track} | Parts={len(budgets)} | Budget={total} words | est_lines={args.est_lines} "
          f"| ~{c:.1f}s (fast {f:.1f}s, slow {s:.1f}s) | Sets={sets}")


def _load_state(ws: Path, tid: str):
    sp = ws / f"{tid}_TT_STATE_V1.json"
    return sp, json.loads(sp.read_text(encoding="utf-8"))


def cmd_verify_part(args):
    ws = Path(args.workspace)
    sp, state = _load_state(ws, args.topic_id)
    pid = args.part_id.upper()
    if pid not in state["parts_registry"]:
        sys.exit(f"[ERROR] Unknown part {pid}")
    idx = int(pid[1:])
    order = sorted(state["parts_registry"])
    if idx > 1 and state["parts_registry"][f"P{idx - 1:02d}"]["status"] != "SECTION_PASSED":
        sys.exit(f"[BLOCKER] Sequential discipline: {pid} before P{idx - 1:02d} passed.")
    pf = Path(args.file)
    raw = pf.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        sys.exit("[BLOCKER] UTF-8 BOM found.")
    text = raw.decode("utf-8")
    for rx, msg in ((FORBIDDEN_TAG_RE, "TTS emotion/SFX tag"), (FORBIDDEN_PROSE_MARKERS_RE, "technical marker/URL")):
        m = rx.search(text)
        if m:
            sys.exit(f"[BLOCKER] {msg} in {pid}: {m.group(0)}")
    if not args.allow_guess:
        m = UNRESOLVED_EPISTEMIC_RE.search(text)
        if m:
            sys.exit(f"[ANTI-FABRICATION BLOCKER] {m.group(0)} in {pid}.")
    m = AI_ESE_PUNCT_RE.search(text)
    if m and not args.allow_ai_punct:
        sys.exit(f"[NATURAL SPEECH BLOCKER] '{m.group(0)}' in {pid}.")

    lines = parse_kit_lines(text, pid)
    if not lines:
        sys.exit(f"[BLOCKER] {pid} has 0 lines.")
    cast, hero = state["cast"], state["hero_code"]
    problems = []
    # line-id continuity
    prev_last = None
    if idx > 1:
        prev_last = state["parts_registry"][f"P{idx - 1:02d}"]["last_line_id"]
    expect = 0 if prev_last is None else int(prev_last[1:]) + 1
    for ln in lines:
        if int(ln["line_id"][1:]) != expect:
            problems.append(f"{ln['line_id']}: expected L{expect:02d} (continuous numbering across parts)")
        expect = int(ln["line_id"][1:]) + 1
        if ln["speaker"] not in cast:
            problems.append(f"{ln['line_id']}: speaker [{ln['speaker']}] not declared in --cast")
        wc = count_units(ln["spoken"])
        if ln["speaker"] not in (NARRATOR_CODE, hero) and wc > SIDE_LINE_MAX_WORDS:
            problems.append(f"{ln['line_id']}: side character line {wc} words > {SIDE_LINE_MAX_WORDS}")
        if ln["speaker"] != NARRATOR_CODE and PROFANITY_RE.search(ln["spoken"]):
            problems.append(f"{ln['line_id']}: profanity only allowed in Tyler's narration")
        if ln["speaker"] == NARRATOR_CODE and ln["spoken"] != WTF_LINE:
            for pm in PROFANITY_RE.finditer(ln["spoken"]):
                problems.append(f"{ln['line_id']}: extra profanity '{pm.group(0)}' (series keeps the WTF line as the only swear unless owner adds more)")
        hits = scan_throttled_words(ln["spoken"])
        if hits:
            problems.append(f"{ln['line_id']}: FYP watchlist {[h['flagged_term'] for h in hits]}")
    # series opening rules
    if idx == 1:
        if lines[0]["speaker"] != hero:
            problems.append(f"L00 must be the cold open by the episode character [{hero}]")
        if len(lines) < 3 or lines[1]["speaker"] != NARRATOR_CODE or lines[1]["spoken"] != WTF_LINE:
            problems.append(f"L01 must be exactly [NARR] '{WTF_LINE}'")
        name = cast[hero]
        if not any(ln["speaker"] == NARRATOR_CODE and f"This is {name}." in ln["spoken"] for ln in lines[:4]):
            problems.append(f"'This is {name}.' must appear in L02/L03")
    # scene sidecar
    side = parse_scene_sidecar(pf.with_suffix(".scenes.tsv"))
    keys = [k for ln in lines for k in ln["keys"]]
    missing = sorted({k for k in keys if k not in side})
    if missing:
        problems.append(f"scene sidecar {pf.with_suffix('.scenes.tsv').name} missing keys: {missing}")
    part_set = state["parts_registry"][pid]["set"]
    for k in sorted(set(keys)):
        if k in side and side[k]["set"] not in (part_set, "insert_2d", "any") and side[k]["set"] in USED_SETS:
            problems.append(f"{k}: uses already-used set '{side[k]['set']}'")
    if problems and not args.allow_deviation:
        sys.exit("[NEEDS_REPAIR] " + pid + "\n  - " + "\n  - ".join(problems))

    actual = count_units(" ".join(l["spoken"] for l in lines))
    budget = state["parts_registry"][pid]["budget_units"]
    dev = (actual - budget) / budget * 100 if budget else 0.0
    if abs(dev) > 22.0 and not args.allow_deviation:
        sys.exit(f"[NEEDS_REPAIR] {pid} words={actual} deviates {dev:+.1f}% from budget {budget}.")

    was_locked = state.get("state") == "SCRIPT_LOCKED"
    if was_locked:
        state["script_version"] += 1
    rec = state["parts_registry"][pid]
    rec.update(revision=int(args.revision), file=str(pf.resolve()), status="SECTION_PASSED", actual_units=actual,
               line_count=len(lines), beat_count=len(keys), sha256=sha256_bytes(raw), first_line=lines[0]["raw"],
               last_line=lines[-1]["raw"], last_line_id=lines[-1]["line_id"],
               scenes_sha256=sha256_bytes(pf.with_suffix(".scenes.tsv").read_bytes()))
    passed = [p for p in state["parts_registry"].values() if p["status"] == "SECTION_PASSED"]
    state["parts_delivered"] = len(passed)
    pending = [k for k in order if state["parts_registry"][k]["status"] != "SECTION_PASSED"]
    state["next_part"] = pending[0] if pending else None
    state["state"] = "WRITING" if pending else "DRAFT_COMPLETE"
    state["current_workflow"] = "WF04_WRITING" if pending else "WF05_READY_FOR_QA"
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    sp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[TT PART PASSED] {pid} R{rec['revision']} | Words={actual}/{budget} ({dev:+.1f}%) | Lines={len(lines)} "
          f"Beats={len(keys)} | Set={part_set} | Next={state['next_part'] or 'WF05_AUDIT'}"
          + (f" | [LOCK INVALIDATED -> v{state['script_version']}]" if was_locked else ""))


def _collect(state: dict, upto_p01: bool = False):
    order = sorted(state["parts_registry"])
    if upto_p01:
        order = order[:1]
    missing = [k for k in order if state["parts_registry"][k]["status"] != "SECTION_PASSED"]
    if missing:
        sys.exit(f"[BLOCKER] Missing passed parts: {missing}")
    lines, scenes, seams, blocks = [], {}, [], []
    for i, pid in enumerate(order):
        rec = state["parts_registry"][pid]
        pf = Path(rec["file"])
        pl = parse_kit_lines(pf.read_text(encoding="utf-8"), pid)
        for ln in pl:
            ln["part_id"] = pid
        sc = parse_scene_sidecar(pf.with_suffix(".scenes.tsv"))
        for k, v in sc.items():
            scenes.setdefault(k, dict(v, part_id=pid))
        if i > 0:
            seams.append({"seam": f"{order[i - 1]}->{pid}", "prev_closing": state["parts_registry"][order[i - 1]]["last_line"],
                          "next_opening": pl[0]["raw"]})
        lines += pl
        blocks.append(pl)
    if lines and not upto_p01:
        seams.append({"seam": "FINAL->0.0s_LOOP", "prev_closing": lines[-1]["raw"], "next_opening": lines[0]["raw"]})
    return lines, scenes, seams, blocks


def analyze_opening(lines: list, state: dict) -> dict:
    rows = timeline_from_lines(lines, state)
    hero, name = state["hero_code"], state["cast"][state["hero_code"]]
    first_beat = rows[0]["dur"] if rows else 0.0
    l00_end = max((r["end"] for r in rows if r["line_id"] == "L00"), default=0.0)
    wtf_end = max((r["end"] for r in rows if r["line_id"] == "L01"), default=0.0)
    intro = [r for r in rows if f"This is {name}." in r["beat"]]
    intro_t = intro[0]["start"] if intro else None
    text15 = " ".join(r["beat"] for r in rows if r["start"] < 15.0)
    text30 = " ".join(r["beat"] for r in rows if r["start"] < 30.0)
    sents = split_sentences(text15)
    long_s = [s for s in sents if count_units(s) > state["max_open_sentence_units"]]
    frame0 = rows[0]["beat"] if rows else ""
    anchors = sorted(set(m.group(0) for m in NUMBER_OR_CLOCK_RE.finditer(text30)) |
                     set(m.group(0).lower() for m in NUMBER_WORDS_RE.finditer(text30)))
    anchor_keys = sorted({r["key"] for r in rows if r["start"] < 30.0 and (NUMBER_OR_CLOCK_RE.search(r["beat"]) or NUMBER_WORDS_RE.search(r["beat"]))})
    warn = []
    if rows and rows[0]["speaker"] != hero:
        warn.append("Frame-0 beat is not the episode character's cold open.")
    if first_beat > 2.6:
        warn.append(f"Beat 1 is {first_beat:.2f}s (>2.6s): split L00 so the first caption page lands fast.")
    if l00_end > 4.8:
        warn.append(f"Cold open L00 ends at {l00_end:.2f}s (>4.8s; TMG01 reference 4.5s).")
    if wtf_end > 7.5:
        warn.append(f"WTF line ends at {wtf_end:.2f}s (>7.5s).")
    if intro_t is None or intro_t > 12.0:
        warn.append(f"'This is {name}.' starts at {intro_t}s (must be <= 12s).")
    if count_units(frame0) > 9:
        warn.append(f"Frame-0 caption beat has {count_units(frame0)} words (>9): too long to read muted.")
    if long_s:
        warn.append(f"{len(long_s)} sentence(s) in 0-15s exceed {state['max_open_sentence_units']} words.")
    th = scan_throttled_words(text30)
    if th:
        warn.append(f"FYP watchlist in 0-30s: {th}")
    if "?" not in text30:
        warn.append("No open question in 0-30s (the WTF line normally provides it).")
    return {"first_beat_est_sec": round(first_beat, 2), "cold_open_end_sec": round(l00_end, 2),
            "wtf_line_end_sec": round(wtf_end, 2), "intro_this_is_start_sec": round(intro_t, 2) if intro_t is not None else None,
            "frame0_caption_beat": frame0, "frame0_rule": "Frame-0 text = burned-in caption of L00 beat 1 (kit rule 9: captions only)",
            "sentences_0_15s": len(sents), "long_sentences_0_15s": long_s,
            "contiguity_anchors_0_30s": anchors, "contiguity_anchor_scene_keys": anchor_keys,
            "contiguity_rule": "each anchor must be SHOWN in-world in its key (INS_/CU_ prop, sign, phone insert), never as an overlay card",
            "fyp_watchlist_hits_0_30s": th, "warnings": warn}


def analyze_beats(lines: list, state: dict) -> dict:
    rows = timeline_from_lines(lines, state)
    th = state["max_beat_sec"]
    over = [{"line": r["line_id"], "key": r["key"], "est_sec": round(r["dur"], 2), "beat": r["beat"][:70]} for r in rows if r["dur"] > th]
    short = [{"line": r["line_id"], "key": r["key"], "est_sec": round(r["dur"], 2), "beat": r["beat"]}
             for i, r in enumerate(rows) if i > 0 and r["dur"] < KIT_MIN_SHOT_SEC - 0.3]
    total = rows[-1]["end"] + KIT_TAIL_SEC if rows else 0.0
    dead = []
    for a, b in zip(rows, rows[1:]):
        if b["start"] - a["end"] > 3.0:
            dead.append({"after": a["line_id"], "gap_sec": round(b["start"] - a["end"], 2)})
    keys_seq = [r["key"] for r in rows]
    shots = 1 + sum(1 for a, b in zip(keys_seq, keys_seq[1:]) if a != b)
    return {"total_beats": len(rows), "est_shots_after_kit_merge": shots, "est_total_sec": round(total, 1),
            "cuts_per_10s": round(shots / total * 10, 2) if total else 0, "max_beat_threshold_sec": th,
            "beats_exceeding_threshold": over, "beats_likely_merged_by_kit_lt_0p6s": short, "dead_air_gt_3s": dead,
            "unique_scene_keys": len(set(keys_seq)), "peak_window_55_65pct_sec": [round(total * 0.55, 1), round(total * 0.65, 1)],
            "lines_in_peak_window": sorted({r["line_id"] for r in rows if total * 0.55 <= r["start"] <= total * 0.65})}


def cmd_opening_audit(args):
    ws = Path(args.workspace)
    sp, state = _load_state(ws, args.topic_id)
    lines, _, _, _ = _collect(state, upto_p01=args.p01_only)
    rep = analyze_opening(lines, state)
    (ws / f"{args.topic_id}_TT_OPENING_AUDIT_V{state['script_version']}.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[TT OPENING AUDIT] Beat1={rep['first_beat_est_sec']}s | ColdOpenEnd={rep['cold_open_end_sec']}s | WTFEnd={rep['wtf_line_end_sec']}s "
          f"| ThisIs@{rep['intro_this_is_start_sec']}s | Frame0='{rep['frame0_caption_beat']}' | Anchors={rep['contiguity_anchors_0_30s']} "
          f"| Warnings={len(rep['warnings'])}")
    for w in rep["warnings"]:
        print("   WARN:", w)
    if args.strict and rep["warnings"]:
        sys.exit("[OPENING AUDIT BLOCKER]")


def cmd_beat_audit(args):
    ws = Path(args.workspace)
    sp, state = _load_state(ws, args.topic_id)
    if args.max_beat_sec is not None:
        state["max_beat_sec"] = float(args.max_beat_sec)
    lines, _, _, _ = _collect(state)
    rep = analyze_beats(lines, state)
    (ws / f"{args.topic_id}_TT_BEAT_AUDIT_V{state['script_version']}.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[TT BEAT AUDIT] Beats={rep['total_beats']} | Shots~{rep['est_shots_after_kit_merge']} | Total~{rep['est_total_sec']}s "
          f"| Cuts/10s={rep['cuts_per_10s']} | Over{rep['max_beat_threshold_sec']}s={len(rep['beats_exceeding_threshold'])} "
          f"| LikelyMerged={len(rep['beats_likely_merged_by_kit_lt_0p6s'])} | DeadAir={len(rep['dead_air_gt_3s'])} "
          f"| Peak55-65%={rep['peak_window_55_65pct_sec']} lines {rep['lines_in_peak_window']}")
    if args.strict and (rep["beats_exceeding_threshold"] or rep["dead_air_gt_3s"]):
        sys.exit("[BEAT AUDIT BLOCKER]")


def _series_final_checks(lines: list, state: dict) -> list:
    issues = []
    alltext = " ".join(l["spoken"] for l in lines).lower()
    if "sandwich" not in alltext:
        issues.append("Running gag missing: Tyler's sandwich must be ruined.")
    last = lines[-1]
    if last["speaker"] != NARRATOR_CODE or len(split_sentences(last["spoken"])) < 3:
        issues.append("Final line must be Tyler's 3-part closer (>= 3 short sentences).")
    hero_lines = [l for l in lines if l["speaker"] == state["hero_code"]]
    if len(hero_lines) < 3:
        issues.append("Episode character needs >= 3 own lines across the episode.")
    sets_seen = {}
    for l in lines:
        sets_seen.setdefault(l["part_id"], 0)
    if len(sets_seen) != len(state["sets"]):
        issues.append("Each declared set needs its own part.")
    return issues


def cmd_stitch_draft(args):
    ws = Path(args.workspace)
    sp, state = _load_state(ws, args.topic_id)
    lines, scenes, seams, blocks = _collect(state)
    draft = "\n\n".join("\n".join(l["raw"] for l in b) for b in blocks) + "\n"
    v = state["script_version"]
    (ws / f"{args.topic_id}_TT_DRAFT_V{v}.txt").write_bytes(draft.encode("utf-8"))
    (ws / f"{args.topic_id}_TT_SEAM_ANCHORS_V{v}.json").write_text(json.dumps(seams, indent=2, ensure_ascii=False), encoding="utf-8")
    br, orp = analyze_beats(lines, state), analyze_opening(lines, state)
    (ws / f"{args.topic_id}_TT_BEAT_AUDIT_V{v}.json").write_text(json.dumps(br, indent=2, ensure_ascii=False), encoding="utf-8")
    (ws / f"{args.topic_id}_TT_OPENING_AUDIT_V{v}.json").write_text(json.dumps(orp, indent=2, ensure_ascii=False), encoding="utf-8")
    est = runtime_estimates(lines, state)
    fin = _series_final_checks(lines, state)
    print(f"[TT DRAFT STITCHED] v{v} | Lines={len(lines)} | Words={est['units']} | Est={est['center']:.1f}s "
          f"(fast {est['fast']:.1f}, slow {est['slow']:.1f}) | OverBeat={len(br['beats_exceeding_threshold'])} "
          f"| OpeningWarn={len(orp['warnings'])} | SeriesIssues={fin}")


def cmd_lock_export(args):
    ws, out = Path(args.workspace), Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sp, state = _load_state(ws, args.topic_id)
    lines, scenes, seams, blocks = _collect(state)
    joined_raw = "\n".join(l["raw"] for l in lines)
    if not args.allow_guess and UNRESOLVED_EPISTEMIC_RE.search(joined_raw):
        sys.exit("[ANTI-FABRICATION BLOCKER] unresolved tag remains.")
    fin = _series_final_checks(lines, state)
    if fin and not args.allow_exception:
        sys.exit(f"[SERIES BLOCKER] {fin}")
    est = runtime_estimates(lines, state)
    if state["track"] == "creator_rewards" and est["fast"] < 62.0 and not args.allow_exception:
        sys.exit(f"[MONETIZATION BLOCKER] fast estimate {est['fast']:.1f}s < 62.0s.")
    lo, hi = SERIES_RUNTIME_WINDOW
    if not (lo <= est["center"] <= hi) and not args.allow_exception:
        sys.exit(f"[SERIES BLOCKER] center estimate {est['center']:.1f}s outside {lo}-{hi}s.")
    missing = sorted({k for l in lines for k in l["keys"] if k not in scenes})
    if missing:
        sys.exit(f"[BLOCKER] scene plan missing keys: {missing}")

    cast, slug = state["cast"], state["slug"]
    master_lines, voice_lines = [], []
    for b in blocks:
        for l in b:
            master_lines.append(f"{l['line_id']} {cast[l['speaker']].upper()}: {l['spoken']}")
            voice_lines.append(l["spoken"])
        master_lines.append("")
    master = "\n".join(master_lines).rstrip("\n") + "\n"
    voice = "\n".join(voice_lines) + "\n"
    strip = re.sub(r"^L\d{2} [^:]+: ", "", master, flags=re.M)
    if re.findall(r"\S+", strip) != re.findall(r"\S+", voice):
        sys.exit("[BLOCKER] Lossless roundtrip failed between 01-TT-SCRIPT and 02-TT-VOICE.")
    kit_shots = "\n".join(l["raw"] for l in lines) + "\n"
    if re.findall(r"\S+", " ".join(l["spoken"] for l in parse_kit_lines(kit_shots, "kit"))) != re.findall(r"\S+", voice):
        sys.exit("[BLOCKER] Lossless roundtrip failed between 05-KIT-shots.txt and 02-TT-VOICE.")

    f1, f2 = out / f"01-TT-SCRIPT-{slug}.txt", out / f"02-TT-VOICE-{slug}.txt"
    f3, f4 = out / f"03-TT-TIMELINE-{slug}.csv", out / f"04-TT-MANIFEST-{slug}.json"
    f5, f6 = out / "05-KIT-shots.txt", out / f"06-KIT-SCENES-{slug}.csv"
    f1.write_bytes(master.encode("utf-8"))
    f2.write_bytes(voice.encode("utf-8"))
    f5.write_bytes(kit_shots.encode("utf-8"))
    rows = timeline_from_lines(lines, state)
    with f3.open("w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["beat_id", "part_id", "line_id", "speaker", "scene_key", "set", "fyp_window_bucket",
                    "est_start_sec", "est_end_sec", "est_duration_sec", "units", "contiguity_anchors", "spoken_text"])
        pmap = {l["line_id"]: l["part_id"] for l in lines}
        for i, r in enumerate(rows, start=1):
            anc = sorted(set(m.group(0) for m in NUMBER_OR_CLOCK_RE.finditer(r["beat"])) |
                         set(m.group(0).lower() for m in NUMBER_WORDS_RE.finditer(r["beat"])))
            w.writerow([f"b{i:03d}", pmap[r["line_id"]], r["line_id"], cast[r["speaker"]], r["key"], scenes[r["key"]]["set"],
                        fyp_window_bucket(r["start"]), f"{r['start']:.2f}", f"{r['end']:.2f}", f"{r['dur']:.2f}",
                        count_units(r["beat"]), ";".join(anc), r["beat"]])
    with f6.open("w", encoding="utf-8", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["order", "scene_key", "shot_type", "set", "part_id", "first_line", "description"])
        seen = []
        for r in rows:
            if r["key"] not in seen:
                seen.append(r["key"])
        for i, k in enumerate(seen, start=1):
            first = next(r["line_id"] for r in rows if r["key"] == k)
            w.writerow([i, k, k.split("_")[0] if not k.startswith("TWO_SHOT") else "TWO_SHOT", scenes[k]["set"],
                        scenes[k]["part_id"], first, scenes[k]["description"]])
    br, orp = analyze_beats(lines, state), analyze_opening(lines, state)
    kid = state.get("kit_episode_id") or state["topic_id"]
    manifest = {
        "schema": "TIKTOK_LOCK_MANIFEST_V4", "profile_id": PROFILE_ID, "profile_revision": PROFILE_REVISION,
        "assembler_version": ASSEMBLER_VERSION, "topic_id": state["topic_id"], "kit_episode_id": kid, "slug": slug,
        "track": state["track"], "mode": "dialogue_scenes", "script_version": state["script_version"], "timing_status": "ESTIMATED",
        "cast": cast, "hero_code": state["hero_code"], "sets": state["sets"], "total_lines": len(lines),
        "total_beats": len(rows), "unique_scene_keys": len(scenes), "total_spoken_words": est["units"],
        "non_speech_seconds_kit_model": round(est["non_speech"], 2), "estimated_center_seconds": round(est["center"], 1),
        "estimated_range_seconds": [round(est["fast"], 1), round(est["slow"], 1)],
        "series_runtime_window": list(SERIES_RUNTIME_WINDOW),
        "creator_rewards_60s_safe": est["fast"] >= 62.0, "lossless_token_roundtrip": True, "seams": seams,
        "beat_pacing_summary": br, "opening_fyp_audit": orp,
        "kit_handoff": {
            "copy_shots_to": f"episodes/{kid}/shots.txt",
            "next_steps_not_run": [
                f"python tools/make_library.py episodes/{kid}/shots.txt episodes/{kid}/library.json",
                f"python tools/sonicvoice_tts.py episodes/{kid}/shots.txt episodes/{kid}/audio --voice uv_1883_1ae2d9e41df6 --voice-map <SPK>=<id> --gap 0.45 --stability 0.4",
                f"python tools/asr.py episodes/{kid}/audio episodes/{kid}/audio/vo16k.wav",
                "Blender: tools/hb/<id>_scene.py (one KEY(n) function per scene key in 06-KIT-SCENES)"],
            "status": "TTS_AND_RENDER_NOT_RUN"},
        "files": {n: {"path": str(p.resolve()), "sha256": sha256_bytes(p.read_bytes())}
                  for n, p in (("01_script", f1), ("02_voice", f2), ("03_timeline_csv", f3), ("05_kit_shots", f5), ("06_kit_scenes", f6))},
        "locked_at": datetime.now(timezone.utc).isoformat(),
    }
    f4.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    state.update(state="SCRIPT_LOCKED", current_workflow="WF06_SCRIPT_LOCKED", updated_at=datetime.now(timezone.utc).isoformat())
    sp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[TT LOCK & EXPORT OK] v{state['script_version']} | Lines={len(lines)} Words={est['units']} | Est={est['center']:.1f}s "
          f"(fast {est['fast']:.1f}, slow {est['slow']:.1f}) | Keys={len(scenes)} | Lossless=PASS | Out={out}")


def cmd_fyp_diagnose(args):
    fpk, cur = float(args.fol_per_k), int(args.current_followers)
    rem = max(0, 10000 - cur)
    views_10k = math.ceil(rem / fpk * 1000) if fpk > 0 and rem > 0 else 0
    qv = int(round(100000 * args.qualified_rate_pct / 100))
    geo = "NOT_PROVIDED" if args.qualified_geo_pct is None else (
        "PASS_TARGET_GEO_CLEAN (>=60%)" if args.qualified_geo_pct >= 60 else "WARN_GEO_DILUTED_BELOW_60PCT (VN self-views / links sent to VN?)")
    ratio, hyg = None, "NOT_PROVIDED"
    if args.views is not None and args.unique_viewers:
        ratio = round(args.views / args.unique_viewers, 2)
        hyg = "CONTAMINATED_LOOP_WATCH_OVER_2.0" if ratio > 2.0 else "CLEAN_UNDER_2.0"
    shrunk, flag = None, "NOT_PROVIDED"
    if None not in (args.mean_with, args.mean_without, args.n_with, args.n_without):
        n = min(args.n_with, args.n_without)
        shrunk = round((args.mean_with - args.mean_without) * n / (n + 5.0), 3)
        flag = "LOW_SAMPLE_NOISE_N_UNDER_4" if n < 4 else "SUFFICIENT_DIRECTIONAL_SIGNAL"
    npa = math.ceil(2 * ((1.96 + 0.84) * args.sigma_pts / args.delta_pts) ** 2) if args.delta_pts > 0 else None
    rep = {"profile_id": PROFILE_ID,
           "monetization_and_sprint_math": {"current_followers": cur, "fol_per_k": fpk, "estimated_views_needed_for_10k_followers": views_10k,
                                            "assumed_qualified_view_rate_pct": args.qualified_rate_pct, "assumed_rpm_usd": args.rpm_usd,
                                            "est_revenue_per_100k_total_views_usd": round(qv / 1000 * args.rpm_usd, 2)},
           "early_48h_fyp_data_hygiene": {"qualified_geo_share_pct": args.qualified_geo_pct, "geo_classification_status": geo,
                                          "views_per_unique_viewer": ratio, "loop_contamination_status": hyg},
           "d7_feature_shrinkage_eval": {"shrunk_effect_n_over_n_plus_5": shrunk, "sample_confidence": flag},
           "retention_experiment_power": {"assumed_hold_sd_pts": args.sigma_pts, "target_detectable_lift_pts": args.delta_pts,
                                          "required_videos_per_arm_95ci_80power": npa}}
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))


def build_parser():
    ap = argparse.ArgumentParser(description=f"TikTok assembler {ASSEMBLER_VERSION} for profile {PROFILE_ID}")
    sub = ap.add_subparsers(dest="cmd", required=True)
    WS = [("--workspace", {"required": True}), ("--topic-id", {"required": True})]
    T = {"action": "store_true"}
    spec = {
        "twin-seo-check": (cmd_twin_seo_check, [("--candidate", {"action": "append", "required": True}), ("--competitor", {"action": "append"}),
                           ("--own-past", {"action": "append"}), ("--seo-keywords", {"default": ""}), ("--json-out", {})]),
        "twin-5axis": (cmd_twin_5axis, [(f"--{a}", {"required": True}) for a in ("question", "stage", "ladder", "payoff", "look")] +
                       [("--sets", {"default": ""}), ("--axis-threshold", {"default": 0.25, "type": float}), ("--allow-exception", T), ("--json-out", {})]),
        "init": (cmd_init, WS + [("--slug", {"required": True}), ("--kit-id", {}),
                 ("--track", {"choices": ["creator_rewards", "viral_short", "serial_sub60", "true_story", "extended_story"], "default": "creator_rewards"}),
                 ("--part-budgets", {"required": True}), ("--sets", {"required": True}), ("--cast", {"required": True}), ("--hero", {"required": True}),
                 ("--est-lines", {"default": 22, "type": int}), ("--rate", {"default": 171.0, "type": float}),
                 ("--rate-min", {"default": 159.0, "type": float}), ("--rate-max", {"default": 176.0, "type": float}),
                 ("--rate-basis", {"choices": ["MEASURED_SAMPLE", "PLANNING_ASSUMPTION"], "default": "MEASURED_SAMPLE"}),
                 ("--max-beat-sec", {"default": 4.0, "type": float}), ("--max-open-sentence-units", {"default": 12, "type": int}),
                 ("--allow-exception", T)]),
        "verify-part": (cmd_verify_part, WS + [("--part-id", {"required": True}), ("--file", {"required": True}),
                        ("--revision", {"default": 1, "type": int}), ("--allow-deviation", T), ("--allow-guess", T), ("--allow-ai-punct", T)]),
        "opening-audit": (cmd_opening_audit, WS + [("--p01-only", T), ("--strict", T)]),
        "beat-audit": (cmd_beat_audit, WS + [("--max-beat-sec", {"type": float}), ("--strict", T)]),
        "stitch-draft": (cmd_stitch_draft, WS),
        "lock-export": (cmd_lock_export, WS + [("--out-dir", {"required": True}), ("--allow-exception", T), ("--allow-guess", T)]),
        "fyp-diagnose": (cmd_fyp_diagnose, [("--current-followers", {"type": int, "default": 0}), ("--fol-per-k", {"type": float, "default": 5.0}),
                         ("--qualified-rate-pct", {"type": float, "default": 55.0}), ("--rpm-usd", {"type": float, "default": 0.80})] +
                         [(f"--{a}", {"type": float}) for a in ("qualified-geo-pct", "mean-with", "mean-without")] +
                         [(f"--{a}", {"type": int}) for a in ("views", "unique-viewers", "n-with", "n-without")] +
                         [("--sigma-pts", {"type": float, "default": 8.0}), ("--delta-pts", {"type": float, "default": 5.0}), ("--json-out", {})]),
    }
    for name, (fn, opts) in spec.items():
        p = sub.add_parser(name)
        for flag, kw in opts:
            p.add_argument(flag, **kw)
        p.set_defaults(func=fn)
    return ap


if __name__ == "__main__":
    a = build_parser().parse_args()
    a.func(a)
