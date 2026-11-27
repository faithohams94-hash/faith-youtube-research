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


ACTION_RE = re.compile(r"\b(throws?|threw|flicks?|slaps?|push(?:es)?|pushed|hits?|punch(?:es)?|drops?|closes?|shuts?|opens?|hands?\b|gives?|snatch(?:es)?|grabs?|picks? (?:it |the \w+ )?up|puts? (?:it |the \w+ )?down|places?|sets? (?:it )?down|lays?|hugs?|kneels?|stands?\b|sits?\b|walks? (?:out|away|in)|leaves?|storms? off|runs?|pours?|writes?|takes?|tears?|bangs?|kicks?|wipes?|lifts?|lowers?|swallows?|flush(?:es)?|presses?|unlocks?|locks?|falls?|catches?|slides?|rolls?|waves?|points?|taps?|squeezes?|turns? away|pulls?|rocks?)\b", re.I)

def onscreen_speakers(s):
    return [parse_owner(o)[1] for _, o, _ in s["dialogue"] if parse_owner(o)[0] == "on"]

BLOCK = {}
_cur = None
for _l in (HERE / "blocking.txt").read_text().splitlines():
    _l = _l.strip()
    if not _l or _l.startswith("# "): continue
    if _l.startswith("## "): _cur = _l[3:].strip(); BLOCK[_cur] = []; continue
    _id, _t = [x.strip() for x in _l.split("|", 1)]; BLOCK[_cur].append((_id, _t))

def plan_continuity(shots, scn="0"):
    """Give every shot its previous shot, its conversation partner and eyeline notes."""
    order = {sh["id"]: i for i, sh in enumerate(shots)}
    for _id, _t in BLOCK.get(scn, []):
        assert _id in order, ("blocking id not found", scn, _id)
    for i, s in enumerate(shots):
        s["_scn"] = scn
        s["_prev"] = shots[i - 1] if i > 0 else None
        blk = [t for _id, t in BLOCK.get(scn, []) if order[_id] <= i]
        s["_block"] = blk[-1] if blk else None
        sp = list(dict.fromkeys(onscreen_speakers(s)))
        s["_speaker"] = sp[0] if sp else None
        partner = None
        if s["_speaker"]:
            others = [w for w in s["who"] if w != s["_speaker"]]
            if others:
                partner = others[0]
            else:
                near = list(range(i - 1, max(-1, i - 4), -1)) + list(range(i + 1, min(len(shots), i + 4)))
                for pool in ("speakers", "who"):          # someone who actually speaks nearby comes first
                    for j in near:
                        cands = onscreen_speakers(shots[j]) if pool == "speakers" else shots[j]["who"]
                        for k in cands:
                            if k != s["_speaker"] and k in C:
                                partner = k; break
                        if partner: break
                    if partner: break
        s["_partner"] = partner
    if int(scn) >= 7:
        plan_coverage(shots)
    return shots

PHONE_RE = re.compile(r"phone (?:held|to)|on the phone|phone up|holding (?:his|her) phone|phone in (?:his|her) hand|phone call|phone low|phone to (?:his|her) ear|phone at (?:his|her) ear|phone screen|video call|wall screen", re.I)

def plan_coverage(shots):
    """Film-style coverage: wide two-shot to open a conversation and after a long speech,
    a close-up on whoever gives a longer opinion, and over-the-shoulder shots for quick replies."""
    prev_pair, prev_cov, prev_spk = None, None, None
    for s in shots:
        S, P = s.get("_speaker"), s.get("_partner")
        is_call = bool(PHONE_RE.search(s["frame"])) or any(parse_owner(o)[0] in ("phone", "screen", "tv", "pa") for _, o, _ in s["dialogue"])
        if S and P and P in C and not is_call:
            pair = frozenset((S, P))
            words = len(" ".join(l for _, o, l in s["dialogue"]).split())
            chained = s["start"].lower().startswith("last frame")
            if chained and pair == prev_pair and prev_cov: cov = prev_cov          # same frame continues: keep the framing
            elif pair != prev_pair: cov = "WIDE"                                 # a conversation opens wide
            elif words >= 14: cov = "CLOSE"                                      # a longer opinion: close on the speaker
            elif prev_cov == "CLOSE" and S != prev_spk: cov = "WIDE"             # after someone's speech, back to wide
            elif prev_cov == "OTS": cov = "WIDE"
            else: cov = "OTS"
            s["_cover"] = cov
            if cov in ("WIDE", "OTS") and P not in s["who"]:
                s["who"] = list(s["who"]) + [P]
            prev_pair, prev_cov, prev_spk = pair, cov, S
        elif not s["who"]:
            prev_pair, prev_cov, prev_spk = None, None, None

