"""Renders the hand-directed test shots (Scenes 1-2) into image + video prompts."""
import pathlib, sys
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
import build
from shots_s1_s2 import S, ID, MOOD, SOUND

C, VIS = build.C, build.VIS
FEM = {"ireti", "funmi", "ronke", "grace", "chioma", "lola"}
scenes = {s["num"]: s for s in build.parse((HERE.parent / "scenes" / "01-08.txt").read_text())}

LOOK = ("Photorealistic cinematic feature film, shot on 35mm, shallow depth of field, muted and slightly desaturated colour, "
        "low contrast, soft film grain, matte natural skin with real texture. No shine, no glow, no bloom, no HDR, never brighter than the image. "
        "Every face stays exactly the same person as in the image in every frame: no morphing, no new faces, no new people. No text on screen.")

def pro(k): return "her" if k in FEM else "his"
def she(k): return "she" if k in FEM else "he"

def name(k): return C[k][0].split(" (")[0]

def video(scn, s):
    ids = ID[scn]
    lines = []
    lines.append(f"1. SCENE: {s['scene']}")
    lines.append(f"2. STAR & FOCUS: {s['focus']}")
    if s["dialogue"]:
        d = ["3. DIALOGUE (exact words, word for word, nothing added, nothing changed, nothing left out):"]
        voiced = set()
        for t, owner, line in s["dialogue"]:
            if owner.startswith("phone:"):
                k = owner.split(":")[1]
                d.append(f'   {t} - VOICE FROM THE PHONE ({name(k).upper()}): "{line}"')
                if owner not in voiced:
                    d.append(f"   This voice comes ONLY out of the phone's speaker and must sound like a real phone line: thin, slightly tinny and compressed, a little crackle, as heard through a phone. "
                             f"{name(k)}'s voice: {C[k][2].split(':',1)[-1].strip()}.")
                    if k in s["who"]:
                        d.append(f"   Only {name(k)}'s small face on the phone screen may move its lips. Nobody in the room talks.")
                voiced.add(owner)
                for w in ([] if len(voiced) > 1 and owner in voiced and d[-1].startswith("   ") and "must NOT open" in d[-1] else s["who"]):
                    if w != k:
                        d.append(f"   {name(w).upper()} ({ids[w]}) must NOT open {pro(w)} mouth at any moment: lips pressed together for all 10 seconds, no talking, no mouthing, no lip movement; {she(w)} only listens.")
            else:
                d.append(f'   {t} - {name(owner).upper()} ({ids[owner]}) says: "{line}"')
                if owner not in voiced:
                    d.append(f"   {name(owner)}'s voice: {C[owner][2].split(':',1)[-1].strip()}. These words come ONLY from {name(owner)}'s mouth.")
                voiced.add(owner)
        speakers = {o for _, o, _ in s["dialogue"]}
        silent = [w for w in s["who"] if w not in speakers and f"phone:{w}" not in speakers]
        on_screen_speakers = [o for o in speakers if not o.startswith("phone:")]
        if on_screen_speakers:
            for w in silent:
                d.append(f"   {name(w).upper()} ({ids[w]}) does NOT talk: mouth closed the whole time, only reacting.")
            d.append("   The phone is silent. No other voice is heard. Nobody else says these lines.")
        lines += d
    else:
        lines.append("3. DIALOGUE: NONE. Nobody speaks. Every mouth stays closed. No voices at all.")
    lines.append("4. TIMESTAMPS:")
    for t, a in s["timeline"]:
        lines.append(f"   {t} - {a}")
    lines.append(f"5. CAMERA: {s['camera']} Smooth and steady, no shake, no sudden zoom.")
    lines.append(f"6. MOOD & LIGHTING: {MOOD[scn]}")
    lines.append(f"7. LOOK / EFFECT: {LOOK}")
    if s["dialogue"] and any(not o.startswith("phone:") for _, o, _ in s["dialogue"]):
        lines.append("8. LIP-SYNC & BODY: the speaker's lips match every word exactly, with natural breaths and pauses. Powerful, truthful acting: real emotion in the eyes, small natural head and hand movements, body language that matches the words. Listeners react with their faces.")
    else:
        lines.append("8. LIP-SYNC & BODY: no lip movement from anyone on screen. Powerful, truthful acting through the eyes, face, breathing and body only.")
    snd = SOUND[scn]
    lines.append(f"9. SOUND: {'the dialogue above, clear' if s['dialogue'] else 'no voices'}, over {snd}. No music, no extra sounds.")
    lines.append("10. DURATION: exactly 10 seconds, one continuous shot, no cuts, no transitions. Start from the uploaded image.")
    return "\n".join(lines)

def image(scn, s):
    sc = scenes[scn]
    chars = [k for k in s["who"]]
    names = ", ".join(C[k][0] for k in chars)
    head = (f"CHARACTERS IN THIS IMAGE: {names}. I have uploaded their approved images and character sheets; they must be the same people with the same faces and body builds, not lookalikes."
            if chars else "CHARACTERS IN THIS IMAGE: none (scenery only, no people in focus).")
    look = " ".join(f"{C[k][0]}: {C[k][1]}; wearing {sc['wear'].get(k, 'the outfit in the reference')}." for k in chars)
    speak = {o for _, o, _ in s["dialogue"] if not o.startswith("phone:")}
    face = (" The face of " + " and ".join(name(k) for k in speak) + " is clearly visible with the mouth in view." if speak else "")
    return (f"{head}\nCreate one image.\nFRAME: {s['frame']}{face}\nSETTING (identical in every shot of this scene): {sc['set']}"
            + (f"\nCHARACTERS: {look}" if look else "") + f"\n{build.IMAGE_LOCK}")

def main():
    out_dir = HERE / "out"; out_dir.mkdir(exist_ok=True)
    for scn in ("1", "2"):
        sc = scenes[scn]
        ups = []
        for s in S[scn]:
            for k in s["who"]:
                if k not in ups: ups.append(k)
        if scn == "1" and "segun" not in ups: ups.append("segun")
        txt = [f"SCENE {scn}: {sc['title']}  (TEST BATCH)\nUPLOAD THESE CHARACTER SHEETS: {', '.join(C[k][0] for k in ups)}\n"
               f"PASTE THE CHATGPT SETUP MESSAGE FIRST (see the guide). In Grok, choose the highest quality and 10 seconds.\n"]
        for s in S[scn]:
            txt.append(f"\n{'='*70}\nSHOT {s['id']} | {s['title']} | Start: {s['start']}\n{'='*70}\n"
                       f"\n[IMAGE PROMPT - ChatGPT]\n{image(scn, s)}\n\n[VIDEO PROMPT - Grok]\n{video(scn, s)}\n")
            if any(o.startswith("phone:") for _, o, _ in s["dialogue"]):
                txt.append("\nBACKUP if Grok still moves the listener's mouth: regenerate once. If it happens again, make this clip with DIALOGUE: NONE and add the phone line in CapCut (Audio > Voice effects > Telephone).\n")
        (out_dir / f"Scene_{int(scn):02d}_TEST.txt").write_text("".join(txt))
        print(scn, len(S[scn]), "shots")

main()
