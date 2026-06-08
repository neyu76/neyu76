# Cozy Lane — SEEDANCE 2.0 · 15s Pipeline (Channel: **BRAMBLE & WISP**)

A full, self-contained production pipeline for the cozy/wordless nature-rescue channel
**BRAMBLE & WISP**, rebuilt for the **Seedance 2.0** video engine with **15-second clips**
(instead of the older VEO Omni 10s pipeline).

```
topic-cozy-nature-seedance   → SERIES CONSTANTS + 12 EPISODE BRIEFS (locked)
   → script-cozy-nature-seedance (ADOPT brief, expand → 15s wordless clips)
        → PHASE 7 emits TOPIC_DATA (SEEDANCE)
            → MASTER-PROMPT-cozy-seedance.md
                 → Asset Bank 16:9 · Seedance 2.0 15s · audio · titles EN/es/pt · review EN/VI · CapCut
```

## What changed vs the VEO Omni (10s) pipeline

| Aspect | OLD (VEO Omni) | NEW (Seedance 2.0) |
|--------|----------------|---------------------|
| Engine | VEO Omni reference-to-video | **Seedance 2.0** reference-to-video |
| Clip length | 10s fixed | **15s fixed** |
| Clip math (480s) | ~48 story + ~24 insert = ~72 | **~32 story + ~16 insert = ~48** |
| Shots / clip | 1–2 slow shots | **3–5 shots** with explicit timestamps |
| Batch size | 16 rows | **12 rows** |
| Prompt format | prose paragraphs | **Seedance bracket format** ([Aesthetic]/[Storyline]/[Characters]/[Environment]/[Action Sequence]/[Production Brief]/[Negative Prompt]) |
| Reference syntax | `REF1=@Handle (ROLE, disambig)` | **`@Image 1 = @Handle (ROLE, disambig)`** |
| Trim in CapCut | 10s → ~4–8s | **15s → ~6–10s** |
| Master prompt file | MASTER-PROMPT-cozy-veo-omni.md | **MASTER-PROMPT-cozy-seedance.md** |

## What stayed (the cozy DNA — unchanged)

- Fixed merch-able duo **Bramble & Wisp** + signature prop (**firefly lantern**) + named world (**Hollow Glen**).
- 6-beat Comfort Arc: `CALM → RIPPLE → REACH → EFFORT & SETBACK → TENDERNESS → RESTORATION`.
- **100% wordless** (no dialogue, no narrator, no lip-sync) — diegetic nature + foley + non-verbal animal vocals only.
- **No villain** (conflict = impersonal circumstance), ends **safe & warm**.
- Signature-prop barometer, kindness-echo (plant CALM → detonate TENDERNESS), silent ritual, effort-not-magic.
- 16:9 horizontal, warm-dominant grade, REFERENCE-ROLE-LOCK + PHYSICS-GUARD.
- Localize-first: EN + es + pt titles, EN/VI scene review.

## Files

- `skills/topic-cozy-nature-seedance/SKILL.md` — season/episode brief generator (4 phases).
- `skills/script-cozy-nature-seedance/SKILL.md` — wordless shooting script generator (7 phases; Phase 7 = TOPIC_DATA handoff for Seedance master prompt).
- `MASTER-PROMPT-cozy-seedance.md` — the Seedance 2.0 production engine (Phases 0–4).

## Channel lock

Channel name is **BRAMBLE & WISP** across all markets (wordless = no name translation needed).