def cover_frame(s):
    S, P, cov = s["_speaker"], s["_partner"], s["_cover"]
    nS, nP = name(S), name(P)
    if cov == "WIDE":
        return (f"WIDE TWO-SHOT: the whole moment exactly as the STAGING describes, everyone in their places and on their own side of the frame. "
                f"{nS} and {nP} are both fully visible, faces clearly seen in three-quarter profile, looking at each other; {nS} is speaking to {nP}.")
    if cov == "CLOSE":
        return (f"MEDIUM CLOSE-UP on {nS} while {she(S)} speaks, filmed from the same side of the room as the wide shot, so {nS} is on the same side of the frame as in the wide shot; "
                f"{nP} is just out of frame, and {nS}'s eyes are on {nP}.")
    return (f"OVER-THE-SHOULDER SHOT: over {nP}'s shoulder onto {nS}'s face. The back of {nP}'s head and shoulder are soft in the foreground on {nP}'s own side of the frame; "
            f"{nS} is in sharp focus, eyes on {nP}.")

def eyeline(scn, s):
    who = s["who"]
    if not who:
        return None
    phone = any(parse_owner(o)[0] in ("phone", "screen") for _, o, _ in s["dialogue"])
    if s.get("_speaker"):
        S, P = s["_speaker"], s.get("_partner")
        fr = s["frame"].lower()
        if re.search(r"phone (?:held|to|at)|on the phone|phone up|holding (?:his|her) phone|phone in (?:his|her) hand|phone call|phone low", fr):
            if scn != "1" and not re.search(r"video call|screen", fr + " " + s["scene"].lower()):
                return f"{name(S)} speaks into the phone at {pro(S)} ear, eyes looking ahead or down into the distance as people do on a call. Nobody looks into the camera lens at any moment."
            return f"{name(S)} keeps {pro(S)} eyes on the phone screen, talking to the face on the video call. Nobody looks into the camera lens at any moment."
        if P:
            off = "" if P in who else f" ({name(P)} is just off-camera, exactly where the previous shot placed {'her' if P in FEM else 'him'})"
            back = "".join(f" {name(w)} looks back at {name(S)}." for w in who if w != S)
            return f"{name(S)} looks directly into {name(P)}'s eyes while speaking{off}.{back} Eye contact is held for the whole clip unless the timestamps say someone looks away. Nobody looks into the camera lens at any moment."
        return f"{name(S)} looks at the person {she(S)} is speaking to, just off-camera. Nobody looks into the camera lens at any moment."
    if phone:
        return "Everyone in the frame keeps their eyes on the phone or screen they are listening to, or looks down in thought. Nobody looks into the camera lens at any moment."
    if len(who) > 1:
        return "Everyone keeps looking where they were looking in the first frame (at each other, or at the action), and only changes when the timestamps say so. Nobody looks into the camera lens at any moment."
    return f"{name(who[0])}'s eyes follow the action exactly as written; {she(who[0])} never looks into the camera lens."

ACT_RULES = [
 (("angry", "anger", "fury", "furious", "rage", "roar", "shout", "cruel", "threat", "glare", "snap", "storm", "bitter", "mock"),
  "anger lives in the body: jaw clenched, the veins on the neck and temples standing out, nostrils flaring, eyes hard, chest heaving, a pointing finger or tightening fists"),
 (("cry", "tears", "sob", "grie", "sad", "broken", "devastat", "heartbr", "weep", "hurt", "pain", "lonely"),
  "sadness lives in the body: the eyes turning red and wet, lips trembling, chin quivering, shoulders sinking, the breath catching, a hand wiping tears away"),
 (("shock", "stunned", "freez", "horror", "realis", "gasp", "widen", "pale", "trap"),
  "shock lives in the body: eyes widening, the breath stopping, the mouth falling slightly open, a hand rising to the mouth or chest, the whole body going still"),
 (("fear", "afraid", "nervous", "terrif", "panic", "scared", "trembl", "frighten", "desperate"),
  "fear lives in the body: quick shallow breathing, eyes darting, swallowing hard, trembling hands"),
 (("joy", "laugh", "happy", "grin", "celebrat", "proud", "delight", "overjoy"),
  "joy lives in the body: eyes crinkling, a smile that reaches the eyes, shoulders lifting, light open gestures"),
 (("tender", "gentle", "loving", "bless", "hug", "comfort", "warm"),
  "tenderness lives in the body: soft eyes, a slow careful touch, leaning in, a gentle breath"),
 (("firm", "determin", "steady", "resolv", "dignity", "brave", "commanding", "calm"),
  "determination lives in the body: chin lifted, steady eyes that do not blink away, one slow deep breath, a still, upright posture"),
]

