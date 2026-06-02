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
| `reference/sports-head-drama-breakdown.md` | Competitive teardown of the **sports-head drama** niche (FilmVibe + aistory.us): hooks, visual tokens, formulas |
| `reference/thunder-boy-spurs-series-scripts.md` | Full 5-part worked example in the sports-head niche (orphan + NBA-fandom drama) |
| `strategy/competing-concepts.md` | 10 alternative skins for the same engine + decision matrix + launch picks |
| `strategy/sports-head-drama-concept.md` | How to turn the sports-head niche into a channel on the existing pipeline (cast presets, cold-opens, reuse map) |
| `strategy/PLAYBOOK-sports-head-vi.md` | **One-stop Vietnamese playbook** for the whole sports-head pipeline — consolidates the channel analysis, viral formula, visual/character design, ~62 WPM pacing, the dual-stream topic + script skills, the V16.3 master prompt, the trend-jack ("bú fame") workflow, team-hex quick ref, brand-safety, QA checklist, and an A→Z quick-start |
| `.kiro/skills/topic-animal-drama/SKILL.md` | **Topic generator (start of the pipeline)** — produces N topics (default 20), all SERIES, each a fully-locked SERIES BRIEF (cast + @Handles + design tokens + promise object + catchphrase + insult + poetic-justice payload + per-part beat map + tier). Anti-drift: nothing is left for a later AI to guess |
| `.kiro/skills/script-animal-drama/SKILL.md` | **One-command script generator (v2, master-prompt-aligned)** — TOPIC + LENGTH (default 90-120s) → 7 phases producing a shooting script + clean TTS lines, with scenes locked to 10s clips / 9:16 / 130-145 WPM. Phase 7 emits a copy-paste `TOPIC_DATA` handoff block that feeds straight into the master prompt |
| `series-templates/topic-bank-30.md` | 30 viral-ready loglines (No. 1-30), cast + promise object + poetic-justice twist baked in |
| `series-templates/topic-bank-30-batch2.md` | 30 more loglines (No. 31-60) across new themes, each tagged with MODE (standalone/series) + viral tier (S/A/B+) |
| `production-prompts/MASTER-PROMPT-seedance-kling.md` | **Full production master prompt (V2.0)** — feeds a topic through 5 phases: Asset Bank (9:16), Seedance 2.0 10s, KLING AI multi-shot 10s, **Veo Omni 10s (native audio, with lip-sync + voice-gender locks)**, and a TikTok title + bilingual (EN/VI) scene review for CapCut. Paced at 130-145 WPM |
| `production-prompts/MASTER-PROMPT-sports.md` | **Sports-head drama master prompt (V16.3, real-team)** — for the anthropomorphic sports-ball-head niche (see `reference/sports-head-drama-breakdown.md`). 6 phases: turnaround Asset Bank (16:9 sheets / 9:16 plates, 2026 basketball), 9:16 Image Prompts, **GROK** multi-shot motion, **KLING** condensed motion (≤2500), **Veo Omni with references** (native audio, ≤7 @assets, no priming image), + bilingual (EN/VI) CapCut breakdown. Slow-storytelling **~62 WPM**, real NFL/NBA/MLB/NHL/MLS teams + exact hex |
| `.kiro/skills/topic-sports-drama/SKILL.md` | **Sports-head topic generator (tri-stream)** — default 10 SERIES BRIEFs split **4 EVERGREEN + 3 RESULT TREND-JACK + 3 CULTURE TREND-JACK**. Phase 1 runs **live web searches** (an EVENT board for sports results + a FORMAT board for trending TikTok sounds/slang/formats), prints a **STREAM STATISTICS** block, and locks each trend topic with a SOURCE EVENT / TREND FORMAT + FRESHNESS WINDOW + evergreen fallback. 6-role sports casting + ball-head design tokens + real-team hex + ST-1..ST-8 tropes + 6-beat arc per part; ≤14 assets; no real athletes as characters. Feeds `script-sports-drama` |
| `.kiro/skills/script-sports-drama/SKILL.md` | **Sports-head script generator** — TOPIC + PART + LENGTH → 7 phases producing a shooting script + clean TTS lines, scenes locked to **~10s shots / 9:16 / ~62 WPM** (slow storytelling). 4-act shape per part, raw colloquial dialogue, real-team hex, 2026 basketball, ≤2 speakers/scene (ensemble hook), karma+forgiveness finale. Phase 7 emits a copy-paste `TOPIC_DATA` handoff (SHOT LIST + BeatWeight) that feeds straight into `MASTER-PROMPT-sports.md` (V16.3). Supports all three streams (evergreen / result-trend / culture-trend) |
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
