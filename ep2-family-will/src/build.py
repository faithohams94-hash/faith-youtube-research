"""Build the Episode 2 image + video prompt book from script.md, shots.py and the rendered cards.
usage: python3 build.py   (writes ../image-video-prompts.md and ../image-video-prompts.html)
"""
import html, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from shots import SHOTS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WPS = 2.6
TITLE = 'POV: Your Family Cut You Off Because You Were "Broke"... Then They Saw Your Will'

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
ME = "The protagonist (the narrator) is " + FACE
OUT = {
    "22": "at twenty-two, fresh-faced, wearing a crisp new light-blue button-up interview shirt, gray slacks and a distribution-center ID lanyard",
    "work": "in his mid-twenties to early thirties, wearing a plain navy button-up shirt with rolled sleeves, gray slacks and a distribution-center ID lanyard",
    "29": "at twenty-nine, wearing a cheap dark gray rain jacket over a navy button-up shirt, damp from the rain",
    "home": "at home, wearing a black hoodie with the hood down and gray sweatpants",
    "now": "at thirty-seven, faint stubble and tired lines around the eyes, wearing a thin faded olive-green zip jacket worn at the elbows over a plain black tee",
}
DANNY = ("Danny, the protagonist's older brother, is a stocky man with a short dark fade haircut, a goatee, warm tan skin and a loud confident grin, ")
DANNY_AGE = {
    "26": "at twenty-six, in a white tank top under an open red flannel shirt",
    "29": "at twenty-nine, in a rented gray suit",
    "33": "at thirty-three, in a teal polo shirt with a small homemade gold logo on the chest",
    "37": "at thirty-seven, heavier, in a black quarter-zip and a gold chain",
    "41": "at forty-one, heavier still, gray creeping into his goatee, a tight black zip hoodie and a nervous over-wide smile",
}
MOM = "Mom is a small woman in her late fifties with short tight gray curls, warm tan skin, tired kind eyes and a faded maroon cardigan"
MOM_NOW = "Mom, now in her mid-sixties and a little frailer, has short tight gray curls, warm tan skin, tired kind eyes and the same faded maroon cardigan"
DAD = "Dad (Raymond) is a sturdy man in his early sixties, bald on top with gray hair on the sides, a thick gray mustache and a navy work shirt with a name patch reading RAY"
DAD_NOW = "Dad (Raymond), now in his late sixties and frailer, is bald on top with gray hair on the sides and a thick gray mustache, wearing a brown cardigan over a navy work shirt"