def acting(scn, s):
    txt = " ".join([s["scene"], s.get("_block") or ""] + [a for _, a in s["timeline"]]).lower()
    tells = [t for keys, t in ACT_RULES if any(k in txt for k in keys)][:3]
    base = "Play it like a real person living this moment, not like an AI: every word and every movement matches the feeling. Each line is spoken the way a real person would say it in this situation, with real breathing and natural pauses."
    return base + (" " + " ".join(t[0].upper() + t[1:] + "." for t in tells) if tells else "")

SMOOTH = ("Every movement is smooth, continuous and natural, like a real actor on a film set: no jerks, no robotic or sudden moves, no frozen bodies. "
          "Each action starts gently, carries through with real weight and finishes gently: sitting down, standing up, walking in, walking out and closing the door, "
          "picking things up and putting them down, touching, hugging, pushing, throwing.")
DETAILS = ("Hands and faces are alive like a real person's: hands hold, adjust, rest in a pocket or on the table, touch the face or glasses while thinking, then settle back smoothly. "
           "Small details (a breath before speaking, a glance down, fingers tightening, a hand going into a pocket and coming back out) give the moment life, but never distract from the main action.")

VOICE_KINDS = ("phone", "screen", "tv", "pa", "off", "memory")

def voice_only(scn, s):
    return int(scn) >= 7 and s["dialogue"] and all(parse_owner(o)[0] in VOICE_KINDS for _, o, _ in s["dialogue"])

