# PIPELINE — CINEMATIC DRAMA (Pure Drama + Visual Art · EN market)

A **separate, parallel** production pipeline alongside the existing viral one. This branch chases **pure emotional drama and visual art** in the "Dog Swings Alone" tradition — the war between **family and money**, good and evil — told through deliberate, beautiful images and a strict **4-Act Audio Dynamic Structure**. Spoken language is **English** (the target market). Vietnamese appears only in the final CapCut review.

> The old viral pipeline (`topic-animal-drama` → `script-animal-drama` → `MASTER-PROMPT-seedance-kling.md`) is **untouched**. Use whichever fits the channel.

---

## The chain

```
topic-drama-cinematic            →  script-drama-cinematic          →  MASTER-PROMPT-drama-cinematic
(.kiro/skills/...)                  (.kiro/skills/...)                 (production-prompts/...)

12 SERIES BRIEFS (locked)        →  ONE PART expanded into a        →  Asset Bank 9:16 · Seedance ·
6-beat arc + 4-act per part         4-ACT shot list (~10s shots)       KLING · Veo Omni (voice-lock) ·
visual signature + audience         + TOPIC_DATA handoff               bilingual EN/VI CapCut review
insight, no meme slang
```

1. **`topic-drama-cinematic`** — generates SERIES BRIEFS. Each locks: cast (6 roles) + `@Handle` + design token + **voice profile**, a **VISUAL SIGNATURE** (recurring motif + emotion→grade map + signature shots), an **AUDIENCE INSIGHT** (injustice→anger / empathy / retention), a promise object + tender catchphrase, the central injustice + karmic payoff, and a **6-beat arc mapped to parts**, each part shaped as **4 acts**.
2. **`script-drama-cinematic`** — adopts ONE brief verbatim, picks a PART, and expands it into a **4-Act shot list**: ACT 1 Hook → ACT 2 Build-Up → ACT 3 Peak → ACT 4 Resolution, each act tagged with an **EMOTION** target, broken into **~10s render shots** with full **cinematography** (camera size+angle+move, lighting, grade, signature shot). Emits a copy-paste `TOPIC_DATA` handoff.
3. **`MASTER-PROMPT-drama-cinematic`** — consumes the handoff verbatim and renders: Phase 1 Asset Bank → Phase 2 Seedance → Phase 3 KLING → Phase 4 **Veo Omni** (native audio + hard voice/lip-sync lock) → Phase 5 English title package + bilingual shot-by-shot review for CapCut.

---

## Story spine

**6-beat DRAMA arc (across parts):**
`HOPE & PROMISE → INJUSTICE → ROCK BOTTOM → THE TURN → KARMA → RESTORATION`
Let evil **win cruelly** at Rock Bottom (the retention engine), then land karma, then heal under golden light.

**4-Act Audio Dynamic Structure (inside every part):**
| Act | Window | Job | Emotion target |
|-----|--------|-----|----------------|
| 1 — The Shocking Hook | ~0-15% | grab in 2s on tension/shock | Tension / Dread |
| 2 — The Build-Up | ~15-50% | escalate, reveal stakes | Injustice / Empathy |
| 3 — The Peak | ~50-85% | this part's climax (often near-silent) | Grief / Catharsis |
| 4 — The Resolution | ~85-100% | button: cliffhanger or golden payoff | Dread / Peace |

---

## Visual-art rules (a pillar, not a footnote)

- **9:16 vertical**, faces in the upper-middle third, lower third clear for CapCut captions (renders have NO on-screen text).
- **Emotion → grade:** family/love = warm amber · villain/scheming = cold blue-gray · loss/rock-bottom = desaturated gray · karma/police = blue-red flash · restoration = glowing gold.
- **Camera grammar:** low-angle on the tyrant, slight high-angle on the hero early (flip at restoration); close-ups dominate; slow push-in on a realization; macro insert on the promise object / a falling tear; slow-motion embrace; pull-back to the golden home; hard cuts; cross-cutting suffering vs. gloating.
- **VISUAL SIGNATURE:** one recurring motif (e.g., the empty swing) returns every part as the visual refrain.

---

## What's different vs. the viral pipeline

| | Viral pipeline | **Cinematic Drama (this)** |
|---|---|---|
| Tone | meme-bait, internet slang (mogged/glow-up/caught in 4K) | **pure drama, sincere lines, NO meme slang** |
| Structure | beats spread over uniform 10s scenes | **4-Act Audio Dynamic** (Hook/Build-Up/Peak/Resolution) over ~10s shots |
| Emotion | implicit | **explicit EMOTION target per act/shot** |
| Visuals | grade-by-emotion | **full cinematography per shot + a series VISUAL SIGNATURE** |
| Pace | 130-145 WPM | **100-130 WPM, silent Peaks** |
| Arc | 7-beat revenge + poetic-justice "mog back" | **6-beat drama: hope→injustice→rock bottom→turn→karma→restoration** |

**Kept identical (so it still renders):** 9:16, ~10s render clips, `@Handle` system, **≤15 asset cap**, English voiceover, triple engine (Seedance/KLING/Veo Omni) with Veo voice/lip-sync lock, bilingual CapCut handoff.

---

## How to run

1. Type `cinematic drama topic` (or paste a theme) → pick briefs from `topic-drama-cinematic`.
2. Paste ONE full SERIES BRIEF into `script-drama-cinematic`, choose a PART → get the 4-Act script + `TOPIC_DATA` handoff.
3. Paste the `TOPIC_DATA` into `MASTER-PROMPT-drama-cinematic.md`, type `Continue` through Phases 1→5.
4. In CapCut: render each ~10s shot (Veo Omni already has voiced audio; Seedance/KLING are silent → add ElevenLabs voiceover per the VOICE LOCK) → assemble in ACT/SHOT order → burn captions from the Caption column → grade per shot → add music/SFX (keep the Peak silent) → export 1080×1920.

**Reference (gold standard):** `reference/dog-swings-alone-breakdown.md`.

**Install the skills:** copy `.kiro/skills/topic-drama-cinematic/` and `.kiro/skills/script-drama-cinematic/` into your workspace `.kiro/skills/` (or `~/.kiro/skills/`), then trigger with "cinematic drama topic" / "cinematic drama script".
