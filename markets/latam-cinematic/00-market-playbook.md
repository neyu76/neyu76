# South America Market Playbook — CINEMATIC DRAMA (pure drama + visual art)

Localization layer that pivots the **Cinematic Drama** pipeline (the pure-drama /
visual-art / 4-Act branch, NOT the viral one) to the **South American market**.
The story/visual engine in `production-prompts/PIPELINE-drama-cinematic.md` is
UNCHANGED — this playbook only swaps **language, cast fauna, names, sincere
insults, settings, music, captions, and voice locale**. The `*-drama-cinematic-latam`
skills + the LatAm cinematic master prompt reference this file.

> This is a SEPARATE market kit from `markets/latam/` (which localizes the older
> viral pipeline). Use this one for the pure-drama, 4-Act, visual-art channels.

---

## 0. WHY CINEMATIC DRAMA WINS IN SOUTH AMERICA (the thesis)
South America is the global home of the **telenovela** — long-form melodrama about
family, betrayal, class, sacrifice and just deserts. The cinematic-drama format is
the telenovela compressed into a beautiful, muted-friendly, AI-animated short.
We are not introducing a new taste; we serve a beloved one with **deliberate images
and real emotion** instead of memes. The audience already cries on cue at
*la familia* wronged and cheers when *le llegó el karma*.

Cultural pillars to lean on:
- **La familia es sagrada** — a parent's sacrifice for a child is the maximum pull.
- **Justicia y fe** — the righteous poor outlasting the corrupt rich is a cultural fantasy.
- **Melodrama is respected, not cringe** — let scenes breathe, let tears fall, hold the frame.

**No meme slang.** This branch forbids internet/meme talk (mogged/glow-up/etc.).
Insults are sincere and personal (see §4), the way a telenovela villain wounds.

---

## 1. LANGUAGE STRATEGY
- **Primary (default): `es-419`** — neutral Latin American Spanish (Argentina, Colombia, Peru, Chile, Venezuela, Ecuador, Bolivia, Uruguay, Paraguay + spillover).
- **Brazil: `pt-BR`** — Brazilian Portuguese; Brazil is the region's largest TikTok market — treat it as its own channel.
- Run TWO channels (one es-419, one pt-BR); same scripts, localized separately. Never mix languages in one video.
- Spoken dialogue = the target locale. Vietnamese/English appear ONLY in the review phase as a gloss for the editor.
- **Pace note:** Spanish & Portuguese pack more syllables per word; this branch already runs the slower DRAMA band (**100-130 WPM**) with silent Peaks, so the extra syllables fit naturally. Keep lines short (one breath, ~4-9 words) and let the PEAK go nearly silent.

---

## 2. SOUTH-AMERICAN FAUNA CASTING TABLE (the visual differentiator)
Cast native/iconic South American animals so the world is unmistakably the region.

| Role | Best animals | Reads as |
|------|--------------|----------|
| **HERO** (loving worker/parent) | **Capybara/Carpincho/Capivara** (calm, humble, beloved icon) · Ox/Buey · Burro · Llama · Armadillo/Tatú · Sloth/Perezoso · Tapir | honest, gentle, underestimated |
| **TYRANT** (moneyed criminal) | **Jaguar/Onça** · Caiman/Yacaré/Jacaré (loan shark, land-grabber) · Harpy Eagle · Puma · Anaconda (finance) | powerful, smooth, cruel |
| **BETRAYER** (materialistic insider) | **Macaw/Guacamayo/Arara** (showy, vain) · Toucan/Tucán · Coati · Flamingo | glamorous, self-serving |
| **INNOCENT** (the child) | baby capybara · llama cria · fawn · baby sloth · duckling | pure, vulnerable anchor |
| **JUSTICE** (calm authority) | **Andean Condor** (majestic, sees all → judge) · Owl/Búho/Coruja · Spectacled Bear/Oso de Anteojos (detective) | incorruptible authority |
| **ACCOMPLICE** (enables the crime) | Vulture/Urubú · Opossum/Zarigüeya/Gambá · Coati · Piranha · slick Fox/Zorro (lawyer) | shifty, expendable / slippery |

Rules: one hero / one villain, never reuse an animal across two roles, match job to nature (capybara builds/farms, caiman does loans, condor judges, macaw flaunts), distinct silhouettes, **≤15 assets/project**, assign a `@Handle` + a frozen voice profile to each.

> Signature mascot: the **capybara** — beloved, humble, ideal recurring hero + channel avatar.

---

## 3. NAMES (lock per locale)
**Spanish (es-419):**
- Hero (father/worker): Mateo, Tomás, Joaquín, Bruno, Aurelio · Mother (betrayer): Carmen, Valeria, Delia
- Villain: Don Salazar, Don Rómulo, El Patrón, Don Cipriano · Innocent (child): Lucía, Sofía, Pedrito, Tomasito
- Justice: Don Augusto (condor), Comisario Oso, Jueza Lechuza · Accomplice: Tito, Nacho, Dr. Zorro (lawyer)

