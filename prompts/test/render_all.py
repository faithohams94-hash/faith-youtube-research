"""Renders ALL scenes into image + video prompts in the director format that passed the Scene 1-2 test.
Scenes 1-2 come from shots_s1_s2.py; scenes 3-32 come from directed/*.txt (compact format below).

Format of directed/*.txt:
## <scene> | <title>
MOOD: <mood and lighting for the whole scene>
# <shot id> | <title> | who: a, b | start: New image / Last frame of X | photo: <prop text, optional>
F: <frame for the image>
S: <one sentence: what this video is>
X: <star and focus, optional>
D: <0:01-0:05> | <owner> | <exact line>      owner = character key, or phone:/tv:/screen:/pa:/off:/memory:<key>, or x:<Name>=<look>
T: <0:00-0:02> | <action>                    (several)
C: <camera>
"""
import pathlib, sys, re
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
import build
import shots_s1_s2 as S12

C, VIS = build.C, build.VIS
FEM = {"ireti", "funmi", "ronke", "grace", "chioma", "lola"}
SCENES = {}
for f in sorted((HERE.parent / "scenes").glob("*.txt")):
    for s in build.parse(f.read_text()):
        SCENES[s["num"]] = s

SRC = {
 "phone": "ONLY out of the phone's speaker and must sound like a real phone line: thin, slightly tinny and compressed, a little crackle, as heard through a phone",
 "tv": "ONLY out of the TV's speaker, like a real TV broadcast: slightly boxy and distant",
 "screen": "ONLY out of the big wall screen's speakers, like a real video call: slightly compressed and digital",
 "pa": "ONLY through the concert hall's loudspeakers from the stage microphone: big, echoing, clearly from the stage",
 "off": "from OFF-SCREEN, outside the frame: a real voice in the same place but not visible, a little further away",
 "memory": "as a soft, echoing memory, gentle and distant, like a remembered voice in his head; nobody in the room says it",
}
LOOK = ("Photorealistic cinematic feature film, shot on 35mm cinema camera, highest resolution, razor-sharp and crystal clear, faces well exposed so every detail shows, "
        "shallow depth of field, rich but natural colour with a soft film grade, soft film grain, matte natural skin with real texture. No shine, no glow, no bloom, no HDR, no plastic skin. "
        "Every face stays exactly the same person as in the image in every frame: no morphing, no new faces, no new people. No text on screen.")

def name(k): return C[k][0].split(" (")[0]
def pro(k): return "her" if k in FEM else "his"
def she(k): return "she" if k in FEM else "he"

def ident(scn, k):
    if scn in S12.ID and k in S12.ID[scn]: return S12.ID[scn][k]
    w = SCENES[scn]["wear"].get(k, "")
    w = re.split(r",| \(|;", w)[0].strip()
    return VIS[k] + (f", wearing {w}" if w else "")

def parse_owner(o):
    if o.startswith("x:"):
        nm, look = (o[2:].split("=", 1) + [""])[:2]
        return ("x", nm.strip(), look.strip())
    if ":" in o:
        src, k = o.split(":", 1); return (src, k.strip(), None)
    return ("on", o.strip(), None)

