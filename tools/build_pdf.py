"""Build the print HTML for an interactive script PDF.

Usage: python3 tools/build_pdf.py CONFIG.json
CONFIG keys: script (md path), scenes (json from parse_script.py), out_html,
title, kicker, tagline, blurb, meta [[value,label],...], threads [[name, desc, [scene titles]]],
colors {SPEAKER: hex}, characters (optional md path), cover_theme {bg, fg, accent, muted}.
Checkbox markers (CHKs<n>x<i>) are placed for tools/add_checkboxes.py.
"""
import html
import json
import re
import sys

cfg = json.load(open(sys.argv[1]))
S = json.load(open(cfg['scenes']))
md = open(cfg['script']).read()
e = html.escape
C = cfg.get('colors', {})
col = lambda w: C.get(w, '#5b5560')
th = {'bg': '#0d0b10', 'fg': '#f5efe6', 'accent': '#d9a441', 'muted': '#a79fae', **cfg.get('cover_theme', {})}


def tc(x):
    small = {'of', 'the', 'a', 'at', 'in', 'to', 'and', 'on', 'or', 'for'}
    words = x.lower().split(' ')
    out = []
    for i, w in enumerate(words):
        if i and w in small:
            out.append(w)
        elif w[:1] in '"“':
            out.append(w[:2].upper() + w[2:])
        else:
            out.append(w[:1].upper() + w[1:])
    return ' '.join(out)


acts = {}
for m in re.finditer(r'^## ((?:ACT|PROLOGUE)\b.+)$', md, re.M):
    nxt = re.search(r'^## SCENE (\d+) — ', md[m.end():], re.M)
    acts[int(nxt.group(1))] = m.group(1)
by_title = {s['title']: s['n'] for s in S}
last = S[-1]['n']

chars = []
if cfg.get('characters'):
    cm = open(cfg['characters']).read()
    for block in re.split(r'^### ', cm, flags=re.M)[1:]:
        head, _, body = block.partition('\n')
        who = re.search(r'\*\*Who (?:she|he|they) (?:is|are):\*\* (.+)', body)
        prompts = re.findall(r'\*\*Image prompt([^:]*):\*\* (.+)', body)
        chars.append((head.strip(), who.group(1) if who else '', prompts))
    extras = re.search(r'## EXTRAS AND CROWDS\n\n(.*?)\n\n---', cm, re.S)
    extras = [re.sub(r'\*\*', '', l[2:]) for l in extras.group(1).split('\n') if l.startswith('- ')] if extras else []

