"""Build the Episode 1 image + video prompt book from script.md and shots.py.

usage: python3 build.py   (run from this folder)
writes ../image-video-prompts.md and ../image-video-prompts.html
"""
import html, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from shots import SHOTS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WPS = 2.6  # narration speed, words per second

# ---------------------------------------------------------------- locked looks
STYLE = ("Flat 2D cartoon webcomic illustration in the Somber Journal style, bold clean black outlines, flat cel shading, "
         "semi-chibi characters with oversized heads, detailed lived-in background, layered foreground, mid-ground and background, "
         "cinematic framing with subtle depth of field and a soft rim light, 16:9 widescreen, bottom 15% of the frame kept free of "
         "important detail for captions")
NEGATIVE = ("no photorealism, no 3D render, no anime style, no extra fingers, no distorted hands, no garbled text, "
            "no watermark, no logo, no speech bubbles, no captions baked into the image")
VSTYLE = ("Flat 2D cartoon webcomic animation, bold clean black outlines, flat cel shading, limited, subtle, intentional motion, "
          "no morphing, no warping, no extra limbs, no lip-sync talking, characters stay exactly on-model, outlines stay crisp, 16:9")

FACE = ("a young man with an oversized head, messy curly jet-black hair, thick black rectangular glasses, heavy half-lidded eyes, "
        "thick slightly furrowed black eyebrows, pale off-white skin and a small flat mouth")
OUTFIT = {
    "owner": "at thirty-four, calm and confident with a faint knowing half-smile, wearing a dark charcoal tailored jacket over a black tee and a slim steel watch",
    "past": "at twenty-nine, quiet and composed, wearing a plain black crewneck sweater over a white collar, gray slacks and an office ID lanyard",
    "home": "at home, wearing a black hoodie with the hood down and gray sweatpants",
}
MARCUS_PAST = ("Marcus is a tall, broad-shouldered man of thirty-six with slicked-back dark brown hair, a square jaw, a smug wide grin, "
               "a fitted light-blue dress shirt with rolled sleeves, a slim navy tie and a chunky gold watch")
MARCUS_NOW = ("Marcus, five years older at forty-one, has the same slicked-back dark brown hair now coming loose with gray at the temples, "
              "a square jaw, red-rimmed tired eyes, a tailored charcoal suit dark with sweat at the collar, a loosened navy tie and the same chunky gold watch")
CHARS = {
    "me_owner": "The protagonist (the narrator) is " + FACE + ", " + OUTFIT["owner"],
    "me_owner_hands": "The hands belong to the protagonist: pale off-white skin, the cuff of a dark charcoal tailored jacket and a slim steel watch",
    "me_past": "The protagonist (the narrator) is " + FACE + ", " + OUTFIT["past"],
    "me_past_hands": "The hands belong to the protagonist: pale off-white skin and the sleeve of a plain black crewneck sweater",
    "me_home": "The protagonist (the narrator) is " + FACE + ", " + OUTFIT["home"],
    "me_home_hands": "The hands belong to the protagonist: pale off-white skin and the sleeve of a black hoodie",
    "marcus_past": MARCUS_PAST,
    "marcus_now": MARCUS_NOW,
    "marcus_now_hands": "The hand belongs to Marcus: a broad hand with a chunky gold watch and the cuff of a sweat-creased charcoal suit",
    "dana_past": "Dana is a young marketing coordinator in her early twenties with warm brown skin, natural curly hair in a high puff, round gold earrings, a mustard cardigan and a company lanyard",
    "dana_now": "Dana, now twenty-six, has warm brown skin, shoulder-length natural curly hair, round gold earrings, a burgundy blazer, a lanyard and a name badge",
    "pm": "The property manager is a composed woman in her forties with a sleek black bob, a tailored gray blazer and a tablet",
    "arthur": "Arthur is a weathered sixty-one-year-old contractor with a white buzz cut and white stubble, a faded red flannel shirt under a tan canvas work jacket and a carpenter's pencil behind his ear",
    "coworkers": "The coworkers are semi-realistic cartoon office workers of mixed ethnicities in trendy business-casual clothes with expressive faces",
    "coworker_tiny": "The tiny figure is an office worker in business-casual clothes, dwarfed by the pile",
    "juniors": "The junior analysts are two young office workers in their early twenties, one woman with a ponytail and one man in a striped shirt, both with nervous faces",
    "receptionist": "The receptionist is a young man with a headset and a cardigan",
    "hr": "The HR officer is a middle-aged woman with reading glasses and a cardigan",
    "investors": "The meetup attendees are a mix of ordinary people of different ages and ethnicities in casual clothes",
    "broker": "The broker is a sharp-dressed man in his forties with a trimmed beard, a navy suit and a phone to his ear",
    "landlord": "The landlord is a gentle white-haired man in his seventies in a brown cardigan",
    "banker": "The banker is a polite woman in her fifties with silver-streaked hair and a navy suit",
    "staffer": "The staffer is a nervous young man in his twenties in a light-gray suit, carrying binders",
    "boss": "The CEO is a stern gray-haired man in his sixties in a dark three-piece suit",
}
LIGHT = {
    "gold": "warm golden morning light through tall windows, rich amber and honey tones, deep soft shadows, warm mahogany and brass accents",
    "cold_past": "flat cool office fluorescent light with a faint flicker, desaturated slate-blue and gray palette with muted olive and mustard accents",
    "home": "soft muted afternoon daylight through a small window, gentle slate-blue palette with warm rust accents",
    "night_home": "dim night interior lit by a single warm lamp or a phone glow, deep blue shadows with one warm pool of light",
    "night_city": "moody evening city light, deep navy shadows with neon and warm bar-light accents",
    "party": "warm string-light glow over cool office shadows, festive red and gold accents in a muted palette",
    "rising": "soft warm daylight, the palette warming from slate-blue toward amber",
    "split": "the left side in cold desaturated slate-blue light, the right side in warm golden light",
    "basement": "flat fluorescent church-basement light, beige and slate tones with warm coffee-brown accents",
    "storm": "dark stormy light, cold blue-gray tones, wet reflections",
    "imagined": "desaturated, cold and slightly faded like an imagined possibility",
    "night_fire": "dark blue night with a flickering orange firelight glow",
}

