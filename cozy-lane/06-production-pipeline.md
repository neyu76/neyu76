# 06 — Production Pipeline & AI Prompt Templates (Cozy Lane)

End-to-end workflow to turn a cozy series bible into finished, localized episodes.
Shares **production muscle** with `/studio-bible/06` (tokens, consistency tactics,
tool categories) but swaps the *style*, the *audio approach* (music/foley, no TTS
dialogue), adds **bedtime-compilation assembly**, and a **localize-first** publish step.

---

## Pipeline overview (per series)

1. **Write the Series Bible** — use `cozy-lane/TEMPLATE-cozy-series-bible.md` (duo, signature prop, kindness-echo, 6-beat map). See `EXAMPLE-bramble-and-wisp.md`.
2. **Lock design tokens** — one frozen description per lead + the **signature prop** + the world (below).
3. **Write each episode** — use the per-episode template in `03-episode-blueprint.md`.
4. **Generate key stills** — one consistent image per shot (character + setting + warm grade), 16:9.
5. **Animate** — image-to-video with **slow, gentle motion** (no snap moves).
6. **Score & sound** — music (lullaby/orchestral) + leitmotifs + ambience + foley + non-verbal vocalizations. **No dialogue TTS.**
7. **Edit** — assemble to the music, breathe (4–8s shots), soft dissolves on time-passing, hold the warm final frame.
8. **Export masters** — **16:9** long-form master (language-agnostic) + **9:16** Shorts pulls.
9. **Localize metadata** — title/description/tags/end-card/pinned comment per market (EN + es/pt now).
10. **Publish** — playlist per series + per language; weekly cadence; monthly bedtime compilation.

> Always check each AI tool's current license/usage terms before publishing
> monetized content, and keep an asset/tool log.

---

## Tool categories (pick your stack)

- **Image (stills):** Midjourney / Stable Diffusion / Leonardo / Ideogram — tuned for soft, plush, golden-hour 3D.
- **Image-to-video / video:** Runway, Pika, Kling, Luma, Hailuo, Veo — use **slow** motion settings.
- **Music:** Suno / Udio (lullaby + orchestral + per-character leitmotifs) — or a composer/royalty-free.
- **Ambience & foley:** royalty-free nature/foley libraries; layer 3–5 ambience beds.
- **Non-verbal VO (optional):** a light human/AI pass for chirps/gasps/hums — **no words**.
- **Edit & grade:** DaVinci Resolve (best for the warm grade) / Premiere / CapCut.

---

## Design tokens (freeze once, reuse verbatim everywhere)

Paste the **exact** string into every image prompt for that character/prop. This is
how the brand stays consistent across episodes and across languages.

```
PROTECTOR token: "Bramble, a small round bear cub, soft honey-brown fur, big gentle
                  dark eyes, a little woven dried-grass cloak, a tiny leather repair
                  satchel, plush rounded proportions, calm kind expression"

WONDER token:    "Wisp, a tiny snowy owlet, fluffy white-and-cream feathers, oversized
                  amber eyes, stubby wings, endlessly curious expression, plush rounded
                  proportions"

PROP token:      "the firefly lantern — a small round glass lantern with a soft warm
                  golden glow and a gentle floating firefly inside, worn carry-handle"

WORLD token:     "Hollow Glen — a lush cozy forest of mossy roots, toadstools,
                  wildflowers, soft god-rays through tall trees, dust motes, a little
                  stream"
```

> Tip: generate a **character sheet** (3–4 views, neutral) per lead first and use it
> as an image reference (`--cref`/style-ref) so faces never drift.

---

## Prompt templates

### A. Still image (per shot)
```
[CHARACTER TOKEN(S)] + [PROP TOKEN if in frame], [gentle action/pose], [emotion on face].
Setting: [WORLD TOKEN] / [specific spot], [time of day].
Style: 3D animated, soft plush cozy, Pixar-cozy-but-softer, thick soft fur, subsurface
scattering, volumetric golden light, shallow depth of field, dust motes, lush nature,
family-film warmth.
Lighting/grade: [warm amber golden-hour | gently cool overcast (RIPPLE) | shimmering
wonder-glow (REACH) | dusky low (SETBACK) | warm bloom returning (TENDERNESS) | rich
golden glow with the lantern brightest (RESTORATION)].
Camera: [soft close-up | gentle medium | lush wide], 16:9 composition, room to breathe.
--ar 16:9
```

Example (TENDERNESS beat):
```
Bramble, a small round bear cub with soft honey-brown fur and a woven grass cloak,
gently cradling a shivering tiny snow owl, the firefly lantern glowing warmly beside them;
Wisp, a tiny snowy owlet with oversized amber eyes, leaning in close.
Setting: Hollow Glen, a mossy hollow under tall trees, dusk turning to night.
Style: 3D animated, soft plush cozy, subsurface scattering, volumetric light, shallow DOF,
dust motes, family-film warmth.
Lighting/grade: warm amber bloom returning, the lantern the key light.
Camera: soft close-up, 16:9. --ar 16:9
```

