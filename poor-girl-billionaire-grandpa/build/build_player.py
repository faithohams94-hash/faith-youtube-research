"""Build player.html (the interactive movie player) from script.md.

Run from the repo root:  python3 poor-girl-billionaire-grandpa/build/build_player.py
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = (ROOT / "script.md").read_text(encoding="utf-8")
TEMPLATE = (HERE / "player-template.html").read_text(encoding="utf-8")
OUT = ROOT / "player.html"


def inline(text):
    """Escape, then turn the script's markdown into HTML."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*\((.+?)\)\*", r'<em class="p">(\1)</em>', t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t


def strip_outer(text):
    text = text.strip()
    if text.startswith("*") and text.endswith("*") and not text.startswith("**"):
        return text[1:-1].strip()
    return text


def speakable(text):
    t = re.sub(r"\*\([^)]*\)\*", " ", text)        # parentheticals are not spoken
    t = re.sub(r"\([^)]*\)", " ", t)
    t = t.replace("*", "")
    t = re.sub(r"₦([\d.,]+)\s*(million|thousand|billion)?",
               lambda m: f"{m.group(1)} {m.group(2) or ''} naira", t)
    t = t.replace("—", ", ").replace("…", "... ")
    return re.sub(r"\s+", " ", t).strip()


# ---------- cast lookup used for colours, voices and "appears in" ----------
CAST_KEYS = ["MAMA FUNMI", "MALLAM AUDU", "DR. HASSAN", "IRETI", "CHIEF", "FEMI",
             "GABRIEL", "DAYO", "RONKE", "LEKAN"]
VOICES = {  # speaker: (gender, pitch)
    "IRETI": ("f", 1.1), "CHIEF": ("m", 0.72), "FEMI": ("m", 0.95), "GABRIEL": ("m", 1.05),
    "MAMA FUNMI": ("f", 0.9), "DAYO": ("m", 1.3), "RONKE": ("f", 0.82), "MALLAM AUDU": ("m", 0.7),
    "DR. HASSAN": ("m", 0.85), "LEKAN": ("m", 0.8), "GRACE": ("f", 1.0), "DR. OKORO": ("m", 0.8),
    "MR. JIDE": ("m", 0.9), "CHIOMA": ("f", 1.15), "SEGUN": ("m", 0.85), "KUNLE": ("m", 0.95),
    "LOLA": ("f", 1.0), "COMMANDER AJALA": ("m", 0.7), "NURSE": ("f", 1.05),
    "WOMAN IN QUEUE": ("f", 1.1), "SECURITY MAN": ("m", 0.85), "PANELIST": ("f", 0.95),
    "NEWSREADER": ("f", 1.0), "PHYSIO": ("m", 1.0), "YOUNG MAN": ("m", 1.15), "TWIN": ("m", 1.45),
    "OFFICER": ("m", 0.8),
}


def cast_key(who):
    for k in CAST_KEYS:
        if who == k or who.startswith(k + " ") or who.startswith(k):
            return k
    return None


def voice(who):
    k = cast_key(who) or who
    for name, v in VOICES.items():
        if k.startswith(name):
            return v
    return ("m", 1.0)


# ---------- scenes ----------
SECTION_OF = {"COLD OPEN": "cold", "ACT ONE": "act1", "ACT TWO": "act2",
              "CLIMAX": "climax", "ENDING": "ending"}
scenes, cur, section, pending = [], None, None, None
for raw in SRC.split("\n"):
    s = raw.strip()
    if s.startswith("## RUNTIME MAP"):
        break
    if s.startswith("# "):
        for name, key in SECTION_OF.items():
            if s[2:].startswith(name):
                section = key
        continue
    m = re.match(r"^## SCENE (\d+): (.+)$", s)
    if m:
        cur = {"n": int(m.group(1)), "title": m.group(2).strip(), "slug": "", "time": ["", ""],
               "section": section, "lines": []}
        scenes.append(cur)
        pending = None
        continue
    if cur is None or not s or s == "---":
        continue
    if pending is not None and s.startswith("*") and not s.startswith("**"):
        add = strip_outer(s)
        pending["html"] += ("<br>" if pending["html"] else "") + inline(add)
        pending["say"] = (pending["say"] + " " + speakable(add)).strip()
        continue
    pending = None
    L = cur["lines"]
    if m := re.match(r"^\*\*((?:INT|EXT)[^*]+)\*\*$", s):
        cur["slug"] = m.group(1).strip()
    elif m := re.match(r"^\*\((\d+:\d\d)[–-](\d+:\d\d)\)\*$", s):
        cur["time"] = [m.group(1), m.group(2)]
    elif m := re.match(r"^\*\*(ESTABLISH|AFTERMATH):\*\*\s*(.*)$", s):
        body = strip_outer(m.group(2))
        L.append({"t": m.group(1).lower(), "html": inline(body), "say": speakable(body)})
    elif m := re.match(r"^\*\*ON SCREEN \(([^)]*)\):\*\*\s*(.*)$", s):
        body = strip_outer(m.group(2))
        ln = {"t": "screen", "label": m.group(1), "html": inline(body), "say": speakable(body)}
        L.append(ln)
        if not body:
            pending = ln
    elif m := re.match(r"^\*(FADE[^*]*)\*$", s):
        L.append({"t": "fade", "html": inline(m.group(1)), "say": ""})
    elif m := re.match(r"^\*\*([^*:]+?):\*\*\s*(.*)$", s):
        who, tag = m.group(1).strip(), ""
        if mm := re.match(r"^(.*?)\s*\((.+)\)$", who):
            who, tag = mm.group(1).strip(), mm.group(2)
        g, p = voice(who)
        L.append({"t": "dialogue", "who": who, "tag": tag, "k": cast_key(who), "g": g, "p": p,
                  "html": inline(m.group(2)), "say": speakable(m.group(2))})
    else:
        body = strip_outer(s[2:] if s.startswith("- ") else s)
        L.append({"t": "action", "html": inline(body), "say": speakable(body)})

