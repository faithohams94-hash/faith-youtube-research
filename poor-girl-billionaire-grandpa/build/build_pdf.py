"""Build script.pdf: a print-ready, clickable PDF of the movie script.

Run from anywhere:  python3 poor-girl-billionaire-grandpa/build/build_pdf.py
Needs Node with Playwright (render_pdf.js) for the Chromium print step.
"""
import html
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_player import data, ROOT  # noqa: E402

D = data
S = D["scenes"]
SEC = {s["key"]: s for s in D["sections"]}
SEC_TITLE = {"cold": "Cold open", "act1": "Act one", "act2": "Act two", "climax": "Climax", "ending": "Ending"}
COLORS = {"IRETI": "#c98a00", "CHIEF": "#3b2a1c", "FEMI": "#2f63b8", "GABRIEL": "#16836a",
          "MAMA FUNMI": "#b8456a", "DAYO": "#4f8a1f", "RONKE": "#c9301f", "MALLAM AUDU": "#8a5a1e",
          "DR. HASSAN": "#2c7aa0", "LEKAN": "#7a3fbf"}
esc = lambda s: html.escape(str(s), quote=True)
col = lambda k: COLORS.get(k, "#6b5a48")


def arc_svg(w=1000, h=280, pad=34):
    n = len(S)
    xs = lambda i: pad + i * (w - 2 * pad) / (n - 1)
    ys = lambda v: h - pad - (v / 100) * (h - 2 * pad - 30)
    P = [(xs(i), ys(v)) for i, v in enumerate(D["tension"])]
    d = f"M{P[0][0]:.1f},{P[0][1]:.1f}"
    for i in range(n - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(n - 1, i + 2)]
        d += (f" C{p1[0] + (p2[0] - p0[0]) / 6:.1f},{p1[1] + (p2[1] - p0[1]) / 6:.1f}"
              f" {p2[0] - (p3[0] - p1[0]) / 6:.1f},{p2[1] - (p3[1] - p1[1]) / 6:.1f} {p2[0]:.1f},{p2[1]:.1f}")
    out = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
           '<defs><linearGradient id="arc" x1="0" x2="1"><stop offset="0" stop-color="#e0402f"/>'
           '<stop offset=".7" stop-color="#f08327"/><stop offset="1" stop-color="#f2b632"/></linearGradient></defs>',
           f'<path d="{d}" fill="none" stroke="url(#arc)" stroke-width="5" stroke-linecap="round"/>']
    for i, (x, y) in enumerate(P):
        sc = S[i]
        beat = next((b for b in D["sections"] if b["dot"] == sc["n"]), None)
        out.append(f'<a href="#s{sc["n"]}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{11 if beat else 6}" '
                   f'fill="{"#f2b632" if beat else SEC[sc["section"]]["color"]}" stroke="#fffaf2" stroke-width="2.5"/></a>')
        if beat:
            ly = y + 32 if beat["key"] in ("act1", "climax") else y - 20
            out.append(f'<text x="{x:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="15" '
                       f'font-family="Courier Prime, monospace" fill="#2a1d12">{esc(beat["name"])}</text>')
    out.append("</svg>")
    return "".join(out)


def line_html(ln):
    t = ln["t"]
    if t == "dialogue":
        tag = f'<span class="tg">{esc(ln["tag"])}</span>' if ln["tag"] else ""
        return (f'<div class="ln dlg"><div class="who" style="color:{col(ln.get("k"))}">{esc(ln["who"])}{tag}</div>'
                f'<div class="say">{ln["html"]}</div></div>')
    if t in ("establish", "aftermath"):
        return f'<div class="ln {t}"><span class="lab">{t.title()}</span><p>{ln["html"]}</p></div>'
    if t == "screen":
        return f'<div class="ln screen"><span class="lab">On screen · {esc(ln["label"])}</span><p>{ln["html"]}</p></div>'
    if t == "fade":
        return f'<div class="ln fade"><span>{ln["html"]}</span></div>'
    return f'<div class="ln act"><p>{ln["html"]}</p></div>'


