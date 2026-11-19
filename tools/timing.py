"""Fill '*(~)*' scene timing lines from dialogue length.

Usage: python3 tools/timing.py SCRIPT.md [SECONDS_OF_VISUALS_PER_SCENE]
Resets every timing line, then estimates each scene as spoken words at
140 wpm (narration at 120 wpm) plus a fixed number of seconds for visuals.
"""
import re
import sys

p = sys.argv[1]
visual = float(sys.argv[2]) if len(sys.argv) > 2 else 12
t = open(p).read()
t = re.sub(r'^\*\(~[^)]*\)\*$', '*(~)*', t, flags=re.M)
parts = re.split(r'(^## SCENE \d+ — .+$)', t, flags=re.M)
out, cur, sp_total = parts[0], 0.0, 0


def fmt(s):
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


for i in range(1, len(parts), 2):
    h, b = parts[i], parts[i + 1]
    sp = nar = 0
    for l in b.split('\n'):
        m = re.match(r'^\*\*([A-Z][^*]*?):\*\* (.*)$', l)
        if not m or m.group(1).startswith(('ON ', 'MEANWHILE', 'TITLE')):
            continue
        n = len(re.sub(r'\*\([^)]*\)\*', '', m.group(2)).split())
        if m.group(1).startswith('NARRATOR'):
            nar += n
        else:
            sp += n
    dur = sp / 140 * 60 + nar / 120 * 60 + visual
    sp_total += sp + nar
    last = i >= len(parts) - 2
    b = b.replace('*(~)*', f'*(~{fmt(cur)} — END)*' if last else f'*(~{fmt(cur)}–{fmt(cur + dur)})*', 1)
    cur += dur
    out += h + b
open(p, 'w').write(out)
print(f'minutes {cur / 60:.1f}; spoken words {sp_total}')