css = f'''
@page{{size:A4;margin:15mm 15mm}} @page:first{{margin:0}}
*{{box-sizing:border-box}}
body{{font-family:Figtree,"DejaVu Sans",sans-serif;font-size:10.4pt;line-height:1.48;color:#1d1a20;margin:0}}
.d{{font-family:"Playfair Display",Gloock,"DejaVu Serif",serif;font-weight:700}}
.m{{font-family:"Courier Prime","Courier 10 Pitch",monospace}}
a{{color:inherit}}
.cover{{height:297mm;background:{th['bg']};color:{th['fg']};padding:28mm 20mm 22mm;display:flex;flex-direction:column;justify-content:space-between;page-break-after:always}}
.cover small{{color:{th['accent']};letter-spacing:.24em;font-size:9.5pt}}
.cover h1{{font-size:58pt;line-height:.95;margin:9mm 0 5mm}}
.cover h1 span{{color:{th['accent']}}}
.cover .tag{{font-size:15pt;margin:0 0 7mm;font-style:italic}}
.cover p{{color:{th['muted']};font-size:11pt;max-width:140mm}}
.spot{{margin-top:8mm;height:58mm;border-radius:4mm;background:radial-gradient(ellipse at 50% 0%,rgba(255,236,190,.55),rgba(255,236,190,.08) 45%,transparent 70%),linear-gradient(#1b1620,#0d0b10);position:relative;overflow:hidden}}
.spot b{{position:absolute;left:50%;bottom:9mm;transform:translateX(-50%);font-family:"Courier Prime",monospace;font-size:9pt;letter-spacing:.3em;color:{th['accent']}}}
.meta{{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;border-top:1px solid #3a3340;padding-top:7mm}}
.meta b{{display:block;color:{th['accent']};font-size:18pt}}
.meta span{{font-size:8.3pt;color:{th['muted']};letter-spacing:.1em}}
h2.sec{{font-size:24pt;margin:0 0 4mm}}
.howto{{border:1px solid #e3d9c8;background:#fbf7f0;border-radius:3mm;padding:4mm 6mm;font-size:9.8pt;margin-bottom:6mm}}
.howto li{{margin:1mm 0}}
.ch{{border:1px solid #e6dfd2;border-radius:3mm;padding:3.4mm 4.6mm;margin-bottom:3.4mm;page-break-inside:avoid}}
.ch h4{{margin:0 0 1mm;font-size:12.5pt}}
.ch .who{{font-size:9.3pt;color:#4d4752;margin:0 0 2mm}}
.ch .pl{{font-family:"Courier Prime",monospace;font-size:7.6pt;letter-spacing:.14em;color:#9a6b12;margin-top:1.6mm}}
.ch .pr{{background:#f6f2ea;border-left:2.5px solid {th['accent']};padding:2mm 3mm;font-size:8.8pt;line-height:1.42;margin-top:.6mm}}
.ch a{{font-size:8pt;color:#8d8a9c;text-decoration:none}}
.threads .th{{border:1.5px solid #e6dcc9;border-radius:3mm;padding:3.4mm 5mm;margin-bottom:3.4mm;background:#fbf8f2;page-break-inside:avoid}}
.th h4{{margin:0 0 .6mm;font-size:13pt}} .th p{{margin:0 0 2mm;color:#6b6260;font-size:9.4pt}}
.th a{{display:inline-block;font-family:"Courier Prime",monospace;font-size:8.3pt;background:#141018;color:#f5efe6;text-decoration:none;border-radius:2mm;padding:.9mm 2.4mm;margin:0 1.5mm 1.5mm 0}}
.toc{{page-break-before:always}}
.toc .acth{{font-family:"Courier Prime",monospace;font-size:8.4pt;letter-spacing:.16em;color:#a2353a;margin:4mm 0 1mm}}
.toc a{{display:grid;grid-template-columns:10mm 1fr 15mm;text-decoration:none;padding:.9mm 0;border-bottom:1px dotted #ddd3c6;font-size:9.3pt}}
.toc .n{{color:#a2353a}} .toc .t{{text-align:right;color:#8d8a9c}}
.actpage{{page-break-before:always;height:255mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}}
.actpage small{{font-family:"Courier Prime",monospace;letter-spacing:.3em;color:#a2353a}}
.actpage h2{{font-size:34pt;margin:4mm 0 0;max-width:150mm}}
.scene{{page-break-before:always}}
.nav{{display:flex;justify-content:space-between;font-family:"Courier Prime",monospace;font-size:8pt;margin-bottom:2.6mm}}
.nav a{{color:#8d8a9c;text-decoration:none}}
.shead{{border-bottom:1.5px solid #1d1a20;padding-bottom:2.6mm;margin-bottom:4mm}}
.shead .n{{color:#a2353a;font-size:9.3pt;letter-spacing:.14em}}
.shead h3{{font-size:21pt;margin:1mm 0 1.2mm;line-height:1.05}}
.shead .slug{{font-size:8.6pt;color:#6b6880;text-transform:uppercase}}
.track{{display:flex;gap:5mm;margin:-1mm 0 3.4mm;font-size:8.4pt;color:#6b6260}}
.track span{{display:flex;align-items:center;gap:1.6mm}}
.track i{{display:inline-block;width:4.2mm;height:4.2mm;border:1.2px solid #a2353a;border-radius:1mm;font-style:normal;font-size:3pt;line-height:1;color:#fff;overflow:hidden;font-family:"DejaVu Sans",sans-serif}}
.act{{font-style:italic;color:#4f4954;border-left:2px solid #e7dfd3;padding-left:4mm;margin:2.6mm 0}}
.act.open{{font-style:normal;background:#f7f3ec;border-left:3px solid {th['accent']};padding:2.6mm 4mm;color:#2c2730}}
.act.open::before{{content:"SCENE OPENING · ";font-family:"Courier Prime",monospace;font-size:7.6pt;letter-spacing:.14em;color:#9a6b12}}
.ln{{margin:2.4mm 0 0;page-break-inside:avoid;display:grid;grid-template-columns:30mm 1fr;gap:3.6mm}}
.ln .w{{font-family:"Courier Prime",monospace;font-weight:700;font-size:9.1pt;text-align:right;padding-top:.4mm}}
.ln .w em{{display:block;font-style:normal;font-weight:400;color:#9a928c;font-size:7.6pt}}
.ln .dir{{color:#8d8580;font-style:italic}}
.ln.sing .s{{font-style:italic;color:#7a2f6b}}
.aa{{margin:.8mm 0 2.4mm 33.6mm;font-size:8.3pt;line-height:1.38;color:#6a6370;background:#f4f1f7;border-radius:1.6mm;padding:1.3mm 2.6mm;page-break-inside:avoid}}
.aa b{{color:#4b3f5c;font-weight:700}}
.card{{margin:3.4mm auto;max-width:125mm;text-align:center;border:1.5px solid #a2353a;border-radius:3mm;padding:2.6mm 5mm;page-break-inside:avoid}}
.card small{{display:block;color:#a2353a;font-size:7.4pt;letter-spacing:.18em}}
.card p{{margin:1mm 0 0;font-family:"Courier Prime",monospace;font-weight:700;font-size:10.6pt}}
.post{{margin:3mm 0 1.6mm;border-left:3px solid #1d1a20;background:#f3f1f4;padding:2mm 3mm;font-size:9.2pt}} .trans{{margin:1.6mm 0;background:#141018;color:#f5efe6;padding:2mm 3mm;font-style:italic;font-size:9.2pt}} .post span,.trans span{{display:block;font-family:"Courier Prime",monospace;font-style:normal;font-size:7.4pt;letter-spacing:.16em;color:#9a6b12}}
.tc{{text-align:center;font-family:"Playfair Display",Gloock,serif;color:#9a6b12;font-size:14pt;margin:6mm 0}}
'''

