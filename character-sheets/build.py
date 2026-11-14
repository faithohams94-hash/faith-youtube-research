"""Character sheet prompts (ChatGPT) for every character, built on the approved character images."""
import html, pathlib, subprocess
HERE = pathlib.Path(__file__).parent

LOOK = ("CINEMATIC LOOK: match the attached image's photographic style exactly: the same warm golden natural light, the same soft movie colour grade, "
 "the same realistic skin rendering and the same fine film grain, as if these were extra frames shot by the same cinematographer on the same day. "
 "Photorealistic real photographs, not an illustration and not a 3D render. Matte natural skin with real pores and texture: no shine, no glow, no HDR, no airbrushing, no beautifying. "
 "Nothing cropped: full-body views show the whole person from head to feet. Evenly spaced on one clean sheet. No text, no labels, no numbers, no logos, no watermark. "
 "This is a fictional adult character.")

IDENTITY = ("IDENTITY LOCK: this must be the SAME person as in the attached image, not a lookalike. Copy exactly: the face shape, eyes, eyebrows, nose, lips, jawline, "
 "hairline and hairstyle, beard or facial hair, skin tone, age, height, weight and body build. Do not slim, lighten, age, de-age, smooth or beautify. "
 "If the attached image shows only part of the body, continue the same build naturally for the full-body views. ")

def sheet(name, look, outfit, expr, pose_note=""):
    return (f"CHARACTER SHEET: {name}. The attached image is my approved character. Use it as the ONLY reference for this person. {IDENTITY}Person: {look}. "
            f"Make one wide 16:9 character reference sheet on a plain, softly lit warm-neutral background (lit with the same warm cinematic light as the attached image) showing the same person in the same outfit: "
            f"top row, four full-body views side by side: front, three-quarter, side profile and back{pose_note}; "
            f"bottom row, five head-and-shoulders close-ups: a neutral face from the front, a neutral face in three-quarter view, and three expressions: {expr}. "
            f"Outfit in every view: {outfit}. {LOOK}")

def wardrobe(name, outfits, pose_note=""):
    n = len(outfits)
    lst = "; ".join(f"({i+1}) {o}" for i, o in enumerate(outfits))
    return (f"WARDROBE SHEET: {name}. Attach BOTH the approved character image and the character sheet. Use them as the ONLY reference for this person. {IDENTITY}"
            f"Make one wide 16:9 sheet on a plain, softly lit warm-neutral background showing the same person {n} times, full body, front view, standing side by side{pose_note}, "
            f"each in a different outfit from the film, left to right: {lst}. Same neutral, relaxed pose and same lighting for all. {LOOK}")

