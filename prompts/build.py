"""Builds the shot-by-shot image (ChatGPT) and video (Grok) prompt pack from scenes/*.txt."""
import html, pathlib, re, subprocess
from split import expand
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

VIDEO_LOCK = ("ORDERS, NO EXCEPTIONS: generate ONLY what is written; anything not written is forbidden. "
 "1) One continuous 10-second take, no cuts. 2) Frame one is the uploaded image; never restyle or redraw it. "
 "3) Every face stays exactly the same person for all 10 seconds: no morphing, no new faces, no new people. A face hidden in the image (back turned, shadow, out of frame) stays hidden: that person never turns to the camera. "
 "4) Keep the exact brightness, darkness, contrast and colour of the image to the last frame: never brighten, never add light, shadows stay dark. "
 "5) Doors, curtains, props and lights never change unless written; closed doors stay closed. "
 "6) Real-life speed; five fingers per hand; feet on the ground. 7) Camera only as written, else locked tripod; no shake, no zoom. "
 "8) Muted film look, matte skin; no shine, glow, bloom or flares. "
 "9) Only the ONE named speaker talks, word for word; all other lips stay closed. If NOBODY SPEAKS is written, there is no talking at all. "
 "10) No music, no singing, no extra sounds. 11) Finish every word before 10 seconds; end on a still moment. If unsure, move LESS; never invent.")

