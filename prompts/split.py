"""Turns each written shot into clips with ONE speaker each, so Grok never has to guess who is talking.
Lines spoken by someone who is not on screen (phone, TV, voice-over, video-call screens) become silent
reaction clips; the voice line is added in editing."""
import re

KEYS = [("mama funmi", "funmi"), ("funmi", "funmi"), ("mallam audu", "audu"), ("audu", "audu"), ("hassan", "hassan"),
        ("okoro", "okoro"), ("jide", "jide"), ("chioma", "chioma"), ("ireti", "ireti"), ("chief", "chief"), ("femi", "femi"),
        ("gabriel", "gabriel"), ("dayo", "dayo"), ("ronke", "ronke"), ("lekan", "lekan"), ("grace", "grace"), ("segun", "segun"),
        ("kunle", "kunle"), ("lola", "lola"), ("ajala", "ajala")]
EXTRAS = {"physio": "the physiotherapist", "panelist": "the female panelist at the table", "security man": "the security man in uniform",
          "young man": "the young man standing in the crowd", "twin": "the twelve-year-old twin boy", "woman in the suit": "the woman in the sharp suit", "newsreader": "the TV newsreader"}
OFF = re.compile(r"'s (?:\w+ )?voice|voice (?:on|from|comes|echoes)|recorded voice|off-screen|on screen|on the screen|from the tv|recorded|^on the phone|newsreader", re.I)
TAG = re.compile(r'(?:(?<=^)|(?<=[.!?…"\)]\s))([A-Z][^":.!?]{0,90}?):\s*"')

# a few tags with no name in them
PRONOUN_FIX = {("13.5", "He slaps her hand away"): "chief", ("7.2", "He covers the phone"): "gabriel", ("7.2", "Back to the phone"): "gabriel"}

def who_is(tag, shot, prev):
    t = tag.lower()
    hits = [(m.start(), v) for k, v in KEYS for m in [re.search(r"\b" + k + r"\b", t)] if m]
    if hits:
        return min(hits)[1]  # the name that comes first in the tag is the speaker
    for k, v in EXTRAS.items():
        if k in t:
            return "x:" + v
    if (shot["id"], tag) in PRONOUN_FIX:
        return PRONOUN_FIX[(shot["id"], tag)]
    if prev:
        return prev
    return shot["who"][0] if shot["who"] else "x:a person"

def turns(shot):
    vid = shot["vid"]
    ms = list(TAG.finditer(vid))
    if not ms:
        return vid, []
    pre = vid[:ms[0].start()].strip()
    out, prev = [], None
    for i, m in enumerate(ms):
        seg = vid[m.start(): ms[i + 1].start() if i + 1 < len(ms) else len(vid)].strip()
        tag = m.group(1)
        spk = who_is(tag, shot, prev)
        off = bool(OFF.search(tag)) or (not spk.startswith("x:") and spk not in shot["who"])
        if spk == "segun" and re.search(r"phone|screen", tag, re.I):
            off = True
        out.append({"spk": spk, "off": off, "seg": seg, "lines": re.findall(r'"([^"]*)"', seg)})
        prev = spk
    # merge consecutive turns of the same speaker / same on-off state
    merged = []
    for t in out:
        if merged and merged[-1]["spk"] == t["spk"] and merged[-1]["off"] == t["off"]:
            merged[-1]["seg"] += " " + t["seg"]; merged[-1]["lines"] += t["lines"]
        elif merged and t["off"] and merged[-1]["off"]:
            merged[-1]["seg"] += " " + t["seg"]; merged[-1]["pairs"].append((t["spk"], " ".join(t["lines"])))
        else:
            d = dict(t); d["pairs"] = [(t["spk"], " ".join(t["lines"]))]; merged.append(d)
    for m in merged:  # same-speaker merges must update pairs too
        if m["off"] and len(m["pairs"]) == 1: m["pairs"] = [(m["spk"], " ".join(m["lines"]))]
    return pre, merged

def strip_quotes(text):
    text = re.sub(r'(?:(?<=^)|(?<=[.!?…"\)]\s))[A-Z][^":.!?]{0,90}?:\s*"[^"]*"', "", text)
    text = re.sub(r'"[^"]*"', "", text)
    return re.sub(r"\s+", " ", text).strip()

def expand(scene, C, VIS):
    clips = []
    rename = {}
    for sh in scene["shots"]:
        pre, ts = turns(sh)
        if len(ts) <= 1 and not (ts and ts[0]["off"]):
            c = dict(sh); c["mode"] = "speak" if ts else "silent"
            c["speaker"] = ts[0]["spk"] if ts else None
            c["lines"] = ts[0]["lines"] if ts else []
            c["offlines"] = []
            clips.append(c); rename[sh["id"]] = sh["id"]
            continue
        for i, t in enumerate(ts):
            one = len(ts) == 1
            c = {"id": sh["id"] if one else f"{sh['id']}.{i+1}", "label": sh["label"] if one else f"{sh['label']} (part {i+1} of {len(ts)})", "who": list(sh["who"]),
                 "start": sh["start"] if i == 0 else "New image", "offlines": [], "lines": []}
            action = (pre + " " if i == 0 and pre else "")
            if t["off"]:
                listeners = [k for k in sh["who"] if k in C and k != t["spk"]]
                c["mode"] = "silent"; c["speaker"] = None
                c["img"] = sh["img"] if i == 0 else (f"Same moment, same place and same light as before: {sh['img']} " +
                           (f"FRAMING FOR THIS SHOT: medium close-up on {', '.join(C[k][0] for k in listeners)} listening, face fully visible." if listeners else ""))
                c["vid"] = (action + strip_quotes(t["seg"]) + (" The people on screen listen silently and react only with their faces and bodies." if listeners else "")).strip()
                c["offlines"] = [(C[n][0] if n in C else n.replace("x:", "").upper(), l) for n, l in t["pairs"] if l]
            else:
                spk = t["spk"]; c["mode"] = "speak"; c["speaker"] = spk; c["lines"] = t["lines"]
                if spk.startswith("x:"):
                    sname, svis = spk[2:], spk[2:]
                else:
                    sname, svis = C[spk][0], VIS[spk]
                others = [k for k in sh["who"] if k in C and k != spk]
                c["img"] = (f"Same moment, same place and same light as before: {sh['img']} FRAMING FOR THIS SHOT: medium close-up favouring {sname} ({svis}) who is speaking, "
                            f"face fully visible, turned toward the camera at a slight angle, lit only by the scene's own light"
                            + (f"; {', '.join(C[k][0] for k in others)} softly out of focus at the edge of the frame, listening." if others else "."))
                c["vid"] = action + t["seg"]
            clips.append(c)
        rename[sh["id"]] = clips[-1]["id"]
    for c in clips:  # keep "last frame of X" pointing at the right clip
        m = re.match(r"last frame of (\S+)", c["start"], re.I)
        if m and m.group(1) in rename:
            c["start"] = f"Last frame of {rename[m.group(1)]}"
    return clips
