"""Builds the shot-by-shot image (ChatGPT) and video (Grok) prompt pack from scenes/*.txt."""
import html, pathlib, re, subprocess
HERE = pathlib.Path(__file__).parent

IMAGE_LOCK = ("DIRECTOR'S LOCK — FOLLOW EVERY RULE, NO EXCEPTIONS. "
 "1) Create ONLY what this prompt describes. Add nothing else: no extra people, objects, signs or decorations. "
 "2) FORMAT: one photorealistic still frame from a high-budget Nigerian drama feature film, wide 16:9 landscape, 35mm cinema lens, shallow depth of field. Never an illustration, painting or 3D render. "
 "3) CHARACTERS: the same people as in the attached approved images and character sheets, not lookalikes. Copy each face, hairline, hairstyle, beard, skin tone, age, height, weight and body build exactly. Never slimmer, lighter, younger or more glamorous. "
 "4) LIGHT: only from real sources in the scene (windows, lamps, sun, bulbs, candles). Match the warm, natural cinematic light and colour of the approved character images. "
 "5) GRADE: soft warm-neutral movie colour, gently muted, never oversaturated. Matte natural skin with visible pores and texture, fine film grain. NO gloss, NO shine, NO glow, NO HDR, NO airbrushing, NO plastic skin, NO bloom. "
 "6) CONTINUITY: the setting, props, wardrobe, weather and time of day are exactly as described for this scene, identical to the other shots of the scene. "
 "7) Hands have five fingers and hold objects naturally. Bodies and faces are anatomically correct. "
 "8) No readable text, logos, captions or watermarks anywhere unless this prompt gives the exact words. "
 "9) All people are fictional adults unless stated. Ordinary, respectful, non-graphic drama.")

VIDEO_LOCK = ("DIRECTOR'S ORDERS. GENERATE ONLY WHAT IS WRITTEN. ANYTHING NOT WRITTEN IS FORBIDDEN. "
 "1) ONE continuous 10-second take: no cuts, no transitions, no slow motion unless written. "
 "2) The uploaded image is frame one: do not restyle, relight, recolour or redraw it. "
 "3) Every person keeps the exact face, skin tone, hair, body size, age and clothes for all 10 seconds: no morphing, no new people, nobody leaves unless written. "
 "4) Doors, windows, curtains, props, lights and time of day never change unless written; closed doors stay closed; objects never move by themselves. "
 "5) Real-life speed and weight; five fingers on every hand; feet on the ground; no floating or sliding. "
 "6) Camera: only the move written, otherwise a locked tripod shot; always steady, no shake, no sudden zoom. "
 "7) Same muted cinematic film look as the image: soft natural light, matte skin, fine grain; no shine, glow, bloom, flares or flashing. "
 "8) Only the named speaker talks, lip-synced word for word to the written lines; no added words; everyone else silent, reacting with face and body; Nigerian English accents; each voice exactly as described. "
 "9) Clean, clear dialogue over the written ambience only: no music, no singing, no extra sound effects. "
 "10) Start at once, finish every word before 10 seconds, end on a still held moment. If anything can't be done perfectly, move LESS; never invent.")