**Portuguese (pt-BR):**
- Hero: Tião, Chico, Zé, Bento, Aurélio · Mother (betrayer): Vera, Marlene, Célia
- Villain: Coronel Genaro, Seu Rômulo, o Patrão · Innocent (child): Lina, Bia, Pedrinho, Tiãozinho
- Justice: Seu Augusto (condor), Delegado Urso, Juíza Coruja · Accomplice: Zeca, Nando, Dr. Raposa (lawyer)

---

## 4. SINCERE INSULT KIT (NO meme slang — telenovela-style wounds)
The personal insult to reverse is delivered straight, cruel, and human — never as a meme.
- **Spanish:** "No eres nada, [Nombre]. Un don nadie." · "Siempre fuiste un perdedor." · "Esto no te incumbe." · "Pobre diablo." · Karma line: "Le llegó el karma." / "Al final, la justicia llega."
- **Portuguese:** "Você não é nada, [Nome]. Um zé-ninguém." · "Sempre foi um perdedor." · "Isso não é da sua conta." · "Pobre coitado." · Karma line: "O karma chegou." / "No fim, a justiça vence."
- The silent reversal at the end is mechanic-identical: the "don nadie / zé-ninguém" now keeps the home, the child, the dignity.

---

## 5. SETTINGS + VISUAL SIGNATURE (pick one per series; this branch is visual-led)
Each series locks a **recurring motif** + an emotion→grade map + 2-3 signature shots.
- **Andean village + mercado** (terraces, ponchos) — motif: a hand-woven blanket / a wooden swing on the hillside · grade: earthy warm vs cold mountain blue.
- **Amazon riverside stilt house** (lush green, canoe) — motif: a carved canoe paddle · grade: deep green / golden river light.
- **Pampas estancia** (gaucho country, big sky) — motif: a leather mate gourd / a fence post · grade: golden grass sunset.
- **Barrio hillside** (colorful stairs) — motif: a painted door / a kite on a wire · grade: warm pastel vs cold night.
- **Coastal fishing town** (boats, nets) — motif: a small red boat · grade: teal sea / amber dusk.

Emotion→grade (locked across the branch): family = warm amber · villain = cold blue-gray · loss/rock-bottom = desaturated gray · karma/police = blue-red flash · restoration = glowing gold (golden hour). Signature shots recur every part (e.g., low-angle on the jaguar, macro tear on the child's drawing, slow-mo embrace, pull-back to the golden home).

---

## 6. MUSIC FLAVOR (emotional, with regional color)
- Loss/grief: Andean charango/quena, or Brazilian viola caipira, or bolero strings; a music box for the child.
- Tension/scheming: low pulse + cuíca/berimbau accents (BR).
- Reunion/warmth: nylon guitar + warm strings.
- Restoration/golden hour: rising strings / brass lift.
- Emotion first; regional instruments are seasoning. **Keep the PEAK nearly silent** — let SFX + a single instrument carry it.

---

## 7. UPLOAD / HASHTAGS / POSTING
- Title & captions in the target locale. Pose the injustice as a question; emotion over clickbait.
- **es hashtags:** #historias #animacion #karma #justicia #familia #emocionante #reels #parati #cuentos #finalfeliz
- **pt hashtags:** #historias #animacao #karma #justica #familia #emocionante #reels #fyp #contos #finalfeliz
- Calendar hooks: **Día de la Madre / Dia das Mães**, **Día del Padre / Dia dos Pais**, **Navidad/Natal**, Carnaval texture.
- Cadence: batch a whole series, post daily/every other day, pin Part 1, one playlist per series, first comment teases the next part.

---

## 8. EMOTIONAL TIER (this branch's scale)
🟣 S = a parent + a child + a moneyed betrayal + a cruel mid-series win for evil + a golden restoration. · 🔵 A = strong, needs clean emotional execution. · 🟢 B+ = gentler / wholesome.

---

## 9. PIPELINE MAP (South America · Cinematic Drama)
```
topic-drama-cinematic-latam  (12 locked SERIES BRIEFS in es-419 or pt-BR; 6-beat + 4-act, visual signature)
  -> script-drama-cinematic-latam  (adopt verbatim -> 4-ACT shot list + handoff, dialogue in es/pt)
     -> markets/latam-cinematic/MASTER-PROMPT-drama-cinematic-latam.md
        (Asset Bank · Seedance · KLING · Veo Omni w/ Spanish/PT voice lock · es-or-pt review, by act)
```
All three reference THIS playbook for fauna, names, sincere insults, settings/visual signature, music, and voice locale. Channel identity: see `channel-setup.md`.
