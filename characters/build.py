"""Builds the character approval sheet. Drop images named <slug>.jpg/.png/.webp into images/ and re-run."""
import base64, html, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).parent
C = [
 # slug, name, age, role, description, group
 ("ireti","Ireti Alade","23","The heroine","Broke waitress who left 300-level Nursing after her father died. Soft-spoken, never small; uses humour as a shield.","Main cast"),
 ("chief","Chief Babatunde Adenuga","75","The billionaire grandpa","Founder of Adenuga Crest Group, now in a wheelchair. Grumpy because he is grieving; insults everyone before they can leave him.","Main cast"),
 ("femi","Femi Adenuga","33","Billionaire CEO grandson","Group CEO of Adenuga Crest. Brilliant, polished, always on two phones. Shows love with money.","Main cast"),
 ("gabriel","Gabriel Okafor","33","Femi's best friend, Head of People","Warm and funny, a man who notices people. He is the one who finds Ireti.","Main cast"),
 ("mama-funmi","Mama Funmi Alade","48","Ireti's mother","A gentle, funny widow, slowly dying of a growth on her heart. She knows more than she says.","Main cast"),
 ("dayo","Dayo Alade","17","Ireti's little brother","Clever boy preparing for JAMB, who secretly does other students' homework for money.","Main cast"),
 ("aunty-ronke","Aunty Ronke","52","Head housekeeper","Has run the mansion for six years. Stiff and polite, smiles only with her mouth. Hands Chief his evening tablet.","Main cast"),
 ("mallam-audu","Mallam Audu","62","The gateman","Has served Chief for thirty years. Drinks tea in the gatehouse and sees everything.","Main cast"),
 ("dr-bello","Dr. Hassan Bello","50","Chief's orthopaedic doctor","Calm, serious specialist overseeing Chief's recovery.","Main cast"),
 ("lekan","Mr. Lekan Bamidele","58","Group Vice-Chairman","Chief's \"loyal\" right hand for twenty years. Charming, always carries flowers, always counting.","Main cast"),
 ("nurse-grace","Nurse Grace","30","Caretaker in the cold open","The caretaker Chief pushes away. Navy scrubs.","Supporting cast"),
 ("dr-okoro","Dr. Okoro","55","Public-hospital doctor","Treats Mama Funmi. Tired and kind, in a faded white coat.","Supporting cast"),
 ("mr-jide","Mr. Jide","45","Manager of Bukka Royale","A sweaty, loud man in a polo shirt.","Supporting cast"),
 ("chioma","Chioma","24","Waitress at Bukka Royale","Sharp-tongued and chews gum.","Supporting cast"),
 ("segun","Segun Adenuga","52","Chief's eldest son","Femi's father, an oil-and-gas executive in Abuja.","Supporting cast"),
 ("kunle","Kunle Adenuga","48","Chief's second son","A banker in Port Harcourt.","Supporting cast"),
 ("lola","Lola Adenuga-Wright","45","Chief's daughter","Lives in London.","Supporting cast"),
 ("commander","Commander Kola Ajala","72","Legendary juju musician (fictional)","In a white suit with a gold guitar.","Supporting cast"),
 ("kehinde","Kehinde Alade","—","Ireti's late father","Seen only in photographs. Danfo driver, broad smile, a burn scar across his right palm.","Supporting cast"),
]
def img(slug):
    import io
    from PIL import Image
    for ext in (".jpg",".jpeg",".png",".webp"):
        p = HERE/"images"/(slug+ext)
        if p.exists():
            im = Image.open(p).convert("RGB"); im.thumbnail((1000,1000))
            b = io.BytesIO(); im.save(b,"JPEG",quality=82)
            return f'<img src="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}">'
    return '<div class="ph">Character image<br><small>to be added</small></div>'
e = html.escape
cards = {}
for slug,name,age,role,desc,grp in C:
    a = "" if age=="—" else f" <span class='age'>({age})</span>"
    cards.setdefault(grp,[]).append(f'''<div class="card"><div class="photo">{img(slug)}</div><div class="info">
<div class="name">{e(name)}{a}</div><div class="role">{e(role)}</div><p>{e(desc)}</p>
<div class="ap"><span>☐ Approved</span><span>☐ Changes needed</span></div><div class="line">Notes:</div></div></div>''')
sections = "".join(f'<h2>{g}</h2><div class="grid">{"".join(v)}</div>' for g,v in cards.items())
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:A4;margin:12mm}}
body{{font-family:Arial,Helvetica,sans-serif;color:#1f2937;margin:0;font-size:11px}}
.cover{{background:#111827;color:#fff;border-radius:10px;padding:22px 24px;margin-bottom:14px}}
.cover .k{{color:#f59e0b;font-size:11px;letter-spacing:2px;font-weight:bold}}
.cover h1{{margin:6px 0 4px;font-size:24px}} .cover p{{margin:0;color:#d1d5db;font-size:12px}}
h2{{font-size:15px;border-bottom:3px solid #f59e0b;padding-bottom:4px;margin:14px 0 10px;break-after:avoid}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.card{{display:flex;flex-direction:column;border:1px solid #d1d5db;border-radius:8px;overflow:hidden;break-inside:avoid}}
.photo{{width:100%;aspect-ratio:16/9;background:#f3f4f6}}
.photo img{{width:100%;height:100%;object-fit:cover;display:block}}
.ph{{height:100%;display:flex;align-items:center;justify-content:center;text-align:center;color:#9ca3af;border-bottom:2px dashed #d1d5db;font-size:11px}}
.info{{padding:8px 10px;display:flex;flex-direction:column;flex:1}}
.name{{font-weight:bold;font-size:13px}} .age{{color:#6b7280;font-weight:normal}}
.role{{color:#b45309;font-weight:bold;margin:2px 0 4px}}
.info p{{margin:0 0 6px;min-height:28px;line-height:1.35;color:#374151}}
.ap{{display:flex;gap:10px;white-space:nowrap;font-size:10px;font-weight:bold;margin-top:auto}}
.line{{border-bottom:1px solid #9ca3af;margin-top:6px;padding-bottom:10px;color:#6b7280}}
.sign{{break-inside:avoid;margin-top:18px;border:2px solid #111827;border-radius:8px;padding:14px 18px}}
.sign h3{{margin:0 0 10px}} .row{{display:flex;gap:24px;margin-top:22px}}
.row div{{flex:1;border-top:1px solid #111827;padding-top:4px;color:#4b5563}}
</style></head><body>
<div class="cover"><div class="k">CHARACTER APPROVAL SHEET</div>
<h1>A Poor Girl Helped a Billionaire CEO Grandpa Walk Again</h1>
<p>AI Nollywood movie · 60 minutes · 19 characters. Please tick Approved or Changes needed for each character and add notes.</p></div>
{sections}
<div class="sign"><h3>Client approval: Mr. Chinedu</h3>
<div>☐ All characters approved &nbsp;&nbsp;&nbsp; ☐ Approved with the changes noted above</div>
<div class="row"><div>Signature</div><div>Date</div></div></div>
</body></html>'''
(HERE/"approval.html").write_text(page)
print("wrote", HERE/"approval.html")