def guess_box(p):
    letters = "ABCD"
    opts = "".join(f"<li><b>{letters[i]}</b> {esc(o)}</li>" for i, o in enumerate(p["o"]))
    return (f'<div class="guess"><span class="lab">Pause and guess · what happens next?</span>'
            f'<p class="q">{esc(p["q"])}</p><ul>{opts}</ul>'
            f'<p class="go">The answer comes in <a href="#s{p["rev"]}">Scene {p["rev"]}</a> · '
            f'<a href="#ans-{p["id"]}">answer key</a></p></div>')


parts = []

# ---------- cover ----------
parts.append(f"""
<section class="cover">
  <div class="cv-top">Mary's AI Movies · Full movie script</div>
  <div class="cv-mid">
    <div class="cv-eyebrow">An AI Nollywood movie · 60 minutes · 32 scenes</div>
    <h1 class="cv-title">A Poor Girl Helped a Billionaire CEO Grandpa <em>Walk Again</em></h1>
    <p class="cv-log">{D["logline"]}</p>
    <p class="cv-thesis">{esc(D["contradiction"])}</p>
  </div>
  <div class="cv-bot"><span>Written by [WRITER'S NAME]</span><span>Dialogue-led · about 90% dialogue</span></div>
</section>""")

# ---------- contents ----------
rows, cur = [], None
for sc in S:
    if sc["section"] != cur:
        cur = sc["section"]
        s = SEC[cur]
        rows.append(f'<div class="tc-sec" style="--c:{s["color"]}">{esc(SEC_TITLE[cur])} · {esc(s["beat"])}</div>')
    rows.append(f'<a class="tc-row" href="#s{sc["n"]}"><span class="n">{sc["n"]}</span>'
                f'<span class="t">{esc(sc["title"])}</span><span class="tm">{sc["time"][0]}</span></a>')
parts.append(f"""
<section class="page" id="contents">
  <h1 class="ph">Contents</h1>
  <p class="intro">Every line below is a link. Tap a scene to jump to it. Each scene has a <b>↑ Contents</b> link to bring you back here, and the PDF's bookmarks panel lists every scene too.</p>
  <div class="tc-extra">
    <a href="#structure">How this story is built</a><a href="#cast">The cast and AI prompts</a>
    <a href="#locations">Key locations</a><a href="#loops">Open questions</a><a href="#answers">Answer key</a>
  </div>
  <div class="tc">{''.join(rows)}</div>
</section>""")

# ---------- structure ----------
beats = "".join(
    f'<a class="beat" href="#s{next(x["n"] for x in S if x["section"] == b["key"])}" style="--c:{b["color"]}">'
    f'<span class="k">{esc(b["name"])}</span><b>{esc(b["beat"])}</b><span>{esc(b["desc"])}</span>'
    f'<span class="tm">{[x for x in S if x["section"] == b["key"]][0]["time"][0]}–{[x for x in S if x["section"] == b["key"]][-1]["time"][1]}</span></a>'
    for b in D["sections"])
parts.append(f"""
<section class="page" id="structure">
  <h1 class="ph">How this story is built</h1>
  <p class="intro">The 1M-view structure: start inside the conflict and never let the tension rest. Each dot on the curve is a scene, and each dot is a link.</p>
  <div class="arc">{arc_svg()}</div>
  <div class="beats">{beats}</div>
  <h2 class="sh">The contradiction</h2>
  <p class="big">{esc(D["contradiction"])}</p>
  <h2 class="sh">Production rules for every scene</h2>
  <ul class="rules">
    <li><b>Establish.</b> Open on scenery for 3–5 seconds so the viewer knows where we are before anyone speaks.</li>
    <li><b>The scene.</b> Clean, cinematic shots with the emotion clear on every face.</li>
    <li><b>Aftermath.</b> Show the consequence: the reaction, the silence, the decision.</li>
    <li><b>Fade.</b> Every scene ends on a fade, so cuts never feel abrupt.</li>
    <li><b>Same face, every shot.</b> Use one reference image per character (see the cast pages) and check hands, props and on-screen text before upload.</li>
  </ul>
</section>""")

