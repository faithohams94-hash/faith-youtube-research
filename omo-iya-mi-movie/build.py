#!/usr/bin/env python3
"""Turn source.txt into index.html (screenplay layout). build.js prints it to PDF."""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "source.txt"
OUT = HERE / "index.html"

TITLE = "ỌMỌ ÌYÁ MI"
SUBTITLE = "My Sister Destroyed My Marriage, Years Later I Bought His Mansion"
ENGLISH = "My Mother's Child"

esc = html.escape


def inline(text: str) -> str:
    return esc(text, quote=False)


def parse(lines):
    body = []
    toc = []
    scene_no = 0
    dlg = None   # [name, paren, [lines]]
    card = None  # (name, {key: value})

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
            name, f = card
            body.append('<div class="card">')
            body.append(f'<div class="cname">{inline(name)}</div>')
            for key, label in (("role", "Role"), ("age", "Age"), ("look", "Appearance"), ("nature", "Nature")):
                if key in f:
                    body.append(f'<p><span class="lab">{label}.</span> {inline(f[key])}</p>')
            if "prompt" in f:
                body.append('<div class="plab">Image prompt</div>')
                body.append(f'<div class="prompt">{inline(f["prompt"])}</div>')
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

        if line.startswith("#CHAR "):
            flush()
            card = (line[6:].strip(), {})
            continue
        if card is not None:
            k, _, v = line.partition(":")
            card[1][k.strip()] = v.strip()
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
    lines = SRC.read_text(encoding="utf-8").splitlines()
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
  <div class="cmeta">Family drama and thriller<br>Written for YouTube release<br>Target runtime: 95 to 105 minutes<br>Draft 1</div>
</section>
{''.join(toc_html)}
{chr(10).join(body)}
</body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT} ({len(doc):,} bytes, {len(toc)} headings)")


if __name__ == "__main__":
    main()