C = {  # name, face/body lock, voice lock, body-language lock (from the script)
 "ireti": ("IRETI (23)", "slim young Nigerian woman, dark brown skin, soft round face, big expressive eyes, long black box braids pulled back into a low ponytail, small silver stud earrings, no makeup",
   "young woman, 23: soft, clear, medium-high pitch, warm Yoruba-Nigerian accent, gentle steady pace; she gets quieter, not louder, when hurt",
   "stands with her hands folded in front, tilts her head when listening, gives a small closed-lip smile when hurt, wipes tears away fast as if embarrassed by them"),
 "chief": ("CHIEF ADENUGA (75)", "elderly Nigerian man, very dark brown skin, deep wrinkles, short snow-white hair, full white beard, heavy-lidded tired eyes, broad but frail frame",
   "old man, 75: very deep, slow, gravelly bass, strong Yoruba-Nigerian accent, long heavy pauses; booming only when angry",
   "tight jaw, slow heavy movements, fingers drum the armrest when restless, turns his face away when hurt; later his shoulders relax and he laughs with his whole chest"),
 "femi": ("FEMI (33)", "tall well-built Nigerian man, dark skin, sharp low-cut fade, short neat black beard, rimless gold-framed glasses",
   "man, 33: smooth, clear baritone, polished Lagos-Nigerian accent with a light British-educated touch, quick and precise",
   "upright posture, checks his watch and phones, rubs his eyes when tired, hands on hips when frustrated"),
 "gabriel": ("GABRIEL (33)", "Nigerian man, light brown skin, short curly hair with a fade, full thick black beard, clear aviator-shaped glasses, big friendly smile",
   "man, 33: bright, warm tenor, relaxed Igbo-Nigerian accent, easy smiling delivery with a light laugh in his voice", "relaxed, open hands, leans in when interested, quick easy smile"),
 "funmi": ("MAMA FUNMI (48)", "thin Nigerian woman, dark skin, thin tired face, kind eyes, wine-coloured head wrap",
   "woman, 48: soft, low, slightly breathy and weak, Yoruba-Nigerian accent, slow and loving", "slow careful movements, a hand on her chest when she coughs, calm loving eye contact"),
 "dayo": ("DAYO (17)", "slim Nigerian teenage boy, dark skin, low haircut, bright cheeky smile",
   "boy, 17: light, energetic teenage voice that sometimes cracks, Lagos street Nigerian accent, fast and playful", "restless and playful, big gestures, shoulders drop when hurt"),
 "ronke": ("AUNTY RONKE (52)", "Nigerian woman, dark brown skin, sharp cheekbones, neat makeup, cold eyes, tight black head wrap",
   "woman, 52: low, crisp, cold alto, clipped Yoruba-Nigerian accent, every word precise and controlled", "very upright, hands folded, smiles only with her mouth, watches people a beat too long"),
 "audu": ("MALLAM AUDU (62)", "older northern Nigerian man, dark skin, grey-white beard, kind eyes, white embroidered cap (hula)",
   "man, 62: soft, warm, husky, strong Hausa-Nigerian accent, slow and gentle", "calm and still, holds his cap in his hands when serious, gentle nods"),
 "hassan": ("DR. HASSAN BELLO (50)", "Nigerian man, dark skin, short greying hair, neat salt-and-pepper beard, calm serious eyes",
   "man, 50: calm, even, mid-low baritone, northern (Hausa) Nigerian accent, measured and never rushed", "composed, still hands, steady eye contact"),
 "lekan": ("MR. LEKAN (58)", "heavy-set Nigerian man, dark skin, round face, receding short hair, thin moustache, gold-rimmed rectangular glasses, gold watch, gold ring",
   "man, 58: rich, oily, booming baritone, Yoruba-Nigerian accent, over-friendly and theatrical", "big friendly gestures, pats people, his smile stays while his eyes go cold"),
 "grace": ("NURSE GRACE (30)", "full-figured Nigerian woman, dark brown skin, cornrows into a low bun, small stud earrings",
   "woman, 30: gentle, polite, mid-pitch, Nigerian accent, trembling when hurt", "gentle and careful, straightens up slowly with dignity"),
 "okoro": ("DR. OKORO (55)", "big heavy-set Nigerian man, dark skin, greying curly hair, full grey beard, tired kind eyes",
   "man, 55: deep, tired, gravelly, Igbo-Nigerian accent, slow and kind", "heavy tired posture, closes the file before bad news, a gentle hand on the shoulder"),
 "jide": ("MR. JIDE (45)", "short heavy Nigerian man, dark skin, round sweaty face, short beard",
   "man, 45: loud, rough, raspy, heavy Lagos Nigerian accent with a pidgin flavour, fast and shouting", "points and waves his arms, laughs at his own jokes, wipes sweat"),
 "chioma": ("CHIOMA (24)", "Nigerian woman, dark brown skin, curly hair pulled up, gold sunglasses on her head, big gold hoop earrings, always chewing gum",
   "woman, 24: sharp, slightly nasal, sassy, Igbo-Lagos Nigerian accent, fast, with gum-chewing sounds", "hand on hip, chews gum loudly, rolls her eyes, hisses and storms off"),
 "segun": ("SEGUN (52)", "fit Nigerian man, brown skin, short hair, full beard with grey, serious frown",
   "man, 52: deep, hurried corporate baritone, polished Nigerian accent, always rushing", "checks his watch, distracted, later sits back slowly in shock"),
 "kunle": ("KUNLE (48)", "big Nigerian man, dark brown skin, clean bald head, dark rectangular glasses, neat goatee",
   "man, 48: flat, low, monotone bass, Nigerian accent, slow banker's delivery", "still and stiff, sits up straight when shocked"),
 "lola": ("LOLA (45)", "full-figured Nigerian woman, brown skin, big voluminous dark wavy hair, polished makeup, gold drop earrings",
   "woman, 45: soft, refined, British-Nigerian (London) accent, gentle", "poised, a hand to her mouth when moved"),
 "ajala": ("COMMANDER AJALA (72)", "elderly Nigerian man, dark skin, white beard, round dark sunglasses, cream fedora hat, huge joyful smile",
   "man, 72: huge, booming, joyful, musical voice, Yoruba-Nigerian accent, a showman's rhythm", "big showman gestures, shades his eyes, laughs with his whole body"),
}