C = {  # name, face/body lock, voice lock, body-language lock (from the script)
 "ireti": ("IRETI (23)", "slim young Nigerian woman, dark brown skin, soft round face, big expressive eyes, long black box braids pulled back into a low ponytail, small silver stud earrings, no makeup",
   "soft, warm, clear voice of a 23-year-old Yoruba-Nigerian woman, medium pitch, gentle and polite; when hurt she lowers her voice instead of raising it",
   "stands with her hands folded in front, tilts her head when listening, gives a small closed-lip smile when hurt, wipes tears away fast as if embarrassed by them"),
 "chief": ("CHIEF ADENUGA (75)", "elderly Nigerian man, very dark brown skin, deep wrinkles, short snow-white hair, full white beard, heavy-lidded tired eyes, broad but frail frame",
   "deep, slow, gravelly baritone of a 75-year-old Yoruba-Nigerian man, Yoruba accent, heavy pauses before painful words, a roar only when angry",
   "tight jaw, slow heavy movements, fingers drum the armrest when restless, turns his face away when hurt; later his shoulders relax and he laughs with his whole chest"),
 "femi": ("FEMI (33)", "tall well-built Nigerian man, dark skin, sharp low-cut fade, short neat black beard, rimless gold-framed glasses",
   "smooth, firm, educated Lagos male voice, quick and clipped when stressed, soft with his grandfather",
   "upright posture, checks his watch and phones, rubs his eyes when tired, hands on hips when frustrated"),
 "gabriel": ("GABRIEL (33)", "Nigerian man, light brown skin, short curly hair with a fade, full thick black beard, clear aviator-shaped glasses, big friendly smile",
   "warm, upbeat, friendly Igbo-Nigerian male voice, relaxed and easy", "relaxed, open hands, leans in when interested, quick easy smile"),
 "funmi": ("MAMA FUNMI (48)", "thin Nigerian woman, dark skin, thin tired face, kind eyes, wine-coloured head wrap",
   "gentle, slightly weak, warm voice of a 48-year-old Yoruba-Nigerian mother, slow and loving, sometimes breathless", "slow careful movements, a hand on her chest when she coughs, calm loving eye contact"),
 "dayo": ("DAYO (17)", "slim Nigerian teenage boy, dark skin, low haircut, bright cheeky smile",
   "lively, cheeky voice of a 17-year-old Nigerian boy, fast and playful, cracks when emotional", "restless and playful, big gestures, shoulders drop when hurt"),
 "ronke": ("AUNTY RONKE (52)", "Nigerian woman, dark brown skin, sharp cheekbones, neat makeup, cold eyes, tight black head wrap",
   "cold, crisp, controlled Nigerian female voice, precise and polite on the surface", "very upright, hands folded, smiles only with her mouth, watches people a beat too long"),
 "audu": ("MALLAM AUDU (62)", "older northern Nigerian man, dark skin, grey-white beard, kind eyes, white embroidered cap (hula)",
   "gentle, slow, Hausa-accented Nigerian male voice, warm and wise", "calm and still, holds his cap in his hands when serious, gentle nods"),
 "hassan": ("DR. HASSAN BELLO (50)", "Nigerian man, dark skin, short greying hair, neat salt-and-pepper beard, calm serious eyes",
   "calm, measured, professional Nigerian male voice, never rushed", "composed, still hands, steady eye contact"),
 "lekan": ("MR. LEKAN (58)", "heavy-set Nigerian man, dark skin, round face, receding short hair, thin moustache, gold-rimmed rectangular glasses, gold watch, gold ring",
   "smooth, oily, charming older Nigerian male voice, loud warmth that sounds rehearsed", "big friendly gestures, pats people, his smile stays while his eyes go cold"),
 "grace": ("NURSE GRACE (30)", "full-figured Nigerian woman, dark brown skin, cornrows into a low bun, small stud earrings",
   "soft, polite Nigerian female voice that trembles when hurt", "gentle and careful, straightens up slowly with dignity"),
 "okoro": ("DR. OKORO (55)", "big heavy-set Nigerian man, dark skin, greying curly hair, full grey beard, tired kind eyes",
   "tired, kind, deep Igbo-Nigerian male voice, slow and gentle", "heavy tired posture, closes the file before bad news, a gentle hand on the shoulder"),
 "jide": ("MR. JIDE (45)", "short heavy Nigerian man, dark skin, round sweaty face, short beard",
   "loud, rough, bossy Lagos male voice", "points and waves his arms, laughs at his own jokes, wipes sweat"),
 "chioma": ("CHIOMA (24)", "Nigerian woman, dark brown skin, curly hair pulled up, gold sunglasses on her head, big gold hoop earrings, always chewing gum",
   "sassy, sharp-tongued Lagos female voice", "hand on hip, chews gum loudly, rolls her eyes, hisses and storms off"),
 "segun": ("SEGUN (52)", "fit Nigerian man, brown skin, short hair, full beard with grey, serious frown",
   "busy, deep, polished Nigerian male voice that cracks when he finally feels guilt", "checks his watch, distracted, later sits back slowly in shock"),
 "kunle": ("KUNLE (48)", "big Nigerian man, dark brown skin, clean bald head, dark rectangular glasses, neat goatee",
   "flat, deep, banker's Nigerian male voice", "still and stiff, sits up straight when shocked"),
 "lola": ("LOLA (45)", "full-figured Nigerian woman, brown skin, big voluminous dark wavy hair, polished makeup, gold drop earrings",
   "soft British-Nigerian female voice", "poised, a hand to her mouth when moved"),
 "ajala": ("COMMANDER AJALA (72)", "elderly Nigerian man, dark skin, white beard, round dark sunglasses, cream fedora hat, huge joyful smile",
   "booming, joyful voice of a 72-year-old Yoruba-Nigerian musician", "big showman gestures, shades his eyes, laughs with his whole body"),
}