# ---------------------------------------------------------------- on-screen text
OVERLAYS = {
    "clock947": ("9:47 AM", "clock"), "clock952": ("9:52 AM", "clock"), "clock1000": ("10:00 AM", "clock"),
    "leasestamp": ("LEASE RENEWAL · DEADLINE MISSED", "stamp"),
    "year1": ("YEAR 1 · NET WORTH: $0", "year"), "year2": ("YEAR 2", "year"), "nw62": ("YEAR 2 · NET WORTH: $62,000", "year"),
    "year3": ("YEAR 3", "year"), "nw94": ("YEAR 3 · NET WORTH: $94,000", "year"), "year5": ("YEAR 5", "year"),
    "weeklunch": ("A WEEK OF LUNCHES · $38 · $3.80 A MEAL", "money"), "math27": ("$27 A DAY × 250 DAYS = $6,750 A YEAR", "money"),
    "refi": ("REFINANCE · $75,000 BACK · $2,200 A MONTH", "money"), "building": ("4-STORY OFFICE BUILDING · $2,400,000 · 20% DOWN", "money"),
    "marcuscard": ("MARCUS · $115,000 SALARY · NET WORTH: −$14,000", "stat_red"), "mecard": ("ME · $68,000 SALARY · INVESTING $1,900 A MONTH", "stat_green"),
    "rules": ("THE RULES · 1. Lunch costs $4. · 2. The car stays paid off. · 3. Every raise gets invested. · 4. Nobody needs to know.", "rules"),
    "rule4": ("4. Nobody needs to know.", "rules"), "choice": ("EXTEND THE LEASE · or · LET THEM GO", "choice"),
    "ep2": ("EPISODE 2 · COMING SOON", "end"),
}
DESIGN = {
    "clock": dict(name="Clock card", how="Top-left corner. White digital-clock font (CapCut: a monospace or LCD-style font), about 9% of frame height, thin dark drop shadow. Hold for the whole shot.", anim="Snap on with a 2-frame flicker, like a digital display waking up.", sfx="A single soft clock tick, and a low heartbeat bass underneath the cold open."),
    "stamp": dict(name="Stamp card", how="Center, slightly rotated 6°. Heavy condensed red letters (CapCut: Anton or Bebas Neue) inside a rough red rectangle border, like a rubber stamp. The folder image already shows the stamp; this card repeats it big for one beat.", anim="Slam in from 120% to 100% scale in 4 frames with a tiny camera shake.", sfx="A heavy rubber-stamp thud."),
    "year": dict(name="Year / net-worth card", how="Center-left. 'YEAR N' in gold heavy condensed caps (Anton or Bebas Neue); the net-worth line underneath in white, with the dollar figure in bright green. Behind the text, a dark-green rounded panel at 70% opacity.", anim="Year text slides up and fades in; the dollar figure counts up from $0 to its value over about 1 second.", sfx="A soft whoosh, then a cash-register 'cha-ching' when the count lands."),
    "money": dict(name="Money math card", how="Upper third, centered. White heavy condensed caps with a thick black outline; every dollar figure in bright green or gold. Split long lines at the ' · ' marks into two or three stacked lines.", anim="Each part pops in one after another (scale 80% to 100%), about 0.3 seconds apart.", sfx="A light pop for each part and a coin clink on the final figure."),
    "stat_red": dict(name="Character stat card (Marcus)", how="Right side, like a video-game stat panel. Name in white caps; SALARY in white; NET WORTH in bold red with a small down-arrow. Thin red border.", anim="Slides in from the right; the net-worth number glitches briefly into place.", sfx="A low error-buzz on the red number."),
    "stat_green": dict(name="Character stat card (you)", how="Left side, mirroring Marcus's card. Name in white caps; SALARY in white; INVESTING in bold green with a small up-arrow. Thin green border.", anim="Slides in from the left; the investing number ticks up.", sfx="A clean, bright chime."),
    "rules": dict(name="Rules card", how="Use the shot's own image of the handwritten index card full screen, then add each rule as a typed white line on the right as it's mentioned, like the plane video's safety card. For rule 4 alone, put it center screen in large handwritten-style white text.", anim="Each rule types on letter by letter.", sfx="A marker squeak per line; for rule 4, a single low piano note."),
    "choice": dict(name="Choice card (like the plane video's 'OPEN YOUR EYES / KEEP THEM SHUT')", how="Two pill-shaped buttons stacked in the lower-middle above the captions: EXTEND THE LEASE (white pill, dark text) and LET THEM GO (red pill, white text), with a small 'or' between them. Darken the image 25% behind them.", anim="Both buttons fade in, then pulse gently twice while the narrator weighs it; the chosen one (EXTEND) glows when he uncaps the pen.", sfx="A ticking clock underneath, cutting to silence on the pen cap."),
    "end": dict(name="End card", how="Center. 'EPISODE 2' in gold heavy caps, 'COMING SOON' in white below. Keep the late-night phone shot visible behind it.", anim="Fade in on the last beat and hold 3 seconds before the end screen.", sfx="A low boom, then silence."),
}
CARD_BG = ("Optional background image for the year and money cards: a minimal dark forest-green textured paper card with a faint gold "
           "border and soft vignette, empty center, flat 2D illustration style, 16:9, no text.")


