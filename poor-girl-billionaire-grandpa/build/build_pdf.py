"""Build script.pdf: the movie in standard screenplay format.

Run from anywhere:  python3 poor-girl-billionaire-grandpa/build/build_pdf.py
Needs Node with Playwright (render_pdf.js) for the Chromium print step.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_player import data, ROOT  # noqa: E402

S = data["scenes"]
TITLE = "A Poor Girl Helped a Billionaire CEO Grandpa Walk Again"
ACTS = {"cold": "Cold Open", "act1": "Act One", "act2": "Act Two", "climax": "Climax", "ending": "Ending"}
esc = lambda s: html.escape(str(s), quote=True)
PAREN = re.compile(r'<em class="p">(\(.*?\))</em>')

CSS = """
@page { size: A4; margin: 25mm 25mm 25mm 24mm; @top-right { content: counter(page) "."; font: 12pt 'Courier Prime', 'Courier New', monospace; } }
@page :first { @top-right { content: none } }
@page front { margin: 25mm 25mm 25mm 24mm; @top-right { content: none } }
html { margin: 0 } body { margin: 0; padding-left: 14mm; background: #fff; color: #000; font: 12pt/1.2 'Courier Prime', 'Courier New', Courier, monospace; }
p { margin: 0 }
.front { page: front }
.title-page { height: 247mm; position: relative; page-break-after: always }
.title-page .t { position: absolute; top: 80mm; left: 0; right: 0; text-align: center }
.title-page h1 { font-weight: 700; font-size: 12pt; text-transform: uppercase; margin: 0 0 12pt }
.title-page .by { margin-top: 24pt }
.title-page .foot { position: absolute; bottom: 0; left: 0; right: 0; display: flex; justify-content: space-between }
.chars h2 { font-weight: 700; font-size: 12pt; text-transform: uppercase; text-decoration: underline; margin: 0 0 12pt }
.chars p { margin-bottom: 12pt }
.chars b { text-transform: uppercase }
.scene { }
.head { position: relative; display: flex; gap: 0; font-weight: 700; text-transform: uppercase; margin: 24pt 0 12pt; break-after: avoid }
.scene:first-child .head { margin-top: 0 }
.head .n { position: absolute; left: -14mm; top: 0 }
.head .s { flex: 1 }
.head .n2 { margin-left: 6mm }
.act { margin: 12pt 0 }
.sp { margin: 12pt 0; break-inside: avoid }\n.cue { margin: 0 0 0 56mm; text-transform: uppercase }
.par { margin-left: 41mm; width: 64mm; padding-left: 1ch; text-indent: -1ch }
.dl { margin-left: 25mm; width: 89mm }
.super { margin: 12pt 0 }
.trans { text-align: right; text-transform: uppercase; margin: 12pt 0 }
em { font-style: italic }
strong { font-weight: 700 }
"""


def page(body, cls=""):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(TITLE)}</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap">'
            f'<style>{CSS}</style></head><body class="{cls}">{body}</body></html>')


def as_action(paren):
    """Turn a full-sentence direction like '(He points at the X-ray.)' into an action line."""
    t = paren.strip()[1:-1].strip()
    t = t[0].upper() + t[1:]
    t = t.rstrip(":").rstrip()
    return t if t[-1] in ".!?…" else t + "."


def dialogue(ln):
    """Standard screenplay speech: wrylies stay as parentheticals, full-sentence
    directions become action lines and the speech resumes with (CONT'D)."""
    name = esc(ln["who"]) + (f' ({esc(ln["tag"])})' if ln["tag"] else "")
    blocks, speech, spoke = [], [], False

    def close():
        nonlocal speech
        trailing = None
        if len(speech) > 1 and speech[-1].startswith('<p class="par">'):  # a speech never ends on a wryly
            trailing = re.sub(r'^<p class="par">|</p>$', "", speech.pop())
        if speech:
            cue = name + (" (CONT'D)" if spoke and not speech_has_new_cue[0] else "")
            blocks.append(f'<div class="sp"><p class="cue">{cue}</p>{"".join(speech)}</div>')
            speech = []
        if trailing:
            blocks.append(f'<p class="act">{as_action(trailing)}</p>')

    speech_has_new_cue = [True]
    for i, part in enumerate(PAREN.split(ln["html"])):
        part = part.strip()
        if not part:
            continue
        if i % 2:  # parenthetical
            if not part[1:2].isupper():  # "(quietly)", "(pointing his cane at her)"
                speech.append(f'<p class="par">{part}</p>')
            else:
                had_line = any('class="dl"' in x for x in speech)
                close()
                blocks.append(f'<p class="act">{as_action(part)}</p>')
                if had_line:
                    spoke = True
                speech_has_new_cue[0] = not spoke
        else:
            speech.append(f'<p class="dl">{part}</p>')
    close()
    return "".join(blocks)


def line(ln):
    t = ln["t"]
    if t == "dialogue":
        return dialogue(ln)
    if t == "screen":
        return f'<p class="super">SUPER: "{ln["html"].replace("<br>", " / ")}"</p>'
    if t == "fade":
        last = ln is S[-1]["lines"][-1]
        word = "FADE OUT." if last else ("FADE TO BLACK." if "BLACK" in ln["html"] else "FADE TO:")
        return f'<p class="trans">{word}</p>'
    return f'<p class="act">{ln["html"]}</p>'


# ---------- front matter: title page + characters ----------
chars = "".join(f'<p><b>{esc(c["name"])}</b> ({c["age"]}). {esc(c["role"][0].upper() + c["role"][1:])}.</p>'
                for c in data["cast"])
chars += "".join(f'<p><b>{esc(s["name"])}</b> {s["desc"]}</p>' for s in data["support"])
front = f"""
<div class="front">
  <section class="title-page">
    <div class="t"><h1>{esc(TITLE)}</h1><p>A feature-length drama</p><p class="by">Written by</p><p>[WRITER'S NAME]</p></div>
    <div class="foot"><span>Mary's AI Movies</span><span>Running time: 60 minutes</span></div>
  </section>
  <section class="chars"><h2>Characters</h2>{chars}</section>
</div>"""

# ---------- the screenplay ----------
body = []
for sc in S:
    body.append(f'<section class="scene" id="s{sc["n"]}"><div class="head"><span class="n">{sc["n"]}</span>'
                f'<span class="s">{esc(sc["slug"])}</span><span class="n2">{sc["n"]}</span></div>'
                + "".join(line(ln) for ln in sc["lines"]) + "</section>")

tmp = HERE / "_pdf"
tmp.mkdir(exist_ok=True)
(tmp / "front.html").write_text(page(front), encoding="utf-8")
(tmp / "body.html").write_text(page("".join(body)), encoding="utf-8")
for name in ("front", "body"):
    subprocess.run(["node", str(HERE / "render_pdf.js"), str(tmp / f"{name}.html"), str(tmp / f"{name}.pdf")], check=True)

# ---------- merge + bookmarks ----------
f_reader, b_reader = PdfReader(str(tmp / "front.pdf")), PdfReader(str(tmp / "body.pdf"))
off = len(f_reader.pages)
# Find each scene's page by its heading text, scanning forward in order.
squash = lambda t: re.sub(r"\s+", "", t).upper()
texts = [squash(p.extract_text() or "") for p in b_reader.pages]
dest, pi = {}, 0
for sc in S:
    key = squash(sc["slug"])[:40]
    while key not in texts[pi]:
        pi += 1
    dest[f's{sc["n"]}'] = pi + off
w = PdfWriter()
for p in list(f_reader.pages) + list(b_reader.pages):
    w.add_page(p)
w.add_outline_item("Title page", 0)
w.add_outline_item("Characters", 1)
cur, parent = None, None
for sc in S:
    if sc["section"] != cur:
        cur = sc["section"]
        parent = w.add_outline_item(ACTS[cur], dest[f's{sc["n"]}'])
    w.add_outline_item(f'{sc["n"]}. {sc["slug"].split(" — ")[0].title()}', dest[f's{sc["n"]}'], parent=parent)
w.add_metadata({"/Title": TITLE, "/Subject": "Screenplay"})
w.page_mode = "/UseOutlines"
out = ROOT / "script.pdf"
with open(out, "wb") as fh:
    w.write(fh)
print(f"wrote {out} · {len(w.pages)} pages")