JOURNAL = cfg.get('style') == 'journal'
if JOURNAL:
    css = """
@page{size:A4;margin:16mm 15mm 18mm}
*{box-sizing:border-box}
body{font-family:"DejaVu Serif",Georgia,serif;font-size:10.2pt;line-height:1.5;color:#1c1f1e;margin:0}
.sans,.ln .w,.shead h3,.nav,.track,.aa,.card,.toc a,.howto,.ch h4,.th h4,.meta{font-family:"DejaVu Sans",Helvetica,Arial,sans-serif}
a{color:inherit}
.jcard{background:#0f1513;color:#f2f0ea;border-radius:3.5mm;padding:8mm 9mm 7mm;margin-bottom:5mm}
.jcard small{display:block;font-family:"DejaVu Sans",sans-serif;font-weight:700;color:#e0b13a;font-size:8pt;letter-spacing:.26em;margin-bottom:3mm}
.jcard h1{font-family:"DejaVu Serif",serif;font-weight:700;font-size:23pt;line-height:1.18;margin:0 0 3mm}
.jcard .sub{font-family:"DejaVu Sans",sans-serif;color:#a6aba8;font-size:8.6pt}
.jcard .tag{font-style:italic;color:#d8d4cb;font-size:10.5pt;margin:0 0 2.5mm}
.jcard .blurb{color:#c7c9c4;font-size:9.4pt;line-height:1.5;margin:0 0 3mm}
.howto{border:1px solid #d6dad8;border-radius:2.5mm;padding:3.4mm 4.5mm;font-size:8.6pt;color:#4a4f4d;line-height:1.55;margin-bottom:5mm}
.howto b{color:#1c1f1e}
.howto ul{margin:1mm 0 0;padding-left:4.5mm}
h2.sec{font-family:"DejaVu Sans",sans-serif;font-weight:700;font-size:12pt;letter-spacing:.04em;text-transform:uppercase;border-bottom:1.5px solid #e0b13a;padding-bottom:1.6mm;margin:0 0 4mm}
.ch{border:1px solid #e3e5e3;border-radius:2.5mm;padding:3mm 4mm;margin-bottom:3mm;page-break-inside:avoid}
.ch h4{margin:0 0 1mm;font-size:10.4pt;font-weight:700}
.ch .who{font-size:9pt;color:#4a4f4d;margin:0 0 1.6mm}
.ch .pl{font-family:"DejaVu Sans",sans-serif;font-weight:700;font-size:6.8pt;letter-spacing:.16em;color:#9a7414;margin-top:1.6mm}
.ch .pr{background:#fff7dc;border:1px solid #ecd27a;border-radius:1.6mm;padding:1.8mm 2.6mm;font-size:8.4pt;line-height:1.45;margin-top:.6mm}
.ch a{font-size:7.6pt;color:#8a8f8c;text-decoration:none;font-weight:400}
.th{border:1px solid #e3e5e3;border-radius:2.5mm;padding:3mm 4mm;margin-bottom:3mm;page-break-inside:avoid}
.th h4{margin:0 0 .6mm;font-size:10.4pt}
.th p{margin:0 0 2mm;color:#4a4f4d;font-size:9pt}
.th a{display:inline-block;font-family:"DejaVu Sans",sans-serif;font-weight:700;font-size:7.4pt;background:#0f1513;color:#e0b13a;text-decoration:none;border-radius:1.4mm;padding:.8mm 2.2mm;margin:0 1.4mm 1.4mm 0}
.toc{page-break-before:always}
.toc .acth{font-family:"DejaVu Sans",sans-serif;font-weight:700;font-size:7.6pt;letter-spacing:.18em;color:#9a7414;margin:4mm 0 1mm}
.toc a{display:grid;grid-template-columns:9mm 1fr 15mm;text-decoration:none;padding:.9mm 0;border-bottom:1px solid #eef0ee;font-size:8.8pt}
.toc .n{color:#9a7414;font-weight:700}.toc .t{text-align:right;color:#8a8f8c}
.actpage{page-break-before:always;margin:4mm 0 5mm;background:#0f1513;color:#f2f0ea;border-radius:3mm;padding:5mm 7mm}
.actpage small{display:block;font-family:"DejaVu Sans",sans-serif;font-weight:700;letter-spacing:.24em;font-size:7.6pt;color:#e0b13a}
.actpage h2{font-family:"DejaVu Serif",serif;font-weight:700;font-size:16pt;margin:1.6mm 0 0}
.scene{margin-top:7mm}
.nav{display:flex;justify-content:space-between;font-size:7pt;margin-bottom:1.6mm}
.nav a{color:#9a9e9c;text-decoration:none}
.shead{display:flex;align-items:center;gap:2.6mm;border-bottom:1.5px solid #e0b13a;padding-bottom:1.6mm;margin-bottom:1.4mm;page-break-after:avoid}
.badge{background:#0f1513;color:#e0b13a;font-family:"DejaVu Sans",sans-serif;font-weight:700;font-size:7.4pt;border-radius:1.4mm;padding:.9mm 2mm;white-space:nowrap}
.shead h3{margin:0;font-size:10.6pt;font-weight:700;text-transform:uppercase;letter-spacing:.02em}
.slug{font-family:"DejaVu Sans",sans-serif;font-size:7.4pt;color:#7d827f;text-transform:uppercase;letter-spacing:.04em;margin-bottom:2mm;page-break-after:avoid}
.track{display:flex;gap:4.5mm;margin:0 0 2.6mm;font-size:7.8pt;color:#7d827f}
.track span{display:flex;align-items:center;gap:1.4mm}
.track i{display:inline-block;width:4.2mm;height:4.2mm;border:1.2px solid #c9971c;border-radius:1mm;font-style:normal;font-size:3pt;line-height:1;color:#fff;overflow:hidden}
.act{margin:2mm 0;color:#2e3230}
.act.open{font-style:italic;color:#3c403e;border-left:2px solid #e0b13a;padding-left:3.4mm}
.ln{margin:2mm 0 0;page-break-inside:avoid}
.ln .w{font-weight:700;font-size:7.8pt;letter-spacing:.1em;color:#1c1f1e}
.ln .w em{font-style:normal;font-weight:400;color:#8a8f8c;margin-left:1.4mm;letter-spacing:.04em}
.ln .s{margin-top:.3mm}
.ln .dir{color:#7d827f;font-style:italic}
.ln.sing .s{font-style:italic}
.aa{margin:.8mm 0 2.2mm;font-size:7.6pt;line-height:1.4;color:#5d625f;border:1px solid #e6e8e6;border-radius:1.6mm;padding:1.1mm 2.2mm;page-break-inside:avoid}
.aa b{color:#1c1f1e}
.card{display:flex;align-items:center;flex-wrap:wrap;gap:1.6mm;margin:2.8mm 0;background:#fff7dc;border:1px solid #ecd27a;border-radius:2mm;padding:2mm 3mm;page-break-inside:avoid}
.card small{font-weight:700;color:#9a7414;font-size:6.8pt;letter-spacing:.16em;margin-right:1.6mm}
.card p{margin:0;background:#fff;border:1px solid #d9dcd9;border-radius:1.2mm;padding:.5mm 1.8mm;font-weight:700;font-size:7.8pt}
.tc{margin:3mm 0;display:flex;align-items:center;gap:1.6mm;background:#fff7dc;border:1px solid #ecd27a;border-radius:2mm;padding:2mm 3mm;font-family:"DejaVu Sans",sans-serif;font-weight:700;font-size:7.8pt}
h2.sec{page-break-before:auto!important}
.ln .w{color:#1c1f1e!important}
.post{margin:3mm 0 1.6mm;border:1px solid #d6dad8;border-left:3px solid #1c1f1e;border-radius:1.6mm;padding:2mm 3mm;font-size:9pt;color:#2e3230;page-break-inside:avoid}
.trans{margin:1.6mm 0 2mm;background:#0f1513;color:#e9e6de;border-radius:1.6mm;padding:2mm 3mm;font-size:9pt;font-style:italic;page-break-inside:avoid}
.post span,.trans span{display:block;font-family:"DejaVu Sans",sans-serif;font-style:normal;font-weight:700;font-size:6.8pt;letter-spacing:.18em;margin-bottom:.8mm;color:#9a7414}
.trans span{color:#e0b13a}
.tc::before{content:"ON SCREEN";color:#9a7414;font-size:6.8pt;letter-spacing:.16em;margin-right:1.6mm}
"""

