"""Builds the shot-by-shot image (ChatGPT) and video (Grok) prompt pack from scenes/*.txt."""
import html, pathlib, re, subprocess
HERE = pathlib.Path(__file__).parent

IMAGE_LOCK = ("STRICT LOOK — do not deviate: photorealistic still frame from a high-budget Nigerian drama film, wide 16:9, "
 "35mm cinema lens, shallow depth of field. Light comes only from real sources in the scene (windows, lamps, sun, bulbs). "
 "Soft, natural, warm-neutral movie colour grade, gently muted, not saturated. Matte natural skin with visible pores and texture: "
 "NO gloss, NO shine, NO glow, NO HDR, NO airbrushing, NO plastic look. Fine film grain. Every face, hairstyle, skin tone, age and body build must match "
 "the attached approved character images exactly: the same people, not lookalikes; never slimmer, lighter, younger or more glamorous. "
 "Match the warm, natural cinematic light and colour of those approved images. All people are fictional adults unless stated. No readable text, logos, captions or "
 "watermarks anywhere unless this prompt gives the exact words.")

VIDEO_LOCK = ("RULES — follow every rule exactly: ONE continuous 10-second shot that begins exactly on the provided image. "
 "Keep every face, hairstyle, outfit, prop, door, window, curtain, light and time of day exactly as in the image for all 10 seconds; "
 "nothing appears, disappears, opens, closes or changes unless written below. Only the people described move, at natural real-life speed. "
 "Camera moves only as written: slow and steady, no shake, no zoom bursts. No cuts, no morphing, no warping faces or hands, no extra fingers, "
 "no flicker, no new people, no text on screen. Muted cinematic film look, soft natural light, matte skin: no shine, no glow, no bright flashes. "
 "Pacing: the action and every spoken line start in the first second and are fully finished before the 10 seconds end, at a natural speaking speed; never rushed, never cut off mid-word, and the shot ends on a calm held moment. "
 "Speech: Nigerian English accents, only the named speaker's lips move, everyone else listens and reacts silently.")

C = {  # face/body locks matched to the approved character images
 "ireti": ("IRETI (23)", "slim young Nigerian woman, dark brown skin, soft round face, big expressive eyes, long black box braids pulled back into a low ponytail, small silver stud earrings, no makeup", "soft, warm, clear young Yoruba-Nigerian female voice"),
 "chief": ("CHIEF ADENUGA (75)", "elderly Nigerian man, very dark brown skin, deep wrinkles, short snow-white hair, full white beard, heavy-lidded tired eyes, broad but frail frame", "deep, slow, gravelly elderly Yoruba-Nigerian male voice"),
 "femi": ("FEMI (33)", "tall well-built Nigerian man, dark skin, sharp low-cut fade, short neat black beard, rimless gold-framed glasses", "smooth, firm, educated Lagos male voice"),
 "gabriel": ("GABRIEL (33)", "Nigerian man, light brown skin, short curly hair with a fade, full thick black beard, clear aviator-shaped glasses, big friendly smile", "warm, upbeat, friendly Igbo-Nigerian male voice"),
 "funmi": ("MAMA FUNMI (48)", "thin Nigerian woman, dark skin, thin tired face, kind eyes, wine-coloured head wrap", "gentle, weak, warm middle-aged Yoruba-Nigerian female voice"),
 "dayo": ("DAYO (17)", "slim Nigerian teenage boy, dark skin, low haircut, bright cheeky smile", "lively, cheeky teenage Nigerian boy's voice"),
 "ronke": ("AUNTY RONKE (52)", "Nigerian woman, dark brown skin, sharp cheekbones, neat makeup, cold eyes, tight black head wrap", "cold, crisp, controlled Nigerian female voice"),
 "audu": ("MALLAM AUDU (62)", "older northern Nigerian man, dark skin, grey-white beard, kind eyes, white embroidered cap (hula)", "gentle, slow, Hausa-accented Nigerian male voice"),
 "hassan": ("DR. HASSAN BELLO (50)", "Nigerian man, dark skin, short greying hair, neat salt-and-pepper beard, calm serious eyes", "calm, measured, professional Nigerian male voice"),
 "lekan": ("MR. LEKAN (58)", "heavy-set Nigerian man, dark skin, round face, receding short hair, thin moustache, gold-rimmed rectangular glasses, gold watch, gold ring", "smooth, oily, charming older Nigerian male voice"),
 "grace": ("NURSE GRACE (30)", "full-figured Nigerian woman, dark brown skin, cornrows into a low bun, small stud earrings", "soft, hurt, polite Nigerian female voice"),
 "okoro": ("DR. OKORO (55)", "big heavy-set Nigerian man, dark skin, greying curly hair, full grey beard, tired kind eyes", "tired, kind, deep Igbo-Nigerian male voice"),
 "jide": ("MR. JIDE (45)", "short heavy Nigerian man, dark skin, round sweaty face, short beard", "loud, rough, bossy Lagos male voice"),
 "chioma": ("CHIOMA (24)", "Nigerian woman, dark brown skin, curly hair pulled up, gold sunglasses on her head, big gold hoop earrings, always chewing gum", "sassy, sharp-tongued Lagos female voice"),
 "segun": ("SEGUN (52)", "fit Nigerian man, brown skin, short hair, full beard with grey, serious frown", "busy, deep, polished Nigerian male voice"),
 "kunle": ("KUNLE (48)", "big Nigerian man, dark brown skin, clean bald head, dark rectangular glasses, neat goatee", "flat, deep, banker's Nigerian male voice"),
 "lola": ("LOLA (45)", "full-figured Nigerian woman, brown skin, big voluminous dark wavy hair, polished makeup, gold drop earrings", "soft British-Nigerian female voice"),
 "ajala": ("COMMANDER AJALA (72)", "elderly Nigerian man, dark skin, white beard, round dark sunglasses, cream fedora hat, huge joyful smile", "booming, joyful elderly Yoruba-Nigerian male voice"),
}

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