VIS = {"ireti":"the young woman with long black braids in a low ponytail","chief":"the elderly man with snow-white hair and a full white beard",
 "femi":"the man with a low fade, short black beard and rimless gold glasses","gabriel":"the man with curly hair, a full thick beard and clear aviator glasses",
 "funmi":"the thin woman in a wine-coloured head wrap","dayo":"the slim teenage boy with a low haircut","ronke":"the woman in a tight black head wrap and white collar",
 "audu":"the older man with a grey-white beard and a white cap","hassan":"the doctor with greying hair and a salt-and-pepper beard",
 "lekan":"the heavy-set man with gold-rimmed glasses and a thin moustache","grace":"the full-figured nurse in navy scrubs with cornrows in a bun",
 "okoro":"the big heavy-set doctor with a full grey beard","jide":"the short heavy sweaty man in a maroon polo shirt","chioma":"the woman with curly hair up, gold sunglasses on her head and big hoop earrings",
 "segun":"the man with a grey-flecked full beard in a charcoal suit","kunle":"the bald man with dark rectangular glasses and a goatee",
 "lola":"the woman with big voluminous wavy hair and gold earrings","ajala":"the elderly man in a cream fedora and round dark sunglasses"}

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


def base(i):
    return '.'.join(i.split('.')[:2])

def shot_type(c):
    if not c["who"] and c.get("mode") != "speak": return "SCENERY / ESTABLISHING SHOT: no main characters; the place, light and mood are the subject."
    if c.get("mode") == "speak": return "DIALOGUE SHOT: ONE person speaks; anyone else listens silently and reacts."
    return "SILENT ACTION / AFTER-ACTION SHOT: nobody speaks; the focus is the physical action and the emotional reaction."

def build_prompts(sc, c, nxt=None):
    bad = [k for k in c["who"] if k not in C]
    if bad: raise SystemExit(f"unknown character {bad} in shot {c['id']}")
    chars = [k for k in c["who"] if k in C]
    look = " ".join(f"{C[k][0]}: {C[k][1]}; wearing {sc['wear'].get(k, 'the outfit in the reference')}; body language: {C[k][3]}." for k in chars)
    names = ", ".join([C[k][0] for k in chars] + ([PHOTO_REFS[base(c["id"])]] if base(c["id"]) in PHOTO_REFS else []))
    head = (f"CHARACTERS IN THIS IMAGE: {names}. I have uploaded their approved images and character sheets; they must be the same people with the same faces and body builds, not lookalikes. " if names
            else "CHARACTERS IN THIS IMAGE: none (scenery only, no main characters, no people in focus). ")
    img = (f"{head}SHOT TYPE: {shot_type(c)} Create one image. FRAME: {c['img']} SETTING (identical in every shot of this scene): {sc['set']}"
           + (f" CHARACTERS: {look}" if look else "") + f" {IMAGE_LOCK}")
    # ---- video
    cast = " ".join(f"{C[k][0]} = {VIS[k]}, wearing {sc['wear'].get(k, 'the same clothes as in the image')}." for k in chars)
    action = re.sub(r'"[^"]*"', "(says the line above)", c["vid"]) if c["mode"] == "speak" else c["vid"]
    if c["mode"] == "speak":
        spk = c["speaker"]
        if spk.startswith("x:"):
            sname, svis, svoice, sbody = spk[2:].upper(), spk[2:], "a natural Nigerian voice, different from every other character", ""
        else:
            sname, svis, svoice, sbody = C[spk][0], VIS[spk], C[spk][2], C[spk][3]
        listeners = [C[k][0] for k in chars if k != spk]
        lines = " ".join(c["lines"])
        speech = (f"SPEAKER: ONLY {sname} ({svis}) speaks in this clip. Only {sname}'s lips move. "
                  f"{sname} SAYS, word for word, nothing added, nothing changed: \"{lines}\" "
                  f"{sname}'S VOICE: {svoice}. "
                  + (f"EVERYONE ELSE ({', '.join(listeners)}) is completely silent with lips closed for all 10 seconds; they only listen and react. " if listeners else "Nobody else speaks. ")
                  + (f"BODY LANGUAGE: {sbody.split(';')[0]}. " if sbody else ""))
    else:
        speech = "SPEECH: NOBODY SPEAKS IN THIS CLIP. No voices, no talking, no whispering, no humming, no lip movement. Only the ambient sound. "
    chain_in = " This clip continues directly from the previous clip: same positions, same light, no jump." if c["start"].lower().startswith("last frame") else ""
    if nxt and nxt["start"].lower().startswith("last frame"):
        chain_out = f" FINAL FRAME (last 2 seconds): ease gently into and hold still on this picture, because the next clip starts from it: {nxt['img']}"
    else:
        chain_out = " FINAL FRAME (last 2 seconds): hold still on a calm, clean frame with everyone in place."
    vid = (f"10-SECOND CLIP. FOLLOW EVERY ORDER EXACTLY. {shot_type(c).split(':')[0]}. FIRST FRAME: the uploaded image. "
           + (f"WHO IS IN THE FRAME: {cast} " if cast else "WHO IS IN THE FRAME: no main characters. ")
           + speech + f"ACTION: {action}{chain_in}{chain_out} "
           + "MOOD: same brightness and darkness as the image; do not brighten. "
           + (f"SOUND: clean, clear dialogue over {AMBIENCE.get(sc['num'], 'quiet natural ambience')}; no music. " if c["mode"] == "speak" else f"SOUND: only {AMBIENCE.get(sc['num'], 'quiet natural ambience')}; no voices, no music. ") + VIDEO_LOCK)
    extra = ""
    for who, line in c.get("offlines", []):
        key = next((k for k in C if C[k][0] == who), None)
        extra += (f"\nADD IN EDITING (voice not on screen): {who}: \"{line}\""
                  + (f"\nVOICE CLIP PROMPT (optional, Grok): Upload {who}'s approved image. 10-SECOND CLIP. ONLY {who} ({VIS[key]}) speaks, word for word, nothing added: \"{line}\" VOICE: {C[key][2]}. Keep the face exactly as in the image, same brightness, no music. Use only the audio from this clip." if key else ""))
    return img, vid, extra