o = [f'''<!doctype html><html><head><meta charset="utf-8"><title>{e(cfg['title'])}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Figtree:ital,wght@0,400;0,600;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap">
<style>{css}</style></head><body>''']

h1 = cfg['title'].split(' ')
mid = len(h1) // 2
if JOURNAL:
    o.append(f'''<section><div class="jcard"><small>{e(cfg['kicker'])}</small><h1>{e(cfg['title'])}</h1><p class="tag">{e(cfg['tagline'])}</p><p class="blurb">{e(cfg['blurb'])}</p><div class="sub">''' + ' · '.join(f'{e(v)} {e(l.lower())}' for v, l in cfg['meta']) + '</div></div>')
else:
    o.append(f'''<section class="cover"><div><small class="m">{e(cfg['kicker'])}</small>
<h1 class="d">{e(' '.join(h1[:mid]))} <span>{e(' '.join(h1[mid:]))}</span></h1>
<p class="tag d">{e(cfg['tagline'])}</p><p>{e(cfg['blurb'])}</p>
<div class="spot"><b>{e(cfg.get('spot', 'PERFORMER TONIGHT'))}</b></div></div>
<div class="meta m">''' + ''.join(f'<div><b>{e(v)}</b><span>{e(l)}</span></div>' for v, l in cfg['meta']) + '</div></section>')

