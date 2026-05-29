# 06 — Production Pipeline & AI Prompt Templates

End-to-end workflow to turn a script into a finished part. Tool names are
examples — swap in whatever you have access to; the *prompt structure* is what matters.

---

## Pipeline overview (per series)

1. **Write the Series Bible** — use `/series-templates/TEMPLATE-series-bible.md` (cast, promise object, 7-part beat map).
2. **Write each part** — use the per-part template in `03-episode-blueprint.md`.
3. **Lock character design tokens** — one frozen description per character (below).
4. **Generate key images** — one consistent still per shot (character + setting + grade).
5. **Animate** — image-to-video on each still (or text-to-video for motion shots).
6. **Voiceover** — TTS per character voice; export per line.
7. **Edit** — assemble on the VO, hard cuts, burn captions, grade, score.
8. **Export** 1080x1920, add title card + part label.
9. **Publish** — playlist per series; consistent posting cadence; cliffhanger caption.

---

## Tool categories (pick your stack)

- **Image (stills):** Midjourney / Stable Diffusion / DALL·E / Leonardo / Ideogram (good for in-image text).
- **Image-to-video / video:** Runway, Pika, Kling, Luma Dream Machine, Sora-class tools, Hailuo.
- **Voiceover (TTS):** ElevenLabs / OpenAI TTS / PlayHT — assign one voice per character.
- **Edit & captions:** CapCut (fast, auto-captions), Premiere, DaVinci Resolve (best grading).
- **Music/SFX:** Suno/Udio for theme, plus a royalty-free SFX library.

> Always check each tool's current license/usage terms before publishing
> monetized content. Keep a record of which tool generated which asset.

---

## Character design token (freeze once, reuse everywhere)

Write ONE line per character and paste it into *every* image prompt for that
character. This is how you keep them consistent across parts.

```
HERO token:    "Buck, a male beaver, warm brown fur, kind tired eyes, blue denim
               overalls over a red plaid shirt, worn leather tool belt, stocky
               friendly build"
TYRANT token:  "Mr. Crane, a male lion, golden mane slicked back, charcoal tailored
               three-piece suit, gold watch, cold amber eyes, arrogant posture"
INNOCENT token:"Pip, a small beaver kit, oversized round eyes, bright yellow t-shirt,
               tiny, hopeful"
```

---

## Prompt templates

### A. Still image (per shot)
```
[CHARACTER TOKEN(S)], [action/pose], [emotion on face].
Setting: [location], [time of day].
Style: 3D animated, Pixar/Illumination style, anthropomorphic, soft global
illumination, expressive, family-film quality.
Lighting/grade: [cold blue low-key | golden hour warm | police-flash | dusty overcast].
Camera: [extreme close-up | close-up | low-angle medium | wide establishing],
9:16 vertical composition, subject in upper-middle third, room for lower-third captions.
--ar 9:16
```

Example (gut-punch shot):
```
Pip, a small beaver kit with oversized round eyes and a bright yellow t-shirt,
clutching a fence, tears welling, mouth trembling.
Setting: front yard of a half-built wooden house, dusk.
Style: 3D animated, Illumination style, anthropomorphic, soft global illumination.
Lighting/grade: cold blue low-key, hard shadows.
Camera: extreme close-up on his face, 9:16 vertical. --ar 9:16
```

### B. Image-to-video (animate a still)
```
Animate this image. [Subtle action: e.g., "the kit's lip trembles, a single tear
falls, slow push-in on his eyes"]. Keep character design identical. Camera: slow
[push-in / pan]. 2-3 seconds. No new objects, no morphing. Consistent lighting.
```

### C. Voiceover (TTS direction)
```
Voice: [warm, weary male | smooth smug male | small earnest child | flat calm authority].
Pace: slightly fast, conversational. Emotion: [despair | contempt | hope | menace].
Line: "[the line]"
```

### D. Title card / in-image text (if your image tool supports text)
```
Bold uppercase title "THE DEMOLITION", top-center, clean sans-serif, white with
subtle shadow, over the establishing shot. Small "PART 3" tag top-left.
```

---

## Consistency tactics (fight AI drift)

- **Reuse the exact token string** for a character in every prompt — don't paraphrase.
- **Generate a character sheet first** (front/3-4 view, neutral) and use it as an
  image reference / `--cref` style reference where supported.
- **Same seed / same style reference** within a series where the tool allows.
- **Lock the outfit and palette** — never restyle a character mid-series.
- **Re-roll, don't settle:** if a face drifts, regenerate rather than shipping inconsistency. Audiences notice.

---

## Per-part production checklist

- [ ] Script approved against the per-part QA list (`03-episode-blueprint.md`).
- [ ] All character tokens pasted unchanged into prompts.
- [ ] Stills generated + culled to ~18-30 keepers, all on-model.
- [ ] Each still animated to 1.5-3s clips.
- [ ] VO recorded per line, per character voice.
- [ ] Edit on the VO, hard cuts only, grade by beat.
- [ ] Captions burned in (readable muted), title + part label added.
- [ ] Cliffhanger frame held 1-2s.
- [ ] Exported 1080x1920; added to the series playlist.
- [ ] Asset/tool log updated for licensing.

---

## Publishing cadence (channel growth)

- **Batch-produce** a whole series before posting Part 1 (so you never break a cliffhanger streak).
- **Post on a fixed schedule** (e.g., daily or every other day) to train the algorithm and the audience.
- **Pin Part 1** and keep a clean **playlist per series** so new viewers binge from the top.
- **First comment = next-part teaser** ("Part 4 is where it all turns…").
- **Recycle the hook** as the thumbnail/first frame; the strongest emotion goes first.
