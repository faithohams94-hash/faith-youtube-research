# Master Image Prompt (Ink Explainer style)

See `STYLE-GUIDE.md` and the pictures in `references/`. Attach two or three reference images to your generator whenever it allows it (one stick-figure scene and one diagram).

- PART A: paste it into a chat with your script to get an image prompt for every beat.
- PART B: fill-in templates for writing single prompts by hand.

---

## PART A: Script → image prompts

```
You are the visual director for a faceless YouTube explainer channel drawn in a simple hand-inked stick-figure style. Turn the script below into image prompts for EVERY beat, without skipping a word.

BEAT RULES
- Split the script in order into beats of 13 words or fewer (3–5 seconds of narration each).
- Split long sentences at natural pauses.
- The beats together must reproduce the script word for word. Number every beat.

TWO SHOT TYPES. Label every beat as SCENE or DIAGRAM.
- SCENE (about 65% of beats): a story moment with the stick figure.
- DIAGRAM (about 35%): use it whenever the narration states a fact, number, place, danger, or body mechanic.

LOCKED SCENE STYLE (put it inside EVERY scene prompt)
Simple 2D hand-drawn cartoon, bold slightly wobbly black ink outlines like marker on paper, flat colors with no gradients on characters, minimal wide background with one horizon line and few props, lots of empty space, 16:9, bottom 12% and bottom-right corner kept clear.

LOCKED STICK FIGURE (describe it fully in EVERY scene prompt)
A stick figure with a large perfect white circle head (one third of its height) outlined in thick black, two small black dot eyes, simple line eyebrows and a small line mouth, a single thin black line torso, thin stick arms and legs, and small round hands. Emotion comes only from the eyebrows, mouth and posture.
Costume by era (one piece only):
- Prehistoric: messy shaggy brown hair, a ragged brown fur tunic with a belt, holding a wooden spear with a stone tip
- Modern: plain stick body, no clothes, optional single prop
- Other eras: one costume piece only (hat, helmet, toga)

SCENE PALETTES
- Calm: pale sky blue over warm tan grass with light yellow grass strokes
- Hardship: flat storm-gray layered clouds over dusty brown cracked earth, a bare dead tree
- Modern: light cyan sky, cream and light-gray blocky flat buildings, gray pavement, a simple street sign

LOCKED DIAGRAM STYLE (put it inside EVERY diagram prompt)
Clean flat vector infographic illustration, smooth even thick black outlines, off-white or warm cream background, muted olive green and brick red with charcoal text, ONE short bold all-caps rounded sans-serif label, thick straight arrows with solid triangle heads, no clutter, 16:9, bottom 12% and bottom-right corner kept clear.
Diagram types: map with brick-red location dots; a single object with an arrow and a warning label; a semi-realistic flat vector person (NOT the stick figure) with an arrow and a one-word label; a big bold number with one icon; a THEN vs NOW split.

COMPOSITION RULES
- Scenes: eye-level wide shot, full body, figure centered or slightly left, key prop on the opposite third.
- Draw motion cues in: curved swing lines by the arms, dust puffs, sweat drops.
- Diagrams: one idea and at most two labels. Text must be short, spelled exactly, and legible.

STANDALONE RULE
Each prompt fully describes the subject, setting, action, expression, palette and style line. Never write "same as before".

OUTPUT FORMAT (for every beat)
Beat [#] (~[seconds]s) [SCENE or DIAGRAM]
[Script Segment Text]: "<exact words>"
Image Prompt: <one standalone paragraph>
On-screen Text: <exact label or "none">
Mood: …

Continue in batches until the last beat. Never summarize or skip beats.

SCRIPT:
[PASTE FULL SCRIPT HERE]
```

---

## PART B: Single-image templates

### Scene

```
[SCENE: where + what the figure is doing + one or two props].
A stick figure with a large perfect white circle head outlined in thick black, two small black dot eyes, [EYEBROWS + MOUTH FOR THE EMOTION], a single thin black line torso, thin stick arms and legs and small round hands, [COSTUME FOR THE ERA], [POSTURE].
Background: [PALETTE: calm / hardship / modern], minimal, one horizon line, lots of empty space.
Simple 2D hand-drawn cartoon, bold slightly wobbly black ink outlines like marker on paper, flat colors, eye-level wide shot, full body, 16:9, bottom 12% and bottom-right corner kept clear.
```

### Diagram

```
[DIAGRAM: map / object / vector person / big number / split] showing [THE ONE IDEA].
Label: "[ONE OR TWO WORDS IN ALL CAPS]" in bold rounded sans-serif charcoal text, placed [top-right / top-center in a dark rounded pill / beside the arrow].
[Arrow: thick charcoal or brick-red arrow pointing at …].
Clean flat vector infographic, smooth thick black outlines, [off-white / warm cream] background, muted olive green and brick red accents, no clutter, 16:9, bottom 12% and bottom-right corner kept clear.
```

---

## Ready-made examples (recreate the reference images)

**Scene, calm prehistoric** (`references/scene-caveman-savanna.jpg`)
A stick figure standing still in an open savanna, holding a tall wooden spear with a stone tip upright in its left hand. Large perfect white circle head outlined in thick black, two small black dot eyes, a tiny flat line mouth, neutral blank expression, messy shaggy brown hair, a ragged brown fur tunic with a belt, thin black stick arms and legs. Pale sky-blue sky over a flat warm tan field with light yellow grass strokes, one horizon line, lots of empty space. Simple 2D hand-drawn cartoon, bold slightly wobbly black ink outlines, flat colors, eye-level wide shot, full body, centered, 16:9.

**Scene, hardship prehistoric** (`references/scene-caveman-drought.jpg`)
The same kind of shaggy-haired stick figure in a ragged brown fur tunic trudging to the left, hunched and exhausted, dragging a stone-tipped spear behind it so it scrapes a line in the dirt with small dust puffs. Worried tilted eyebrows, droopy tired eyes, a small wavy frown. Flat storm-gray layered clouds over dry brown cracked earth, a bare leafless dead tree on the right third. Simple 2D hand-drawn cartoon, bold wobbly black ink outlines, flat colors, eye-level wide shot, 16:9.

**Scene, modern urgency** (`references/scene-modern-city.jpg`)
A plain stick figure with a large white circle head walking fast to the left on a gray city sidewalk, arms swinging with small curved motion lines, a nervous gritted-teeth grimace and darting eyes. Light cyan sky, flat cream and light-gray blocky buildings, a green street sign with a white arrow pointing right on a gray pole. Simple 2D hand-drawn cartoon, bold black ink outlines, flat colors, eye-level wide shot, 16:9.

**Diagram, map**
A flat world map with olive-green continents outlined in thick black on a warm cream background, many small brick-red dots spread across every continent. Label "GLOBAL HELP" in bold charcoal all-caps rounded sans-serif in the top-right corner. Clean flat vector infographic, 16:9.

**Diagram, caution object**
A single thick brick-red rope or tube with dark outlines, winding left to right across a plain off-white background with one loose loop in the middle. A thick charcoal arrow points at the loop from the upper right, with the label "CAUTION" in bold charcoal all-caps rounded sans-serif. Clean flat vector infographic, 16:9.

**Diagram, body mechanics**
A semi-realistic flat vector man in profile in a deep squat, olive-green t-shirt, slate-gray shorts, dark sneakers, fists together at the chest, back upright, on a thin black ground line. Label "UPRIGHT" in cream all-caps text inside a dark charcoal rounded pill at the top center. A thick brick-red downward arrow on the right with the label "GRAVITY" in brick red. Off-white background, clean flat vector infographic, 16:9.