first = {}
for s in S:
    for it in s['items']:
        if it['k'] == 'line':
            first.setdefault(it['who'], s['n'])

opening_li = ('<li><b>Scene opening</b> (italic, gold rule): the establishing shot, before anyone speaks.</li>' if JOURNAL
              else '<li><b>Scene opening</b> (gold box): the establishing shot, before anyone speaks.</li>')
aa_li = ('<li><b>After-action</b> (small boxed line under each line of dialogue): ' if JOURNAL
         else '<li><b>After-action</b> (lilac box under each line): ')
o.append(('' if JOURNAL else '<section><h2 class="sec d">How to use this PDF</h2>')
         + '<div class="howto">' + ('<b>How to use this script:</b> ' if JOURNAL else '')
         + '<ul style="margin:0;padding-left:5mm">'
         + '<li><b>Tap</b> any scene in the contents or any thread to jump to it. Every scene has ◀ Previous, All scenes and Next ▶ links, and your PDF app\'s bookmarks list every scene.</li>'
         + opening_li
         + aa_li + '<b>Lip-sync</b> for the mouth and delivery, <b>Body</b> for posture and movement. Paste it into your video prompt for that shot.</li>'
         + '<li><b>Post-action</b> (outlined box at the end of a scene): what happens after the conversation, who stays behind and how they react. <b>Transition</b> (dark box): the bridge shot into the next scene, so the film flows without jumps.</li>'
         + '<li><b>Production checkboxes</b> on every scene (Images, Voice, Edited). Tick them as you go; most PDF apps save them.</li>'
         + '<li><b>Characters</b>: every character with an image prompt, next. Tap "first appears" to jump to their first scene.</li></ul></div>')
