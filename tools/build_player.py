"""Build a read-aloud player page from scene JSON.

Usage: python3 tools/build_player.py CONFIG.json
CONFIG keys: scenes, out, title, kicker, h1, key (localStorage prefix),
cast {SPEAKER: [hex, "f"|"m", pitch]}, read_directions (bool).
After-action notes ("aa" items) are left out of the player.
"""
import json
import sys

cfg = json.load(open(sys.argv[1]))
S = json.load(open(cfg['scenes']))
for s in S:
    s['items'] = [it for it in s['items'] if it['k'] != 'aa']
tp = open('tools/player_template.html').read()
rep = {
    '__SCENES__': json.dumps(S, ensure_ascii=False).replace('</', '<\\/'),
    '__CAST__': json.dumps(cfg['cast'], ensure_ascii=False) + ';',
    '__TITLE__': cfg['title'], '__KICKER__': cfg['kicker'], '__H1__': cfg['h1'],
    '__N__': str(len(S)), '__KEY__': cfg['key'],
    '__ACTCHECKED__': 'checked' if cfg.get('read_directions', True) else '',
}
for k, v in rep.items():
    assert k in tp, k
    tp = tp.replace(k, v)
open(cfg['out'], 'w').write(tp)
print('player written', cfg['out'], len(S), 'scenes')
