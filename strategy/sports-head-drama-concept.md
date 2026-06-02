# Concept Spec: "SPORTS-HEAD DRAMA" — same engine, sports-fandom skin

> A new defensible **skin** for the proven `injustice → endurance → karma → rebirth`
> engine, reverse-engineered from two breakout channels: **FilmVibe (`@film.vibe88`)**
> and **aistory.us (`@aistory.us`)**. The signature: every character has a **sports
> ball for a head** (basketball / football) on a realistic human body in official
> team colors, with **team allegiance as the built-in conflict engine.**
>
> Full teardown: `reference/sports-head-drama-breakdown.md`.
> Full 5-part worked series: `reference/thunder-boy-spurs-series-scripts.md`.
> This file = how to turn it into a channel using our existing pipeline.

---

## Why this skin "wins" (the trifecta)

- **Click (thumbnail novelty):** a ball-headed human in team colors is instantly
  recognizable and almost nobody renders it at quality → ownable thumbnail.
- **Retention (proven engine):** it's our exact 6-beat arc with a protected-child
  anchor — retention is already solved.
- **Moat (built-in audience + stakes):** US sports fandoms (NBA + NFL) are huge,
  tribal, and opinionated. The team rivalry *is* the conflict — free stakes + a
  comment-war engine ("Spurs > Thunder", "Eagles all day").

Maps directly onto `strategy/competing-concepts.md` → concept #7 ("Underdogs FC"),
but pushed harder: not just sports action, but **fandom-as-family-identity drama.**

---

## The skin in one screen

| Dimension | Lock |
|-----------|------|
| **Character token** | Sports ball = head (basketball / football), seams + logo visible; realistic human body, brown skin common; official team kit. Kids = smaller / chibi. Women = hair + jewelry + curves, still ball-headed. |
| **Conflict engine** | Team-A fandom vs Team-B fandom, lived as family/identity (dad's team vs kid's rival team; orphan caught between two fan families). |
| **Protected anchor** | An orphaned / bullied kid who loves the "wrong" or losing team. |
| **Promise object** | A team keepsake — late parent's necklace/medal/jersey/foam finger — planted early, paid off in finale. |
| **Color-coding** | Each side owned by its team color (Lakers purple, Eagles green, Thunder blue, Spurs black/silver). Sets are color-drenched so "who's who" reads instantly. |
| **Lighting** | Chiaroscuro for sad beats; warm amber "lantern light" for hope; cold blue for cruelty. |
| **Dialogue** | Short, raw, colloquial AAVE-flavored English; ALL-CAPS curiosity-gap captions cut off mid-line (*"ANYMORE", "BUSTING", "YOU BROUGHT"*). |
| **Format** | 9:16, ~10s clips, ~1:30–3:00 per part, serialized Parts, hard cuts, burned-in captions, original dramatic sound. |

---

## Two proven cold-open templates

1. **Conflict-explodes open (FilmVibe):** drop into a confrontation already at full
   boil — betrayal discovered, rival jersey revealed. 1–3 chars, ≤3s setup,
   wide → zoom-to-face → close-up. *"VANESSA WHOSE MONEY" / "EXPLAIN YOU BROUGHT".*
2. **Lonely-child open (aistory.us):** a lone abandoned kid in the dark, **no
   dialogue, sad music only** → instant empathy, then a 1–2 word caption seeds the
   conflict. Silence hits harder.

> 10-second hook spine (both channels): `in medias res → visual shock (big vs small /
> light vs dark) → sympathy close-up on the weak character → 1–2 word tension seed`.

---

## Ready-to-shoot cast presets (fictionalize for monetized work)

> Use **invented** team names/colors + AI-generated disclosure if monetizing. The
> real-team versions below are only to show the rivalry pattern.

- **Hoops Orphan:** Blue-ball orphan kid · Silver/black cruel foster family · kind neighbor girl · grocery-owner protector · two bully brothers. *(= Thunder Boy series)*
- **Gridiron House War:** Green-ball fanatic dad · green-ball mom · son secretly in rival red/blue colors · neutral logoless cousin.
- **Purple Dynasty Betrayal:** Purple/gold-ball family · green-ball secret-rival kid · the money/spending betrayal (LV-bags reveal).
- **Two-Town Rivalry (ensemble):** mirror two fan families across a deciding Game 7; bully arc flips to karma + reconciliation.

Each plugs into the 6 roles from `studio-bible/02-character-archetypes.md`
(HERO / TYRANT / BETRAYER / INNOCENT / JUSTICE / HENCHMAN).

---

## How it runs on the existing pipeline (near-zero rework)

| Asset | Reuse |
|-------|-------|
| `studio-bible/01-story-engine` | **As-is** — arc is universal. |
| `studio-bible/02-character-archetypes` | Add a "sports-head" casting table (ball-head token + team-color sides). Keep 6 roles + poetic-justice rules. |
| `studio-bible/03,04,05,06` | **As-is** — blueprint, visual/editing (add ball-head + color-code locks), dialogue (AAVE caption style), pipeline. |
| `topic-animal-drama` skill | Same skill; frame topics as "sports-head fandom drama" with team-rivalry stakes. |
| `script-animal-drama` skill | Same; only the design tokens change (ball-head + team kit + color-code). |
| `MASTER-PROMPT-seedance-kling` (V2.0) | Same 5 phases incl. Veo Omni voice/lip-sync locks; lock ball-head token in the Asset Bank phase. |

**To launch:** clone `02-character-archetypes` into a sports-head casting table,
write 1 series bible (start from the Thunder Boy worked example), then run the same
topic → script → master-prompt chain.

---

## Strengths to emulate / gaps to exploit

**Emulate:** unique ball-head visual; razor-sharp niche (NBA+NFL fans ∩ AI content);
serialized retention; premium render; expressive eyes despite the ball head.

**Exploit (their gaps = our edge):**
- They sit at 32K–64K → **consistency/cadence** is the growth lever. Batch + serialize.
- Uneven views (some 13K–49K) → tighter hooks + better topic selection (use the topic skill).
- **English-only** → localize. The `markets/latam/` pipeline (es-419 / pt-BR, Veo Omni
  voice+accent locks) can fork a sports-head channel for LatAm football (soccer) fandoms
  — a massive, even more tribal audience.

---

## Responsible production notes (important for this skin)
- **Fictionalize team names, logos, and colors** for monetized content — real
  league/team IP is trademarked. Invent plausible cities/teams + original color sets.
- Add the platform-required **"AI-generated" disclosure**.
- Keep characters fictional; do not depict real players, coaches, or real people.
- Keep the bullying/abuse beats **hopeful and resolved** (karma + forgiveness finale),
  not gratuitous — the source series always lands on reconciliation.