CHARS = {
    "me_22": f"{ME}, {OUT['22']}", "me_22_hands": "The hands belong to the protagonist: pale off-white skin and the cuff of a light-blue button-up shirt",
    "me_work": f"{ME}, {OUT['work']}", "me_work_hands": "The hands belong to the protagonist: pale off-white skin and the rolled sleeve of a navy button-up shirt",
    "me_29": f"{ME}, {OUT['29']}", "me_29_hands": "The hands belong to the protagonist: pale off-white skin and the sleeve of a dark gray rain jacket",
    "me_home": f"{ME}, {OUT['home']}", "me_hands_home": "The hands belong to the protagonist: pale off-white skin and the sleeve of a black hoodie",
    "me_now": f"{ME}, {OUT['now']}", "me_now_hands": "The hands belong to the protagonist: pale off-white skin and the worn sleeve of a faded olive-green jacket",
    "me_kid": "The boy is the protagonist as a ten-year-old: an oversized head, messy curly jet-black hair, thick black rectangular glasses, pale off-white skin, an oversized faded t-shirt",
    **{f"danny_{a}": DANNY + DANNY_AGE[a] for a in DANNY_AGE},
    "danny_33_hands": "The hand belongs to Danny: a thick tan hand and the sleeve of a teal polo shirt",
    "danny_37_hands": "The hand belongs to Danny: a thick tan hand with a gold chain bracelet",
    "mom": MOM, "mom_now": MOM_NOW, "dad": DAD, "dad_now": DAD_NOW,
    "kayla": "Kayla, Danny's wife, is a woman in her thirties with a blonde high ponytail, lash extensions, a pink top and her phone always in her hand",
    "aunt": "The aunt is a warm, heavyset woman in her sixties with a silver bob and a floral blouse",
    "tasha": "Cousin Tasha is a woman in her late twenties with long box braids and big gold hoop earrings",
    "nephew_5": "The nephew is Danny's cheerful five-year-old son with short dark curls and a dinosaur t-shirt",
    "nephew_7": "The nephew is Danny's seven-year-old son with short dark curls",
    "nephew_13": "The nephew is Danny's lanky thirteen-year-old son with short dark curls and a red hoodie",
    "okafor": "Ms. Okafor is a Black woman in her sixties with short cropped gray hair, reading glasses on a beaded chain and a navy suit",
    "gloria": "Gloria is a nurse in her thirties with long braids and teal scrubs, with her twin boys of about eight",
    "paralegal": "The paralegal is a young woman with a neat bun, a cardigan and a headset",
    "brandon": "Brandon is a muscular man in his thirties with a buzz cut and a tight dress shirt",
    "waitress": "The waitress is a tired woman in her fifties in a pink diner uniform, holding a coffee pot",
    "billing": "The billing clerk is a kind middle-aged woman with a headset and a lanyard",
    "coworkers": "The coworkers are semi-realistic cartoon office workers of mixed ethnicities in business-casual clothes",
}
LIGHT = {
    "night_blue": "cold blue evening light in a small dim apartment, the only warm light the glow of a phone screen, deep shadows",
    "night_dim": "dim nighttime interior light, muted navy shadows with a single warm lamp",
    "lonely": "lonely night light, dark navy shadows with one small warm lamp or phone glow",
    "memory": "faded, desaturated sepia memory light with a soft vignette",
    "warm_photo": "bright, warm, slightly overexposed family-photo light with cheerful saturated colors",
    "family_day": "soft warm afternoon light in a modest family home, muted earth tones",
    "family_night": "warm yellow kitchen lamp light at night against dark windows",
    "office": "flat fluorescent warehouse-office light, beige and gray palette",
    "office_day": "clean neutral office daylight, cool whites and grays",
    "home_day": "soft muted daylight through a small window, gentle slate-blue palette with warm rust accents",
    "rain": "gray rainy daylight, cold blue-gray palette, wet reflections and rain streaks on glass",
    "diner": "dim rainy diner light, warm yellow lamps against cold gray rain outside the window",
    "hospital": "cold sodium and fluorescent light in a concrete parking garage at night, green-gray shadows",
    "morning": "soft pale morning light through a steamy kitchen window, steam curling",
    "lawyer": "calm daylight in an old-fashioned law office, warm wood and paper tones",
    "rising": "clear soft daylight, the palette warming toward gold",
    "gold": "warm golden late-afternoon light, cozy amber tones, long soft shadows",
}