if chars:
    o.append('<h2 class="sec d" style="page-break-before:always">Characters &amp; image prompts</h2>'
             '<p style="color:#6b6260;margin-top:-2mm;font-size:9.4pt">Add this to every prompt: <i>cinematic film still, photorealistic, shot on ARRI Alexa, 35mm lens, shallow depth of field, natural skin texture, soft film grain, modern Lagos, Nigeria</i>. Save your best result for each main character as their reference face.</p>')
    for head, who, prompts in chars:
        key = re.sub(r'^\d+\.\s*', '', head).split(' (')[0].split(',')[0].upper()
        key = {'SIENNA VALE': 'SIENNA', 'ELI OKAFOR': 'ELI', 'ADA NWOSU': 'ADA', 'CHIOMA BELLO': 'NEWS ANCHOR', 'TUNDE ALLI': 'HOST',
               'BARRISTER FUNMI OKOYE': 'LAWYER', 'MR. OKONJO': 'EXECUTIVE', 'KOLA': 'STAGE MANAGER', 'SADE': 'WIG STYLIST', 'ZARA': 'STYLIST',
               'LOLA': 'DANCER', 'BLESSING': 'BLOGGER', 'KUNLE': 'PRODUCER', 'POLICE INSPECTOR': 'INSPECTOR', 'THE SUPERFAN': 'FAN IN FRONT ROW',
               'DELE': 'PHOTOGRAPHER', 'VENUE SECURITY MANAGER / SECURITY CHIEF': 'VENUE SECURITY MANAGER'}.get(key, key)
        link = f' <a href="#s{first[key]}">→ first appears in Scene {first[key]}</a>' if key in first else ''
        o.append(f'<div class="ch"><h4 class="d">{e(head)}{link}</h4>' + (f'<p class="who">{e(who)}</p>' if who else '')
                 + ''.join(f'<div class="pl">IMAGE PROMPT{e(lbl.upper())}</div><div class="pr">{e(pr)}</div>' for lbl, pr in prompts) + '</div>')
    if extras:
        o.append('<div class="ch"><h4 class="d">Extras &amp; crowds</h4>' + ''.join(f'<div class="pr" style="margin-bottom:1.4mm">{e(x)}</div>' for x in extras) + '</div>')
o.append('</section>')