AMBIENCE = {"1":"rain on the windows, distant thunder, a quiet clock ticking","2":"soft heart-monitor beeps, rain on the glass, a quiet corridor hum",
 "3":"a ceiling fan whirring, soft murmurs in the ward, distant traffic","4":"restaurant chatter, pots clanging, Lagos street noise and danfo horns",
 "5":"a generator rumbling, children playing, oil sizzling","6":"night insects, soft snoring, near silence","7":"lunchtime chatter, plates and plastic chairs, a radio very low",
 "8":"city traffic and crowd murmur outside; a quiet echoing hall inside","9":"a light breeze, soft restaurant chatter, glasses clinking","10":"rain on a zinc roof dripping into a bucket; morning birds",
 "11":"a quiet office air-conditioning hum","12":"palm leaves in the breeze, a gate creaking; silence and a soft echo inside","13":"kitchen sounds; a quiet bedroom; water in a bucket at night",
 "14":"wind, thunder and rain on an umbrella","15":"a storm: rain on windows and rolling thunder","16":"soft Hausa music from a small radio, evening birds",
 "17":"juju music from the TV; a concert crowd and brass band; a car engine hum","18":"a fridge humming, a clock ticking, near silence","19":"daytime birds outside, quiet equipment beeps",
 "20":"crickets and a quiet night","21":"soft monitor beeps, morning birds","22":"birds, fountain water, a puppy barking","23":"birds, a crowd murmuring, a microphone",
 "24":"hot afternoon insects and birds","25":"footsteps echoing on marble in a big hall","26":"a quiet night house, a puppy whining","27":"a generator hum, oxygen hissing, a ceiling fan",
 "28":"an office hum, faint traffic outside","29":"rain on glass, a puppy barking","30":"a boardroom hush, a cane tapping on marble","31":"fountain water, birds, family chatter","32":"birds, a light breeze, sunset wind"}

def shot_type(sh):
    if not sh["who"]: return "SCENERY / ESTABLISHING SHOT: no main characters; the place, light and mood are the subject."
    if '"' in sh["vid"]: return "DIALOGUE SHOT: the speaker talks; listeners react silently with face and body."
    return "SILENT ACTION / AFTER-ACTION SHOT: no dialogue; the focus is the physical action and the emotional reaction on faces and bodies."

PHOTO_REFS = {  # shots that need Kehinde's photo uploaded as a prop
 "6.1": "KEHINDE photo (framed on the wall)", "6.5": "KEHINDE photo (framed on the wall)", "6.7": "KEHINDE photo (framed on the wall)",
 "27.7": "KEHINDE photo (he is the man in the green shirt)", "27.12": "KEHINDE photo (on the phone screen)"}

def parse(text):
    scenes, sc, sh = [], None, None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("=== "):
            num, title = [x.strip() for x in line[4:].split("|", 1)]
            sc = {"num": num, "title": title, "set": "", "wear": {}, "shots": []}; scenes.append(sc); sh = None
        elif line.startswith("--- "):
            sid, label = [x.strip() for x in line[4:].split("|", 1)]
            sh = {"id": sid, "label": label, "who": [], "img": "", "vid": "", "start": "New image"}; sc["shots"].append(sh)
        elif sh is None and line.startswith("SET:"): sc["set"] = line[4:].strip()
        elif sh is None and line.startswith("WEAR:"):
            for part in line[5:].split(";"):
                if "=" in part:
                    k, v = part.split("=", 1); sc["wear"][k.strip()] = v.strip()
        elif sh is not None:
            for key, field in (("WHO:", "who"), ("IMG:", "img"), ("VID:", "vid"), ("START:", "start")):
                if line.startswith(key):
                    val = line[len(key):].strip()
                    sh[field] = [w.strip() for w in val.split(",") if w.strip()] if field == "who" else val
    return scenes