REF = [
    ("REF-1 · The protagonist (you)", "Save as REF-1-protagonist.png. Also upload brand/protagonist-reference.png when you generate it, so the face matches your logo.",
     "Character reference sheet of the protagonist: " + FACE + ". Show him five times side by side, full body, front view, same face and hair in every pose: "
     "(1) age 22 in a light-blue interview shirt, gray slacks and ID lanyard; (2) mid-twenties in a navy button-up with rolled sleeves and ID lanyard; "
     "(3) a cheap dark gray rain jacket; (4) at home in a black hoodie and gray sweatpants; (5) age 37 with faint stubble, in a faded olive-green zip jacket worn at the elbows over a black tee. "
     "Plain light-gray background, outfit labels under each pose. " + STYLE + "."),
    ("REF-2 · Danny, through the years", "Save as REF-2-danny.png.",
     "Character reference sheet of the same man four times side by side, full body, front view: " + DANNY + "(1) " + DANNY_AGE["26"] + "; (2) " + DANNY_AGE["33"] + "; (3) " +
     DANNY_AGE["37"] + "; (4) " + DANNY_AGE["41"] + ". Same face in every pose. Plain light-gray background, age labels underneath. " + STYLE + "."),
    ("REF-3 · Mom, then and now", "Save as REF-3-mom.png.",
     "Character reference sheet of the same woman twice, full body, front view: (1) " + MOM + ", kind smile; (2) " + MOM_NOW + ", tearful. Plain light-gray background. " + STYLE + "."),
    ("REF-4 · Dad, then and now", "Save as REF-4-dad.png.",
     "Character reference sheet of the same man twice, full body, front view: (1) " + DAD + ", proud expression; (2) " + DAD_NOW + ", quiet expression. Plain light-gray background. " + STYLE + "."),
    ("REF-5 · Kayla", "Save as REF-5-kayla.png.",
     "Character reference sheet, full body front view: " + CHARS["kayla"] + ", a bright practiced smile. Plain light-gray background. " + STYLE + "."),
    ("REF-6 · Ms. Okafor", "Save as REF-6-okafor.png.",
     "Character reference sheet, full body front view and a close-up portrait: " + CHARS["okafor"] + ", calm and perceptive expression. Plain light-gray background. " + STYLE + "."),
    ("LOC-1 · Your apartment above the dry cleaner", "Save as LOC-1-apartment.png.",
     "Location reference sheet of a small one-bedroom apartment above a dry cleaner: a narrow kitchen with a worn laminate counter, an old clanking radiator, a steamy window, "
     "a tiny table for one, a small bed. Show a wide view of the kitchen and a view toward the window. " + LIGHT["night_blue"] + ". " + STYLE + ", no people."),
    ("LOC-2 · Your parents' house", "Save as LOC-2-parents-house.png.",
     "Location reference sheet of a modest working-class family house: a kitchen with an old round wall clock and a refrigerator, a dining table for eight, a front door with a small porch, "
     "a short driveway and back steps. Show the kitchen, the dining table and the exterior. " + LIGHT["family_day"] + ". " + STYLE + ", no people."),
    ("LOC-3 · Rosie's diner", "Save as LOC-3-diner.png.",
     "Location reference sheet of a roadside diner called Rosie's: red vinyl back booths, a long counter, coffee pots, a rain-streaked window looking out on the parking lot. "
     "Show a wide view and the back booth. " + LIGHT["diner"] + ". " + STYLE + ", no people."),
]
REF_OF = [("me_", "REF-1 Protagonist"), ("danny", "REF-2 Danny"), ("mom", "REF-3 Mom"), ("dad", "REF-4 Dad"), ("kayla", "REF-5 Kayla"), ("okafor", "REF-6 Ms. Okafor")]
REF_NOTE = {"me_22": "age 22", "me_work": "navy shirt", "me_29": "rain jacket", "me_home": "hoodie", "me_now": "age 37 olive jacket", "me_kid": "draw him as a 10-year-old",
            "me_hands_home": "hoodie", "danny_26": "age 26", "danny_29": "rented suit", "danny_33": "age 33", "danny_37": "age 37", "danny_41": "age 41",
            "mom": "then", "mom_now": "now", "dad": "then", "dad_now": "now"}
LOC_NAME = {"LOC-1": "LOC-1 Apartment", "LOC-2": "LOC-2 Parents' house", "LOC-3": "LOC-3 Diner"}

FLOW_STEPS = [
    "Make the 9 reference images first (section 1) and save them with the names shown.",
    "For each shot, attach exactly the images on its UPLOAD FIRST line, then paste the prompt. In Google Flow, add them as ingredients or reference images; in Grok Imagine, upload them with the prompt.",
    "Attach only what's listed. Extra references can mix up faces.",
    "IMAGE shots: generate, pick the best, and save it with its shot number (shot-012.png).",
    "VIDEO shots: make the start-frame image first, then animate it from that first frame with the video prompt.",
    "Shots longer than 8 seconds: in the edit, split the still into two moves (a slow push-in, then a cut to a tighter crop of a detail) so the picture changes about every 4 seconds.",
]
POLICY = [
    "Every character is fictional: no real people, celebrities or public figures. Only upload images you created yourself (the REF and LOC sheets).",
    "Dad's heart attack is never shown: only a spilled grocery bag and distant ambulance lights. Hospital scenes are a garage, a lobby and a bill. No injury, blood or medical procedure on screen.",
    "Danny's nephew appears only in everyday family moments (a birthday, a photo, the back steps). He is never used as a reference upload. If a tool is strict about children, frame him from behind or at a distance.",
    "No brand names or logos: cars, apps and stores are generic. Danny's \"SHINE SQUAD\" logo is his own made-up business.",
    "No violence, weapons, nudity, sexual content, drugs, gambling imagery or hate content. The gambling line is only spoken by Mom, never shown.",
    "No prompt imitates a named artist, studio or franchise. 'Somber Journal style' is your own channel.",
    "If a generation is blocked, rewrite that one line more neutrally. Never work around a block by misspelling words.",
]
POLICY_NOTE = ("Checked against the content rules Google (Flow) and xAI (Grok) publish for image and video generation, as I understand them. "
               "Their filters change, so treat this as a strong first pass rather than a guarantee.")