def main():
    scenes = []
    for f in sorted((HERE / "scenes").glob("*.txt")):
        scenes += parse(f.read_text())
    e = html.escape
    for sc_ in scenes:
        sc_["clips"] = expand(sc_, C, VIS)
    total = sum(len(s["clips"]) for s in scenes)
    txt = []
    toc = "".join(f'<li><a href="#s{s["num"]}">Scene {s["num"]}: {e(s["title"])}</a> <span>· {len(s["clips"])} clips</span></li>' for s in scenes)
    body = []
    checklist = []
    for s in scenes:
        sc_chars = []
        for x in s["clips"]:
            for k in x["who"]:
                if k in C and k not in sc_chars: sc_chars.append(k)
        upl = ", ".join([C[k][0] for k in sc_chars] + (["KEHINDE photo"] if any(base(x["id"]) in PHOTO_REFS for x in s["clips"]) else [])) or "None"
        checklist.append(f"<tr><td><b>Scene {s['num']}</b><br>{e(s['title'])}</td><td><b>{e(upl)}</b></td><td>" + "<br>".join(f"{x['id']}: {e(', '.join([C[k][0] for k in x['who'] if k in C] + ([PHOTO_REFS[base(x['id'])]] if base(x['id']) in PHOTO_REFS else [])) or 'scenery only')}" for x in s["clips"]) + "</td></tr>")
        body.append(f'<section id="s{s["num"]}"><h2>Scene {s["num"]} · {e(s["title"])}</h2><div class="upl"><b>Upload these character sheets for this scene:</b> {e(upl)}</div><div class="set"><b>Scene set (stays the same in every shot):</b> {e(s["set"])}</div>')
        txt.append(f"\n\n==================== SCENE {s['num']}: {s['title']} ====================\nUPLOAD THESE CHARACTER SHEETS: {upl}\n")
        scene_txt = [f"SCENE {s['num']}: {s['title']}\nUPLOAD THESE CHARACTER SHEETS: {upl}\nPASTE THE CHATGPT SETUP MESSAGE FIRST (see the PDF guide).\n"]
        clips = s["clips"]
        for i, sh in enumerate(clips):
            img, vid, extra = build_prompts(s, sh, clips[i+1] if i+1 < len(clips) else None)
            scene_txt.append(f"\n--- SHOT {sh['id']} | {sh['label']} | Start: {sh['start']}\n\n[IMAGE PROMPT - ChatGPT]\n{img}\n\n[VIDEO PROMPT - Grok, 10 seconds]\n{vid}\n{extra}\n")
            who = ", ".join([C[k][0] for k in sh["who"] if k in C] + ([PHOTO_REFS[base(sh["id"])]] if base(sh["id"]) in PHOTO_REFS else [])) or "None (scenery only)"
            body.append(f'<div class="shot"><div class="hd"><b>Shot {sh["id"]}</b> · {e(sh["label"])} <i class="ty">{e(shot_type(sh).split(":")[0])}</i><span>10 sec · Start: {e(sh["start"])} · Attach refs: {e(who)}</span></div>'
                        f'<div class="lab img">IMAGE PROMPT · ChatGPT</div><div class="p">{e(img)}</div>'
                        f'<div class="lab vid">VIDEO PROMPT · Grok (image-to-video, 10s)</div><div class="p">{e(vid)}</div>' + (f'<div class="lab ed">ADD IN EDITING</div><div class="p">{e(extra.strip())}</div>' if extra else '') + '</div>')
            txt.append(f"\n--- SHOT {sh['id']} | {sh['label']} | Start: {sh['start']} | Attach: {who}\n\n[IMAGE PROMPT - ChatGPT]\n{img}\n\n[VIDEO PROMPT - Grok]\n{vid}\n{extra}\n")
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
.lab{{font-weight:bold;font-size:8.5px;letter-spacing:1px;margin-top:4px}} .img{{color:#1d4ed8}} .ed{{color:#7c3aed}} .vid{{color:#b45309}}
.p{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:5px;padding:5px 6px;line-height:1.4;white-space:pre-wrap}}
ol.toc{{columns:2;font-size:10px;padding-left:18px}} ol.toc span{{color:#6b7280}} a{{color:#111827;text-decoration:none}}
.lock{{background:#f3f4f6;border-left:4px solid #111827;padding:6px 9px;white-space:pre-wrap;line-height:1.45;margin:4px 0 8px}}
table{{border-collapse:collapse;width:100%;font-size:9.5px}} td,th{{border:1px solid #d1d5db;padding:3px 5px;text-align:left;vertical-align:top}}
</style></head><body>
<div class="cover"><div class="k">SHOT-BY-SHOT PROMPT PACK</div><h1>A Poor Girl Helped a Billionaire CEO Grandpa Walk Again</h1>
<p>{len(scenes)} scenes · {total} clips · one speaker per clip · every clip has an image prompt (ChatGPT) and a 10-second video prompt (Grok)</p></div>
{guide.replace("{{IMAGE_LOCK}}", e(IMAGE_LOCK)).replace("{{VIDEO_LOCK}}", e(VIDEO_LOCK)).replace("{{CAST}}", "".join(f"<tr><td><b>{e(v[0])}</b></td><td>{e(v[1])}<br><i>Body language: {e(v[3])}</i></td><td>{e(v[2])}</td></tr>" for v in C.values()))}
<h2>Scenes</h2><ol class="toc">{toc}</ol>
<section><h2>Character upload checklist</h2><p>Which character sheets to upload for each scene, and who is in each shot.</p><table><tr><th style="width:20%">Scene</th><th style="width:28%">Upload for this scene</th><th>Characters in each shot</th></tr>{"".join(checklist)}</table></section>
{"".join(body)}</body></html>'''
    (HERE / "prompt_pack.html").write_text(page)
    (HERE / "guide_only.html").write_text(page.split("<section id=\"s1\">")[0] + "</body></html>")
    (HERE / "All_Prompts_copy_paste.txt").write_text("IMAGE + VIDEO PROMPTS — A Poor Girl Helped a Billionaire CEO Grandpa Walk Again\n" + "".join(txt))
    print(len(scenes), "scenes", total, "shots")

if __name__ == "__main__":
    main()