FLOW_STEPS = [
    "Make the 7 reference images first (section 1) and save them with the names shown: REF-1 to REF-5 for the characters, LOC-1 and LOC-2 for the two main locations.",
    "For each shot, look at its UPLOAD FIRST line and attach exactly those images before you paste the prompt. In Google Flow, add them as ingredients or reference images; in Grok Imagine, upload them with the prompt.",
    "Attach only the images listed. Extra references confuse the generator and can mix characters' faces.",
    "IMAGE shots: generate, pick the best result, and download it with its shot number in the file name (e.g. shot-023.png) so the edit stays in order.",
    "VIDEO shots: first make the start-frame image the same way. Then start an image-to-video generation (in Flow, the option that animates from a starting frame), use that image as the first frame and paste the video prompt.",
    "If a face drifts off-model, regenerate with the reference re-attached rather than editing the prompt.",
]
POLICY = [
    "Every character is fictional. There are no real people, celebrities, politicians or public figures, and no children or teenagers.",
    "No violence, injuries, blood, weapons, nudity, sexual content, drugs, hate symbols or harassment. The tensest moments are emotional (a stamp, a stare, sweat, a choice).",
    "No brand names or logos in any image or video prompt. Cars and products are described generically (a luxury sedan, a compact sedan, unbranded delivery bags). The narration can still say the brand names.",
    "The one fire reference (the Episode 2 teaser) is only an orange glow through window blinds and a phone call. No one is shown in danger.",
    "Upload only images you created yourself (the REF and LOC sheets). Never upload photos of real people as references.",
    "No prompt imitates a named living artist, studio or franchise. 'Somber Journal style' refers to your own channel.",
    "If a generation is still blocked, it's usually one word: rephrase that line more neutrally and try again. Don't try to get around a block by spelling words differently.",
]
POLICY_NOTE = ("I checked every prompt against the content rules Google (Flow) and xAI (Grok) publish for image and video generation, as I understand them. "
               "Their filters change over time, so treat this as a strong first pass rather than a guarantee.")