def build_prompts(sc, sh):
    bad = [k for k in sh["who"] if k not in C]
    if bad: raise SystemExit(f"unknown character {bad} in shot {sh['id']}")
    chars = [k for k in sh["who"] if k in C]
    look = " ".join(f"{C[k][0]}: {C[k][1]}; wearing {sc['wear'].get(k, 'the outfit in the reference')}." for k in chars)
    names = ", ".join([C[k][0] for k in chars] + ([PHOTO_REFS[sh["id"]]] if sh["id"] in PHOTO_REFS else []))
    head = (f"CHARACTERS IN THIS IMAGE: {names}. I have uploaded their approved images and character sheets; they must be the same people with the same faces and body builds, not lookalikes. " if names
            else "CHARACTERS IN THIS IMAGE: none (scenery only, no main characters). ")
    img = (f"{head}Create one image. {sh['img']} SETTING (keep identical in every shot of this scene): {sc['set']}"
           + (f" CHARACTERS (match attached references exactly): {look}" if look else "") + f" {IMAGE_LOCK}")
    voices = " ".join(f"{C[k][0]} voice: {C[k][2]}." for k in chars)
    cont = " This clip continues directly from the previous clip: same positions, same light, no jump." if sh["start"].lower().startswith("last frame") else ""
    vid = (f"LENGTH: exactly 10 seconds. ACTION: {sh['vid']}{cont}" + (f" VOICES: {voices}" if voices else "")
           + f" SETTING: {sc['set']} Sound: natural room and ambient sound only, no music. {VIDEO_LOCK}")
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
        for sh in s["shots"]:
            img, vid = build_prompts(s, sh)
            who = ", ".join([C[k][0] for k in sh["who"] if k in C] + ([PHOTO_REFS[sh["id"]]] if sh["id"] in PHOTO_REFS else [])) or "None (scenery only)"
            body.append(f'<div class="shot"><div class="hd"><b>Shot {sh["id"]}</b> · {e(sh["label"])}<span>10 sec · Start: {e(sh["start"])} · Attach refs: {e(who)}</span></div>'
                        f'<div class="lab img">IMAGE PROMPT · ChatGPT</div><div class="p">{e(img)}</div>'
                        f'<div class="lab vid">VIDEO PROMPT · Grok (image-to-video, 10s)</div><div class="p">{e(vid)}</div></div>')
            txt.append(f"\n--- SHOT {sh['id']} | {sh['label']} | Start: {sh['start']} | Attach: {who}\n\n[IMAGE PROMPT - ChatGPT]\n{img}\n\n[VIDEO PROMPT - Grok]\n{vid}\n")
        body.append("</section>")
    guide = (HERE / "guide.html").read_text()
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Image and Video Prompt Pack</title><style>
@page{{size:A4;margin:11mm}} body{{font-family:Arial,Helvetica,sans-serif;color:#111827;font-size:9.5px;margin:0}}
.cover{{background:#111827;color:#fff;border-radius:10px;padding:20px 22px;margin-bottom:12px}} .cover h1{{margin:4px 0;font-size:22px}}
.cover .k{{color:#f59e0b;letter-spacing:2px;font-size:10px;font-weight:bold}} .cover p{{margin:2px 0;color:#d1d5db;font-size:11px}}
h2{{font-size:14px;border-bottom:3px solid #f59e0b;padding-bottom:3px;margin:16px 0 6px;break-after:avoid}} h3{{font-size:12px;margin:12px 0 4px}}
section{{break-before:page}} .upl{{background:#dbeafe;border-radius:6px;padding:6px 8px;margin-bottom:6px;font-size:10.5px}} .set{{background:#fef3c7;border-radius:6px;padding:6px 8px;margin-bottom:8px}}
.shot{{border:1px solid #d1d5db;border-radius:7px;padding:6px 8px;margin-bottom:7px;break-inside:avoid}}
.hd{{font-size:10.5px;margin-bottom:4px}} .hd span{{float:right;color:#6b7280;font-size:9px}}
.lab{{font-weight:bold;font-size:8.5px;letter-spacing:1px;margin-top:4px}} .img{{color:#1d4ed8}} .vid{{color:#b45309}}
.p{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:5px;padding:5px 6px;line-height:1.4;white-space:pre-wrap}}
ol.toc{{columns:2;font-size:10px;padding-left:18px}} ol.toc span{{color:#6b7280}} a{{color:#111827;text-decoration:none}}
.lock{{background:#f3f4f6;border-left:4px solid #111827;padding:6px 9px;white-space:pre-wrap;line-height:1.45;margin:4px 0 8px}}
table{{border-collapse:collapse;width:100%;font-size:9.5px}} td,th{{border:1px solid #d1d5db;padding:3px 5px;text-align:left;vertical-align:top}}
</style></head><body>
<div class="cover"><div class="k">SHOT-BY-SHOT PROMPT PACK</div><h1>A Poor Girl Helped a Billionaire CEO Grandpa Walk Again</h1>
<p>{len(scenes)} scenes · {total} shots · every shot has an image prompt (ChatGPT) and a 10-second video prompt (Grok)</p></div>
{guide.replace("{{IMAGE_LOCK}}", e(IMAGE_LOCK)).replace("{{VIDEO_LOCK}}", e(VIDEO_LOCK)).replace("{{CAST}}", "".join(f"<tr><td><b>{e(v[0])}</b></td><td>{e(v[1])}</td><td>{e(v[2])}</td></tr>" for v in C.values()))}
<h2>Scenes</h2><ol class="toc">{toc}</ol>
<section><h2>Character upload checklist</h2><p>Which character sheets to upload for each scene, and who is in each shot.</p><table><tr><th style="width:20%">Scene</th><th style="width:28%">Upload for this scene</th><th>Characters in each shot</th></tr>{"".join(checklist)}</table></section>
{"".join(body)}</body></html>'''
    (HERE / "prompt_pack.html").write_text(page)
    (HERE / "All_Prompts_copy_paste.txt").write_text("IMAGE + VIDEO PROMPTS — A Poor Girl Helped a Billionaire CEO Grandpa Walk Again\n" + "".join(txt))
    print(len(scenes), "scenes", total, "shots")

if __name__ == "__main__":
    main()
