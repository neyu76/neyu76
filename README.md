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

## 🇺🇸 New genre + market — US Sad-Story Human Drama (photoreal)

A second, **photoreal human** pipeline lives in `markets/us/` + two skills + a
dedicated master prompt. It is the human-drama cousin of the animal-drama saga —
**same emotional engine** (protected innocent, betrayal, endurance, rescue,
poetic-justice/reunion, cliffhangers), but **real-looking people in American
English (en-US)** instead of animated animals. Reverse-engineered from the German
"@heartwarming_stories4" tearjerker channel and ported to the **United States**.

What makes this genre different from the animal saga:
- **Photoreal, NOT animated.** Cinematic US film look, 35mm, cool blue-grey grade,
  pathetic-fallacy snow/rain.
- **Two-track audio.** SCENE 1 = an acted **HOOK** with real lip-synced English
  dialogue (Veo Omni); SCENE 2→N = **silent b-roll + one narrator voiceover**
  (ElevenLabs). Only the hook lip-syncs.
- **The 3-PARTY HOOK ("Triangle of Cruelty").** The opening 10 seconds field **≥3
  interacting characters** (AGGRESSOR + VICTIM + THIRD-PARTY: a co-victim, a
  complicit witness, or a transactional stranger) in **3 beats, one speaker per
  beat**, the other two reacting in silence.
- **Longer runtime.** ~240-300s (4-5 min) of **10-second scenes** at 140-150 WPM,
  every part ending on a **hard cliffhanger** that farms "Part 2!" comments.

| File | What it gives you |
|------|-------------------|
| `markets/us/00-market-playbook.md` | The US localization brain: language, thesis, photoreal human-cast table, American names, settings, moral-outrage idiom kit, music, hashtags, posting calendar, monetization, **content-safety guardrails**, tiers |
| `.kiro/skills/topic-sad-story-drama/SKILL.md` | US topic generator — 20 hard-locked SERIES BRIEFs (en-US) with the 3-party hook, hero prop, catch-line, label-to-reverse, withheld truth, per-part 5-Act beat map |
| `.kiro/skills/script-sad-story-drama/SKILL.md` | US script generator — 7 phases, English dialogue + narrator, 10s scenes, two-track audio, Phase 7 emits a `TOPIC_DATA` handoff |
| `production-prompts/MASTER-PROMPT-sad-story-drama.md` | US master prompt (V1.2) — Asset Bank (16:9) + seed images (9:16, A/B) + Seedance + KLING silent b-roll + **Veo Omni for the 3-party HOOK with en-US voice lock** + English title + narrator script + EN/VI review |
| `markets/us/channel-setup.md` | Channel names, handles, avatar/banner prompts, bios, launch checklist (incl. the AI-generated label), pipeline quick-start |

**US sad-story pipeline:** `topic-sad-story-drama` → `script-sad-story-drama` →
`production-prompts/MASTER-PROMPT-sad-story-drama.md`. Suggested channel:
**"Heartfelt Stories"** / `@heartfeltstories`.

> ⚠️ **Responsible use (this genre depicts children in distress):** keep
> characters fictional (no real people or cases), keep cruelty emotional/neglect
> (never graphic or exploitative), keep a hopeful arc, and **always turn on the
> platform's AI-generated label**. See `markets/us/00-market-playbook.md` §9.