# ---------------------------------------------------------------- narration
def narration():
    text = open(os.path.join(ROOT, "script.md")).read().split("\n---\n", 1)[1]
    sections, cur = [], None
    for line in text.splitlines():
        l = line.strip()
        if l.startswith("## "):
            cur = [re.sub(r"^\[[^\]]*\]\s*", "", l[3:]), []]
            sections.append(cur)
        elif l and not l.startswith(("[ON SCREEN", "---")) and cur:
            cur[1].append(l)
    return [(name, " ".join(paras)) for name, paras in sections]

def assign():
    secs = narration()
    full = ""
    bounds = []
    for name, t in secs:
        bounds.append((len(full), name))
        full += t + " "
    pos, starts = 0, []
    for s in SHOTS:
        i = full.find(s["a"], pos)
        if i < 0:
            sys.exit("anchor not found in order: " + s["a"])
        starts.append(i)
        pos = i + 1
    if starts[0] != 0:
        sys.exit("first shot must start at the first word")
    out = []
    for n, s in enumerate(SHOTS):
        end = starts[n + 1] if n + 1 < len(SHOTS) else len(full)
        seg = full[starts[n]:end].strip()
        sec = [b for b in bounds if b[0] <= starts[n]][-1][1]
        out.append(dict(s, text=seg, words=len(seg.split()), section=sec))
    return out, len(full.split())

