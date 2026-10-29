# Master Video Prompt (Ink Explainer style)

These prompts animate your finished beat images (image-to-video). This style barely moves, so most beats can stay as still images with a slow zoom in your editor. Animate only the strongest 15–25% of beats.

---

## PART A: Image prompts → video prompts

```
You are the motion director for a faceless YouTube explainer channel drawn in a simple hand-inked stick-figure style, with clean flat infographic inserts. Write image-to-video prompts that animate my existing beat images.

INPUT: [PASTE YOUR IMAGE PROMPTS (with beat numbers, SCENE/DIAGRAM labels and script text)]
HOW MANY: [ALL beats / the [N] strongest beats]
CLIP LENGTH: [4] seconds each

If I ask for fewer than ALL, pick the opening hook, emotional turns, moments with movement (walking, running, falling), and diagrams that reveal something (dots appearing, an arrow landing). Spread them across the whole video.

LOCKED STYLE (put it in every prompt)
Simple 2D hand-drawn cartoon animation, bold black ink outlines, flat colors, 16:9. Limited, snappy, cut-out style motion like a whiteboard explainer. No morphing, no 3D, no extra limbs, no realistic shading, no lip-sync. The stick figure keeps its perfect white circle head and thin black stick limbs at all times.

SCENE MOTION
- One main action: a blink, an eyebrow lift, a head tilt, a simple 2–3 frame walk cycle, dragging a prop, a slump of the shoulders.
- At most one ambient motion: grass swaying, clouds drifting, dust puffs, a sweat drop falling, motion lines flicking.
- Camera: static or a very slow push-in only.

DIAGRAM MOTION
- Elements pop or draw on: map dots appear one by one, an arrow slides in and stops, a label pops in with a small bounce, a line draws itself.
- The background stays perfectly still. Text stays sharp and spelled exactly as in the image.
- Camera: static.

STANDALONE RULE
Every prompt fully describes the starting image, the one action, the ambient motion, the camera, and repeats the style line.

OUTPUT FORMAT (for each clip)
[#]. Beat [#] [SCENE/DIAGRAM]: "<exact script text>"
Video Prompt: <one standalone paragraph>
Camera: …
Duration: [X]s
```

---

## PART B: Single-clip templates

### Scene

```
[STARTING IMAGE: setting + stick figure + costume + props].
The stick figure has a large perfect white circle head outlined in thick black, dot eyes, a thin black line body and stick limbs.
Main action: [ONE SIMPLE ACTION].
Ambient motion: [ONE: grass sways / clouds drift / dust puffs / sweat drop].
Camera: [static / very slow push-in].
Simple 2D hand-drawn cartoon animation, bold black ink outlines, flat colors, snappy cut-out motion, no morphing, character stays on-model, 16:9, [4] seconds.
```

### Diagram

```
[STARTING IMAGE: diagram type + label + colors].
Motion: [dots pop in one by one / the arrow slides in and stops / the label pops in with a small bounce].
Everything else stays still and the text stays sharp and unchanged.
Camera: static.
Clean flat vector infographic animation, smooth thick black outlines, no morphing, 16:9, [4] seconds.
```

## Editing tips (CapCut / Premiere)

- Still images: 105% → 110% slow zoom over the beat, then a hard cut. No fancy transitions.
- Diagram labels can be added in the editor instead of the generator, so the spelling is always perfect (use Montserrat ExtraBold or Nunito Black).
- Add a soft "pop" sound when a diagram appears and light whooshes for walking scenes.
- Put your own channel logo in the bottom-right corner on every frame.
