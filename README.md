# 🎬 Animal Drama Studio — Viral Series Production System

A complete, repeatable framework for producing serialized **AI-animated animal
drama** shorts (TikTok / Reels / Shorts) — reverse-engineered from the breakout
series **"Dog Swings Alone"** and generalized so it works for **any animal cast**,
not just dog/cat/wolf.

> Core idea: don't make random clips. Run a proven **rags → ruin → revenge →
> rebirth** engine with cast you can swap (beaver, lion, ox, owl, shark, sparrow…),
> a recurring promise object, and poetic-justice payoff. Serialize it, cliffhang
> every part, and let viewers binge the playlist.

---

## How to use this repo

1. **Learn the system** — read `/studio-bible/` in order (01 → 06).
2. **Start a series** — copy `/series-templates/TEMPLATE-series-bible.md` to
   `/series/your-series.md` and fill in cast + beat map.
3. **See it done** — read `/series-templates/EXAMPLE-beaver-builds-alone.md`, a
   full series built with a brand-new cast to prove the formula scales.
4. **Write each part** — use the per-part template in `03-episode-blueprint.md`.
5. **Produce** — follow `06-production-pipeline.md` (prompt templates + checklist).

---

## Map of the system

| File | What it gives you |
|------|-------------------|
| `studio-bible/01-story-engine.md` | The universal 7-beat arc, 5 emotional levers, the promise/payoff loop, anti-patterns |
| `studio-bible/02-character-archetypes.md` | The 6 core roles + animal→role casting tables + 5 ready-to-shoot cast presets (**the "scale to any animal" part**) |
| `studio-bible/03-episode-blueprint.md` | Per-part structure, runtime/shot/word numbers, cliffhanger menu, copy-paste part template, QA |
| `studio-bible/04-visual-and-editing.md` | 3D render look, color-grade-by-emotion table, camera language, hard-cut editing, sound |
| `studio-bible/05-dialogue-and-hooks.md` | Dialogue rules, Gen Z/Alpha slang kit, reusable line templates, title formula |
| `studio-bible/06-production-pipeline.md` | Tool stack, character design tokens, image/video/TTS prompt templates, consistency tactics, posting cadence |
| `series-templates/TEMPLATE-series-bible.md` | Blank fill-in template to launch a new series |
| `series-templates/EXAMPLE-beaver-builds-alone.md` | Worked example (Beaver/Lion/Peacock/Owl/Hyena) — no dog/cat/wolf |
| `reference/dog-swings-alone-breakdown.md` | Full analysis + 7-part scripts of the source series |
| `.kiro/skills/topic-animal-drama/SKILL.md` | **Topic generator (start of the pipeline)** — produces N topics (default 20), all SERIES, each a fully-locked SERIES BRIEF (cast + @Handles + design tokens + promise object + catchphrase + insult + poetic-justice payload + per-part beat map + tier). Anti-drift: nothing is left for a later AI to guess |
| `.kiro/skills/script-animal-drama/SKILL.md` | **One-command script generator (v2, master-prompt-aligned)** — TOPIC + LENGTH (default 90-120s) → 7 phases producing a shooting script + clean TTS lines, with scenes locked to 10s clips / 9:16 / 130-145 WPM. Phase 7 emits a copy-paste `TOPIC_DATA` handoff block that feeds straight into the master prompt |
| `series-templates/topic-bank-30.md` | 30 viral-ready loglines (No. 1-30), cast + promise object + poetic-justice twist baked in |
| `series-templates/topic-bank-30-batch2.md` | 30 more loglines (No. 31-60) across new themes, each tagged with MODE (standalone/series) + viral tier (S/A/B+) |
| `production-prompts/MASTER-PROMPT-seedance-kling.md` | **Full production master prompt (V2.0)** — feeds a topic through 5 phases: Asset Bank (9:16), Seedance 2.0 10s, KLING AI multi-shot 10s, **Veo Omni 10s (native audio, with lip-sync + voice-gender locks)**, and a TikTok title + bilingual (EN/VI) scene review for CapCut. Paced at 130-145 WPM |
| `series/baker-last-loaf/` | **Worked full series** — all 7 parts of "The Baker's Last Loaf" (topic #1) scripted with the skill: a series bible + Parts 1-7 (shooting script + clean TTS voiceover lines each) |

---

## ⚡ Generate a script in one command (the Skill)

This repo ships a Kiro **skill** that turns the whole bible into a script generator.
Give it a topic and a length; it plays a "100M-view animation showrunner", runs 6
phases (Concept & Casting → Beat Map → Shot Outline → Draft → Punch-up → Final Clean),
and outputs:
- **Layer 1 — Shooting script** (shot-by-shot, visual direction + grade + dialogue)
- **Layer 2 — Clean voiceover lines** (bracket-free, per character, paste straight into ElevenLabs/TTS)
- **Layer 3 — Shot prompt sheet** (optional image/video-gen prompts)

**Inputs:** `TOPIC` · `LENGTH` (default 90-120s) · `MODE` (standalone / series-part / pilot) · `TONE`.

To activate it in your own Kiro environment, copy `.kiro/skills/script-animal-drama/`
to your workspace `.kiro/skills/` (or `~/.kiro/skills/` for global use), then ask
Kiro for an "animal drama script" with your topic.

---

## The formula in one screen

**Arc (per series, 6-8 parts):**
`LOSS → INJUSTICE → ENDURANCE → AWAKENING → KARMA → REBIRTH → ULTIMATE REVENGE`

**Cast (per series, swap the animals):**
`HERO (honest builder) · TYRANT (rich predator) · BETRAYER (trusted insider) ·
INNOCENT (the child anchor) · JUSTICE (calm authority) · HENCHMAN (leaks the secret)`

**Glue (what makes it feel authored):**
a **promise object** + a **catchphrase**, an **insult to reverse**, and a
**poetic-justice payload** planted early and detonated in the finale.

**Format:** 9:16, ~65s/part, shots 1.5-3s, 100% hard cuts, burned-in captions,
cliffhanger every part, one playlist per series.

---

## Pick a cast and go (presets)

- **Builder's Betrayal:** Beaver · Lion · Peacock · Owl · Hyena
- **The Farmer's Land:** Ox · Crocodile · Fox · Bear · Rat
- **Feathers & Greed:** Sparrow · Eagle · Flamingo · Elephant · Vulture
- **The Baker's Recipe:** Bear · Tiger · Cat · Owl · Weasel
- **Underwater Empire:** Sea Turtle · Shark · Dolphin · Orca · Eel

See `studio-bible/02-character-archetypes.md` for the full casting tables and rules.

---

## Responsible production notes
- Check each AI tool's license/usage terms before publishing monetized content, and keep an asset/tool log.
- Add a clear "AI-generated" disclosure where the platform requires it.
- Keep characters fictional; avoid depicting real people or real brands.


---

## 🌎 Market localization — South America (LatAm)

A full localized pipeline lives in `markets/latam/` + two localized skills.
Same 7-beat engine, **telenovela-flavored** for South America: dialogue in
**Spanish (es-419)** or **Brazilian Portuguese (pt-BR)**, a **South-American
fauna cast** (capybara hero, jaguar/caiman tyrant, macaw betrayer, condor
justice), local names + slang, and Veo Omni voice locks that pin **language +
accent + gender** (fixes male→female voice flips and wrong-character lip-sync).

| File | What it gives you |
|------|-------------------|
| `markets/latam/00-market-playbook.md` | The localization brain: language strategy, telenovela thesis, fauna casting table, names, slang, settings, music, hashtags, posting calendar |
| `.kiro/skills/topic-animal-drama-latam/SKILL.md` | LatAm topic generator — 20 locked SERIES BRIEFs in es/pt with VOICE PROFILEs |
| `.kiro/skills/script-animal-drama-latam/SKILL.md` | LatAm script generator — es/pt dialogue, 10s scenes, handoff to the LatAm master prompt |
| `markets/latam/MASTER-PROMPT-latam.md` | LatAm master prompt (Seedance + KLING + **Veo Omni** with es/pt voice+accent locks) + es/pt title & bilingual review |
| `markets/latam/channel-setup.md` | Channel names, usernames, capybara avatar/banner prompts, bilingual bios (es/pt), launch checklist |

**LatAm pipeline:** `topic-animal-drama-latam` → `script-animal-drama-latam` →
`markets/latam/MASTER-PROMPT-latam.md`. Recommended: run two channels —
`@patasykarma` (es) and `@patasekarma` (pt).



---

## 🌿 Second lane — the Cozy Lane (healing / no-dialogue / bedtime)

A complete **parallel system** in `cozy-lane/` for a *different* kind of channel:
**cozy, (near-)wordless, nature-rescue stories** built around a **fixed, merch-able
signature duo**, shipped **localize-first**. It is the studio's second lane — same
production muscle, **opposite emotional engine**.

> Built by reverse-engineering the competitor in
> `reference/roro-dodo-tales-breakdown.md` (Roro & Dodo Tales), then attacking the
> exact weaknesses that dossier found. Where the main lane farms **catharsis**
> (revenge/karma), the cozy lane farms **reassurance** (comfort/healing). It is
> **not** a reskin of the revenge engine — it has its own arc, pacing, and look.

**Core idea:** run a proven **calm → disruption → effort → restoration** engine with
a constant duo, a **signature prop** (a firefly lantern / music box) that doubles as
the **merch product + emotional barometer**, and a **kindness-echo** (plant a tiny
kindness early, pay it off as the rescue) — instead of a villain and a revenge twist.

### Why a cozy lane (vs cloning the competitor)
- **Don't clone** (swap-character copycat **loses** — late, no moat, AI quality-inflation erodes the "pretty render" USP).
- **Win with the 3 things the competitor lacks:** a **merch-able duo + prop moat**, a **localize-first wedge** (wordless = ~free to localize; reuse the LatAm es/pt pipeline), and **out-execution** (weekly cadence, SEO, bedtime long-form, Shorts funnel, community).

### Map of the cozy lane
| File | What it gives you |
|------|-------------------|
| `cozy-lane/00-overview-and-strategy.md` | The lane brain: positioning vs the competitor, the moat, the localization wedge, Hero/Hub/Hygiene content strategy, pillars, cadence, monetization, anti-copycat checklist |
| `cozy-lane/01-comfort-engine.md` | The **6-beat Comfort Arc** (CALM → RIPPLE → REACH → EFFORT & SETBACK → TENDERNESS → RESTORATION), 5 emotional levers, the signature-prop + kindness-echo + silent-ritual loops, anti-patterns |
| `cozy-lane/02-character-archetypes.md` | The cozy roles (Protector / Wonder / Guest-in-need / World-Force / Gentle Foil / Chorus), **merch-first duo design rules**, cozy casting tables, 5 ready-to-shoot duo presets |
| `cozy-lane/03-episode-blueprint.md` | Per-episode structure, **dual-format** (16:9 long-form ~8 min + 9:16 Shorts), hook & worry-loop menus, the **bedtime 45–60 min compilation** variant, QA |
| `cozy-lane/04-visual-and-editing.md` | Soft-plush render identity, **warm-dominant cool-dip-return-to-gold** grade, slow 4–8s pacing (+ soft dissolves), no-text thumbnail system, consistency checklist |
| `cozy-lane/05-sound-and-wordless-storytelling.md` | **Telling story with no words** (image + sound + prop), leitmotifs, non-verbal vocalizations, prop-as-narrator, the title + thumbnail open-loop formula, localization notes |
| `cozy-lane/06-production-pipeline.md` | Cozy AI prompt templates (still / image-to-video / music / foley / end-card), frozen design tokens, **bedtime-compilation assembly**, **localize-first publishing**, the Shorts funnel, checklists |
| `cozy-lane/TEMPLATE-cozy-series-bible.md` | Blank fill-in template to launch a new cozy series |
| `cozy-lane/EXAMPLE-bramble-and-wisp.md` | Worked example — "Bramble & Wisp: Hollow Glen Tales" (bear cub + snowy owlet + firefly lantern), a 7-episode Season 1 incl. the hero nature episode "The Broken Forest," with condensed **wordless** beat scripts |
| `cozy-lane/MASTER-PROMPT-cozy-veo-omni.md` | The **production master prompt** for the cozy lane: single-engine **VEO Omni** reference-to-video, **16:9 · 10s · 100% wordless**, unlimited 16:9 Asset Bank (≤7 refs/clip), **REFERENCE-ROLE-LOCK + PHYSICS-GUARD**, 6-beat Comfort Arc, EN+es+pt title package + EN/VI review + CapCut handoff. Requests input if none given (no auto-invention) |
| `.kiro/skills/topic-cozy-nature/SKILL.md` | **Cozy topic generator (start of the cozy pipeline)** — locks SERIES CONSTANTS (the fixed merch-able duo + prop + world + silent ritual) once, then emits N locked EPISODE BRIEFS (default 12 = a season) rotating the guest-in-need; each brief locks pillar + worry loop + kindness-echo + 6-beat map + tier. Anti-drift, fixed-IP moat, no villain |
| `.kiro/skills/script-cozy-nature/SKILL.md` | **Cozy wordless script generator** — TOPIC (or an EPISODE BRIEF) → 7 phases producing a **wordless shooting script + an audio/music design** (no dialogue, no narrator), clips locked to 10s / 16:9. Phase 7 emits a copy-paste `TOPIC_DATA` block that feeds straight into the cozy master prompt |

### The cozy production chain
```
topic-cozy-nature  →  script-cozy-nature  →  cozy-lane/MASTER-PROMPT-cozy-veo-omni.md
 (SERIES CONSTANTS    (wordless script +     (Asset Bank 16:9 · VEO Omni 10s ≤7-ref
  + EPISODE BRIEFS)     TOPIC_DATA handoff)    ROLE-LOCK + PHYSICS-GUARD · audio · EN/es/pt + EN/VI)
```
Mirrors the revenge pipeline (`topic-animal-drama → script-animal-drama → MASTER-PROMPT-seedance-kling`), but wordless, 16:9, single-engine, and ending **safe & warm**.

### The cozy formula in one screen
**Arc (per series & per episode):**
`CALM → RIPPLE → REACH → EFFORT & SETBACK → TENDERNESS → RESTORATION`

**Cast (constant duo + rotating guest):**
`PROTECTOR (calm caregiver) · WONDER (curious, tends the prop) · GUEST-IN-NEED (rotates each ep) · WORLD/FORCE (impersonal conflict — weather, time, a felled grove) · GENTLE FOIL + CHORUS (optional)`

**Glue (what makes it feel authored):**
a **signature prop** (merch + emotional barometer), a **silent ritual** (the wordless
catchphrase), and a **kindness-echo** (a small kindness planted early returns as the
rescue) — and **effort, not magic**, always solves it.

**Format:** 16:9 long-form (~8 min) + 9:16 Shorts + monthly 45–60 min bedtime
compilation; slow 4–8s shots; **no dialogue** (non-verbal vocals only) → **localizes
for free** (EN + es/pt now via `markets/latam/`, then hi/ar/vi); ends **safe & warm**.

> Run the two lanes as **two channels off one pipeline**: the revenge engine
> (`studio-bible/`) for catharsis, the comfort engine (`cozy-lane/`) for reassurance.