def ts(sec):
    return "%d:%02d" % (sec // 60, round(sec) % 60 if round(sec) % 60 != 60 else 0)

def image_prompt(s):
    chars = " ".join(CHARS[c] + "." for c in s["ch"])
    return (f"{s['sc']}. {chars} Style: {STYLE}. Lighting and palette: {LIGHT[s['lt']]}. "
            f"Camera: {s['cam']}. Mood: {s['md']}.").replace("  ", " ").replace(". .", ".")

def video_prompt(s, clip):
    who = " ".join(CHARS[c] + "." for c in s["ch"] if not c.endswith("_hands") and c not in ("coworkers", "juniors", "investors"))
    return (f"Animate the start frame: {s['sc']}. {who} Main action: {s['mv']}. Camera: {s['cm']}. "
            f"Lighting: {LIGHT[s['lt']]}. Mood: {s['md']}. {VSTYLE}, {clip} seconds.").replace("  ", " ")

def main():
    shots, total_words = assign()
    t = 0.0
    for n, s in enumerate(shots, 1):
        s["n"] = n
        s["dur"] = s["words"] / WPS
        s["t0"], s["t1"] = t, t + s["dur"]
        t += s["dur"]
        s["clip"] = 5 if s["dur"] <= 6.5 else 10
    runtime = t
    vid = [s for s in shots if s["k"] == "V"]
    vsec = sum(s["dur"] for s in vid)
    first = [s for s in shots if s["section"] == shots[0]["section"]]
    first_v = sum(s["dur"] for s in first if s["k"] == "V") / sum(s["dur"] for s in first)
    stats = dict(shots=len(shots), images=len(shots) - len(vid), videos=len(vid), runtime=runtime,
                 vpct=100 * vsec / runtime, vsec=vsec, intro_v=100 * first_v, words=total_words)
    print("shots {shots}  images {images}  videos {videos}  runtime {runtime:.0f}s  video {vsec:.0f}s = {vpct:.1f}%  intro video {intro_v:.0f}%".format(**stats))
    write_md(shots, stats)
    write_html(shots, stats)

# ---------------------------------------------------------------- reference sheets
REF = [
    ("REF-1 · The protagonist (you, the narrator)", "Save as REF-1-protagonist.png. When generating it, also upload brand/protagonist-reference.png so the face matches your logo.",
     "Character reference sheet of the protagonist: " + FACE + ". Show him three times side by side, full body, front view, same face and hair in every pose: "
     "(1) age 29 at the office: plain black crewneck sweater over a white collar, gray slacks, office ID lanyard, quiet composed expression; "
     "(2) at home: black hoodie with the hood down, gray sweatpants; "
     "(3) age 34, the owner: dark charcoal tailored jacket over a black tee, slim steel watch, calm confident faint half-smile. "
     "Plain light-gray background, outfit labels under each pose. " + STYLE + "."),
    ("REF-2 · Marcus, then and now", "Save as REF-2-marcus.png.",
     "Character reference sheet showing the same man twice side by side, full body, front view: (1) " + MARCUS_PAST + ", smug grin; (2) " + MARCUS_NOW +
     ", anxious expression. Same face shape and hair in both. Plain light-gray background, labels '36' and '41' underneath. " + STYLE + "."),
    ("REF-3 · Dana, then and now", "Save as REF-3-dana.png.",
     "Character reference sheet showing the same young woman twice, full body, front view: (1) " + CHARS["dana_past"] + ", kind sympathetic expression; (2) " +
     CHARS["dana_now"] + ", serious expression. Plain light-gray background, labels '21' and '26'. " + STYLE + "."),
    ("REF-4 · Arthur", "Save as REF-4-arthur.png.",
     "Character reference sheet, full body front view and a close-up portrait: " + CHARS["arthur"] + ", warm but no-nonsense expression. Plain light-gray background. " + STYLE + "."),
    ("REF-5 · The property manager", "Save as REF-5-property-manager.png.",
     "Character reference sheet, full body front view: " + CHARS["pm"] + ", composed professional expression. Plain light-gray background. " + STYLE + "."),
    ("LOC-1 · The owner's office", "Save as LOC-1-owners-office.png.",
     "Location reference sheet of a private top-floor executive office in a four-story red-brick building: a large polished mahogany desk, a brass-framed analog wall clock, "
     "tall windows full of city skyline, a frosted-glass door with a brushed brass lever handle, and a glass wall looking across a marble lobby to brushed-steel elevator doors. "
     "Show a wide view and a reverse view. " + LIGHT["gold"] + ". " + STYLE + ", no people."),
    ("LOC-2 · The third-floor breakroom", "Save as LOC-2-breakroom.png.",
     "Location reference sheet of a cramped corporate breakroom on the third floor of an office: beige laminate tables, a small corner table by the window, an office microwave, "
     "a coffee machine, vending machine and fluorescent ceiling tubes. Show a wide view and a view toward the corner table. " + LIGHT["cold_past"] + ". " + STYLE + ", no people."),
]

REF_OF = [("me_", "REF-1 Protagonist"), ("marcus", "REF-2 Marcus"), ("dana", "REF-3 Dana"), ("arthur", "REF-4 Arthur"), ("pm", "REF-5 Property manager")]
REF_NOTE = {"me_owner": "owner outfit", "me_past": "office outfit", "me_home": "hoodie outfit",
            "marcus_past": "age 36", "marcus_now": "age 41", "dana_past": "age 21", "dana_now": "age 26"}
OFFICE_RX = re.compile(r"mahogany|executive office|top-floor office|frosted|elevator|lobby|wall clock|office door|doorway|the office|on the desk|behind the desk|desk calendar")
BREAK_RX = re.compile(r"breakroom|corner table|microwave")
OUTSIDE_RX = re.compile(r"exterior|facade|sign bolted|triptych|portraits|split frame|three-panel|two side-by-side|across the street|long hallway|end of a long hallway")

def uploads(s):
    out = []
    for c in s["ch"]:
        base = c.replace("_hands", "")
        for prefix, name in REF_OF:
            if base.startswith(prefix):
                note = REF_NOTE.get(base)
                item = name + (f" ({note})" if note else "")
                if item not in out:
                    out.append(item)
    sc = s["sc"].lower()
    in_office_scene = s["section"].startswith(("COLD OPEN", "THE REVEAL", "THE CLOSE")) and not OUTSIDE_RX.search(sc)
    if s["lt"] == "gold" and (OFFICE_RX.search(sc) or in_office_scene):
        out.append("LOC-1 Owner's office")
    if BREAK_RX.search(sc):
        out.append("LOC-2 Breakroom")
    return out

def upload_text(s):
    u = uploads(s)
    return ", ".join(u) if u else "nothing (no recurring character or location in this shot)"

def section_order(shots):
    seen = []
    for s in shots:
        if s["section"] not in seen:
            seen.append(s["section"])
    return seen

def write_md(shots, st):
    L = []
    L.append("# Episode 1 · Image and Video Prompts\n")
    L.append("**They Pitied Me for Bringing Leftovers to Work... Until I Bought the Building**\n")
    L.append(f"{st['shots']} shots · **{st['images']} images ({100 - st['vpct']:.0f}% of runtime)** · **{st['videos']} video clips ({st['vpct']:.0f}% of runtime)** · "
             f"cold open {st['intro_v']:.0f}% video · runtime ≈ {ts(st['runtime'])} at {WPS} words per second\n")
    L.append("## How to use this book\n")
    L.append("1. **Make the reference sheets first** (section 1) and attach them as character or style references to every shot where your generator allows it.")
    L.append("2. **IMAGE shots:** generate the image from its prompt. In the edit, give every still a slow zoom or pan so nothing on screen is ever frozen.")
    L.append("3. **VIDEO shots:** generate the image first (it's the start frame), then feed it to your image-to-video tool with the video prompt. Generate the clip length shown and trim it to the narration time.")
    L.append("4. **Timecodes** are calculated from the narration at 2.6 words per second. Once your voiceover is recorded, slide each shot to its line.")
    L.append("5. **ON SCREEN** items are text you add in CapCut on top of that shot. Section 2 has the design for each kind.")
    L.append("6. **Captions:** keep word-by-word captions like your previous videos, in the bottom 15% of the frame (every prompt keeps that area clear).\n")
    L.append("**Negative prompt (add to every image if your tool supports it):** " + NEGATIVE + "\n")
    L.append("**Lighting rule:** the past is cold slate-blue fluorescent; the present is warm gold. The palette warms year by year as the money grows, so the color shift tells the story.\n")
    L.append("## Google Flow and Grok: uploading references\n")
    L += [f"{i}. {t}" for i, t in enumerate(FLOW_STEPS, 1)]
    L.append("")
    L.append("## Policy check (Google Flow and Grok)\n")
    L += [f"- {t}" for t in POLICY]
    L.append(f"\n_{POLICY_NOTE}_\n")
    L.append("## 1. Reference sheets (make these first)\n")
    for name, note, p in REF:
        L.append(f"### {name}\n_{note}_\n\n{p}\n")
    L.append("## 2. ON SCREEN text design\n")
    for key, d in DESIGN.items():
        L.append(f"### {d['name']}\n- **Look:** {d['how']}\n- **Animation:** {d['anim']}\n- **Sound:** {d['sfx']}\n")
    L.append(f"_{CARD_BG}_\n")
    L.append("## 3. Shot list\n")
    for sec in section_order(shots):
        ss = [s for s in shots if s["section"] == sec]
        v = sum(1 for s in ss if s["k"] == "V")
        L.append(f"### {sec} · {ts(ss[0]['t0'])}–{ts(ss[-1]['t1'])} · {len(ss) - v} images, {v} videos\n")
        for s in ss:
            kind = "🎬 VIDEO" if s["k"] == "V" else "🖼 IMAGE"
            L.append(f"#### Shot {s['n']:03d} · {kind} · {ts(s['t0'])}–{ts(s['t1'])} ({s['dur']:.1f}s)\n")
            L.append(f"**Script:** \"{s['text']}\"\n")
            L.append(f"**Upload first:** {upload_text(s)}\n")
            label = "Start frame (image prompt)" if s["k"] == "V" else "Image prompt"
            L.append(f"**{label}:** {image_prompt(s)}\n")
            if s["k"] == "V":
                L.append(f"**Video prompt:** {video_prompt(s, s['clip'])}\n")
                L.append(f"**Clip:** generate {s['clip']}s, use about {s['dur']:.1f}s · **Camera move:** {s['cm']}\n")
            for o in s.get("ov", []):
                txt, kind2 = OVERLAYS[o]
                L.append(f"**ON SCREEN:** `{txt}` · {DESIGN[kind2]['name']} (see section 2)\n")
    open(os.path.join(ROOT, "image-video-prompts.md"), "w").write("\n".join(L))

def write_html(shots, st):
    e = html.escape
    P = []
    P.append(f"""<div class="cover"><div class="kick">SOMBER JOURNAL · EPISODE 1 · IMAGE &amp; VIDEO PROMPTS</div>
<h1>They Pitied Me for Bringing Leftovers to Work... Until I Bought the Building</h1>
<div class="stats"><div><b>{st['shots']}</b><span>shots</span></div><div><b>{st['images']}</b><span>images · {100 - st['vpct']:.0f}%</span></div>
<div><b>{st['videos']}</b><span>video clips · {st['vpct']:.0f}%</span></div><div><b>{st['intro_v']:.0f}%</b><span>of the cold open is video</span></div>
<div><b>{ts(st['runtime'])}</b><span>runtime</span></div></div></div>""")
    P.append("""<div class="box"><h3>How to use this book</h3><ol>
<li><b>Make the reference sheets first</b> (section 1) and attach them as references for every shot where your generator allows it.</li>
<li><b>IMAGE shots:</b> generate the image. In the edit, give every still a slow zoom or pan so nothing on screen is ever frozen.</li>
<li><b>VIDEO shots:</b> generate the image first (it's the start frame), then feed it to your image-to-video tool with the video prompt. Generate the clip length shown and trim it to the narration time.</li>
<li><b>Timecodes</b> assume 2.6 words per second. Once the voiceover is recorded, slide each shot to its line.</li>
<li><b>ON SCREEN</b> items are text you add in CapCut on top of that shot. Section 2 has the design for each kind.</li>
<li><b>Captions:</b> keep word-by-word captions like your previous videos, in the bottom 15% of the frame.</li></ol>
<p><b>Negative prompt (add to every image if your tool supports it):</b> """ + e(NEGATIVE) + """</p>
<p><b>Lighting rule:</b> the past is cold slate-blue fluorescent; the present is warm gold. The palette warms year by year as the money grows.</p></div>""")
    P.append('<div class="box"><h3>Google Flow and Grok: uploading references</h3><ol>' + "".join(f"<li>{e(t)}</li>" for t in FLOW_STEPS) + '</ol></div>')
    P.append('<div class="box pol"><h3>Policy check (Google Flow and Grok)</h3><ul>' + "".join(f"<li>{e(t)}</li>" for t in POLICY) + f'</ul><p class="note">{e(POLICY_NOTE)}</p></div>')
    P.append('<h2 class="part">1 · Reference sheets (make these first)</h2>')
    for name, note, p in REF:
        P.append(f'<div class="ref"><h3>{e(name)}</h3><div class="note">{e(note)}</div><p class="prompt">{e(p)}</p></div>')
    P.append('<h2 class="part">2 · ON SCREEN text design</h2>')
    for key, d in DESIGN.items():
        P.append(f'<div class="ref"><h3>{e(d["name"])}</h3><p><b>Look:</b> {e(d["how"])}</p><p><b>Animation:</b> {e(d["anim"])}</p><p><b>Sound:</b> {e(d["sfx"])}</p></div>')
    P.append(f'<p class="note">{e(CARD_BG)}</p>')
    P.append('<h2 class="part">3 · Shot list</h2>')
    for sec in section_order(shots):
        ss = [s for s in shots if s["section"] == sec]
        v = sum(1 for s in ss if s["k"] == "V")
        P.append(f'<h2 class="sec"><span class="ts">{ts(ss[0]["t0"])}–{ts(ss[-1]["t1"])}</span>{e(sec)}<span class="cnt">{len(ss) - v} images · {v} videos</span></h2>')
        for s in ss:
            vid = s["k"] == "V"
            ov = "".join(f'<div class="scr"><span class="lbl">ON SCREEN</span><span class="it">{e(OVERLAYS[o][0])}</span><span class="kind">{e(DESIGN[OVERLAYS[o][1]]["name"])}</span></div>' for o in s.get("ov", []))
            vp = (f'<div class="row vrow"><div class="lab">Video prompt</div><p>{e(video_prompt(s, s["clip"]))}</p></div>'
                  f'<div class="clip">Generate {s["clip"]}s · use about {s["dur"]:.1f}s · camera: {e(s["cm"])}</div>') if vid else ""
            P.append(f'''<div class="shot {'v' if vid else 'i'}"><div class="hd"><span class="num">{s["n"]:03d}</span><span class="tag">{'VIDEO' if vid else 'IMAGE'}</span>
<span class="tc">{ts(s["t0"])}–{ts(s["t1"])} · {s["dur"]:.1f}s</span></div>
<div class="script">“{e(s["text"])}”</div>
<div class="up"><span>UPLOAD FIRST</span>{e(upload_text(s))}</div>
<div class="row"><div class="lab">{'Start frame' if vid else 'Image prompt'}</div><p>{e(image_prompt(s))}</p></div>{vp}{ov}</div>''')
    css = """
@page { size: A4; margin: 16mm 14mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; color:#1b1f1d; font-size: 9.6pt; line-height: 1.45; }
.cover { background:#0B1410; color:#F2F5F3; padding: 24px 26px; border-radius: 10px; margin-bottom: 14px; }
.kick { font-size: 8.5pt; letter-spacing: 3px; color:#E3B341; font-weight:700; }
.cover h1 { font-family: Georgia, 'DejaVu Serif', serif; font-size: 21pt; line-height:1.2; margin: 8px 0 14px; }
.stats { display:flex; gap: 10px; flex-wrap: wrap; }
.stats div { background:#13231B; border-radius: 8px; padding: 8px 12px; min-width: 88px; }
.stats b { display:block; font-size: 17pt; color:#E3B341; font-family: Georgia, serif; }
.stats span { font-size: 8pt; color:#9DB0A6; }
.box, .ref { border:1px solid #d5ddd8; border-radius: 8px; padding: 10px 14px; margin: 8px 0; break-inside: avoid; }
.box ol, .box ul { margin: 4px 0 6px 18px; padding: 0; } .box.pol { border-color:#2fbf71; background:#F1FAF4; } .box li { margin-bottom: 3px; }
h3 { margin: 0 0 4px; font-size: 11pt; color:#0B1410; }
.note { color:#5a6660; font-style: italic; font-size: 8.8pt; margin-bottom: 4px; }
.prompt { margin: 4px 0 0; }
h2.part { font-family: Georgia, serif; font-size: 16pt; color:#0B1410; margin: 18px 0 8px; break-after: avoid; }
h2.sec { font-size: 12pt; color:#0B1410; margin: 16px 0 8px; padding-bottom: 5px; border-bottom: 2px solid #E3B341; break-after: avoid; }
h2.sec .ts { background:#0B1410; color:#E3B341; font-size: 8.5pt; padding: 2px 7px; border-radius: 4px; margin-right: 8px; vertical-align: 2px; }
h2.sec .cnt { float:right; font-size: 8.5pt; color:#5a6660; font-weight: normal; margin-top: 4px; }
.shot { border:1px solid #dfe5e1; border-radius: 8px; padding: 8px 11px; margin: 0 0 8px; break-inside: avoid; }
.shot.v { border-color:#E3B341; background:#FFFBEE; }
.hd { display:flex; align-items:center; gap: 8px; margin-bottom: 4px; }
.num { font-weight:700; font-size: 10.5pt; color:#0B1410; }
.tag { font-size: 7.5pt; font-weight:700; letter-spacing: 1.5px; padding: 2px 7px; border-radius: 10px; background:#e7ece9; color:#2c3a33; }
.shot.v .tag { background:#E3B341; color:#0B1410; }
.tc { margin-left:auto; font-size: 8.5pt; color:#5a6660; }
.up { font-size: 8.6pt; background:#E8F3EC; border-radius: 5px; padding: 3px 8px; margin: 0 0 6px; } .up span { font-weight:700; color:#1f7a45; letter-spacing:1px; margin-right:8px; font-size:7.5pt; }
.script { font-family: Georgia, 'DejaVu Serif', serif; font-size: 10.5pt; font-style: italic; margin: 2px 0 6px; color:#0B1410; }
.row { display:flex; gap: 8px; margin: 3px 0; } .row p { margin: 0; flex: 1; }
.lab { flex: 0 0 82px; font-size: 7.5pt; font-weight:700; letter-spacing: 1px; color:#5a6660; text-transform: uppercase; padding-top: 2px; }
.vrow .lab { color:#8a6a10; }
.clip { font-size: 8.3pt; color:#8a6a10; font-weight:600; margin: 4px 0 0 90px; }
.scr { background:#0B1410; color:#F2F5F3; border-radius: 6px; padding: 4px 9px; margin-top: 6px; font-size: 8.5pt; }
.scr .lbl { color:#E3B341; font-weight:700; letter-spacing: 1.5px; margin-right: 8px; font-size: 7.5pt; }
.scr .it { font-weight:700; } .scr .kind { color:#9DB0A6; margin-left: 8px; font-size: 7.8pt; }
"""
    doc = f'<!doctype html><html><head><meta charset="utf-8"><title>Episode 1 Image and Video Prompts</title><style>{css}</style></head><body>{"".join(P)}</body></html>'
    open(os.path.join(ROOT, "image-video-prompts.html"), "w").write(doc)

if __name__ == "__main__":
    main()