### B. Image-to-video (animate a still — SLOW)
```
Animate this image gently. [Subtle action: e.g., "the owlet's chest rises and falls,
a single firefly drifts, slow push-in on the lantern's glow"]. Keep character design
and the lantern identical. Camera: very slow [push-in / drift / parallax]. 4–6 seconds.
No fast motion, no morphing, no new objects. Soft, continuous, calm.
```

### C. Music & leitmotif (Suno/Udio or composer brief)
```
Mood: warm, tender, lullaby; [calm | wonder | uncertain | swelling | settled].
Instruments: soft piano, warm strings, harp/celesta; gentle, low dynamics; no percussion spikes.
Motif: [Protector = warm cello phrase | Wonder = light celesta/flute phrase | Prop = a soft 3-note chime].
Use: [beat — CALM/RIPPLE/REACH/SETBACK/TENDERNESS/RESTORATION]. Loopable, bedtime-safe.
Length: [~30–60s bed].
```

### D. Ambience & foley list (per episode)
```
Ambience beds: [forest day birdsong | night crickets | soft stream | wind in leaves | light rain].
Foley: [moss footsteps | fur rustle | lantern handle creak + chime | wing flutter | heartbeat (tender beat)].
Non-verbal vocals: [soft owlet chirp | bear hum/sigh | guest whimper → content coo]. NO words.
```

### E. End-card fact (optional; localizable / icon-first)
```
A soft illustrated card in the cozy style, 16:9. Default = ICON-ONLY (no text) to stay
language-free. Localized variant = one short sentence per market:
EN: "Real owls can turn their heads almost all the way around."
es: "..."  pt: "..."
```

> No title card with story text is required; if used, keep it to a short evocative
> episode name only. **Never add dialogue captions** — there is no dialogue.

---

## Consistency tactics (fight AI drift)

- **Reuse the exact token strings** — never paraphrase a character or the prop.
- **Character sheet + style reference** within a series (`--cref` / seed / style-ref).
- **Lock the palette & light model** to the grade curve in `04` — warm-dominant.
- **The lantern is sacred:** same shape every time; only its **glow state** changes.
- **Re-roll, don't settle:** if fur, eyes, or the lantern drift, regenerate. Cozy audiences are calm but attentive.

---

## Bedtime compilation assembly (the sleep moat, monthly)

1. Select **3–4 finished episodes** of similar calm energy (skip highest-peril ones).
2. Order them on a **descending energy curve** (most-engaging → most-soothing).
3. Insert **30–60s ambient bridges** (slow Hollow Glen scenes + continuous soft score) between episodes so it never jolts.
4. Keep **music continuous** across the whole runtime; normalize levels low and even.
5. End on a **near-silent starlit Hollow Glen** loop point (could cut back to the top).
6. Target **45–60 min**; export 16:9; title with the bedtime/SEO formula (`05`).
7. Disable jarring mid-rolls where possible; this is a sleep asset, not a retention sprint.

---

## Shorts funnel (3 / week)

- Pull the **2–3 most emotive 20–40s moments** marked in each episode template (tender/wonder beats).
- Format **9:16**; open on the single most emotive frame; end with a soft "full story →" nudge (visual, not spoken).
- Add the **prop + leitmotif** so Shorts are unmistakably the brand.
- Goal: Shorts = discovery → subscribe → long-form + bedtime library (the conversion layer).

---

## Localize-first publishing (the wedge)

Because the master is wordless, **one render serves every market.** Per language:

- Localized **title** (worry-loop formula), **description** (+ SEO keywords), **tags**.
- Same **thumbnail image** (no text) — optionally swap an end-card text card.
- Localized **pinned comment** (emotional question).
- **Channel strategy:** master channel (EN/global) first; add **es** + **pt** mirrors (reuse `/markets/latam/` strings, names, hashtags, calendar); then **hi/ar/vi**.
- Maintain a **per-language playlist** so each market binges in its own feed.

---

## Per-episode production checklist

- [ ] Script passes the QA in `03-episode-blueprint.md` (effort-not-magic, kindness-echo, safe-warm ending).
- [ ] All design tokens (leads + lantern + world) pasted unchanged into prompts.
- [ ] Stills generated, culled on-model, 16:9, graded by beat.
- [ ] Each still animated to slow 4–6s clips.
- [ ] Music scored by beat with leitmotifs + prop chime; ambience + foley layered; non-verbal vocals only (no words).
- [ ] Edit breathes (4–8s shots), soft dissolves only on time-passing, warm final frame held 2–4s.
- [ ] 16:9 master exported (language-agnostic) + 2–3 Shorts pulls (9:16).
- [ ] Metadata localized per market (EN + es + pt); per-language playlist updated.
- [ ] Added to bedtime-compilation queue for the month.
- [ ] Asset/tool log updated for licensing.

---

## Publishing cadence (recap from `00`)
- **1 long-form / week** + **3 Shorts / week** + **1 bedtime compilation / month** + **4–6 seasonal specials / year**.
- **Batch-produce** a full mini-arc before publishing so the cadence never breaks.
- Pin the **series opener**; keep a clean **playlist per series + per language**.
- First comment / pinned = an **emotional question** (community, not CTA).