# ---------------------------------------------------------------- narration and timing
def narration():
    body = open(os.path.join(ROOT, "script.md")).read().split("\n---\n", 1)[1]
    full, sections, cues, pauses = "", [], [], []
    for line in body.splitlines():
        l = line.strip()
        if not l or l == "---":
            continue
        if l.startswith("## "):
            sections.append((len(full), re.sub(r"^\[[^\]]*\]\s*", "", l[3:])))
        elif l.startswith("[ON SCREEN:"):
            cues.append((len(full), l[len("[ON SCREEN:"):-1].strip()))
        elif l == "[PAUSE]":
            pauses.append(len(full))
        else:
            full += l + " "
    return full, sections, cues, pauses

def ts(sec):
    sec = int(round(sec))
    return "%d:%02d" % (sec // 60, sec % 60)

def cards():
    js = "const {CARDS}=require(%s);console.log(JSON.stringify(CARDS.map(c=>[c.id,c.key,c.dur+0.6])))" % json.dumps(os.path.join(ROOT, "cards-src/cards-ep2.js"))
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    return {k: (i, d) for i, k, d in json.loads(out)}

def assign():
    full, sections, cues, pauses = narration()
    pos, starts = 0, []
    for s in SHOTS:
        i = full.find(s["a"], pos)
        if i < 0:
            sys.exit("anchor not found in order: " + s["a"])
        starts.append(i)
        pos = i + 1
    if starts[0] != 0:
        sys.exit("first shot must start at the first word")
    card = cards()
    shots, t = [], 0.0
    for n, s in enumerate(SHOTS):
        a, b = starts[n], (starts[n + 1] if n + 1 < len(SHOTS) else len(full))
        seg = full[a:b].strip()
        words = len(seg.split())
        dur = words / WPS + sum(1 for p in pauses if a < p <= b)
        sec = [x for x in sections if x[0] <= a][-1][1]
        after = [card[k] + (k,) for (cpos, k) in cues if a < cpos <= b]
        shots.append(dict(s, n=n + 1, text=seg, words=words, dur=dur, t0=t, t1=t + dur, section=sec, cards=after,
                          clip=(5 if dur <= 6.5 else 10)))
        t += dur
    return shots, t

def uploads(s):
    out = []
    for c in s["ch"]:
        base = c.replace("_hands", "") if not c.startswith("me_hands") else "me_home"
        for prefix, name in REF_OF:
            if base.startswith(prefix):
                note = REF_NOTE.get(base) or REF_NOTE.get(c)
                item = name + (f" ({note})" if note else "")
                if item not in out:
                    out.append(item)
    if s.get("loc"):
        out.append(LOC_NAME[s["loc"]])
    return ", ".join(out) if out else "nothing (no recurring character or location in this shot)"

def image_prompt(s):
    chars = " ".join(CHARS[c] + "." for c in s["ch"])
    return f"{s['sc']}. {chars} Style: {STYLE}. Lighting and palette: {LIGHT[s['lt']]}. Camera: {s['cam']}. Mood: {s['md']}.".replace("  ", " ")

def video_prompt(s):
    who = " ".join(CHARS[c] + "." for c in s["ch"] if not c.endswith("_hands") and not c.startswith("me_hands") and c != "coworkers")
    return (f"Animate the start frame: {s['sc']}. {who} Main action: {s['mv']}. Camera: {s['cm']}. "
            f"Lighting: {LIGHT[s['lt']]}. Mood: {s['md']}. {VSTYLE}, {s['clip']} seconds.").replace("  ", " ")

def section_order(shots):
    seen = []
    for s in shots:
        if s["section"] not in seen:
            seen.append(s["section"])
    return seen

# ---------------------------------------------------------------- output
def main():
    shots, runtime = assign()
    vid = [s for s in shots if s["k"] == "V"]
    vsec = sum(s["dur"] for s in vid)
    cold = [s for s in shots if s["section"] == shots[0]["section"]]
    st = dict(shots=len(shots), images=len(shots) - len(vid), videos=len(vid), runtime=runtime, vpct=100 * vsec / runtime,
              intro_v=100 * sum(s["dur"] for s in cold if s["k"] == "V") / sum(s["dur"] for s in cold),
              ncards=sum(len(s["cards"]) for s in shots), avg=runtime / len(shots))
    print("shots {shots} images {images} videos {videos} runtime {runtime:.0f}s video {vpct:.1f}% intro video {intro_v:.0f}% cards {ncards} avg {avg:.1f}s".format(**st))
    write_md(shots, st)
    write_html(shots, st)

def howto_lines(st):
    return [
        "**Make the 9 reference images first** (section 1). Every shot lists which ones to upload.",
        "**IMAGE shots:** generate the image; in the edit, give every still a slow zoom or pan.",
        "**VIDEO shots:** generate the start-frame image, then animate it with the video prompt. Generate the clip length shown and trim to the narration.",
        f"**Cards:** when a shot says **THEN PLAY CARD**, put that card from `episode2-on-screen-cards.zip` right after the shot, with the voice paused ({st['ncards']} cards in total).",
        "**Timecodes** assume 2.6 words per second plus the script's pauses. Once the voiceover is recorded, slide each shot to its line.",
        "**Captions:** keep word-by-word captions in the bottom 15% of the frame (every prompt keeps that area clear).",
    ]

def write_md(shots, st):
    L = [f"# Episode 2 · Image and Video Prompts\n", f"**{TITLE}**\n",
         f"{st['shots']} shots · **{st['images']} images ({100 - st['vpct']:.0f}% of runtime)** · **{st['videos']} video clips ({st['vpct']:.0f}% of runtime)** · "
         f"cold open {st['intro_v']:.0f}% video · {st['ncards']} on-screen cards · narration ≈ {ts(st['runtime'])}\n", "## How to use this book\n"]
    L += [f"{i}. {t}" for i, t in enumerate(howto_lines(st), 1)]
    L += ["", "**Negative prompt (add to every image if your tool supports it):** " + NEGATIVE + "\n",
          "**Color rule:** the present-day Tuesday is cold blue with phone glow; the family photos you're excluded from are bright and warm; the past is faded sepia; the ending warms to gold.\n",
          "## Google Flow and Grok: uploading references\n"]
    L += [f"{i}. {t}" for i, t in enumerate(FLOW_STEPS, 1)]
    L += ["", "## Policy check (Google Flow and Grok)\n"] + [f"- {t}" for t in POLICY] + [f"\n_{POLICY_NOTE}_\n", "## 1. Reference sheets (make these first)\n"]
    for name, note, p in REF:
        L.append(f"### {name}\n_{note}_\n\n{p}\n")
    L.append("## 2. Shot list\n")
    for sec in section_order(shots):
        ss = [s for s in shots if s["section"] == sec]
        v = sum(1 for s in ss if s["k"] == "V")
        L.append(f"### {sec} · {ts(ss[0]['t0'])}–{ts(ss[-1]['t1'])} · {len(ss) - v} images, {v} videos\n")
        for s in ss:
            kind = "🎬 VIDEO" if s["k"] == "V" else "🖼 IMAGE"
            L.append(f"#### Shot {s['n']:03d} · {kind} · {ts(s['t0'])}–{ts(s['t1'])} ({s['dur']:.1f}s)\n")
            L.append(f"**Script:** \"{s['text']}\"\n")
            L.append(f"**Upload first:** {uploads(s)}\n")
            L.append(f"**{'Start frame (image prompt)' if s['k'] == 'V' else 'Image prompt'}:** {image_prompt(s)}\n")
            if s["k"] == "V":
                L.append(f"**Video prompt:** {video_prompt(s)}\n")
                L.append(f"**Clip:** generate {s['clip']}s, use about {s['dur']:.1f}s · **Camera move:** {s['cm']}\n")
            for cid, d, key in s["cards"]:
                L.append(f"**THEN PLAY CARD:** `{cid}.mp4` ({d:.1f}s, voice paused) · shows `{key}`\n")
    open(os.path.join(ROOT, "image-video-prompts.md"), "w").write("\n".join(L))

def write_html(shots, st):
    e = html.escape
    md = lambda t: re.sub(r"`([^`]+)`", r"<code>\1</code>", re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", e(t)))
    P = [f"""<div class="cover"><div class="kick">SOMBER JOURNAL · EPISODE 2 · IMAGE &amp; VIDEO PROMPTS</div><h1>{e(TITLE)}</h1>
<div class="stats"><div><b>{st['shots']}</b><span>shots</span></div><div><b>{st['images']}</b><span>images · {100 - st['vpct']:.0f}%</span></div>
<div><b>{st['videos']}</b><span>video clips · {st['vpct']:.0f}%</span></div><div><b>{st['intro_v']:.0f}%</b><span>of the cold open is video</span></div>
<div><b>{st['ncards']}</b><span>on-screen cards</span></div><div><b>{ts(st['runtime'])}</b><span>narration</span></div></div></div>"""]
    P.append('<div class="box"><h3>How to use this book</h3><ol>' + "".join(f"<li>{md(t)}</li>" for t in howto_lines(st)) + "</ol>"
             f"<p><b>Negative prompt:</b> {e(NEGATIVE)}</p><p><b>Color rule:</b> present-day Tuesday is cold blue with phone glow; the family photos you're excluded from are bright and warm; the past is faded sepia; the ending warms to gold.</p></div>")
    P.append('<div class="box"><h3>Google Flow and Grok: uploading references</h3><ol>' + "".join(f"<li>{e(t)}</li>" for t in FLOW_STEPS) + "</ol></div>")
    P.append('<div class="box pol"><h3>Policy check (Google Flow and Grok)</h3><ul>' + "".join(f"<li>{e(t)}</li>" for t in POLICY) + f'</ul><p class="note">{e(POLICY_NOTE)}</p></div>')
    P.append('<h2 class="part">1 · Reference sheets (make these first)</h2>')
    for name, note, p in REF:
        P.append(f'<div class="ref"><h3>{e(name)}</h3><div class="note">{e(note)}</div><p>{e(p)}</p></div>')
    P.append('<h2 class="part">2 · Shot list</h2>')
    for sec in section_order(shots):
        ss = [s for s in shots if s["section"] == sec]
        v = sum(1 for s in ss if s["k"] == "V")
        P.append(f'<h2 class="sec"><span class="ts">{ts(ss[0]["t0"])}–{ts(ss[-1]["t1"])}</span>{e(sec)}<span class="cnt">{len(ss) - v} images · {v} videos</span></h2>')
        for s in ss:
            vid = s["k"] == "V"
            vp = (f'<div class="row vrow"><div class="lab">Video prompt</div><p>{e(video_prompt(s))}</p></div>'
                  f'<div class="clip">Generate {s["clip"]}s · use about {s["dur"]:.1f}s · camera: {e(s["cm"])}</div>') if vid else ""
            cd = "".join(f'<div class="scr"><span class="lbl">THEN PLAY CARD</span><span class="it">{e(cid)}.mp4</span><span class="kind">{d:.1f}s · voice paused · {e(key)}</span></div>' for cid, d, key in s["cards"])
            P.append(f'''<div class="shot {'v' if vid else 'i'}"><div class="hd"><span class="num">{s["n"]:03d}</span><span class="tag">{'VIDEO' if vid else 'IMAGE'}</span>
<span class="tc">{ts(s["t0"])}–{ts(s["t1"])} · {s["dur"]:.1f}s</span></div><div class="script">“{e(s["text"])}”</div>
<div class="up"><span>UPLOAD FIRST</span>{e(uploads(s))}</div>
<div class="row"><div class="lab">{'Start frame' if vid else 'Image prompt'}</div><p>{e(image_prompt(s))}</p></div>{vp}{cd}</div>''')
    css = open(os.path.join(HERE, "book.css")).read()
    open(os.path.join(ROOT, "image-video-prompts.html"), "w").write(
        f'<!doctype html><html><head><meta charset="utf-8"><title>Episode 2 Image and Video Prompts</title><style>{css}</style></head><body>{"".join(P)}</body></html>')

if __name__ == "__main__":
    main()