def video(scn, s):
    if voice_only(scn, s):
        return video_listen(scn, s)
    who = s["who"]; L = []
    if s.get("ref"):
        refs = " ".join(f"IMAGE {i+2} is the face of {name(k).upper()} ({ident(scn, k)}): {name(k)}'s face MUST be exactly the face in image {i+2} in every frame, the same person, not a lookalike, especially when the camera shows the face." for i, k in enumerate(s["ref"]))
        L.append(f"0. REFERENCE IMAGES: IMAGE 1 is the first frame of the video. {refs}")
    if int(scn) >= 7:
        L.append("ORDER TO GROK: generate this video ONLY with every item below in it: the exact dialogue and nothing more, every mandatory action clearly shown, everyone in their staging positions, the eye contact and the emotions. Do not leave anything out, do not add anything, do not change anything.")
    L.append(f"1. SCENE: {s['scene']}")
    focus = s.get("focus")
    if not focus:
        on = [parse_owner(o)[1] for _, o, _ in s["dialogue"] if parse_owner(o)[0] == "on"]
        focus = (f"{name(on[0])}'s face, centre frame." if on and on[0] in C else
                 f"{name(who[0])}'s face and body, centre frame." if who else "The place itself, centre frame.")
    if s.get("_cover") == "WIDE":
        focus = f"Both {name(s['_speaker'])} and {name(s['_partner'])} in a wide two-shot; {name(s['_speaker'])} is the one speaking."
    elif s.get("_cover") == "CLOSE":
        focus = f"{name(s['_speaker'])}'s face in a medium close-up while {she(s['_speaker'])} speaks."
    elif s.get("_cover") == "OTS":
        focus = f"{name(s['_speaker'])}'s face, seen over {name(s['_partner'])}'s shoulder."
    L.append(f"2. STAR & FOCUS: {focus}")
    prev = s.get("_prev")
    if prev and who:
        pend = prev["timeline"][-1][1] if prev.get("timeline") else ""
        if s["start"].lower().startswith("last frame"):
            L.append(f"2A. CONTINUITY IN: this clip begins on the exact last frame of the previous clip ({pend}) and carries straight on: same positions, same eyelines, same emotion, same things in their hands.")
        else:
            L.append(f"2A. CONTINUITY IN: this is the next angle of the SAME moment, straight after: {pend} At 0:00 everyone is already in that position, with that eyeline and that emotion. No reset, no fresh pose, nobody turns to the camera first.")
    ey = eyeline(scn, s)
    if ey:
        L.append(f"2B. EYE CONTACT: {ey}")
    if who:
        L.append(f"2C. EMOTION: faces and bodies show exactly what this moment means: {s['scene']} Bad news brings worry, shock or grief; anger brings tension; nobody smiles or laughs unless the timestamps say so. Strong, truthful facial expression and body language.")
    if s.get("_block"):
        L.append(f"2D. STAGING (exactly the same as the previous shot unless the timestamps say someone moves): {s['_block']} Sitting people stay sitting, standing people stay standing, and nobody changes side of the frame. The camera stays on the same side of the action, so left stays left and right stays right in every shot.")
    if who and int(scn) >= 6:
        L.append("2E. REACTIONS: every listener reacts with their whole body to what they hear, as real people do. Bad news: shoulders drop, faces fall, eyes fill, breathing catches, hands go to the mouth or chest. Insults: the body stiffens, the jaw tightens, the eyes flash. Good news: the face opens, eyes shine, breath rushes out. Never a neutral face, never a smile at bad news.")
    if int(scn) >= 11 and who:
        L.append(f"2F. ACTING: {acting(scn, s)}")
        L.append(f"2G. SMOOTH HUMAN MOVEMENT: {SMOOTH}")
        L.append(f"2H. HANDS & SMALL DETAILS: {DETAILS}")
    if s.get("split") and len(who) >= 2:
        L.append(f"2I. SPLIT SCREEN PHONE CALL: the frame is split down the middle into two halves, two different places at the same moment. LEFT half = {name(who[0]).upper()} ({ident(scn, who[0])}). RIGHT half = {name(who[1]).upper()} ({ident(scn, who[1])}). Each person stays in their own half, in their own place, holding their phone. Each person speaks ONLY their own line in their own half; while one talks, the other listens with mouth closed. The two halves never swap, merge or move.")
    if s["dialogue"]:
        d = ["3. DIALOGUE (exact words, word for word, nothing added, nothing changed, nothing left out):"]
        voiced, speakers_on, voices_off = set(), set(), set()
        for t, o, line in s["dialogue"]:
            kind, k, look = parse_owner(o)
            if kind == "on":
                if int(scn) >= 6:
                    d.append(f'   {t} - {name(k).upper()} ({ident(scn, k)}) says EXACTLY these words and NOTHING else: "{line}" Then {she(k)} stops talking.')
                else:
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
        if int(scn) >= 7 and s.get("_block"):
            shown = set(who) | speakers_on | voices_off
            for k in C:
                nm = name(k).split()[-1].lower()
                if k not in shown and re.search(r"\b" + re.escape(nm) + r"\b", s["_block"].lower()):
                    d.append(f"   {name(k).upper()} ({ident(scn, k)}), if anywhere in the frame, does NOT talk: mouth closed the whole time.")
        if speakers_on and voices_off:
            order = []
            for t, o, line in s["dialogue"]:
                kind, k, _ = parse_owner(o)
                who_txt = f"the voice from the {'phone' if kind == 'phone' else 'screen' if kind == 'screen' else 'TV' if kind == 'tv' else 'off-screen'} ({name(k) if k in C else k})" if kind not in ("on", "x") else f"{name(k)} ({ident(scn, k)})"
                order.append(f"{t} {who_txt}")
            d.append("   TURN-TAKING (this is a real conversation with sound, NOT a silent video): " + "; then ".join(order) + ". Only one voice at a time.")
            for k in speakers_on:
                if k in C:
                    d.append(f"   While the phone voice is speaking, {name(k).upper()} keeps {pro(k)} mouth closed and listens; {name(k).upper()} opens {pro(k)} mouth ONLY at {pro(k)} own time above. While {name(k).upper()} speaks, the phone is silent.")
        if speakers_on and not voices_off:
            d.append("   No phone, TV or off-screen voice is heard. Nobody else says these lines.")
        if int(scn) >= 6:
            d.append("   STRICT SCRIPT: these are the ONLY words spoken in this whole clip. Not one extra word before, between or after them: no goodbyes, no thank-yous, no 'take care', no added sentences, no humming or mumbling. Outside the times above, every mouth is closed. Any action in the timestamps after the last line (standing, leaving, paying, turning) happens in complete silence.")
        L += d
    else:
        L.append("3. DIALOGUE: NONE. Nobody speaks. Every mouth stays closed. No voices at all.")
    L.append("4. TIMESTAMPS:")
    def _sec(x): 
        m, sec = x.split(":"); return int(m) * 60 + int(sec)
    last_line = max([_sec(t.split("-")[1]) for t, _, _ in s["dialogue"]] or [-1])
    for t, a in s["timeline"]:
        silent = int(scn) >= 6 and s["dialogue"] and _sec(t.split("-")[0]) >= last_line
        L.append(f"   {t} - {a}" + (" (in complete silence, no words)" if silent else ""))
    if who:
        L.append(f"4A. CONTINUITY OUT: end on: {s['timeline'][-1][1]} Hold that exact position, eyeline and emotion in the final second, so the next clip continues from it.")
        L.append("4B. DETAILS: finish every physical action fully and naturally. Anyone who leaves a room walks out and closes the door behind them, unless told otherwise. When a phone call ends, the phone is lowered or put down. Objects are set down properly and never vanish. Hands always hold things naturally.")
    if int(scn) >= 7 and who:
        acts = [(t, a) for t, a in s["timeline"] if ACTION_RE.search(a)]
        if acts:
            L.append("4C. MANDATORY ACTIONS: these MUST happen on screen, fully and clearly, at exactly these times. Show each whole movement from start to finish: a thrown or flicked object really flies through the air and lands on the floor, a door really swings and shuts, a hand really passes an object to another hand, a push really moves the other person. Never skip, shorten, hide or only suggest them:")
            for t, a in acts:
                L.append(f"   {t} - {a}")
    cam = s['camera']
    if s.get("_cover") == "WIDE": cam = "Static wide two-shot showing both people, with a very slow, gentle push-in."
    elif s.get("_cover") == "CLOSE": cam = "Static medium close-up on the speaker, with a very slow push-in."
    elif s.get("_cover") == "OTS": cam = "Static over-the-shoulder shot."
    L.append(f"5. CAMERA: {cam} Smooth and steady, no shake, no sudden zoom.")
    L.append(f"6. MOOD & LIGHTING: {s.get('mood') or MOODS[scn]}")
    L.append(f"7. LOOK / EFFECT: {LOOK}" + (f" {s['extra_look']}" if s.get('extra_look') else ""))
    on_talk = any(parse_owner(o)[0] in ("on", "x") for _, o, _ in s["dialogue"])
    if on_talk:
        L.append(("8. LIP-SYNC & BODY: the speaker's lips move ONLY during the written words and match every word exactly; before and after them the mouth stays closed." if int(scn) >= 6 else "8. LIP-SYNC & BODY: the speaker's lips match every word exactly, with natural breaths and pauses.") + " Powerful, truthful acting: real emotion in the eyes, natural head and hand movements, body language that matches the words. Everyone else reacts with their faces and bodies, mouths closed.")
    else:
        L.append("8. LIP-SYNC & BODY: no lip movement from anyone in the room. Powerful, truthful acting through the eyes, face, breathing and body only.")
    snd = s.get("sound") or build.AMBIENCE.get(scn, "quiet room tone")
    L.append(f"9. SOUND: {'the dialogue above, clean and clear, over ' if s['dialogue'] else 'no voices, only '}{snd}. No music, no extra sounds.")
    L.append(f"10. DURATION: exactly {s.get('dur', 10)} seconds, one continuous shot, no cuts, no transitions. Start from the uploaded image. Highest quality.")
    if int(scn) >= 7:
        call = any(parse_owner(o)[0] in ("phone", "screen", "tv", "pa", "off", "memory") for _, o, _ in s["dialogue"])
        eyes_chk = "eyes are where section 2B says, never the camera" if call else "eyes are on the other person, never the camera"
        voice_chk = ("the voice comes only from where section 3 says and every mouth in the room stays closed while it plays" if call
                     else "each line comes only from the character named for it, and nobody else speaks")
        L.append(f"FINAL CHECK BEFORE GENERATING: the words spoken are exactly the dialogue above and nothing else; {voice_chk}; every mandatory action is clearly visible; nobody changes position, side or posture unless the timestamps say so; {eyes_chk}; faces stay the same people; the light and mood stay exactly as in the image.")
    return "\n".join(L)