# ---------- cast ----------
cards = []
for c in D["cast"]:
    scenes = " ".join(f'<a href="#s{n}">{n}</a>' for n in c["scenes"])
    extra = ""
    if c["body"]:
        extra += f'<p><b>Body language:</b> {c["body"]}</p>'
    if c["wardrobe"]:
        extra += f'<p><b>Wardrobe:</b> {c["wardrobe"]}</p>'
    cards.append(f"""<article class="cc" style="--c:{col(c['key'])}">
      <h3>{esc(c['name'])} <span>({c['age']}) · {esc(c['role'])}</span></h3>
      {f"<p>{c['who']}</p>" if c['who'] else ""}{extra}
      <div class="prompt"><span class="lab">AI image prompt</span>{esc(c['prompt'])}</div>
      <p class="in">In scenes: {scenes}</p></article>""")
sup = "".join(f'<li><b>{esc(s["name"])}</b> {s["desc"]}</li>' for s in D["support"])
locs = "".join(f'<li><b>{esc(l["name"])}.</b> {esc(l["desc"])}</li>' for l in D["locations"])
parts.append(f"""
<section class="page" id="cast">
  <h1 class="ph">The cast</h1>
  <p class="intro">Generate one reference image per character from the AI prompt and attach it to every shot so the face never changes. Scene numbers are links.</p>
  <div class="cast">{''.join(cards)}</div>
  <h2 class="sh">Supporting cast</h2><ul class="plain">{sup}</ul>
  <h2 class="sh" id="locations">Key locations</h2><ul class="plain">{locs}</ul>
</section>""")

# ---------- open loops ----------
loop_rows = "".join(
    f'<tr><td>{esc(p["q"])}</td><td><a href="#s{p["at"]}">Scene {p["at"]}</a></td>'
    f'<td><a href="#s{p["rev"]}">Scene {p["rev"]}</a></td></tr>' for p in D["polls"])
parts.append(f"""
<section class="page" id="loops">
  <h1 class="ph">Open questions that keep viewers watching</h1>
  <p class="intro">Each question is planted in one scene and answered much later. In the script, a <b>Pause and guess</b> box marks each one. The answers are in the <a href="#answers">answer key</a> at the back, so the reader isn't spoiled.</p>
  <table class="loops"><thead><tr><th>Question</th><th>Planted</th><th>Answered</th></tr></thead><tbody>{loop_rows}</tbody></table>
</section>""")

# ---------- script ----------
polls_at = {}
for p in D["polls"]:
    polls_at.setdefault(p["at"], []).append(p)
cur = None
for sc in S:
    if sc["section"] != cur:
        cur = sc["section"]
        s = SEC[cur]
        parts.append(f'<section class="divider" style="--c:{s["color"]}"><span class="k">{esc(SEC_TITLE[cur])}</span>'
                     f'<h1>{esc(s["beat"])}</h1><p>{esc(s["desc"])}</p></section>')
    slug = sc["slug"].split(" — ")
    body = "".join(line_html(ln) for ln in sc["lines"])
    guesses = "".join(guess_box(p) for p in polls_at.get(sc["n"], []))
    parts.append(f"""
<section class="scene" id="s{sc['n']}">
  <div class="sh-top"><span class="chip" style="--c:{SEC[sc['section']]['color']}">{esc(SEC_TITLE[sc['section']])}</span>
    <span class="meta">Scene {sc['n']} of 32 · {sc['time'][0]}–{sc['time'][1]}</span><a class="up" href="#contents">↑ Contents</a></div>
  <h2 class="st">{sc['n']}. {esc(sc['title'])}</h2>
  <div class="slug"><b>{esc(slug[0])}</b> {esc(' — '.join(slug[1:]))}</div>
  <div class="lines">{body}</div>{guesses}
</section>""")

# ---------- answer key ----------
ans = "".join(
    f'<li id="ans-{p["id"]}"><p class="q">{esc(p["q"])}</p><p><b>{esc(p["o"][p["a"]])}.</b> {esc(p["why"])}</p>'
    f'<p class="go">Planted in <a href="#s{p["at"]}">Scene {p["at"]}</a> · revealed in <a href="#s{p["rev"]}">Scene {p["rev"]}</a></p></li>'
    for p in D["polls"])
