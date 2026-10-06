# Master Video Prompt (Quiet Equity niche)

These prompts animate your finished beat images (image-to-video).
- PART A: paste it into a chat with your image prompts or script to get video prompts.
- PART B: a fill-in template for writing a single clip prompt by hand.

---

## PART A: Image prompts → video prompts

```
You are the motion director for a faceless YouTube channel that tells cinematic second-person money stories in a flat 2D cartoon webcomic style. Write image-to-video prompts that animate my existing beat images.

INPUT: [PASTE YOUR IMAGE PROMPTS (with beat numbers and script text) OR THE FULL SCRIPT]
HOW MANY: [ALL beats / the [N] strongest beats]
CLIP LENGTH: [5] seconds each

If I ask for fewer than ALL, pick the beats with the most emotional or visual payoff: the opening hook, each level's first beat, shocking numbers or bills, rich-versus-poor contrasts, recurring motifs and callbacks, the emotional turn near the top, and the final outro line. Spread them across the whole video.

LOCKED STYLE (put it in every prompt)
Flat 2D cartoon webcomic animation, bold clean black outlines, flat cel shading, desaturated slate-blue and gray palette with muted warm accents, 16:9. Limited, subtle, intentional motion. No morphing, no warping, no extra limbs, no lip-sync talking; characters stay on-model and the outlines stay crisp.

LOCKED PROTAGONIST (describe him in every clip he appears in)
A young man with an oversized head, messy curly jet-black hair, thick black rectangular glasses, heavy half-lidded tired eyes with faint dark under-eye lines, thick slightly furrowed black eyebrows, pale off-white skin and a small flat frowning mouth, always deadpan. Outfit by tier: black hoodie (broke) → black crewneck sweater (middle) → black quarter-zip (upper-middle) → dark tailored jacket (rich).
Signature look (matches the channel logo, brand/protagonist-reference.webp): black hoodie with the hood up. Attach that image as a character reference whenever your generator allows it.
How he moves: minimal. Slow blinks, a small head turn, eyes flicking to the side, a slight tightening of the jaw, lowering an object. He never smiles widely or gestures big. His stillness is the point.

MOTION RULES
- ONE main action per clip, plus at most one ambient motion (a flickering light, drifting dust, steam, rain, a passing crowd, papers settling).
- Camera moves are slow and simple: a gentle push-in, slow pull-back, slow pan or tilt, rack focus, or static. Use at most one camera move per clip, and no shaky or fast cuts.
- Background characters may be more animated (laughing, rushing, nodding) to keep the calm-versus-chaos contrast.
- Insert shots (phones, bills, screens): text appears, a number ticks or a notification pops in, a finger taps, and the paper unfolds or slides.
- Metaphor shots: literal, simple motion (envelopes stacking into a tower, a name sliding to the top of a list, gears turning).
- Lighting follows the tier: cold flickering fluorescent at the bottom, warming to golden at the top. Flashbacks are desaturated. Transitions between worlds can use a slow double-exposure dissolve.
- The last clip of the video ends on a slow fade to black.

STANDALONE RULE
Every prompt fully describes the scene, characters, action, camera move, lighting and mood, and repeats the style line. Never reference another clip.

OUTPUT FORMAT (for each clip)
[#]. Beat [#]: "<exact script text>"
Video Prompt: <one standalone paragraph: starting scene, protagonist description, main action, ambient motion, camera move, lighting, mood, style line>
Camera Move: …
Duration: [X]s
```

---

## PART B: Single clip template

```
[STARTING SCENE: setting + who is in frame + key props].
The protagonist is a young man with an oversized head, messy curly jet-black hair, thick black rectangular glasses, heavy half-lidded tired eyes with faint dark under-eye lines, thick slightly furrowed black eyebrows, pale off-white skin and a small flat frowning mouth, always deadpan, wearing [OUTFIT].
Main action: [ONE SUBTLE ACTION, e.g. "he blinks slowly and lowers the bill"].
Ambient motion: [e.g. "the fluorescent light flickers twice" / "steam rises" / "background patients shift"].
Camera: [slow push-in / slow pull-back / slow pan / slow tilt / rack focus / static].
Lighting: [TIER LIGHTING]. Mood: [2–3 WORDS].
Flat 2D cartoon webcomic animation, bold clean black outlines, flat cel shading, desaturated slate-blue and gray palette with muted warm accents, subtle limited motion, no morphing, characters stay on-model, 16:9, [5] seconds.
```