assert len(scenes) == 32, len(scenes)

# ---------- character bible ----------
bible = SRC[SRC.index("# CHARACTER BIBLE"):SRC.index("## KEY LOCATIONS")]
cast = []
for block in re.split(r"\n### ", bible)[1:]:
    head = block.split("\n", 1)[0].strip()
    if head.startswith("SUPPORTING"):
        continue
    m = re.match(r"(.+?) \((\d+)\), (.+)", head)
    name, age, role = m.group(1), m.group(2), m.group(3)
    f = dict(re.findall(r"\*\*(Who (?:she|he) is|Body language|AI prompt|Wardrobe):\*\*\s*(.+)", block))
    key = cast_key(name.replace("CHIEF BABATUNDE ADENUGA", "CHIEF").replace("AUNTY ", "")
                   .replace("MR. ", "").replace("DR. HASSAN BELLO", "DR. HASSAN"))
    cast.append({
        "key": key, "name": name.title().replace("Dr. ", "Dr. "), "age": age, "role": role,
        "who": inline(f.get("Who she is") or f.get("Who he is") or ""),
        "body": inline(f.get("Body language", "")),
        "wardrobe": inline(f.get("Wardrobe", "")),
        "prompt": strip_outer(f.get("AI prompt", "")),
        "scenes": sorted({sc["n"] for sc in scenes for ln in sc["lines"] if ln.get("k") == key}),
    })
support = []
sup_block = bible[bible.index("### SUPPORTING CAST"):]
for m in re.finditer(r"^- \*\*(.+?)\*\*\s*(.*)$", sup_block, re.M):
    support.append({"name": m.group(1).rstrip(".").title(), "desc": inline(m.group(2).lstrip(". "))})

loc_block = SRC[SRC.index("## KEY LOCATIONS"):SRC.index("## CURIOSITY MAP")]
locations = [{"name": m.group(1), "desc": m.group(2).strip()}
             for m in re.finditer(r"^- \*\*(.+?):\*\*\s*(.*)$", loc_block, re.M)]

logline = SRC.split("## LOGLINE", 1)[1].split("##", 1)[0].strip()
contradiction = re.search(r"\*\*(The man who has everything.+?)\*\*", SRC).group(1)

# ---------- story shape ----------
SECTIONS = [
    {"key": "cold", "name": "Cold open", "beat": "Cold open on the conflict",
     "desc": "A billionaire falls down 22 steps. No slow build-up.", "color": "#e0402f", "dot": 1},
    {"key": "act1", "name": "Act 1", "beat": "Set the contradiction",
     "desc": "The man who has everything has given up. The girl who has nothing refuses to.",
     "color": "#ec5e2b", "dot": 3},
    {"key": "act2", "name": "Act 2", "beat": "Escalate in rounds",
     "desc": "Soup, rain, a concert, a blue tablet, a necklace. Every round has an aftermath.",
     "color": "#f08327", "dot": 12},
    {"key": "climax", "name": "Climax", "beat": "The reveal",
     "desc": "He walks into the boardroom at the worst possible moment for Lekan.",
     "color": "#f2a92e", "dot": 30},
    {"key": "ending", "name": "Ending", "beat": "Payoff + lesson",
     "desc": "The children come home. Hope is a person who refuses to leave.",
     "color": "#f2c75a", "dot": 31},
]
TENSION = [30, 26, 32, 30, 34, 36, 38, 40, 42, 44, 46, 50, 52, 54, 58, 56, 58, 64, 66, 68,
           62, 60, 64, 76, 86, 84, 88, 86, 90, 100, 72, 62]