def build_prompts(sc, sh, nxt=None):
    bad = [k for k in sh["who"] if k not in C]
    if bad: raise SystemExit(f"unknown character {bad} in shot {sh['id']}")
    chars = [k for k in sh["who"] if k in C]
    look = " ".join(f"{C[k][0]}: {C[k][1]}; wearing {sc['wear'].get(k, 'the outfit in the reference')}; body language: {C[k][3]}." for k in chars)
    names = ", ".join([C[k][0] for k in chars] + ([PHOTO_REFS[sh["id"]]] if sh["id"] in PHOTO_REFS else []))
    head = (f"CHARACTERS IN THIS IMAGE: {names}. I have uploaded their approved images and character sheets; they must be the same people with the same faces and body builds, not lookalikes. " if names
            else "CHARACTERS IN THIS IMAGE: none (scenery only, no main characters, no people in focus). ")
    img = (f"{head}SHOT TYPE: {shot_type(sh)} Create one image. FRAME: {sh['img']} SETTING (identical in every shot of this scene): {sc['set']}"
           + (f" CHARACTERS: {look}" if look else "") + f" {IMAGE_LOCK}")
    voices = " ".join(f"{C[k][0]}: {C[k][2]}." for k in chars)
    body = " ".join(f"{C[k][0]}: {C[k][3]}." for k in chars)
    chain_in = " This clip continues directly from the previous clip: same positions, same light, no jump." if sh["start"].lower().startswith("last frame") else ""
    chain_out = ""
    if nxt and nxt["start"].lower().startswith("last frame"):
        chain_out = f" FINAL FRAME (last 2 seconds): ease gently into and hold still on this picture, because the next clip starts from it: {nxt['img']}"
    else:
        chain_out = " FINAL FRAME (last second): hold still on a calm, clean frame with everyone in place."
    vid = (f"LENGTH: exactly 10 seconds. SHOT TYPE: {shot_type(sh)} FIRST FRAME: the uploaded image ({sh['img']}) ACTION: {sh['vid']}{chain_in}{chain_out}"
           + (f" VOICES (keep identical in every clip): {voices}" if voices else "")
           + (f" BODY LANGUAGE: {body}" if body else "")
           + f" LOCATION: stay exactly in the place shown in the image. SOUND: clean, clear dialogue over {AMBIENCE.get(sc['num'], 'quiet natural ambience')}; no music. {VIDEO_LOCK}")
    return img, vid