parts.append(f"""
<section class="page" id="answers">
  <h1 class="ph">Answer key</h1>
  <p class="intro">Spoilers. Read only after the scene that reveals each answer.</p>
  <ol class="answers">{ans}</ol>
  <div class="lesson"><p>You may be sitting in the darkest room of your life.</p><p>Open one inch of curtain.</p><p><em>Hope only needs one inch.</em></p></div>
</section>""")

CSS = """
@page { size: A4; margin: 16mm 16mm 18mm;
  @bottom-left { content: "A Poor Girl Helped a Billionaire CEO Grandpa Walk Again"; font: 8pt 'Courier Prime', monospace; color: #8a7660; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 8pt 'Courier Prime', monospace; color: #8a7660; } }
@page :first { margin: 0; @bottom-left { content: none } @bottom-right { content: none } }
:root { --paper:#fffaf2; --ink:#21170f; --muted:#6b5a48; --rule:#e6d8c3; --gold:#f2b632; --gold-d:#a8730a; --red:#e0402f; --night:#140f0b;
  --display:'Anton', Impact, 'Arial Narrow', sans-serif; --body:'Source Sans 3', 'Segoe UI', Arial, sans-serif; --slug:'Courier Prime', 'Courier New', monospace; }
* { box-sizing: border-box }
html, body { margin:0; background: var(--paper); color: var(--ink); font-family: var(--body); font-size: 10.5pt; line-height: 1.45;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
a { color: var(--gold-d); text-decoration: none }
h1, h2, h3 { margin: 0; font-weight: 400 }
.lab { display:block; font: 700 7.5pt var(--slug); letter-spacing: .14em; text-transform: uppercase; margin-bottom: 2pt }

.cover { width: 210mm; height: 297mm; background: radial-gradient(80% 50% at 50% 0%, rgba(242,182,50,.28), transparent 70%), var(--night);
  color: #f6eee3; padding: 22mm 20mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
.cv-top, .cv-bot { font: 9pt var(--slug); letter-spacing: .16em; text-transform: uppercase; color: var(--gold) }
.cv-bot { display:flex; justify-content: space-between; color: #bba98f }
.cv-eyebrow { font: 10pt var(--slug); letter-spacing: .14em; text-transform: uppercase; color: var(--red); margin-bottom: 8mm }
.cv-title { font-family: var(--display); text-transform: uppercase; font-size: 54pt; line-height: .98; }
.cv-title em { font-style: normal; color: var(--gold) }
.cv-log { font-size: 12.5pt; color: #d9cbb6; max-width: 150mm; margin: 10mm 0 4mm }
.cv-thesis { font-size: 13pt; font-weight: 700; color: #fff; max-width: 150mm; border-left: 3pt solid var(--gold); padding-left: 4mm; margin: 0 }

.page { page-break-before: always }
.ph { font-family: var(--display); text-transform: uppercase; font-size: 30pt; line-height: 1; margin-bottom: 4mm }
.intro { color: var(--muted); max-width: 150mm; margin: 0 0 6mm }
.sh { font-family: var(--display); text-transform: uppercase; font-size: 16pt; margin: 8mm 0 3mm }
.big { font-size: 15pt; font-weight: 700; max-width: 160mm; margin: 0 }

.tc-extra { display:flex; flex-wrap: wrap; gap: 3mm; margin-bottom: 5mm }
.tc-extra a { border: 1px solid var(--rule); border-radius: 20pt; padding: 1.5mm 4mm; font-weight: 600; color: var(--ink) }
.tc { columns: 2; column-gap: 9mm }
.tc-sec { font: 700 8pt var(--slug); letter-spacing: .12em; text-transform: uppercase; color: var(--c); margin: 4mm 0 1.5mm; break-after: avoid; border-bottom: 1.5pt solid var(--c); padding-bottom: 1mm }
.tc-row { display: grid; grid-template-columns: 8mm 1fr auto; gap: 2mm; color: var(--ink); padding: 1.1mm 0; border-bottom: 1px dotted var(--rule); break-inside: avoid; font-size: 10pt }
.tc-row .n { font: 700 9pt var(--slug); color: var(--gold-d) }
.tc-row .tm { font: 8.5pt var(--slug); color: var(--muted) }

.arc { border: 1px solid var(--rule); border-radius: 4mm; padding: 3mm; background: #fff }
.arc svg { width: 100%; height: auto; display: block }
.beats { display: grid; grid-template-columns: repeat(5, 1fr); gap: 3mm; margin-top: 4mm }
.beat { border-top: 2.5pt solid var(--c); padding-top: 2mm; display: grid; gap: 1mm; color: var(--ink); font-size: 9pt }
.beat .k { font: 700 7.5pt var(--slug); letter-spacing: .12em; text-transform: uppercase; color: var(--c) }
.beat b { font-size: 10.5pt }
.beat .tm { font: 8pt var(--slug); color: var(--muted) }
.rules { margin: 0; padding-left: 5mm } .rules li { margin-bottom: 1.5mm }

.cast { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm }
.cc { border: 1px solid var(--rule); border-top: 3pt solid var(--c); border-radius: 3mm; padding: 3.5mm; background: #fff; break-inside: avoid; font-size: 9pt; display: grid; gap: 1.5mm; align-content: start }
.cc h3 { font-family: var(--display); text-transform: uppercase; font-size: 14pt; line-height: 1.05; color: var(--c) }
.cc h3 span { font-family: var(--body); text-transform: none; font-size: 9pt; color: var(--muted); font-weight: 600 }
.cc p { margin: 0 }
.prompt { font: 8pt/1.45 var(--slug); background: #f6efe3; border-radius: 2mm; padding: 2.5mm; color: var(--ink) }
.prompt .lab { color: var(--gold-d) }
.cc .in { font-size: 8.5pt; color: var(--muted) } .cc .in a { font-weight: 700; margin-right: 1mm }
.plain { margin: 0; padding-left: 5mm; font-size: 9.5pt } .plain li { margin-bottom: 1.5mm; break-inside: avoid }

table.loops { width: 100%; border-collapse: collapse; font-size: 10pt }
table.loops th { text-align: left; font: 700 8pt var(--slug); letter-spacing: .1em; text-transform: uppercase; color: var(--muted); border-bottom: 1.5pt solid var(--ink); padding: 2mm }
table.loops td { border-bottom: 1px solid var(--rule); padding: 2.5mm 2mm; vertical-align: top }
table.loops td:not(:first-child) { white-space: nowrap; font-weight: 700 }

.divider { page-break-before: always; padding-top: 70mm; border-top: 0 }
.divider .k { font: 700 11pt var(--slug); letter-spacing: .2em; text-transform: uppercase; color: var(--c) }
.divider h1 { font-family: var(--display); text-transform: uppercase; font-size: 46pt; line-height: 1; margin: 3mm 0 4mm; border-bottom: 4pt solid var(--c); padding-bottom: 4mm }
.divider p { font-size: 13pt; color: var(--muted); max-width: 150mm }
.divider + .scene { page-break-before: always }

.scene { margin-top: 9mm }
.sh-top { display: flex; align-items: center; gap: 3mm; break-after: avoid }
.chip { font: 700 7.5pt var(--slug); letter-spacing: .12em; text-transform: uppercase; background: var(--c); color: #1b1305; border-radius: 1mm; padding: .7mm 2mm }
.meta { font: 8.5pt var(--slug); color: var(--muted); flex: 1 }
.up { font: 700 8pt var(--slug) }
.st { font-family: var(--display); text-transform: uppercase; font-size: 22pt; line-height: 1.05; margin: 1.5mm 0 1mm; break-after: avoid }
.slug { font: 9pt var(--slug); text-transform: uppercase; color: var(--muted); padding-bottom: 2.5mm; border-bottom: 1px dashed var(--rule); margin-bottom: 3mm; break-after: avoid }
.slug b { color: var(--ink) }
.lines { display: grid; gap: 1.8mm }
.ln p { margin: 0 }
.ln.act p { font-style: italic; color: var(--muted); padding-left: 3mm; border-left: 1.5pt solid var(--rule) }
.ln.act p em, .ln.establish p em, .ln.aftermath p em { font-style: normal }
.ln.establish, .ln.aftermath { background: #f6efe3; border-radius: 2mm; padding: 2mm 3mm; break-inside: avoid }
.ln.establish .lab { color: var(--gold-d) } .ln.aftermath .lab { color: var(--red) }
.ln.establish p, .ln.aftermath p { font-style: italic; color: #4a3b2c }
.ln.dlg { display: grid; grid-template-columns: 33mm 1fr; gap: 3mm; break-inside: avoid }
.who { font: 700 8.5pt var(--slug); letter-spacing: .04em; text-transform: uppercase; padding-top: .6mm }
.who .tg { display: block; font-weight: 400; font-size: 7.5pt; color: var(--muted) }
.say { font-size: 10.5pt }
.say em.p { color: var(--muted); font-size: 9pt }
.ln.screen { background: var(--night); color: #f6eee3; text-align: center; border-radius: 2mm; padding: 3mm; break-inside: avoid }
.ln.screen .lab { color: #9b8a74 }
.ln.screen p { font-family: var(--display); text-transform: uppercase; font-size: 15pt; line-height: 1.15; color: var(--gold) }
.ln.screen p em { font-style: normal }
.ln.fade { text-align: center; font: 8pt var(--slug); letter-spacing: .3em; color: var(--muted); text-transform: uppercase; padding: 1mm 0 }

.guess { margin-top: 4mm; border: 1.5pt dashed var(--gold); border-radius: 3mm; padding: 3mm 4mm; background: #fff8e6; break-inside: avoid }
.guess .lab { color: var(--gold-d) }
.guess .q { font-weight: 700; font-size: 11pt; margin: 1mm 0 }
.guess ul { list-style: none; margin: 0 0 1.5mm; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 1mm 4mm; font-size: 9.5pt }
.guess ul b { color: var(--gold-d); margin-right: 1mm }
.guess .go, .answers .go { font: 8.5pt var(--slug); margin: 0; color: var(--muted) }
.guess .go a, .answers .go a { font-weight: 700 }

.answers { padding-left: 6mm; margin: 0 } .answers li { margin-bottom: 4mm; break-inside: avoid } .answers p { margin: 0 0 .8mm }
.answers .q { font-weight: 700 }
.lesson { margin-top: 12mm; background: var(--night); color: #f6eee3; border-radius: 4mm; padding: 10mm; text-align: center;
  font-family: var(--display); text-transform: uppercase; font-size: 16pt; line-height: 1.3 }
.lesson p { margin: 0 } .lesson em { font-style: normal; color: var(--gold) }
"""

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>A Poor Girl Helped a Billionaire CEO Grandpa Walk Again</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=Courier+Prime:wght@400;700&display=swap">
<style>{CSS}</style></head><body>{''.join(parts)}</body></html>"""

html_path = HERE / "script-print.html"
html_path.write_text(doc, encoding="utf-8")
out = ROOT / "script.pdf"
subprocess.run(["node", str(HERE / "render_pdf.js"), str(html_path), str(out)], check=True)

# Clean bookmarks: front matter, then each part with its scenes, then the answer key.
from pypdf import PdfReader, PdfWriter  # noqa: E402

reader = PdfReader(str(out))
pages = {k.lstrip("/"): reader.get_destination_page_number(v) for k, v in reader.named_destinations.items()}
writer = PdfWriter(clone_from=reader)
writer.add_outline_item("Cover", 0)
for key, label in [("contents", "Contents"), ("structure", "How this story is built"),
                   ("cast", "The cast and AI prompts"), ("locations", "Key locations"),
                   ("loops", "Open questions")]:
    writer.add_outline_item(label, pages[key])
cur, parent = None, None
for sc in S:
    if sc["section"] != cur:
        cur = sc["section"]
        parent = writer.add_outline_item(f'{SEC_TITLE[cur]}: {SEC[cur]["beat"]}', max(0, pages[f's{sc["n"]}'] - 1))
    writer.add_outline_item(f'{sc["n"]}. {sc["title"]}  ({sc["time"][0]})', pages[f's{sc["n"]}'], parent=parent)
writer.add_outline_item("Answer key", pages["answers"])
writer.add_metadata({"/Title": "A Poor Girl Helped a Billionaire CEO Grandpa Walk Again",
                     "/Subject": "60-minute AI Nollywood movie script"})
writer.page_mode = "/UseOutlines"
with open(out, "wb") as fh:
    writer.write(fh)
print(f"wrote {out} · {len(reader.pages)} pages")