HOPE = [12, 4, 6, 8, 18, 14, 28, 22, 30, 42, 50, 18, 22, 26, 24, 36, 55, 45, 40, 62,
        68, 78, 84, 58, 10, 30, 72, 78, 88, 95, 100, 100]

POLLS = [
    {"id": "tablet", "at": 1, "rev": 24, "q": "Chief swallowed a small blue tablet just before he fell. What is it really?",
     "o": ["Blood-pressure medicine, like Ronke said", "A sedative someone is slipping him", "Vitamins", "Painkillers"], "a": 1,
     "why": "Dr. Hassan's lab test: a strong sedative mixed with a drug that crashes blood pressure. It's why he was dizzy, and why he fell."},
    {"id": "money", "at": 3, "rev": 27, "q": "Ireti needs ₦38 million in one year. How does her mother's surgery get paid?",
     "o": ["She saves every naira herself", "Someone her family once helped pays it back", "A loan from the restaurant", "It never gets paid"], "a": 1,
     "why": "Chief pays. Her father pulled him out of a burning car in 2010. “Sixteen years ago, your father paid in advance.”"},
    {"id": "card", "at": 7, "rev": 9, "q": "Gabriel gave Ireti his card. How does she get the job?",
     "o": ["She wows the interview panel", "Gabriel vouches for her to Femi", "Chief picks her himself", "She doesn't get it"], "a": 1,
     "why": "The panel laughed at her. Gabriel told Femi over lunch: “I know a good girl when I see one.”"},
    {"id": "month", "at": 12, "rev": 25, "q": "Aunty Ronke promised Ireti would be gone within a month. What happens?",
     "o": ["Chief fires her", "Ireti quits", "Someone else throws her out", "Nobody can get rid of her"], "a": 2,
     "why": "Ronke planted Mama Abike's necklace in Ireti's bag, and Femi threw her out."},
    {"id": "kehinde", "at": 15, "rev": 27, "q": "Who is the “Kehinde” in the burnt shirt on Chief's wall?",
     "o": ["Chief's lost son", "His old driver", "Ireti's father", "A business partner who died"], "a": 2,
     "why": "Kehinde Alade, a danfo driver, pulled Chief from a burning Mercedes on the Ibadan expressway and ran. He couldn't read the newspaper adverts."},
    {"id": "lekan", "at": 18, "rev": 26, "q": "Aunty Ronke reports to “LEKAN B.” What is the plan?",
     "o": ["Steal Mama Abike's jewellery", "Keep Chief weak until the AGM so Lekan takes his shares", "Get Femi married off", "Sell the mansion"], "a": 1,
     "why": "“Keep you weak, keep you sad, until the AGM, so the doctors would sign that you're not fit.” He promised her a house in Lekki."},
    {"id": "surgery", "at": 19, "rev": 20, "q": "Chief refuses the surgery that could make him walk. What changes his mind?",
     "o": ["Femi begs him", "Ireti tells him the truth about her mother", "His children call", "The doctor scares him"], "a": 1,
     "why": "“I came for the money, sir. But I stay for you.” His condition: hers is the first face he sees when he wakes."},
    {"id": "truth", "at": 25, "rev": 26, "q": "Chief turned his face away from Ireti. Who brings out the truth?",
     "o": ["Femi", "Mallam Audu, the gateman", "Gabriel", "Aunty Ronke feels guilty"], "a": 1,
     "why": "Audu came upstairs for the first time in thirty years. Then Dr. Hassan arrived with the lab report Ireti left for Chief."},
    {"id": "children", "at": 28, "rev": 31, "q": "Chief's children said “let us come ourselves.” Will they?",
     "o": ["Yes, all three, on a Sunday", "Only Segun", "They send another gift", "They come to the AGM only"], "a": 0,
     "why": "Three cars on a Sunday. Eleven people in the driveway. He walked down the 22 steps that broke him to meet them."},
    {"id": "femi", "at": 29, "rev": 30, "q": "Chief is hiding his first steps from Femi. Where will Femi find out?",
     "o": ["At home that night", "On the news", "In the boardroom, in front of Lekan", "At the family dinner"], "a": 2,
     "why": "Tap. Tap. Tap. Chief walked the length of the boardroom alone. Femi could only say “Grandpa.”"},
]

data = {
    "title": "A Poor Girl Helped a Billionaire CEO Grandpa Walk Again",
    "logline": inline(logline), "contradiction": contradiction,
    "sections": SECTIONS, "tension": TENSION, "hope": HOPE, "polls": POLLS,
    "scenes": scenes, "cast": cast, "support": support, "locations": locations,
}
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
OUT.write_text(TEMPLATE.replace("__DATA__", blob), encoding="utf-8")
print(f"wrote {OUT} · {len(scenes)} scenes · {sum(len(s['lines']) for s in scenes)} lines · {len(cast)} cast")