def video_listen(scn, s):
    """A listening clip: Grok makes NO voice at all; the off-screen voice is added in CapCut."""
    who = s["who"]; L = []
    src = {"phone": "a phone call", "screen": "a video call on the screen", "tv": "the TV", "pa": "the stage speakers", "off": "someone off-screen", "memory": "a memory"}
    kind = parse_owner(s["dialogue"][0][1])[0]
    L.append("THIS CLIP IS SILENT. NOBODY TALKS. NO VOICES AT ALL. Only the background sounds below. Do not make anyone speak.")
    L.append(f"1. SCENE: {s['scene']}")
    L.append(f"2. STAR & FOCUS: {s.get('focus') or (name(who[0]) + chr(39) + 's face, listening') if who else 'the place'}")
    for w in who:
        L.append(f"   {name(w).upper()} = {ident(scn, w)}. {name(w).upper()} does NOT talk: lips pressed together for the whole clip, no mouth movement at all.")
    L.append(f"3. WHAT IS HAPPENING: {', '.join(name(w) for w in who) or 'Everyone'} {'is' if len(who) < 2 else 'are'} listening to {src[kind]} in silence. The voice they hear is NOT in this video. Nobody on screen speaks, whispers or mouths words.")
    if s.get("_block"):
        L.append(f"4. STAGING: {s['_block']} Nobody changes position, side or posture.")
    L.append("5. TIMESTAMPS:")
    for t, a in s["timeline"]:
        L.append(f"   {t} - {a} (mouth closed, silent)")
    L.append("6. EYES: eyes on the phone or screen, or looking down in thought. Nobody looks into the camera lens.")
    L.append(f"7. EMOTION: {s['scene']} Show it only through the eyes, the jaw, the breathing and the body.")
    L.append(f"8. CAMERA: {s['camera']} No shake, no zoom.")
    L.append(f"9. MOOD & LIGHTING: {s.get('mood') or MOODS[scn]}")
    L.append("10. LOOK: Photorealistic 35mm feature film, highest resolution, sharp, soft film grain, matte natural skin. Faces stay exactly the same people as in the image.")
    L.append(f"11. SOUND: only {s.get('sound') or build.AMBIENCE.get(scn, 'quiet room tone')}. NO VOICES. No music.")
    end = max(int(t.split("-")[1].split(":")[1]) for t, _ in s["timeline"])
    dur = s.get("dur") or max(5, min(10, end))
    L.append(f"12. DURATION: exactly {dur} seconds, one continuous shot.")
    L.append("FINAL CHECK: nobody on screen talks or moves their lips at any moment; this is a silent listening shot.")
    return "\n".join(L)