CHARS = [
 ("Ireti Alade (23), the heroine",
  "slim young Nigerian woman, about 5 feet 5, dark brown skin, soft round face, big expressive eyes, long black box braids pulled back into a low ponytail, small silver stud earrings, no makeup",
  "a light-blue scrubs top, white trousers and white sneakers (her caretaker uniform, the outfit she wears most)",
  "a gentle tired smile with lips closed, tears she is wiping away fast, and a wide happy laugh",
  "",
  ["a faded yellow ankara blouse, a plain black skirt and brown slippers mended with tape (poor)",
   "a black T-shirt with a plain orange apron and the same taped slippers (restaurant waitress)",
   "a light-blue scrubs top, white trousers and white sneakers (caretaker)",
   "a simple neat navy dress and flat shoes (her one good dress)",
   "a cream lace iro and buba with a gold gele (ending celebration)",
   "a crisp white nursing-school uniform with white shoes (final scene)"]),
 ("Chief Babatunde Adenuga (75), the billionaire grandpa (standing)",
  "elderly Nigerian man, about 6 feet tall but slightly stooped, very dark brown skin, deep wrinkles, short snow-white hair, full white beard, heavy-lidded tired eyes, broad but frail frame",
  "a white kaftan, holding an ivory-handled walking cane",
  "a stern, hurt stare with a tight jaw, his face turned away in sadness, and a wide wet-eyed smile",
  ", leaning on the cane",
  ["a white kaftan with the ivory-handled cane (before the fall)",
   "a grey kaftan with a wool blanket folded over one arm (dark period)",
   "a bright colourful ankara shirt and dark trousers (healing)",
   "a royal-blue agbada with a matching fila cap (Sundays)",
   "a cream agbada with the ivory-handled cane (climax)",
   "a white vest and grey track trousers (rehab)"]),
 ("Chief Babatunde Adenuga (75), seated in his wheelchair",
  "the same elderly man as the attached reference, sitting in a black leather wheelchair",
  "a grey kaftan with a wool blanket over his knees, sitting in a black leather wheelchair",
  "a cold glare, a tired empty stare at nothing, and a small reluctant smile",
  ", all seated in the same wheelchair (front, three-quarter, side and back of the wheelchair)", None),
 ("Femi Adenuga (33), the billionaire CEO grandson",
  "tall well-built Nigerian man, dark skin, sharp low-cut fade, short neat black beard, rimless gold-framed glasses",
  "a tailored navy three-piece suit, white shirt, navy tie, gold cufflinks, black leather shoes",
  "a serious, focused frown, an exhausted look while rubbing his eyes, and tears of joy",
  "",
  ["a tailored navy three-piece suit with gold cufflinks (office)",
   "the same suit with the jacket off, white shirt sleeves rolled up and tie loosened (stress)",
   "a smart casual white shirt and dark trousers (ending)"]),
 ("Gabriel Okafor (33), Femi's best friend",
  "Nigerian man, light brown skin, short curly hair with a fade, full thick black beard, clear aviator-shaped glasses, big friendly smile",
  "a grey suit with a white shirt open at the collar, no tie, brown shoes",
  "a big warm smile, a thoughtful curious look, and a polite but patient look",
  "", None),
 ("Mama Funmi Alade (48), Ireti's mother",
  "thin Nigerian woman, dark skin, thin tired face, kind eyes, wine-coloured head wrap",
  "a faded blue patterned wrapper and matching blouse with the wine-coloured head wrap, barefoot or in simple slippers",
  "a soft loving smile, a weak tired look, and laughing with her eyes closed",
  "",
  ["a faded blue patterned wrapper and blouse with the wine head wrap (sick, at home and in hospital)",
   "the same wrapper with a shawl over her shoulders (cooking at home)",
   "a cream lace iro and buba with a matching head wrap, healthy and glowing (ending)"]),
 ("Dayo Alade (17), Ireti's little brother",
  "slim Nigerian teenage boy, dark skin, low haircut, bright cheeky smile",
  "a faded green secondary-school uniform shirt, dark trousers, black sandals and a school bag on one shoulder",
  "a cheeky grin, a hurt serious face, and crying with joy",
  "",
  ["a faded green secondary-school uniform shirt and dark trousers (school)",
   "a white singlet and shorts (at home)",
   "a brand-new university T-shirt and jeans (ending)"]),
 ("Aunty Ronke (52), the head housekeeper",
  "Nigerian woman, dark brown skin, sharp cheekbones, neat makeup, cold eyes, tight black head wrap",
  "a neat black housekeeper's dress with a crisp white collar, black flat shoes, holding a silver tray",
  "a polite smile that doesn't reach her eyes, a cold suspicious stare, and sobbing in fear",
  "",
  ["a black housekeeper's dress with a white collar (day)",
   "a long dark nightgown with the black head wrap (night)"]),
 ("Mallam Audu (62), the gateman",
  "older northern Nigerian man, dark skin, grey-white beard, kind eyes, white embroidered cap (hula)",
  "a long white kaftan, white embroidered cap and simple sandals",
  "a gentle smile, a sad thoughtful look, and laughing in surprise",
  "", None),
 ("Dr. Hassan Bello (50), Chief's orthopaedic doctor",
  "Nigerian man, dark skin, short greying hair, neat salt-and-pepper beard, calm serious eyes",
  "a clean white doctor's coat over a light blue shirt, dark trousers, a stethoscope around his neck",
  "calm and serious, gently hopeful, and shocked",
  "", None),
 ("Mr. Lekan Bamidele (58), Group Vice-Chairman",
  "heavy-set Nigerian man, dark skin, round face, receding short hair, thin moustache, gold-rimmed rectangular glasses, gold watch, gold ring",
  "an expensive black agbada with silver embroidery, a big gold watch, holding a bouquet of white lilies",
  "a charming smile that doesn't reach his eyes, a cold calculating stare, and pale panic",
  "", None),
 ("Nurse Grace (30), the caretaker in the cold open",
  "full-figured Nigerian woman, dark brown skin, cornrows into a low bun, small stud earrings",
  "navy blue nurse scrubs with a small name badge on the chest, a stethoscope, white shoes",
  "polite and caring, worried, and holding back tears",
  "", None),
 ("Dr. Okoro (55), the public-hospital doctor",
  "big heavy-set Nigerian man, dark skin, greying curly hair, full grey beard, tired kind eyes",
  "a faded, slightly worn white doctor's coat over a blue shirt, a stethoscope, holding a brown file",
  "tired and kind, sad and sorry, and gently encouraging",
  "", None),
 ("Mr. Jide (45), manager of Bukka Royale",
  "short heavy Nigerian man, dark skin, round sweaty face, short beard",
  "a maroon polo shirt with a stained white apron, dark trousers, slippers",
  "shouting and pointing, laughing loudly at his own joke, and a mocking sneer",
  "", None),
 ("Chioma (24), waitress at Bukka Royale",
  "Nigerian woman, dark brown skin, curly hair pulled up, gold sunglasses on her head, big gold hoop earrings",
  "a yellow T-shirt with a dark brown apron, jeans, slippers",
  "blowing a pink bubble-gum bubble, a sassy side-eye, and an annoyed hiss",
  "", None),
 ("Segun Adenuga (52), Chief's eldest son",
  "fit Nigerian man, brown skin, short hair, full beard with grey, serious frown",
  "a charcoal suit, white shirt and brown paisley tie, black shoes",
  "a busy distracted look, a guilty shocked face, and crying with regret",
  "", None),
 ("Kunle Adenuga (48), Chief's second son",
  "big Nigerian man, dark brown skin, clean bald head, dark rectangular glasses, neat goatee",
  "a dark pinstripe suit, white shirt and blue tie, black shoes",
  "a flat doubtful look, sitting up in shock, and a soft regretful smile",
  "", None),
 ("Lola Adenuga-Wright (45), Chief's daughter in London",
  "full-figured Nigerian woman, brown skin, big voluminous dark wavy hair, polished makeup, gold drop earrings",
  "a stylish burgundy blazer over a matching top, dark trousers, heeled shoes",
  "a cool judging look, her hand over her mouth in shock, and a warm teary smile",
  "", None),
 ("Commander Kola Ajala (72), legendary juju musician (fictional)",
  "elderly Nigerian man, dark skin, white beard, round dark sunglasses, cream fedora hat, huge joyful smile",
  "a crisp cream suit with a gold patterned tie, cream fedora, holding a gold acoustic guitar",
  "a huge joyful laugh, shading his eyes to look into the crowd, and singing with passion",
  "", None),
]