def video(scn, s):
    who = s["who"]; L = []
    L.append(f"1. SCENE: {s['scene']}")
    focus = s.get("focus")
    if not focus:
        on = [parse_owner(o)[1] for _, o, _ in s["dialogue"] if parse_owner(o)[0] == "on"]
        focus = (f"{name(on[0])}'s face, centre frame." if on and on[0] in C else
                 f"{name(who[0])}'s face and body, centre frame." if who else "The place itself, centre frame.")
    L.append(f"2. STAR & FOCUS: {focus}")
    if s["dialogue"]:
        d = ["3. DIALOGUE (exact words, word for word, nothing added, nothing changed, nothing left out):"]
        voiced, speakers_on, voices_off = set(), set(), set()
        for t, o, line in s["dialogue"]:
            kind, k, look = parse_owner(o)
            if kind == "on":
                d.append(f'   {t} - {name(k).upper()} ({ident(scn, k)}) says: "{line}"')
                if k not in voiced:
                    d.append(f"   {name(k)}'s voice: {C[k][2].split(':',1)[-1].strip()}. These words come ONLY from {name(k)}'s mouth.")
                voiced.add(k); speakers_on.add(k)
            elif kind == "x":
                d.append(f'   {t} - {k.upper()} ({look}) says: "{line}"')
                if k not in voiced:
                    d.append(f"   {k}'s voice: a natural Nigerian voice, clearly different from every main character. These words come ONLY from {k}'s mouth.")
                voiced.add(k); speakers_on.add("x:" + k)
            else:
                label = name(k).upper() if k in C else k.upper()
                where = {"phone": "VOICE FROM THE PHONE", "tv": "VOICE FROM THE TV", "screen": "VOICE FROM THE SCREEN", "pa": "VOICE FROM THE STAGE SPEAKERS",
                         "off": "VOICE FROM OFF-SCREEN", "memory": "REMEMBERED VOICE"}[kind]
                d.append(f'   {t} - {where} ({label}): "{line}"')
                if k not in voiced:
                    vd = C[k][2].split(':', 1)[-1].strip() if k in C else "a clear, professional Nigerian voice"
                    d.append(f"   This voice comes {SRC[kind]}. {label.title()}'s voice: {vd}.")
                    if k in who and kind in ("phone", "screen"):
                        d.append(f"   Only {name(k)}'s face on the screen may move its lips. Nobody in the room talks.")
                voiced.add(k); voices_off.add(k)
        onscreen_people = [w for w in who if w not in speakers_on and not (w in voices_off and any(parse_owner(o)[0] in ('phone','screen') for _, o, _ in s['dialogue']))]
        for w in onscreen_people:
            if voices_off and not speakers_on:
                d.append(f"   {name(w).upper()} ({ident(scn, w)}) must NOT open {pro(w)} mouth at any moment: lips pressed together for all 10 seconds, no talking, no mouthing, no lip movement; {she(w)} only listens.")
            else:
                d.append(f"   {name(w).upper()} ({ident(scn, w)}) does NOT talk: mouth closed the whole time, only reacting.")
        if speakers_on and not voices_off:
            d.append("   No phone, TV or off-screen voice is heard. Nobody else says these lines.")
        L += d
    else:
        L.append("3. DIALOGUE: NONE. Nobody speaks. Every mouth stays closed. No voices at all.")
    L.append("4. TIMESTAMPS:")
    for t, a in s["timeline"]:
        L.append(f"   {t} - {a}")
    L.append(f"5. CAMERA: {s['camera']} Smooth and steady, no shake, no sudden zoom.")
    L.append(f"6. MOOD & LIGHTING: {s.get('mood') or MOODS[scn]}")
    L.append(f"7. LOOK / EFFECT: {LOOK}")
    on_talk = any(parse_owner(o)[0] in ("on", "x") for _, o, _ in s["dialogue"])
    if on_talk:
        L.append("8. LIP-SYNC & BODY: the speaker's lips match every word exactly, with natural breaths and pauses. Powerful, truthful acting: real emotion in the eyes, natural head and hand movements, body language that matches the words. Everyone else reacts only with their faces.")
    else:
        L.append("8. LIP-SYNC & BODY: no lip movement from anyone in the room. Powerful, truthful acting through the eyes, face, breathing and body only.")
    snd = build.AMBIENCE.get(scn, "quiet room tone")
    L.append(f"9. SOUND: {'the dialogue above, clean and clear, over ' if s['dialogue'] else 'no voices, only '}{snd}. No music, no extra sounds.")
    L.append("10. DURATION: exactly 10 seconds, one continuous shot, no cuts, no transitions. Start from the uploaded image. Highest quality.")
    return "\n".join(L)

def image(scn, s):
    sc = SCENES[scn]; who = s["who"]
    names = ", ".join([C[k][0] for k in who] + ([s["photo"]] if s.get("photo") else []))
    head = (f"CHARACTERS IN THIS IMAGE: {names}. I have uploaded their approved images and character sheets; they must be the same people with the same faces and body builds, not lookalikes."
            if names else "CHARACTERS IN THIS IMAGE: none (scenery only, no main characters in focus).")
    look = " ".join(f"{C[k][0]}: {C[k][1]}; wearing {sc['wear'].get(k, 'the outfit in the reference')}." for k in who)
    speak = [parse_owner(o)[1] for _, o, _ in s["dialogue"] if parse_owner(o)[0] == "on"]
    speak = list(dict.fromkeys(speak))
    face = (" The face of " + " and ".join(name(k) for k in speak) + " is clearly visible, facing the camera, with the mouth in view." if speak else "")
    return (f"{head}\nCreate one image, highest resolution, sharp and clear.\nFRAME: {s['frame']}{face}\nSETTING (identical in every shot of this scene): {sc['set']}"
            + (f"\nCHARACTERS: {look}" if look else "") + f"\n{build.IMAGE_LOCK}")