def capcut_voice(scn, s):
    FX = {"phone": "Telephone", "screen": "Telephone (lighter)", "tv": "Radio or Telephone", "pa": "Megaphone, or Hall reverb", "off": "no effect; lower the volume a little", "memory": "Echo"}
    out = []
    for t, o, line in s["dialogue"]:
        kind, k, _ = parse_owner(o)
        who = name(k).upper() if k in C else k.upper()
        out.append(f"VOICE TO ADD IN CAPCUT at {t}: {who}: \"{line}\"")
        if k in C:
            out.append(f"  Step 1 - make the voice in Grok: upload {who}'s approved image and paste: \"Static close-up. {VIS[k][0].upper() + VIS[k][1:]} speaks, facing slightly off-camera: '{line}' Voice: {C[k][2].split(':', 1)[-1].strip()}. Only these words. Sound: clear voice only, no music. 10 seconds.\" Keep only the audio.")
        else:
            out.append("  Step 1 - make the voice with CapCut text-to-speech (a clear Nigerian news voice) or record it.")
        out.append(f"  Step 2 - in CapCut: Extract audio, place it under this clip at {t}, then Audio > Voice effects > {FX[kind]}.")
    return "\n".join(out)

FRAMING_RE = re.compile(r"^(?:same\s+)?(?:(?:medium|wide|close|low|extreme|low-angle|high|cold)[ -])*(?:close-up|close shot|shot|two-shot|over-the-shoulder shot|view)(?:\s+(?:of|at|from|on|over))?[:,]?\s*", re.I)
LENS_RE = re.compile(r",?\s*face turned three-quarters toward the camera, [^,]*, never looking into the lens", re.I)