KEHINDE = ("PHOTO PROP: KEHINDE ALADE (Ireti's late father). The attached image is my approved photo of him. Keep this man's face, smile, skin tone and build exactly the same, not a lookalike, and match its warm, faded photographic colour. "
 "Make one wide 16:9 sheet on a plain light-grey background with three old family photographs of the same man laid side by side, each slightly faded with soft worn edges like real photos from about 2008: "
 "(1) smiling broadly beside a yellow Lagos danfo bus, waving with his right palm open to show a healed burn scar across it, in a grey T-shirt; "
 "(2) a head-and-shoulders portrait, broad smile, in a green short-sleeved shirt; (3) the same portrait in a simple dark wooden frame. "
 "Photorealistic, natural colours, no text, no logos, no watermark. Fictional adult.")

def main():
    e = html.escape
    items, txt = [], []
    for name, look, outfit, expr, pose, wr in CHARS:
        sp = sheet(name, look, outfit, expr, pose)
        if name.startswith("Dayo"): sp = sp.replace("This is a fictional adult character.", "This is a fictional 17-year-old schoolboy in ordinary everyday clothes.")
        block = f'<div class="c"><h2>{e(name)}</h2><div class="lab">1 · CHARACTER SHEET PROMPT</div><div class="p">{e(sp)}</div>'
        txt.append(f"\n\n========== {name} ==========\n\n[1] CHARACTER SHEET PROMPT (attach the approved image)\n{sp}\n")
        if wr:
            wp = wardrobe(name.replace(" (standing)", ""), wr, "")
            if name.startswith("Dayo"): wp = wp.replace("This is a fictional adult character.", "This is a fictional 17-year-old schoolboy in ordinary everyday clothes.")
            block += f'<div class="lab">2 · WARDROBE SHEET PROMPT (attach the approved image AND the character sheet you just made)</div><div class="p">{e(wp)}</div>'
            txt.append(f"\n[2] WARDROBE SHEET PROMPT (attach the approved image AND the character sheet from step 1)\n{wp}\n")
        items.append(block + "</div>")
    items.append(f'<div class="c"><h2>Kehinde Alade (photo only)</h2><div class="lab">PHOTO PROP PROMPT</div><div class="p">{e(KEHINDE)}</div></div>')
    txt.append(f"\n\n========== Kehinde Alade (photo only) ==========\n\n[PHOTO PROP PROMPT] (attach the approved Kehinde image)\n{KEHINDE}\n")
    page = f'''<!doctype html><html><head><meta charset="utf-8"><title>Character Sheet Prompts</title><style>
@page{{size:A4;margin:12mm}} body{{font-family:Arial,Helvetica,sans-serif;color:#111827;font-size:10px;margin:0}}
.cover{{background:#111827;color:#fff;border-radius:10px;padding:18px 22px;margin-bottom:12px}} .cover h1{{margin:4px 0;font-size:21px}}
.cover .k{{color:#f59e0b;letter-spacing:2px;font-size:10px;font-weight:bold}} .cover p{{margin:2px 0;color:#d1d5db;font-size:11px}}
.c{{border:1px solid #d1d5db;border-radius:8px;padding:8px 10px;margin-bottom:9px;break-inside:avoid}} h2{{font-size:13px;margin:0 0 4px;border-bottom:3px solid #f59e0b;padding-bottom:3px}}
.lab{{font-weight:bold;font-size:9px;letter-spacing:1px;color:#1d4ed8;margin-top:5px}} .p{{background:#f9fafb;border:1px solid #e5e7eb;border-radius:5px;padding:6px 7px;line-height:1.45}}
ol{{margin:4px 0 0;padding-left:18px;line-height:1.5}} .how{{border:1px solid #d1d5db;border-radius:8px;padding:8px 12px;margin-bottom:12px}}
</style></head><body><div class="cover"><div class="k">CHARACTER SHEET PROMPTS · CHATGPT</div><h1>A Poor Girl Helped a Billionaire CEO Grandpa Walk Again</h1>
<p>19 character sheets (Chief has two: standing and in his wheelchair), wardrobe sheets for the characters who change clothes, and Kehinde's photo prop.</p></div>
<div class="how"><b>How to use</b><ol>
<li>Open a new ChatGPT chat for each character.</li>
<li>Attach that character's <b>approved image</b> (from the character approval sheet) and paste prompt 1. You get a sheet with front, three-quarter, side and back views plus face close-ups.</li>
<li>Check the sheet side by side with the approved image. If the face, body size or colour is even slightly different, reply: <i>"This is not the same person. Make every face and the body build exactly like the attached approved image, with the same warm cinematic light. Change nothing else."</i></li>
<li>For characters with a wardrobe prompt, attach <b>both the approved image and the character sheet you just made</b> and paste prompt 2 to get every outfit from the film.</li>
<li>Save the sheets with the character's name. From now on, these are the "character sheets" you upload with every shot in the prompt pack.</li>
<li>There are no name labels on the sheets, because AI spells badly. Add names in Canva if you want them.</li></ol></div>
{"".join(items)}</body></html>'''
    (HERE / "character_sheets.html").write_text(page)
    (HERE / "Character_Sheet_Prompts_copy_paste.txt").write_text("CHARACTER SHEET PROMPTS (ChatGPT) — A Poor Girl Helped a Billionaire CEO Grandpa Walk Again\n" + "".join(txt))
    print("ok", len(CHARS))
main()