def parse_dsl(text):
    out, scn, cur = {}, None, None
    for raw in text.splitlines():
        l = raw.strip()
        if not l: continue
        if l.startswith("## "):
            scn = l[3:].split("|")[0].strip(); out[scn] = {"mood": "", "shots": []}; cur = None
        elif l.startswith("MOOD:") and cur is None:
            out[scn]["mood"] = l[5:].strip()
        elif l.startswith("# "):
            parts = [p.strip() for p in l[2:].split("|")]
            cur = {"id": parts[0], "title": parts[1], "who": [], "start": "New image", "dialogue": [], "timeline": [], "camera": "Static.", "scene": "", "frame": ""}
            for p in parts[2:]:
                if p.startswith("who:"): cur["who"] = [w.strip() for w in p[4:].split(",") if w.strip()]
                elif p.startswith("start:"): cur["start"] = p[6:].strip()
                elif p.startswith("photo:"): cur["photo"] = p[6:].strip()
            out[scn]["shots"].append(cur)
        elif cur is not None and l.startswith("start:"):
            cur["start"] = l[6:].strip()
        elif cur is not None:
            key, val = l[:2], l[2:].strip()
            if key == "F:": cur["frame"] = val
            elif key == "S:": cur["scene"] = val
            elif key == "X:": cur["focus"] = val
            elif key == "C:": cur["camera"] = val
            elif key == "M:": cur["mood"] = val
            elif key == "D:":
                t, o, line = [x.strip() for x in val.split("|", 2)]; cur["dialogue"].append((t, o, line.strip('"')))
            elif key == "T:":
                t, a = [x.strip() for x in val.split("|", 1)]; cur["timeline"].append((t, a))
    return out

MOODS = dict(S12.MOOD)
ALL = {"1": S12.S["1"], "2": S12.S["2"]}
for f in sorted((HERE / "directed").glob("*.txt")):
    for scn, v in parse_dsl(f.read_text()).items():
        MOODS[scn] = v["mood"]; ALL[scn] = v["shots"]

def check(scn, s):
    keys = set(C)
    for w in s["who"]:
        assert w in keys, (s["id"], w)
    for _, o, _ in s["dialogue"]:
        kind, k, _ = parse_owner(o)
        if kind == "on": assert k in s["who"], (s["id"], "speaker not in who", k)
        if kind not in ("x",): assert k in keys or kind in ("tv",), (s["id"], k)
    assert s["frame"] and s["scene"] and s["timeline"], (s["id"], "missing field")

def main():
    out = HERE / "final"; out.mkdir(exist_ok=True)
    total = 0
    for scn in sorted(ALL, key=int):
        sc = SCENES[scn]; shots = ALL[scn]
        ups = []
        for s in shots:
            check(scn, s)
            for k in s["who"]:
                if k not in ups: ups.append(k)
            for _, o, _ in s["dialogue"]:
                kind, k, _ = parse_owner(o)
                if kind in ("phone", "screen") and k in C and k not in ups: ups.append(k)
        extra = " + KEHINDE photo" if any(s.get("photo") for s in shots) else ""
        txt = [f"SCENE {scn}: {sc['title']}\nUPLOAD THESE CHARACTER SHEETS: {', '.join(C[k][0] for k in ups) or 'none'}{extra}\n"
               f"PASTE THE CHATGPT SETUP MESSAGE FIRST. In Grok: highest quality, 10 seconds, paste the whole video prompt.\n"]
        for s in shots:
            txt.append(f"\n{'='*70}\nSHOT {s['id']} | {s['title']} | Start: {s['start']}\n{'='*70}\n"
                       f"\n[IMAGE PROMPT - ChatGPT]\n{image(scn, s)}\n\n[VIDEO PROMPT - Grok]\n{video(scn, s)}\n")
            if any(parse_owner(o)[0] in ("phone", "screen", "tv") for _, o, _ in s["dialogue"]):
                txt.append("\nBACKUP if Grok still moves the listener's mouth: regenerate once. If it happens again, make this clip with DIALOGUE: NONE and add the line in CapCut (Audio > Voice effects > Telephone).\n")
        (out / f"Scene_{int(scn):02d}.txt").write_text("".join(txt))
        total += len(shots)
        print(f"scene {scn}: {len(shots)} shots")
    print("TOTAL", total)

if __name__ == "__main__":
    main()