def flow_look(k, scn):
    """Neutral, Flow-friendly description of a character (no ages, no body or skin rules)."""
    base = {"ireti": "an adult woman with long black box braids tied back in a low ponytail and small silver stud earrings",
            "chief": "an elderly man with short snow-white hair and a full white beard",
            "femi": "an adult man with a short low-cut fade, a neat short black beard and rimless gold glasses",
            "gabriel": "an adult man with short curly hair, a full beard and clear aviator glasses",
            "funmi": "a middle-aged woman with a wine-coloured head wrap",
            "dayo": "a slim young man with a low haircut",
            "ronke": "a middle-aged woman with a tight black head wrap and neat make-up",
            "audu": "an older man with a grey-white beard and a white embroidered cap",
            "hassan": "a middle-aged doctor with short greying hair and a salt-and-pepper beard",
            "lekan": "a heavy-set older man with gold-rimmed glasses and a thin moustache",
            "grace": "an adult woman with her hair in cornrows pulled into a low bun",
            "okoro": "a big older doctor with greying curly hair and a full grey beard",
            "jide": "a short, heavy man with a short beard",
            "chioma": "an adult woman with curly hair pulled up, gold sunglasses on her head and big gold hoop earrings",
            "segun": "a middle-aged man with short hair and a full beard with some grey",
            "kunle": "a big man with a clean bald head, dark rectangular glasses and a neat goatee",
            "lola": "a middle-aged woman with big, voluminous dark wavy hair and gold drop earrings",
            "ajala": "an elderly man with a white beard, round dark sunglasses and a cream fedora"}[k]
    wear = SCENES[scn]["wear"].get(k, "")
    return f"{name(k).upper()}: {base}" + (f", wearing {wear}" if wear else "")

def image_flow(scn, s):
    """Image prompt written for Google Flow: calm, neutral wording, one clear framing."""
    sc = SCENES[scn]; who = s["who"]
    detail = LENS_RE.sub("", s["frame"])
    detail = re.sub(r",?\s*facing the camera(?: at three-quarters)?", "", detail)
    if s.get("_cover"):
        S, P, cov = s["_speaker"], s["_partner"], s["_cover"]
        framing = {"WIDE": f"A wide two-shot showing both {name(S)} and {name(P)} in their places, both faces clearly visible in three-quarter view, looking at each other; {name(S)} is speaking.",
                   "CLOSE": f"A medium close-up of {name(S)} speaking, face clearly visible in three-quarter view, looking at {name(P)} just out of frame.",
                   "OTS": f"An over-the-shoulder shot: over {name(P)}'s shoulder onto {name(S)}'s face; the back of {name(P)}'s head soft in the foreground; {name(S)} in sharp focus, looking at {name(P)}."}[cov]
        detail = FRAMING_RE.sub("", detail)
        frame = f"{framing} Details of the moment: {detail}"
    else:
        frame = detail
    L = ["A photorealistic still frame from a Nigerian drama film, wide 16:9, shot on a 35mm cinema lens with shallow depth of field."]
    if who:
        L.append("Use my uploaded character images for the people in this shot and keep their faces, hairstyles and builds the same as in those images." + (" The framed photo uses my uploaded photo of the father." if s.get("photo") else ""))
    L.append(f"SCENE: {sc['set']}")
    L.append(f"FRAMING: {frame}")
    if s.get("_block"):
        L.append(f"POSITIONS (keep these exactly): {s['_block']}")
    prev = s.get("_prev")
    if prev and who and prev.get("timeline"):
        L.append(f"CONTINUITY: this frame comes straight after: {prev['timeline'][-1][1]} Same positions, clothes, props and light as that moment.")
    if who:
        L.append("PEOPLE: " + " | ".join(flow_look(k, scn) for k in who) + ".")
        L.append("Nobody looks into the camera; people look at each other or at what they are doing.")
    L.append("LOOK: natural light from real sources only, a soft, slightly muted film colour grade, gentle film grain, natural skin texture with no glossy or airbrushed look, realistic hands and posture. All people shown are adults. No text, logos or watermarks anywhere.")
    out = "\n".join(L)
    for a, b in FLOW_SOFTEN:
        out = re.sub(a, b, out, flags=re.I)
    return out

FLOW_SOFTEN = [
    (r"burnt at the edges", "frayed and darkened at the edges"), (r"\bburnt\b", "scorched"), (r"\bburn scar\b", "healed scar"),
    (r"there is fire in them", "there is new determination in them"), (r"opening with fire", "opening with new determination"), (r"fire in (his|her) eyes", r"determination in \1 eyes"), (r"cold fire", "cold determination"),
    (r"with flames rising from its far side", "with a soft orange glow behind it"), (r"flames flicker behind them", "a soft orange glow behind them"),
    (r"\s*No blood, no injuries (shown|visible)\.?", ""), (r",?\s*no injuries visible", ""),
    (r"Aunty Ronke in handcuffs", "Aunty Ronke escorted by two police officers"), (r"Ronke in handcuffs", "Ronke escorted by two police officers"), (r"in handcuffs", "escorted by police"),
    (r"\bslapping\b", "brushing"), (r"\bslaps\b", "brushes"), (r"\bpoisonous\b", "cold"),
]

