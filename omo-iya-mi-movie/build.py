#!/usr/bin/env python3
"""Turn source-*.txt (in order) into index.html (screenplay layout). build.js prints it to PDF."""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "index.html"

TITLE = "ỌMỌ ÌYÁ MI"
SUBTITLE = "My Sister Destroyed My Marriage, Years Later I Bought His Mansion"
ENGLISH = "My Mother's Child"

esc = html.escape

# label for each card field, in display order, per card kind
FIELDS = {
    "CHAR": [("role", "Role"), ("age", "Age"), ("look", "Appearance"),
             ("body", "Body language and expressions"), ("voice", "Voice and speech"),
             ("nature", "Nature")],
    "LOC": [("where", "Where"), ("look", "Look"), ("light", "Light and color"),
            ("sound", "Sound"), ("mood", "Mood")],
}
PROMPTS = [("prompt", "Image prompt"), ("vprompt", "Voice prompt")]


def inline(text: str) -> str:
    return esc(text, quote=False)


def parse(lines):
    body = []
    toc = []
    scene_no = 0
    dlg = None   # [name, paren, [lines]]
    card = None  # (kind, name, {key: value})

    def flush():
        nonlocal dlg, card
        if dlg:
            name, paren, parts = dlg
            body.append('<div class="dlg">')
            body.append(f'<div class="who">{inline(name)}</div>')
            if paren:
                body.append(f'<div class="paren">({inline(paren)})</div>')
            body.append(f'<div class="said">{inline(" ".join(parts))}</div>')
            body.append("</div>")
            dlg = None
        if card:
            kind, name, f = card
            body.append('<div class="card">')
            body.append(f'<div class="cname">{inline(name)}</div>')
            for key, label in FIELDS[kind]:
                if key in f:
                    body.append(f'<p><span class="lab">{label}.</span> {inline(f[key])}</p>')
            for key, label in PROMPTS:
                if key in f:
                    body.append(f'<div class="plab">{label}</div>')
                    body.append(f'<div class="prompt">{inline(f[key])}</div>')
            body.append("</div>")
            card = None

    for raw in lines:
        line = raw.rstrip("\n")
        if not line.strip():
            flush()
            continue

        if line.startswith("@"):
            flush()
            m = re.match(r"^@(.+?)(?: \((.*)\))?$", line)
            if not m:
                sys.exit(f"bad dialogue header: {line!r}")
            dlg = [m.group(1).strip(), m.group(2), []]
            continue
        if dlg is not None:
            dlg[2].append(line.strip())
            continue

        m = re.match(r"^#(CHAR|LOC) (.+)$", line)
        if m:
            flush()
            card = (m.group(1), m.group(2).strip(), {})
            continue
        if card is not None:
            k, _, v = line.partition(":")
            card[2][k.strip()] = v.strip()
            continue

        if line.startswith("#H1 "):
            flush()
            title = line[4:].strip()
            toc.append((1, title))
            body.append(f'<h1 class="pb">{inline(title)}</h1>')
        elif line.startswith("#H2 "):
            title = line[4:].strip()
            toc.append((2, title))
            cls = "pb" if title.startswith(("Act ", "Post-Credit")) else ""
            body.append(f'<h2 class="{cls}">{inline(title)}</h2>')
        elif line.startswith("#H3 "):
            body.append(f'<h3>{inline(line[4:].strip())}</h3>')
        elif line.startswith("#P "):
            body.append(f'<p class="prose">{inline(line[3:].strip())}</p>')
        elif line.startswith("#B "):
            body.append(f'<p class="bullet">{inline(line[3:].strip())}</p>')
        elif line.startswith("#SC "):
            parts = [p.strip() for p in line[4:].split("|")]
            where, when = parts[1], (parts[2] if len(parts) > 2 else "")
            scene_no += 1
            heading = where + (f" — {when}" if when else "")
            body.append(f'<div class="scene"><span class="num">{scene_no}</span>{inline(heading)}</div>')
        elif line.startswith("#SET "):
            body.append(f'<div class="set"><b>Setting.</b> {inline(line[5:].strip())}</div>')
        elif line.startswith("#RX "):
            body.append(f'<p class="rx"><b>Reaction.</b> {inline(line[4:].strip())}</p>')
        elif line.startswith("#TR "):
            body.append(f'<div class="trans">{inline(line[4:].strip())}</div>')
        elif line.startswith("#TW "):
            body.append(f'<div class="note"><b>Director\'s note.</b> {inline(line[4:].strip())}</div>')
        elif line.startswith("#TITLE "):
            t = line[7:].strip()
            body.append(f'<div class="titlecard">{inline(t)}</div>')
        else:
            body.append(f'<p class="action">{inline(line.strip())}</p>')
    flush()
    return body, toc


def main():
    files = sorted(HERE.glob("source-*.txt"))
    if not files:
        sys.exit("no source-*.txt files found")
    lines = []
    for f in files:
        lines.extend(f.read_text(encoding="utf-8").splitlines())
        lines.append("")
    body, toc = parse(lines)

    toc_html = ['<div class="toc"><h1>Contents</h1>']
    for level, title in toc:
        toc_html.append(f'<div class="toc{level}">{inline(title)}</div>')
    toc_html.append("</div>")

    css = (HERE / "style.css").read_text(encoding="utf-8")
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{inline(TITLE)} | {inline(ENGLISH)}</title>
<style>{css}</style></head><body>
<section class="cover">
  <div class="kicker">A Nollywood Feature Screenplay</div>
  <div class="ctitle">{inline(TITLE)}</div>
  <div class="cen">{inline(ENGLISH)}</div>
  <div class="rule"></div>
  <div class="csub">{inline(SUBTITLE)}</div>
  <div class="cmeta">Family drama and thriller<br>Written for YouTube release<br>Target runtime: 95 to 105 minutes<br>Draft 2: full visual detail edition</div>
</section>
{''.join(toc_html)}
{chr(10).join(body)}
</body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT} ({len(doc):,} bytes, {len(toc)} headings, {scene_count(body)} scenes)")


def scene_count(body):
    return sum(1 for b in body if b.startswith('<div class="scene">'))


if __name__ == "__main__":
    main()