def main():
    scenes = []
    for f in sorted((HERE / "scenes").glob("*.txt")):
        scenes += parse(f.read_text())
    e = html.escape
    total = sum(len(s["shots"]) for s in scenes)
    txt = []
    toc = "".join(f'<li><a href="#s{s["num"]}">Scene {s["num"]}: {e(s["title"])}</a> <span>· {len(s["shots"])} shots</span></li>' for s in scenes)
    body = []
    checklist = []
    for s in scenes:
        sc_chars = []
        for x in s["shots"]:
            for k in x["who"]:
                if k in C and k not in sc_chars: sc_chars.append(k)
        upl = ", ".join([C[k][0] for k in sc_chars] + (["KEHINDE photo"] if any(x["id"] in PHOTO_REFS for x in s["shots"]) else [])) or "None"
        checklist.append(f"<tr><td><b>Scene {s['num']}</b><br>{e(s['title'])}</td><td><b>{e(upl)}</b></td><td>" + "<br>".join(f"{x['id']}: {e(', '.join([C[k][0] for k in x['who'] if k in C] + ([PHOTO_REFS[x['id']]] if x['id'] in PHOTO_REFS else [])) or 'scenery only')}" for x in s["shots"]) + "</td></tr>")
        body.append(f'<section id="s{s["num"]}"><h2>Scene {s["num"]} · {e(s["title"])}</h2><div class="upl"><b>Upload these character sheets for this scene:</b> {e(upl)}</div><div class="set"><b>Scene set (stays the same in every shot):</b> {e(s["set"])}</div>')
        txt.append(f"\n\n==================== SCENE {s['num']}: {s['title']} ====================\nUPLOAD THESE CHARACTER SHEETS: {upl}\n")
        scene_txt = [f"SCENE {s['num']}: {s['title']}\nUPLOAD THESE CHARACTER SHEETS: {upl}\nPASTE THE CHATGPT SETUP MESSAGE FIRST (see the PDF guide).\n"]
        for i, sh in enumerate(s["shots"]):
            img, vid = build_prompts(s, sh, s["shots"][i+1] if i+1 < len(s["shots"]) else None)
            scene_txt.append(f"\n--- SHOT {sh['id']} | {sh['label']} | Start: {sh['start']}\n\n[IMAGE PROMPT - ChatGPT]\n{img}\n\n[VIDEO PROMPT - Grok, 10 seconds]\n{vid}\n")
            who = ", ".join([C[k][0] for k in sh["who"] if k in C] + ([PHOTO_REFS[sh["id"]]] if sh["id"] in PHOTO_REFS else [])) or "None (scenery only)"
            body.append(f'<div class="shot"><div class="hd"><b>Shot {sh["id"]}</b> · {e(sh["label"])} <i class="ty">{e(shot_type(sh).split(":")[0])}</i><span>10 sec · Start: {e(sh["start"])} · Attach refs: {e(who)}</span></div>'
                        f'<div class="lab img">IMAGE PROMPT · ChatGPT</div><div class="p">{e(img)}</div>'
                        f'<div class="lab vid">VIDEO PROMPT · Grok (image-to-video, 10s)</div><div class="p">{e(vid)}</div></div>')
            txt.append(f"\n--- SHOT {sh['id']} | {sh['label']} | Start: {sh['start']} | Attach: {who}\n\n[IMAGE PROMPT - ChatGPT]\n{img}\n\n[VIDEO PROMPT - Grok]\n{vid}\n")
        body.append("</section>")
        (HERE / "by_scene").mkdir(exist_ok=True)
        (HERE / "by_scene" / f"Scene_{int(s['num']):02d}.txt").write_text("".join(scene_txt))
    guide = (HERE / "guide.html").read_text()
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Image and Video Prompt Pack</title><style>
@page{{size:A4;margin:11mm}} body{{font-family:Arial,Helvetica,sans-serif;color:#111827;font-size:9.5px;margin:0}}
.cover{{background:#111827;color:#fff;border-radius:10px;padding:20px 22px;margin-bottom:12px}} .cover h1{{margin:4px 0;font-size:22px}}
.cover .k{{color:#f59e0b;letter-spacing:2px;font-size:10px;font-weight:bold}} .cover p{{margin:2px 0;color:#d1d5db;font-size:11px}}
h2{{font-size:14px;border-bottom:3px solid #f59e0b;padding-bottom:3px;margin:16px 0 6px;break-after:avoid}} h3{{font-size:12px;margin:12px 0 4px}}
section{{break-before:page}} .upl{{background:#dbeafe;border-radius:6px;padding:6px 8px;margin-bottom:6px;font-size:10.5px}} .set{{background:#fef3c7;border-radius:6px;padding:6px 8px;margin-bottom:8px}}
.shot{{border:1px solid #d1d5db;border-radius:7px;padding:6px 8px;margin-bottom:7px;break-inside:avoid}}
.hd{{font-size:10.5px;margin-bottom:4px}} .ty{{color:#047857;font-style:normal;font-size:9px;font-weight:bold}} .hd span{{float:right;color:#6b7280;font-size:9px}}
.lab{{font-weight:bold;font-size:8.5px;letter-spacing:1px;margin-top:4px}} .img{{color:#1d4ed8}} .vid{{color:#b45309}}
.p{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:5px;padding:5px 6px;line-height:1.4;white-space:pre-wrap}}
ol.toc{{columns:2;font-size:10px;padding-left:18px}} ol.toc span{{color:#6b7280}} a{{color:#111827;text-decoration:none}}
.lock{{background:#f3f4f6;border-left:4px solid #111827;padding:6px 9px;white-space:pre-wrap;line-height:1.45;margin:4px 0 8px}}
table{{border-collapse:collapse;width:100%;font-size:9.5px}} td,th{{border:1px solid #d1d5db;padding:3px 5px;text-align:left;vertical-align:top}}
</style></head><body>
<div class="cover"><div class="k">SHOT-BY-SHOT PROMPT PACK</div><h1>A Poor Girl Helped a Billionaire CEO Grandpa Walk Again</h1>
<p>{len(scenes)} scenes · {total} shots · every shot has an image prompt (ChatGPT) and a 10-second video prompt (Grok)</p></div>
{guide.replace("{{IMAGE_LOCK}}", e(IMAGE_LOCK)).replace("{{VIDEO_LOCK}}", e(VIDEO_LOCK)).replace("{{CAST}}", "".join(f"<tr><td><b>{e(v[0])}</b></td><td>{e(v[1])}<br><i>Body language: {e(v[3])}</i></td><td>{e(v[2])}</td></tr>" for v in C.values()))}
<h2>Scenes</h2><ol class="toc">{toc}</ol>
<section><h2>Character upload checklist</h2><p>Which character sheets to upload for each scene, and who is in each shot.</p><table><tr><th style="width:20%">Scene</th><th style="width:28%">Upload for this scene</th><th>Characters in each shot</th></tr>{"".join(checklist)}</table></section>
{"".join(body)}</body></html>'''
    (HERE / "prompt_pack.html").write_text(page)
    (HERE / "All_Prompts_copy_paste.txt").write_text("IMAGE + VIDEO PROMPTS — A Poor Girl Helped a Billionaire CEO Grandpa Walk Again\n" + "".join(txt))
    print(len(scenes), "scenes", total, "shots")

if __name__ == "__main__":
    main()
