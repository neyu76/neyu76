# 04 — Visual Style Guide & Editing

Lock these so every series looks like it came from the same studio, and so AI
image/video generations stay consistent across parts.

---

## Visual identity

- **Render style:** 3D animated, anthropomorphic animals — *Zootopia* /
  Illumination feel. Soft global illumination, slightly stylized proportions,
  expressive faces with big readable eyes. Familiar, family-movie polish.
- **Aspect ratio:** 9:16 vertical, 1080x1920.
- **Framing for vertical:** keep faces in the upper-middle third; leave lower
  third for burned-in captions.
- **Character consistency:** lock each character's outfit, color, and silhouette
  in a one-line "design token" reused in every prompt (see pipeline doc). The
  outfit IS the character — never change it mid-series.

### Costume = class (deliberate stereotyping)
- **Hero:** work clothes (overalls, plaid, tool belt, apron), worn but clean.
- **Tyrant:** tailored suit, watch, sunglasses, luxury car keys.
- **Betrayer:** glam — jewelry, pearls, designer bag, heels.
- **Innocent:** one bright solid-color item (yellow shirt) so the eye locks onto them.
- **Justice:** uniform/badge or plain suit + glasses; understated authority.
- **Henchman:** dark coat, hunched, shifty.

---

## Color grading & lighting = emotion (non-negotiable)

This is half the storytelling. Grade by emotional beat, not by location.

| Emotional beat | Palette | Lighting | When |
|----------------|---------|----------|------|
| Despair / betrayal / scheming | cold blue, gray, teal | low-key, hard shadows, underlit | Loss, Injustice, villain scenes |
| Endurance / labor | desaturated, dusty, overcast | flat, harsh midday | Demolition / rock-bottom |
| Hope / love / family | warm amber, soft gold | golden hour, soft backlight | reunions, the promise |
| Triumph / rebirth | rich gold, saturated, glowing | sunset, lens warmth, sparkle on gold | hero's glow-up, finding the reward |
| Karma / downfall | cold blue + red/blue police flash | harsh, exposed | arrest, exposure |

Rule of thumb: **villain = cold, family = warm, victory = golden.**
When the hero "mogs back," the grade flips from cold to gold — let the audience *feel* the reversal.

---

## Camera language

- **Close-ups** dominate. We're farming emotion: the villain's smirk, the
  innocent's wet eyes, the hero's clenched jaw. At least 1 close-up of the
  innocent per part.
- **Low-angle on the Tyrant** (makes them loom), **slightly high-angle on the
  Hero early** (makes them small) — then flip the angles at the rebirth.
- **Wide establishing only when it sells status** (the villa, the demolished
  house) — and keep it under 1.5s.
- **Insert shots** of the promise object (swing, ring, recipe book) and the motif
  (the family painting, the gold) — these carry the through-line.

---

## Editing rules

- **100% hard cuts.** No fades, no spins, no "whoosh" transitions. The energy
  comes from the cut itself.
- **Match-on-action & match-on-audio:** cut on a movement or on a beat of the
  voiceover so cuts feel motivated, not random.
- **Pacing:** every shot 1.5-3s. If a shot has no new information, it's too long.
- **Cross-cutting:** intercut two threads (hero suffering / villain gloating;
  heist / tip-off call) to build rhythm and dread.
- **Hold the last frame** of the part 1-2s longer than the others — that's the
  cliffhanger beat where retention is decided.

---

## Sound design

- **Voiceover-led:** dialogue/VO is the backbone; cut picture to the VO rhythm.
- **Score by beat:** somber piano (loss), tense low strings/pulse (scheming &
  heist), warm strings/swell (reunion), triumphant rising theme (rebirth).
- **One signature sound** per recurring motif (e.g., the swing's creak, a music
  box) so the audio cues the callback before the image does.
- **Mix for mute viewing first:** captions must carry the story with sound off,
  but the score must reward sound-on viewers.

---

## Consistency checklist across parts

- [ ] Same render style + lighting model every part.
- [ ] Each character's outfit/color identical to Part 1.
- [ ] Promise object looks the same each appearance (built/destroyed/rebuilt states only).
- [ ] Grade matches the emotional beat table.
- [ ] Captions use the same font/size/position throughout the series.
- [ ] Title card format identical ("PART # — TITLE").