if cfg.get('threads'):
    o.append('<section class="threads" style="page-break-before:always"><h2 class="sec d">Follow a story thread</h2>')
    for name, desc, titles in cfg['threads']:
        o.append(f'<div class="th"><h4 class="d">{e(name)}</h4><p>{e(desc)}</p>' + ''.join(f'<a href="#s{by_title[x]}">SCENE {by_title[x]}</a>' for x in titles) + '</div>')
    o.append('</section>')

o.append('<section class="toc" id="toc"><h2 class="sec d">Scenes</h2>')
for s in S:
    if s['n'] in acts:
        o.append(f'<div class="acth">{e(acts[s["n"]])}</div>')
    o.append(f'<a href="#s{s["n"]}"><span class="n m">{s["n"]:02d}</span><span>{e(tc(s["title"]))}</span><span class="t m">{e(s["time"].split("–")[0].split(" ")[0])}</span></a>')
o.append('</section>')


def aa_html(t):
    t = e(t)
    t = re.sub(r'^After action\.\s*', '', t)
    return re.sub(r'(Lip-sync:|Body(?: \([^)]*\))?:)', r'<b>\1</b>', t)


for s in S:
    n = s['n']
    if n in acts:
        a, _, b = acts[n].partition(' — ')
        o.append(f'<section class="actpage"><small>{e(a)}</small><h2 class="d">{e(tc(b) if b else a)}</h2></section>')
    prev = f'<a href="#s{n-1}">◀ Scene {n-1}</a>' if n > 1 else '<span></span>'
    nxt = f'<a href="#s{n+1}">Scene {n+1} ▶</a>' if n < last else '<span></span>'
    o.append(f'<section class="scene" id="s{n}"><div class="nav m">{prev}<a href="#toc">All scenes</a>{nxt}</div>'
             + (f'<div class="shead"><span class="badge">{e(s["time"])}</span><h3>Scene {n}: {e(s["title"])}</h3></div><div class="slug">{e(s["slug"])}</div>' if JOURNAL else
                f'<div class="shead"><div class="n m">SCENE {n} OF {last} · {e(s["time"])}</div><h3 class="d">{e(tc(s["title"]))}</h3><div class="slug m">{e(s["slug"])}</div></div>')
             + 
             f'<div class="track"><span><i>CHKs{n}x0</i>Images</span><span><i>CHKs{n}x1</i>Voice</span><span><i>CHKs{n}x2</i>Edited</span></div>')
    opened = False
    for it in s['items']:
        k = it['k']
        if k == 'act':
            txt = it['t']
            if txt.startswith('POST-ACTION'):
                o.append(f'<div class="post"><span>POST-ACTION</span>{e(txt.split("—", 1)[1].strip())}</div>')
            elif txt.startswith('TRANSITION'):
                o.append(f'<div class="trans"><span>TRANSITION ▸ NEXT SCENE</span>{e(txt.split("→", 1)[1].strip())}</div>')
            else:
                o.append(f'<div class="act{"" if opened else " open"}">{e(txt)}</div>')
            opened = True
        elif k == 'aa':
            o.append(f'<div class="aa">↳ {aa_html(it["t"])}</div>')
        elif k == 'line':
            opened = True
            body = ''.join(f'<span class="dir">({e(g["d"])})</span> ' if 'd' in g else e(g['s']) + ' ' for g in it['segs'])
            tag = f'<em>{e(it["tag"])}</em>' if it['tag'] else ''
            sing = ' sing' if 'SINGING' in it['tag'] else ''
            o.append(f'<div class="ln{sing}"><div class="w" style="color:{col(it["who"])}">{e(it["who"])}{tag}</div><div class="s">{body}</div></div>')
        elif k == 'card':
            o.append(f'<div class="card"><small class="m">{e(it["who"])}</small><p>{e(it["t"])}</p></div>')
        else:
            o.append(f'<div class="tc">{e(it["t"])}</div>')
    o.append('</section>')
o.append('<section style="text-align:center"><p class="d" style="font-size:20pt;margin-top:70mm">THE END</p><p class="m"><a href="#toc">↑ Back to all scenes</a></p></section></body></html>')
open(cfg['out_html'], 'w').write(''.join(o))
print('html written', cfg['out_html'])