def policy_safe(scn, txt):
    """From Scene 11: same picture and look, but wording that suits ChatGPT and Google Flow policies."""
    if int(scn) < 11:
        return txt
    txt = re.sub(r"\s*\((\d{2})\)", "", txt)                                   # no ages
    txt = txt.replace("Never slimmer, lighter, younger or more glamorous. ", "")
    txt = txt.replace("DIRECTOR'S LOCK — FOLLOW EVERY RULE, NO EXCEPTIONS.", "Please follow these rules:")
    txt = txt.replace("NO gloss, NO shine, NO glow, NO HDR, NO airbrushing, NO plastic skin, NO bloom.", "Natural matte skin, no glossy or airbrushed look.")
    for a, b in FLOW_SOFTEN:
        txt = re.sub(a, b, txt, flags=re.I)
    return txt

def image(scn, s):
    sc = SCENES[scn]; who = s["who"]
    names = ", ".join([C[k][0] for k in who] + ([s["photo"]] if s.get("photo") else []))
    head = (f"CHARACTERS IN THIS IMAGE: {names}. I have uploaded their approved images and character sheets; they must be the same people with the same faces and body builds, not lookalikes."
            if names else "CHARACTERS IN THIS IMAGE: none (scenery only, no main characters in focus).")
    look = " ".join(f"{C[k][0]}: {C[k][1]}; wearing {sc['wear'].get(k, 'the outfit in the reference')}." for k in who)
    speak = [parse_owner(o)[1] for _, o, _ in s["dialogue"] if parse_owner(o)[0] == "on"]
    speak = list(dict.fromkeys(speak))
    face = (" The face of " + " and ".join(name(k) for k in speak) + " is clearly visible in three-quarter view with the mouth in view." if speak else "")
    ey = eyeline(scn, s)
    frame = s["frame"]
    if s.get("_cover"):
        frame = cover_frame(s) + f" MOMENT DETAILS (use these details, but the framing above decides the camera): {frame}"
    P = s.get("_partner")
    look_at = f"eyes on {name(P)}" if P else "eyes on the other person or the action"
    frame = re.sub(r"facing the camera(?: at three-quarters)?", f"face turned three-quarters toward the camera, {look_at}, never looking into the lens", frame)
    prev = s.get("_prev")
    cont = (f"\nCONTINUITY: this frame comes straight after: {prev['timeline'][-1][1]} Same positions, same eyelines, same props in their hands, same wardrobe and light." if prev and who and prev.get("timeline") else "")
    eyes = f"\nEYES: {ey}" if ey else ""
    if s.get("_block"):
        eyes += f"\nSTAGING (keep exactly; this wins over anything above if different): {s['_block']} The camera is on the same side of the action as the other shots of this scene, so everyone stays on the same side of the frame."
    if s.get("split"):
        frame = ("SPLIT SCREEN for a phone call: the 16:9 frame is divided down the middle by a thin, clean vertical line into two halves, two different places at the same moment, each half lit by its own real light. " + frame)
    return (f"{head}\nCreate one image, highest resolution, sharp and clear.\nFRAME: {frame}{face}{cont}{eyes}\nSETTING (identical in every shot of this scene): {sc['set']}"
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
                elif p.strip() == "split": cur["split"] = True
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
            elif key == "N:": cur["sound"] = val
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
        sc = SCENES[scn]; shots = plan_continuity(ALL[scn], scn)
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
                       + f"\n[IMAGE PROMPT - ChatGPT or Google Flow]\n{policy_safe(scn, image(scn, s))}\n"
                       + f"\n[VIDEO PROMPT - Grok]\n{video(scn, s)}\n")
            if voice_only(scn, s):
                txt.append("\n" + capcut_voice(scn, s) + "\n")
            elif any(parse_owner(o)[0] in ("phone", "screen", "tv") for _, o, _ in s["dialogue"]):
                txt.append("\nBACKUP if Grok still moves the listener's mouth: regenerate once. If it happens again, make this clip with DIALOGUE: NONE and add the line in CapCut (Audio > Voice effects > Telephone).\n")
        (out / f"Scene_{int(scn):02d}.txt").write_text("".join(txt))
        total += len(shots)
        print(f"scene {scn}: {len(shots)} shots")
    print("TOTAL", total)

if __name__ == "__main__":
    main()
