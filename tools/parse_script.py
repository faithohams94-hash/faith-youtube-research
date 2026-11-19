"""Parse a script.md into scene JSON for the player and PDF builders.

Usage: python3 tools/parse_script.py SCRIPT.md OUT.json
Item kinds: act (visual direction), aa (after-action note), line (dialogue),
card (ON SCREEN / ON PAPER / MEANWHILE), title (TITLE CARD), end.
"""
import json
import re
import sys

src, out = sys.argv[1], sys.argv[2]
t = open(src).read()
parts = re.split(r'^## SCENE (\d+) — (.+)$', t, flags=re.M)
scenes = []
for i in range(1, len(parts), 3):
    num, title, body = int(parts[i]), parts[i + 1].strip(), parts[i + 2]
    body = body.split('\n---')[0]
    lines = [l.strip() for l in body.strip().split('\n') if l.strip()]
    slug = re.sub(r'\*\*', '', lines[0])
    time = lines[1].strip('*()~')
    items = []
    for l in lines[2:]:
        m = re.match(r'^\*\*(ON SCREEN|ON PAPER|MEANWHILE)[^:]*:\*\* \*(.*)\*$', l)
        if m:
            items.append({'k': 'card', 'who': m.group(1), 't': re.sub(r'^"|"$', '', m.group(2).replace('*', ''))})
            continue
        m = re.match(r'^\*\*TITLE CARD:\*\* \*(.*)\*$', l)
        if m:
            items.append({'k': 'title', 't': m.group(1)})
            continue
        if l == '**END.**':
            items.append({'k': 'end', 't': 'END'})
            continue
        m = re.match(r"^\*\*([A-Z][A-Za-z .&'/,]*?)(?: \(([^)]*)\))?:\*\* (.*)$", l)
        if m:
            segs = []
            for p in re.split(r'(\*\([^)]*\)\*)', m.group(3)):
                if not p.strip():
                    continue
                segs.append({'d': p[2:-2]} if p.startswith('*(') else {'s': p.strip()})
            items.append({'k': 'line', 'who': m.group(1).strip(), 'tag': m.group(2) or '', 'segs': segs})
            continue
        if l.startswith('*↳'):
            items.append({'k': 'aa', 't': l.strip('*').lstrip('↳').strip()})
            continue
        items.append({'k': 'act', 't': l.strip('*') if l.startswith('*') and l.endswith('*') else l.replace('*', '')})
    scenes.append({'n': num, 'title': title, 'slug': slug, 'time': time, 'items': items})
json.dump(scenes, open(out, 'w'), ensure_ascii=False)
print(len(scenes), 'scenes;', sorted({it['who'] for s in scenes for it in s['items'] if it['k'] == 'line'}))
